"""Article parsing utilities."""

import re
import uuid
from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup, Tag

from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class ArticleSection:
    """A section of an article with a title and content."""

    title: str
    """The title of the section."""

    content: str
    """The content of the section."""

    level: int = 0
    """The heading level (1-6) of the section."""


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


def extract_article_title(html_content: str) -> str:
    """
    Extract the title of an article from HTML content.

    Args:
        html_content: The HTML content of the article.

    Returns:
        The title of the article.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    
    h1 = soup.find("h1")
    if h1:
        return h1.get_text().strip()
    
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text().strip()
        title = re.sub(r"\s*[-–|]\s*.*$", "", title).strip()
        return title
    
    return "Untitled Article"


def extract_wikipedia_sections(html_content: str) -> list[ArticleSection]:
    """
    Extract sections from a Wikipedia article.

    Args:
        html_content: The HTML content of the Wikipedia article.

    Returns:
        A list of ArticleSection objects representing the sections of the article.
    """
    logger.info("Extracting Wikipedia sections")
    soup = BeautifulSoup(html_content, "html.parser")
    
    content_div = soup.find("div", {"id": "mw-content-text"})
    if not content_div or not isinstance(content_div, Tag):
        logger.warning("Could not find main content div in Wikipedia article")
        return [ArticleSection(title="Main Content", content=extract_article_text(html_content))]
    
    article_title = extract_article_title(html_content)
    
    headings = content_div.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
    
    if not headings:
        logger.warning("No headings found in Wikipedia article")
        return [ArticleSection(title=article_title, content=extract_article_text(html_content))]
    
    sections = []
    
    intro_content = ""
    intro_elements = []
    
    first_p = content_div.find("p")
    if first_p and isinstance(first_p, Tag):
        current_element: Tag | None = first_p
        while current_element is not None:
            if current_element.name in ["p", "ul", "ol", "blockquote"]:
                intro_elements.append(current_element)
            
            next_element = current_element.next_sibling
            while next_element and not isinstance(next_element, Tag):
                next_element = next_element.next_sibling
                
            if next_element and isinstance(next_element, Tag) and next_element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                break
                
            current_element = next_element if isinstance(next_element, Tag) else None
    
    for element in intro_elements:
        if isinstance(element, Tag) and element.name in ["p", "ul", "ol", "blockquote"]:
            intro_content += element.get_text().strip() + "\n\n"
    
    if intro_content:
        sections.append(ArticleSection(title="Introduction", content=intro_content.strip(), level=0))
    
    for _i, heading in enumerate(headings):
        if not isinstance(heading, Tag):
            continue
            
        heading_text = heading.get_text().strip()
        heading_level = int(heading.name[1])  # h1 -> 1, h2 -> 2, etc.
        
        if heading_text.lower() in ["contents", "references", "external links", "see also", "notes", "bibliography"]:
            continue
        
        content = ""
        section_elements = []
        
        next_element = heading.next_sibling
        while next_element and not isinstance(next_element, Tag):
            next_element = next_element.next_sibling
            
        section_element: Tag | None = next_element if isinstance(next_element, Tag) else None
        
        while section_element is not None:
            if section_element.name in ["p", "ul", "ol", "blockquote"]:
                section_elements.append(section_element)
            elif section_element.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
                break
                
            next_element = section_element.next_sibling
            while next_element and not isinstance(next_element, Tag):
                next_element = next_element.next_sibling
                
            section_element = next_element if isinstance(next_element, Tag) else None
        
        for element in section_elements:
            if isinstance(element, Tag):
                content += element.get_text().strip() + "\n\n"
        
        if content:
            sections.append(ArticleSection(title=heading_text, content=content.strip(), level=heading_level))
    
    logger.info(f"Extracted {len(sections)} sections from Wikipedia article")
    return sections


def generate_unique_filename(base_name: str) -> str:
    """
    Generate a unique filename based on the base name.

    Args:
        base_name: The base name for the filename.

    Returns:
        A unique filename.
    """
    clean_name = re.sub(r"[^\w\-_]", "_", base_name.lower())
    
    short_uuid = str(uuid.uuid4())[:8]
    
    return f"{clean_name}_{short_uuid}"
