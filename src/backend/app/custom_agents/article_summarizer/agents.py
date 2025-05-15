"""Agents for article summarization."""

from agents import Agent, gen_trace_id
from pydantic import BaseModel


class ArticleContent(BaseModel):
    """Data structure for extracted article content."""

    title: str
    """The title of the article."""

    content: str
    """The main content of the article."""

    url: str
    """The URL of the article."""

    subsections: list[dict[str, str]] = []
    """Subsections of the article with heading and content."""


class SummaryData(BaseModel):
    """Data structure for article summary."""

    title: str
    """The title of the article."""

    short_summary: str
    """A short 2-3 sentence summary of the article."""

    detailed_summary: str
    """A more detailed summary of the article in markdown format."""

    key_points: list[str]
    """Key points from the article."""


class AudioFormat(BaseModel):
    """Data structure for audio formatting."""

    title: str
    """The title of the article for the audio."""

    narration_text: str
    """The text to be converted to audio."""

    filename: str
    """The suggested filename for the audio file (without extension)."""


content_extractor_agent = Agent(
    name="ContentExtractorAgent",
    instructions=(
        "You are an expert content extractor. Your task is to analyze the provided HTML content "
        "and extract the main article text. Focus on identifying the title and main content, "
        "while ignoring advertisements, navigation elements, and other non-content parts. "
        "Clean up the text by removing unnecessary whitespace, formatting issues, and other "
        "artifacts that might interfere with summarization."
    ),
    model="gpt-4o",
    output_type=ArticleContent,
)

summarizer_agent = Agent(
    name="ArticleSummarizerAgent",
    instructions=(
        "You are an expert article summarizer. Your task is to read the provided article "
        "text and create a concise, informative summary. Focus on extracting the main "
        "points, key arguments, and important details. Your summary should be "
        "well-structured and easy to understand. Include a short summary (2-3 sentences), "
        "a more detailed summary in markdown format, and a list of key points."
    ),
    model="gpt-4o",
    output_type=SummaryData,
)

audio_formatter_agent = Agent(
    name="AudioFormatterAgent",
    instructions=(
        "You are an expert audio content formatter. Your task is to take a summary of an article "
        "and format it for audio narration. Create a script that flows naturally when spoken, "
        "with appropriate transitions and pacing. Avoid complex sentence structures or references "
        "that don't work well in audio format. Format the text to be engaging and clear for listeners. "
        "Also suggest a descriptive filename based on the article title (without extension)."
    ),
    model="gpt-4o",
    output_type=AudioFormat,
)


def generate_trace_id() -> str:
    """Generate a trace ID that starts with 'trace_'."""
    raw_id = gen_trace_id()
    clean_id = raw_id.replace("trace_", "")
    return f"trace_{clean_id}"
