"""Manager for article summarization process."""

import re
from pathlib import Path

from agents import Runner, trace

from backend.app.custom_agents.article_summarizer.agents import (
    ArticleContent,
    AudioFormat,
    SummaryData,
    audio_formatter_agent,
    generate_trace_id,
    summarizer_agent,
)
from backend.app.custom_agents.article_summarizer.audio import generate_audio
from backend.app.custom_agents.article_summarizer.parser import fetch_article_content
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


class ArticleSummarizerManager:
    """Manager for the article summarization process."""

    async def summarize_article(self, url: str) -> tuple[Path, Path, Path] | None:
        """
        Summarize an article from a URL and generate audio.

        Args:
            url: The URL of the article to summarize.

        Returns:
            A tuple containing the paths to the generated audio file, raw text file, and final text file,
            or None if the process failed.
        """
        trace_id = generate_trace_id()

        with trace("Article Summarization", trace_id=trace_id):
            logger.info(f"Starting article summarization for {url}")
            logger.info(f"Trace ID: {trace_id}")

            # Extract content - first step of the pipeline
            article_content = await self._extract_content(url)
            if not article_content:
                logger.error("Failed to extract article content")
                return None

            from backend.app.custom_agents.article_summarizer.pipeline import (
                run_audio_formatter,
                run_summarizer,
            )

            summary = await run_summarizer(article_content)
            if not summary:
                logger.error("Failed to summarize article")
                return None

            audio_format = await run_audio_formatter(summary)
            if not audio_format:
                logger.error("Failed to format for audio")
                return None

            # Format the final text that will be saved along with the audio
            formatted_text = (
                f"# {audio_format.title}\n\n"
                f"{audio_format.narration_text}\n\n"
                f"Generated from: {url}"
            )

            # Pass the article title, content, and formatted text to generate_audio
            audio_path, raw_text_path, final_text_path = await generate_audio(
                audio_format.narration_text,
                audio_format.filename,
                article_content.title,
                article_content.content,
                formatted_text,
            )

            logger.info(f"Article summarization complete. Files saved to {audio_path.parent}")
            return audio_path, raw_text_path, final_text_path

    async def _extract_content(self, url: str) -> ArticleContent | None:
        """
        Extract content from a URL.

        Args:
            url: The URL of the article.

        Returns:
            The extracted article content or None if extraction failed.
        """
        try:
            logger.info(f"Extracting content from {url}")
            html_content = await fetch_article_content(url)
            if not html_content:
                logger.error("Failed to fetch article content")
                return None

            from backend.app.custom_agents.article_summarizer.parser import extract_article_text
            from backend.app.custom_agents.article_summarizer.agents import ArticleMetadata, ArticleStructure

            article_text, subsections, metadata_dict, structure_dict = extract_article_text(html_content)

            import re

            if not metadata_dict["title"]:
                title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE)
                title = title_match.group(1) if title_match else "Untitled Article"
                title = re.sub(r"\s*[-–|]\s*.*$", "", title).strip()
                metadata_dict["title"] = title
            else:
                title = metadata_dict["title"]

            metadata = ArticleMetadata(
                title=metadata_dict["title"],
                author=metadata_dict["author"],
                published_date=metadata_dict["published_date"],
                source=metadata_dict["source"],
                tags=metadata_dict["tags"]
            )
            
            structure = ArticleStructure(
                headings=structure_dict["headings"],
                images=structure_dict["images"],
                links=structure_dict["links"],
                tables=structure_dict["tables"]
            )
            
            return ArticleContent(
                title=title,
                content=article_text,
                url=url,
                subsections=subsections,
                metadata=metadata,
                structure=structure
            )
        except Exception as e:
            logger.error(f"Error extracting content: {e}")
            return None

    async def _summarize_article(self, article_content: ArticleContent) -> SummaryData | None:
        """
        Summarize the article content.

        Args:
            article_content: The extracted article content.

        Returns:
            The summary data or None if summarization failed.
        """
        try:
            logger.info("Summarizing article...")
            result = await Runner.run(
                summarizer_agent,
                f"Title: {article_content.title}\n\nArticle text:\n\n{article_content.content}",
            )
            return result.final_output_as(SummaryData)
        except Exception as e:
            logger.error(f"Error summarizing article: {e}")
            return None

    async def _format_for_audio(self, summary: SummaryData) -> AudioFormat | None:
        """
        Format the summary for audio narration.

        Args:
            summary: The article summary.

        Returns:
            The audio format data or None if formatting failed.
        """
        try:
            logger.info("Formatting for audio...")
            result = await Runner.run(
                audio_formatter_agent,
                f"Title: {summary.title}\n\n"
                f"Short Summary: {summary.short_summary}\n\n"
                f"Detailed Summary: {summary.detailed_summary}\n\n"
                f"Key Points: {', '.join(summary.key_points)}",
            )

            audio_format = result.final_output_as(AudioFormat)

            safe_filename = re.sub(r"[^\w\-_]", "_", audio_format.filename)
            audio_format.filename = safe_filename

            return audio_format
        except Exception as e:
            logger.error(f"Error formatting for audio: {e}")
            return None
