"""Audio generation utilities."""

import os
from pathlib import Path

from openai import AsyncOpenAI

from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(exist_ok=True)

DEFAULT_VOICE = "alloy"


async def generate_audio(
    text: str, output_filename: str, article_title: str, article_content: str, formatted_text: str
) -> tuple[Path, Path, Path]:
    """
    Generate audio from text using OpenAI's text-to-speech API and save output files.

    Args:
        text: The text to convert to speech.
        output_filename: The name of the output file (without extension).
        article_title: The title of the article.
        article_content: The raw text content of the article.
        formatted_text: The formatted text ready for audio processing.

    Returns:
        A tuple containing the paths to the generated audio file, raw text file, and final text file.
    """
    import datetime
    import re

    logger.info(f"Generating audio for text ({len(text)} chars)")

    safe_title = re.sub(r"[^\w\-_]", "_", article_title)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir_name = f"{safe_title}_{timestamp}"

    run_dir = OUTPUTS_DIR / run_dir_name
    run_dir.mkdir(exist_ok=True)

    audio_path = run_dir / "final.mp3"
    raw_text_path = run_dir / "raw.txt"
    final_text_path = run_dir / "final.txt"

    with open(raw_text_path, "w", encoding="utf-8") as f:
        f.write(article_content)
    logger.info(f"Raw text content saved to {raw_text_path}")

    with open(final_text_path, "w", encoding="utf-8") as f:
        f.write(formatted_text)
    logger.info(f"Final text content saved to {final_text_path}")

    # Generate audio
    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = await client.audio.speech.create(
        model="tts-1",
        voice=DEFAULT_VOICE,
        input=text,
        response_format="mp3",
    )

    audio_data = response.content
    with open(audio_path, "wb") as f:
        f.write(audio_data)

    logger.info(f"Audio saved to {audio_path}")
    return audio_path, raw_text_path, final_text_path
