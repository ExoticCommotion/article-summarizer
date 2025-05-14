from pathlib import Path

import pytest


@pytest.fixture
def empty_mp3_file(tmp_path: Path) -> Path:
    """Creates an empty placeholder MP3 file for file-based integration tests."""
    file_path = tmp_path / "blank.mp3"
    file_path.write_bytes(b"")  # you could also write mock bytes
    return file_path
