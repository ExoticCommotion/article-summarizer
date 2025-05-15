"""Article Summarizer CLI.

Usage examples:
    uv run python -m backend.app.cli greet                # → Hello, Example!
    uv run python -m backend.app.cli greet "Example User" # → Hello, Example User!
    uv run python -m backend.app.cli summarize https://example.com/article
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import typer
from rich import print

from backend.app.custom_agents.article_summarizer.manager import ArticleSummarizerManager
from backend.app.utils.logger import get_logger

logger = get_logger(__name__)
app = typer.Typer(add_completion=False, help="🧠 Article Summarizer CLI")



@app.command()
def greet(
    name: str = typer.Argument("Example", help="Name to greet"),
    times: int = typer.Option(1, "--times", "-t", help="Repeat how many times"),
    excited: bool = typer.Option(
        False,
        "--excited/--no-excited",
        help="Add an exclamation mark!",
    ),
) -> None:
    """Greet NAME a number of TIMES.

    Examples
    --------
    uv run python -m backend.app.cli greet
    uv run python -m backend.app.cli greet "Example" --times 3 --excited
    """
    punctuation = "!" if excited else "."
    for _ in range(times):
        print(f"[bold green]Hello, {name}{punctuation}[/]")




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
