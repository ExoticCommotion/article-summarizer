"""Tests for audio generation."""

import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.app.custom_agents.article_summarizer.audio import generate_audio


@pytest.mark.asyncio
async def test_generate_audio():
    """Test audio generation."""
    mock_response = MagicMock()
    mock_response.content = b"audio data"

    mock_speech = AsyncMock()
    mock_speech.create = AsyncMock(return_value=mock_response)

    mock_audio = MagicMock()
    mock_audio.speech = mock_speech

    mock_client = MagicMock()
    mock_client.audio = mock_audio

    with (
        patch(
            "backend.app.custom_agents.article_summarizer.audio.AsyncOpenAI",
            return_value=mock_client,
        ),
        patch("backend.app.custom_agents.article_summarizer.audio.open", MagicMock()) as mock_open,
        patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}),
    ):
        result = await generate_audio("Test text", "test_output")

        assert isinstance(result, Path)
        assert str(result).endswith("test_output.mp3")

        mock_speech.create.assert_called_once_with(
            model="tts-1",
            voice="alloy",
            input="Test text",
            response_format="mp3",
        )

        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_called_once_with(b"audio data")
