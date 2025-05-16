"""Article parsing utilities."""

import httpx
from bs4 import BeautifulSoup

from backend.app.types.article_summarizer.parser_types import (
    ArticleHeading,
    ArticleImage,
    ArticleLink,
    ArticleMetadataResult,
    ArticleStructureResult,
    ArticleSubsection,
    ArticleTable,
    ExtractedArticleContent,
)
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


async def fetch_article_content(url: str) -> str | None:
    """
    Fetch article content from a URL.

    Args:
        url: The URL of the article to fetch.

    Returns:
        The HTML content of the article or None if the request failed.
    """
    logger.info(f"Fetching article from: {url}")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.HTTPError as e:
        logger.error(f"Error fetching article: {e}")
        return None


def extract_article_text(html_content: str) -> ExtractedArticleContent:
    """
    Extract the main article text and metadata from HTML content.

    Args:
        html_content: The HTML content of the article.

    Returns:
        An ExtractedArticleContent object containing the article text, subsections,
        metadata, and structure.
    """
    logger.info("Extracting article text, subsections, and metadata from HTML content")
    soup = BeautifulSoup(html_content, "html.parser")

    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.extract()

    metadata: dict[str, str | list[str]] = {
        "title": "",
        "author": "",
        "published_date": "",
        "source": "",
        "tags": [],
    }

    title_meta = soup.find("meta", property="og:title") or soup.find(
        "meta", property="twitter:title"
    )
    if title_meta and hasattr(title_meta, "get") and title_meta.get("content"):
        content = title_meta.get("content")
        metadata["title"] = str(content) if content is not None else ""

    author_meta = soup.find("meta", attrs={"name": "author"}) or soup.find(
        "meta", property="article:author"
    )
    if author_meta and hasattr(author_meta, "get") and author_meta.get("content"):
        content = author_meta.get("content")
        metadata["author"] = str(content) if content is not None else ""

    date_meta = soup.find("meta", property="article:published_time") or soup.find(
        "meta", attrs={"name": "date"}
    )
    if date_meta and hasattr(date_meta, "get") and date_meta.get("content"):
        content = date_meta.get("content")
        metadata["published_date"] = str(content) if content is not None else ""

    source_meta = soup.find("meta", property="og:site_name")
    if source_meta and hasattr(source_meta, "get") and source_meta.get("content"):
        content = source_meta.get("content")
        metadata["source"] = str(content) if content is not None else ""

    tags: list[str] = []
    keywords_meta = soup.find("meta", attrs={"name": "keywords"})
    if keywords_meta and hasattr(keywords_meta, "get") and keywords_meta.get("content"):
        content = keywords_meta.get("content")
        if isinstance(content, str):
            tags = [tag.strip() for tag in content.split(",")]
    metadata["tags"] = tags

    structure: dict[str, list[dict[str, str | int | list[str]]]] = {
        "headings": [],
        "images": [],
        "links": [],
        "tables": [],
    }

    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    for heading in headings:
        heading_level = int(heading.name[1])
        structure["headings"].append({"text": heading.get_text().strip(), "level": heading_level})

    images = soup.find_all("img")
    for img in images:
        image_data = {"url": img.get("src", ""), "alt": img.get("alt", ""), "caption": ""}
        caption = img.find_next("figcaption")
        if caption:
            image_data["caption"] = caption.get_text().strip()
        structure["images"].append(image_data)

    links = soup.find_all("a")
    for link in links:
        link_data = {"url": link.get("href", ""), "text": link.get_text().strip(), "context": ""}
        structure["links"].append(link_data)

    tables = soup.find_all("table")
    for table in tables:
        rows = []
        for tr in table.find_all("tr"):
            cells = []
            for td in tr.find_all(["td", "th"]):
                cells.append(td.get_text().strip())
            if cells:
                rows.append(cells)
        if rows:
            row_text = ", ".join([" ".join([str(cell) for cell in row]) for row in rows])
            structure["tables"].append({"content": row_text})

    paragraphs = soup.find_all("p")
    article_text = "\n\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

    if not article_text:
        main_content = soup.find("main") or soup.find("article") or soup.find("body")
        if main_content:
            article_text = main_content.get_text().strip()

    subsections = []
    for i, heading in enumerate(headings):
        heading_text = heading.get_text().strip()
        if heading_text:
            content = []
            next_element = heading.find_next_sibling()
            while next_element and (i == len(headings) - 1 or next_element != headings[i + 1]):
                if next_element.name == "p" and next_element.get_text().strip():
                    content.append(next_element.get_text().strip())
                next_element = next_element.find_next_sibling()

            if content:
                subsections.append({"heading": heading_text, "content": "\n\n".join(content)})

    logger.info(
        f"Extracted {len(article_text)} characters of text, {len(subsections)} subsections, and {len(structure['headings'])} headings"
    )

    article_subsections = []
    for subsection in subsections:
        article_subsections.append(
            ArticleSubsection(heading=subsection["heading"], content=subsection["content"])
        )

    title = str(metadata["title"]) if isinstance(metadata["title"], str) else ""
    author = str(metadata["author"]) if isinstance(metadata["author"], str) else ""
    published_date = (
        str(metadata["published_date"]) if isinstance(metadata["published_date"], str) else ""
    )
    source = str(metadata["source"]) if isinstance(metadata["source"], str) else ""
    tags = metadata["tags"] if isinstance(metadata["tags"], list) else []

    metadata_result = ArticleMetadataResult(
        title=title,
        author=author,
        published_date=published_date,
        source=source,
        tags=tags,
    )

    heading_objects = []
    for h in structure["headings"]:
        text = str(h["text"]) if isinstance(h["text"], str) else ""
        level = int(h["level"]) if isinstance(h["level"], int) else 1
        heading_objects.append(ArticleHeading(text=text, level=level))

    image_objects = []
    for img in structure["images"]:
        url = str(img["url"]) if isinstance(img["url"], str) else ""
        alt = str(img["alt"]) if isinstance(img["alt"], str) else ""
        caption = str(img["caption"]) if isinstance(img["caption"], str) else ""
        image_objects.append(ArticleImage(url=url, alt=alt, caption=caption))

    link_objects = []
    for link in structure["links"]:
        url = str(link["url"]) if isinstance(link["url"], str) else ""
        text = str(link["text"]) if isinstance(link["text"], str) else ""
        context = str(link["context"]) if isinstance(link["context"], str) else ""
        link_objects.append(ArticleLink(url=url, text=text, context=context))

    table_objects = []
    for table in structure["tables"]:
        content = str(table["content"]) if isinstance(table["content"], str) else ""
        table_objects.append(ArticleTable(content=content))

    structure_result = ArticleStructureResult(
        headings=heading_objects,
        images=image_objects,
        links=link_objects,
        tables=table_objects,
    )

    return ExtractedArticleContent(
        text=article_text,
        subsections=article_subsections,
        metadata=metadata_result,
        structure=structure_result,
    )
