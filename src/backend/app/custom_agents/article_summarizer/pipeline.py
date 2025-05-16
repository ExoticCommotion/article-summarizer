"""Agent-native pipeline for article summarization."""


from pydantic import BaseModel
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


class ArticleAnalysisInput(BaseModel):
    """Input data for the article analysis step."""
    
    raw_text: str
    """Raw text extracted from the article."""
    
    title: str
    """Title of the article."""
    
    subsections: list[dict[str, str]]
    """Subsections of the article with heading and content."""
    
    metadata: dict
    """Metadata extracted from the article."""
    
    structure: dict
    """Structural elements of the article."""


class ContentAnalysisResult(BaseModel):
    """Result of the content analysis step."""
    
    key_topics: list[str] = []
    """Key topics identified in the article."""
    
    sentiment: str = ""
    """Overall sentiment of the article."""
    
    complexity_score: float = 0.0
    """Readability/complexity score of the article."""
    
    main_entities: list[str] = []
    """Main entities mentioned in the article."""


async def analyze_content(article_content: ArticleContent) -> ContentAnalysisResult | None:
    """
    Analyze the article content to extract additional insights.
    
    Args:
        article_content: The extracted article content.
        
    Returns:
        Analysis results or None if analysis failed.
    """
    try:
        logger.info("Analyzing article content...")
        return ContentAnalysisResult(
            key_topics=["placeholder topic"],
            sentiment="neutral",
            complexity_score=0.5,
            main_entities=["placeholder entity"]
        )
    except Exception as e:
        logger.error(f"Error in content analysis: {e}")
        return None


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
        
        analysis_result = await analyze_content(article_content)
        if not analysis_result:
            logger.warning("Content analysis failed, proceeding with basic summarization")
        
        with custom_span("Summarize article"):
            input_data = (
                f"Title: {article_content.title}\n\n"
                f"Article text:\n\n{article_content.content}"
            )

            if article_content.subsections:
                input_data += "\n\nArticle subsections:\n"
                for section in article_content.subsections:
                    input_data += f"\n## {section['heading']}\n{section['content']}\n"
            
            if analysis_result:
                input_data += "\n\nContent Analysis:\n"
                input_data += f"- Key Topics: {', '.join(analysis_result.key_topics)}\n"
                input_data += f"- Sentiment: {analysis_result.sentiment}\n"
                input_data += f"- Main Entities: {', '.join(analysis_result.main_entities)}\n"
            
            if article_content.metadata and article_content.metadata.author:
                input_data += f"\n\nArticle by: {article_content.metadata.author}"
                if article_content.metadata.published_date:
                    input_data += f" (Published: {article_content.metadata.published_date})"
            
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
