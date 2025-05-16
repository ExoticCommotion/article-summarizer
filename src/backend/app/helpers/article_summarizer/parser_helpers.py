"""Helper functions for article parsing operations."""

import re

from backend.app.custom_agents.article_summarizer.agents import (
    ArticleContent,
    ArticleMetadata,
    ArticleStructure,
)
from backend.app.types.article_summarizer.parser_types import (
    ExtractedArticleContent,
)


def convert_to_article_content(
    extracted_content: ExtractedArticleContent, url: str
) -> ArticleContent:
    """
    Convert ExtractedArticleContent to ArticleContent.

    Args:
        extracted_content: The extracted article content.
        url: The URL of the article.

    Returns:
        An ArticleContent object.
    """
    metadata = ArticleMetadata(
        title=extracted_content.metadata.title,
        author=extracted_content.metadata.author,
        published_date=extracted_content.metadata.published_date,
        source=extracted_content.metadata.source,
        tags=extracted_content.metadata.tags,
    )

    headings = [
        {"text": h.text, "level": str(h.level)} for h in extracted_content.structure.headings
    ]
    images = [
        {"url": img.url, "alt": img.alt, "caption": img.caption}
        for img in extracted_content.structure.images
    ]
    links = [
        {"url": link.url, "text": link.text, "context": link.context}
        for link in extracted_content.structure.links
    ]
    # ArticleStructure expects tables: list[dict[str, list[str]]]
    tables = [{"content": [table.content]} for table in extracted_content.structure.tables]

    structure = ArticleStructure(
        headings=headings,
        images=images,
        links=links,
        tables=tables,
    )

    subsections = [
        {"heading": sub.heading, "content": sub.content} for sub in extracted_content.subsections
    ]

    return ArticleContent(
        title=extracted_content.metadata.title or "Untitled Article",
        content=extracted_content.text,
        url=url,
        subsections=subsections,
        metadata=metadata,
        structure=structure,
    )


def extract_title_from_html(html_content: str) -> str:
    """
    Extract title from HTML content when metadata is missing.

    Args:
        html_content: The HTML content.

    Returns:
        The extracted title or "Untitled Article".
    """
    title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Untitled Article"
    return re.sub(r"\s*[-–|]\s*.*$", "", title).strip()
