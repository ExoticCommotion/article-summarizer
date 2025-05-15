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


def extract_article_text(html_content: str) -> tuple[str, list[dict[str, str]]]:
    """
    Extract the main article text and subsections from HTML content.

    Args:
        html_content: The HTML content of the article.

    Returns:
        A tuple containing the extracted article text and a list of subsections
        with their headings and content.
    """
    logger.info("Extracting article text and subsections from HTML content")
    soup = BeautifulSoup(html_content, "html.parser")

    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.extract()

    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

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
        f"Extracted {len(article_text)} characters of text and {len(subsections)} subsections"
    )
    return article_text, subsections
