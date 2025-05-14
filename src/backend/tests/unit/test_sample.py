from backend.tests.conftest import MockUserRecord


def test_user_email_format(mock_user_record: MockUserRecord) -> None:
    """Basic format check on mocked user."""
    email = mock_user_record["email"]
    assert "@" in email
    assert email.endswith(".com")


def test_user_is_active(mock_user_record: MockUserRecord) -> None:
    assert mock_user_record["is_active"] is True
