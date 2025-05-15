"""Agents for article summarization."""

from agents import Agent
from pydantic import BaseModel


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


summarizer_agent = Agent(
    name="ArticleSummarizerAgent",
    instructions=(
        "You are an expert article summarizer. Your task is to read the provided article "
        "text and create a concise, informative summary. Focus on extracting the main "
        "points, key arguments, and important details. Ignore advertisements, navigation "
        "elements, and other non-content parts of the article. Your summary should be "
        "well-structured and easy to understand."
    ),
    model="gpt-4o",
    output_type=SummaryData,
)
