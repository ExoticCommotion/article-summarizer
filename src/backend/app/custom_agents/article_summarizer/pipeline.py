"""Agent-native pipeline for article summarization."""


from agents import Runner, custom_span

from backend.app.custom_agents.article_summarizer.agents import (
    ArticleContent,
    AudioFormat,
    SummaryData,
    audio_formatter_agent,
    summarizer_agent,
)
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


async def run_summarizer(article_content: ArticleContent) -> SummaryData | None:
    """
    Run the summarizer agent to create article summaries.

    Args:
        article_content: The extracted article content.

    Returns:
        The summary data or None if summarization failed.
    """
    try:
        logger.info("Running summarizer agent...")
        with custom_span("Summarize article"):
            input_data = (
                f"Title: {article_content.title}\n\nArticle text:\n\n{article_content.content}"
            )

            if article_content.subsections:
                input_data += "\n\nArticle subsections:\n"
                for section in article_content.subsections:
                    input_data += f"\n## {section['heading']}\n{section['content']}\n"

            result = await Runner.run(summarizer_agent, input_data)
            return result.final_output_as(SummaryData)
    except Exception as e:
        logger.error(f"Error in summarizer agent: {e}")
        return None


async def run_audio_formatter(summary: SummaryData) -> AudioFormat | None:
    """
    Run the audio formatter agent to format the summary for audio.

    Args:
        summary: The article summary.

    Returns:
        The audio format data or None if formatting failed.
    """
    try:
        logger.info("Running audio formatter agent...")
        with custom_span("Format for audio"):
            input_data = (
                f"Title: {summary.title}\n\n"
                f"Short Summary: {summary.short_summary}\n\n"
                f"Detailed Summary: {summary.detailed_summary}\n\n"
                f"Key Points: {', '.join(summary.key_points)}"
            )

            result = await Runner.run(audio_formatter_agent, input_data)
            audio_format = result.final_output_as(AudioFormat)

            import re

            safe_filename = re.sub(r"[^\w\-_]", "_", audio_format.filename)
            audio_format.filename = safe_filename

            return audio_format
    except Exception as e:
        logger.error(f"Error in audio formatter agent: {e}")
        return None
