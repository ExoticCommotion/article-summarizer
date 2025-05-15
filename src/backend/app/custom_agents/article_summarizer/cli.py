"""CLI for article summarization."""

import asyncio
import sys
from pathlib import Path

import typer
from rich import print

from backend.app.custom_agents.article_summarizer.manager import ArticleSummarizerManager
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

app = typer.Typer(
    add_completion=False,
    help="🔍 Article Summarizer - Convert articles to audio summaries",
)


@app.command()
def summarize(
    url: str = typer.Argument(..., help="URL of the article to summarize"),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
) -> None:
    """
    Summarize an article from a URL and generate an audio file.

    Examples
    --------
    uv run python -m backend.app.cli summarize https://example.com/article
    uv run python -m backend.app.cli summarize https://example.com/article --verbose
    """
    if verbose:
        print(f"[bold blue]Summarizing article from URL:[/] {url}")

    audio_path = asyncio.run(_summarize_article(url))

    if not audio_path:
        print("[bold red]Failed to summarize article.[/]")
        sys.exit(1)

    print(f"[bold green]Summary audio generated:[/] {audio_path}")


async def _summarize_article(url: str) -> Path:
    """Run the article summarization process."""
    manager = ArticleSummarizerManager()
    result = await manager.summarize_article(url)
    if not result:
        print("[bold red]Failed to summarize article.[/]")
        sys.exit(1)
    return result


if __name__ == "__main__":
    app()
