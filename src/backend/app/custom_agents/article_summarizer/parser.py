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


def extract_article_text(html_content: str) -> str:
    """
    Extract the main article text from HTML content.

    Args:
        html_content: The HTML content of the article.

    Returns:
        The extracted article text.
    """
    logger.info("Extracting article text from HTML content")
    soup = BeautifulSoup(html_content, "html.parser")

    for script in soup(["script", "style", "nav", "footer", "header"]):
        script.extract()

    paragraphs = soup.find_all("p")
    article_text = "\n\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

    if not article_text:
        main_content = soup.find("main") or soup.find("article") or soup.find("body")
        if main_content:
            article_text = main_content.get_text().strip()

    logger.info(f"Extracted {len(article_text)} characters of text")
    return article_text
