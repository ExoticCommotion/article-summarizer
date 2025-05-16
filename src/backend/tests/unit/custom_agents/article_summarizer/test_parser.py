"""Tests for article parser."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.custom_agents.article_summarizer.parser import (
    extract_article_text,
    fetch_article_content,
)
from backend.app.types.article_summarizer.parser_types import (
    ArticleMetadataResult,
    ArticleStructureResult,
)


@pytest.mark.asyncio
async def test_fetch_article_content_success():
    """Test successful article content fetching."""
    mock_response = MagicMock()
    mock_response.text = "<html><body><p>Test content</p></body></html>"
    mock_response.raise_for_status = AsyncMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    mock_async_client = AsyncMock()
    mock_async_client.__aenter__.return_value = mock_client

    with patch("httpx.AsyncClient", return_value=mock_async_client):
        result = await fetch_article_content("https://example.com")

    assert result == "<html><body><p>Test content</p></body></html>"
    mock_client.get.assert_called_once_with("https://example.com")


@pytest.mark.asyncio
async def test_fetch_article_content_failure():
    """Test failed article content fetching."""
    import httpx

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(side_effect=httpx.HTTPError("Connection error"))

    mock_async_client = AsyncMock()
    mock_async_client.__aenter__.return_value = mock_client

    with patch("httpx.AsyncClient", return_value=mock_async_client):
        result = await fetch_article_content("https://example.com")

    assert result is None


def test_extract_article_text():
    """Test article text extraction."""
    html_content = """
    <html>
        <head><title>Test</title></head>
        <body>
            <script>console.log('test');</script>
            <p>Paragraph 1</p>
            <p>Paragraph 2</p>
            <div>Not a paragraph</div>
        </body>
    </html>
    """

    result = extract_article_text(html_content)

    assert "Paragraph 1" in result.text
    assert "Paragraph 2" in result.text
    assert "console.log" not in result.text
    assert isinstance(result.subsections, list)
    assert isinstance(result.metadata, ArticleMetadataResult)
    assert isinstance(result.structure, ArticleStructureResult)


def test_extract_article_text_with_subsections():
    """Test extracting article text with subsections."""
    html_content = """
    <html>
        <head>
            <title>Test Article</title>
        </head>
        <body>
            <article>
                <h1>Main Heading</h1>
                <p>Introduction paragraph.</p>
                <h2>First Section</h2>
                <p>First section content.</p>
                <p>More first section content.</p>
                <h2>Second Section</h2>
                <p>Second section content.</p>
            </article>
        </body>
    </html>
    """

    result = extract_article_text(html_content)

    assert "Introduction paragraph" in result.text
    assert "First section content" in result.text
    assert "Second section content" in result.text

    assert len(result.subsections) == 3
    assert result.subsections[0].heading == "Main Heading"
    assert result.subsections[1].heading == "First Section"
    assert result.subsections[2].heading == "Second Section"
    assert "First section content" in result.subsections[1].content
    assert "Second section content" in result.subsections[2].content

    assert isinstance(result.metadata, ArticleMetadataResult)
    assert isinstance(result.structure, ArticleStructureResult)
    assert result.structure.headings[0].text == "Main Heading"
