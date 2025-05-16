"""Tests for parser helpers."""

from backend.app.helpers.article_summarizer.parser_helpers import (
    convert_to_article_content,
    extract_title_from_html,
)
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


def test_extract_title_from_html():
    """Test extracting title from HTML content."""
    html_content = "<html><head><title>Test Title | Website</title></head><body></body></html>"
    title = extract_title_from_html(html_content)
    assert title == "Test Title"


def test_convert_to_article_content():
    """Test converting ExtractedArticleContent to ArticleContent."""
    extracted_content = ExtractedArticleContent(
        text="Article text content.",
        subsections=[
            ArticleSubsection(heading="First Section", content="First section content."),
            ArticleSubsection(heading="Second Section", content="Second section content."),
        ],
        metadata=ArticleMetadataResult(
            title="Test Article",
            author="Test Author",
            published_date="2023-01-01",
            source="Test Source",
            tags=["tag1", "tag2"],
        ),
        structure=ArticleStructureResult(
            headings=[
                ArticleHeading(text="First Section", level=2),
                ArticleHeading(text="Second Section", level=2),
            ],
            images=[ArticleImage(url="image.jpg", alt="Image", caption="Caption")],
            links=[ArticleLink(url="link.html", text="Link", context="Context")],
            tables=[ArticleTable(content="Table content")],
        ),
    )

    url = "https://example.com/article"
    article_content = convert_to_article_content(extracted_content, url)

    assert article_content.title == "Test Article"
    assert article_content.content == "Article text content."
    assert article_content.url == url
    assert len(article_content.subsections) == 2
    assert article_content.subsections[0]["heading"] == "First Section"
    assert article_content.subsections[1]["heading"] == "Second Section"
    assert article_content.metadata.title == "Test Article"
    assert article_content.metadata.author == "Test Author"
    assert article_content.metadata.published_date == "2023-01-01"
    assert article_content.metadata.source == "Test Source"
    assert article_content.metadata.tags == ["tag1", "tag2"]
    assert len(article_content.structure.headings) == 2
    assert article_content.structure.headings[0]["text"] == "First Section"
    assert article_content.structure.headings[1]["text"] == "Second Section"
