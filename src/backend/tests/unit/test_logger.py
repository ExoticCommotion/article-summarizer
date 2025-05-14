# src/backend/tests/unit/test_logger.py

import logging

from backend.app.utils.logger import get_logger


def test_get_logger_creates_handlers() -> None:
    logger_name = "test_logger_clean"

    # Clear any pre-existing logger config (critical!)
    existing_logger = logging.getLogger(logger_name)
    existing_logger.handlers.clear()
    existing_logger.propagate = False

    # Get a fresh logger using our factory
    logger = get_logger(logger_name)

    # Assertions
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name
    assert len(logger.handlers) == 2

    handler_types = {type(h) for h in logger.handlers}
    assert logging.FileHandler in handler_types
    assert logging.StreamHandler in handler_types
