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
        result = await generate_audio(
            "Test text", "test_output", "Test Article", "Test article content", "Formatted text"
        )

        audio_path, raw_text_path, final_text_path = result
        assert isinstance(audio_path, Path)
        assert isinstance(raw_text_path, Path)
        assert isinstance(final_text_path, Path)
        assert audio_path.name == "final.mp3"
        assert raw_text_path.name == "raw.txt"
        assert final_text_path.name == "final.txt"

        mock_speech.create.assert_called_once_with(
            model="tts-1",
            voice="alloy",
            input="Test text",
            response_format="mp3",
        )

        mock_file = mock_open.return_value.__enter__.return_value
        mock_file.write.assert_any_call("Test article content")
        mock_file.write.assert_any_call("Formatted text")
        mock_file.write.assert_any_call(b"audio data")
