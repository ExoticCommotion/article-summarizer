"""Article parsing utilities."""

import httpx
from bs4 import BeautifulSoup

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


def extract_article_text(html_content: str) -> tuple[str, list[dict[str, str]], dict, dict]:
    """
    Extract the main article text and metadata from HTML content.

    Args:
        html_content: The HTML content of the article.

    Returns:
        A tuple containing:
        - The extracted article text
        - A list of subsections with their headings and content
        - Article metadata (title, author, date, source, tags)
        - Article structure (headings, images, links, tables)
    """
    logger.info("Extracting article text, subsections, and metadata from HTML content")
    soup = BeautifulSoup(html_content, "html.parser")

    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.extract()

    metadata = {
        "title": "",
        "author": "",
        "published_date": "",
        "source": "",
        "tags": []
    }
    
    title_meta = soup.find("meta", property="og:title") or soup.find("meta", property="twitter:title")
    if title_meta and title_meta.get("content"):
        metadata["title"] = title_meta.get("content")
    
    author_meta = soup.find("meta", attrs={"name": "author"}) or soup.find("meta", property="article:author")
    if author_meta and author_meta.get("content"):
        metadata["author"] = author_meta.get("content")
    
    date_meta = soup.find("meta", property="article:published_time") or soup.find("meta", attrs={"name": "date"})
    if date_meta and date_meta.get("content"):
        metadata["published_date"] = date_meta.get("content")
    
    source_meta = soup.find("meta", property="og:site_name")
    if source_meta and source_meta.get("content"):
        metadata["source"] = source_meta.get("content")
    
    tags = []
    keywords_meta = soup.find("meta", attrs={"name": "keywords"})
    if keywords_meta and keywords_meta.get("content"):
        tags = [tag.strip() for tag in keywords_meta.get("content").split(",")]
    metadata["tags"] = tags
    
    structure = {
        "headings": [],
        "images": [],
        "links": [],
        "tables": []
    }
    
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    for heading in headings:
        heading_level = int(heading.name[1])
        structure["headings"].append({
            "text": heading.get_text().strip(),
            "level": heading_level
        })

    images = soup.find_all("img")
    for img in images:
        image_data = {
            "url": img.get("src", ""),
            "alt": img.get("alt", ""),
            "caption": ""
        }
        caption = img.find_next("figcaption")
        if caption:
            image_data["caption"] = caption.get_text().strip()
        structure["images"].append(image_data)
    
    links = soup.find_all("a")
    for link in links:
        link_data = {
            "url": link.get("href", ""),
            "text": link.get_text().strip(),
            "context": ""
        }
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
            structure["tables"].append({"rows": rows})
    
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
    return article_text, subsections, metadata, structure
