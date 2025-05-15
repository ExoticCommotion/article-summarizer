"""Audio generation utilities."""

import os
from pathlib import Path

from openai import AsyncOpenAI

from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(exist_ok=True)

DEFAULT_VOICE = "alloy"


async def generate_audio(text: str, output_filename: str) -> Path:
    """
    Generate audio from text using OpenAI's text-to-speech API.

    Args:
        text: The text to convert to speech.
        output_filename: The name of the output file (without extension).

    Returns:
        The path to the generated audio file.
    """
    logger.info(f"Generating audio for text ({len(text)} chars)")

    client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    output_path = OUTPUTS_DIR / f"{output_filename}.mp3"

    response = await client.audio.speech.create(
        model="tts-1",
        voice=DEFAULT_VOICE,
        input=text,
        response_format="mp3",
    )

    audio_data = response.content
    with open(output_path, "wb") as f:
        f.write(audio_data)

    logger.info(f"Audio saved to {output_path}")
    return output_path
