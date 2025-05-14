"""
Main application for the Article Audio Converter.

This module provides the FastAPI application for the Article Audio Converter.
"""

import uvicorn
from fastapi import FastAPI

# TODO: Complete this

app = FastAPI(title="Article Audio Converter")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


def run_app() -> None:
    """Run the FastAPI application."""
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_app()
