"""Type definitions for article parser module."""

from pydantic import BaseModel


class ArticleSubsection(BaseModel):
    """A subsection of an article with heading and content."""

    heading: str
    """The heading text of the subsection."""

    content: str
    """The content text of the subsection."""


class ArticleHeading(BaseModel):
    """A heading within an article."""

    text: str
    """The text of the heading."""

    level: int
    """The level of the heading (1-6)."""


class ArticleImage(BaseModel):
    """An image within an article."""

    url: str
    """The URL of the image."""

    alt: str = ""
    """The alt text of the image."""

    caption: str = ""
    """The caption of the image."""


class ArticleLink(BaseModel):
    """A link within an article."""

    url: str
    """The URL of the link."""

    text: str = ""
    """The link text."""

    context: str = ""
    """The surrounding context of the link."""


class ArticleTable(BaseModel):
    """A table within an article."""

    content: str = ""
    """The content of the table as text."""


class ArticleMetadataResult(BaseModel):
    """Metadata extracted from an article."""

    title: str = ""
    """The title of the article."""

    author: str = ""
    """The author of the article."""

    published_date: str = ""
    """The publication date of the article."""

    source: str = ""
    """The source of the article."""

    tags: list[str] = []
    """Tags or categories associated with the article."""


class ArticleStructureResult(BaseModel):
    """Structural elements extracted from an article."""

    headings: list[ArticleHeading] = []
    """Hierarchical headings in the article."""

    images: list[ArticleImage] = []
    """Images in the article."""

    links: list[ArticleLink] = []
    """Links in the article."""

    tables: list[ArticleTable] = []
    """Tables in the article."""


class ExtractedArticleContent(BaseModel):
    """The complete extracted content from an article."""

    text: str
    """The main text content of the article."""

    subsections: list[ArticleSubsection] = []
    """Subsections of the article with heading and content."""

    metadata: ArticleMetadataResult = ArticleMetadataResult()
    """Metadata extracted from the article."""

    structure: ArticleStructureResult = ArticleStructureResult()
    """Structural elements of the article."""
