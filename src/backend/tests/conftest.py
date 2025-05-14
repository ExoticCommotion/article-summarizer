from pathlib import Path
from typing import TypedDict

import pytest


@pytest.fixture
def sample_text() -> str:
    return "This is sample text. It has content."


@pytest.fixture
def temp_output_file(tmp_path: Path) -> str:
    return str(tmp_path / "test_output.mp3")


class MockUserRecord(TypedDict):
    id: int
    name: str
    email: str
    is_active: bool


# Fixture
@pytest.fixture
def mock_user_record() -> MockUserRecord:
    return {
        "id": 42,
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "is_active": True,
    }
