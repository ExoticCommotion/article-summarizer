"""Tests for article parser."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.custom_agents.article_summarizer.parser import (
    extract_article_text,
    fetch_article_content,
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

    assert "Paragraph 1" in result
    assert "Paragraph 2" in result
    assert "console.log" not in result
