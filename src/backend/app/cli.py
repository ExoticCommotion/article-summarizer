"""Article Summarizer CLI.

Usage examples:
    uv run python -m backend.app.cli greet                # → Hello, Example!
    uv run python -m backend.app.cli greet "Example User" # → Hello, Example User!
    uv run python -m backend.app.cli summarize https://example.com/article
"""

from __future__ import annotations

import typer
from rich import print

from backend.app.custom_agents.article_summarizer.cli import app as summarize_app

app = typer.Typer(add_completion=False, help="🧠 Article Summarizer CLI")

# ------------------------------------------------------------------ #
#  Example command with diverse arguments
# ------------------------------------------------------------------ #


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


app.add_typer(summarize_app, name="summarize")

# ------------------------------------------------------------------ #
#  Python ‑m entry shim
# ------------------------------------------------------------------ #

if __name__ == "__main__":
    app()
