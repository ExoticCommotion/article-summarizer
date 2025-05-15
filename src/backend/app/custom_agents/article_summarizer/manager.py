"""Manager for article summarization process."""

import time
import uuid
from pathlib import Path

from agents import Runner, trace

from backend.app.custom_agents.article_summarizer.agents import SummaryData, summarizer_agent
from backend.app.custom_agents.article_summarizer.audio import generate_audio
from backend.app.custom_agents.article_summarizer.parser import (
    extract_article_text,
    fetch_article_content,
)
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)


class ArticleSummarizerManager:
    """Manager for the article summarization process."""

    async def summarize_article(self, url: str) -> Path | None:
        """
        Summarize an article from a URL and generate audio.

        Args:
            url: The URL of the article to summarize.

        Returns:
            The path to the generated audio file or None if the process failed.
        """
        trace_id = f"article-summary-{uuid.uuid4().hex[:8]}"

        with trace("Article Summarization", trace_id=trace_id):
            logger.info(f"Starting article summarization for {url}")
            logger.info(f"Trace ID: {trace_id}")

            html_content = await fetch_article_content(url)
            if not html_content:
                logger.error("Failed to fetch article content")
                return None

            article_text = extract_article_text(html_content)
            if not article_text or len(article_text) < 100:
                logger.error("Failed to extract meaningful article text")
                return None

            logger.info("Summarizing article...")
            summary = await self._run_summarizer(article_text)
            if not summary:
                logger.error("Failed to summarize article")
                return None

            output_filename = f"summary_{int(time.time())}"
            audio_text = (
                f"Article: {summary.title}\n\n"
                f"Summary: {summary.short_summary}\n\n"
                f"Key points: {'. '.join(summary.key_points)}"
            )
            audio_path = await generate_audio(audio_text, output_filename)

            logger.info(f"Article summarization complete. Audio saved to {audio_path}")
            return audio_path

    async def _run_summarizer(self, article_text: str) -> SummaryData | None:
        """
        Run the summarizer agent on the article text.

        Args:
            article_text: The text of the article to summarize.

        Returns:
            The summary data or None if summarization failed.
        """
        try:
            result = await Runner.run(
                summarizer_agent,
                f"Article text:\n\n{article_text}",
            )
            return result.final_output_as(SummaryData)
        except Exception as e:
            logger.error(f"Error running summarizer agent: {e}")
            return None
