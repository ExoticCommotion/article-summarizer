"""
Async‑function unit tests that run with pytest‑asyncio.

Nothing in here depends on project code yet; swap in your own async helpers later.
"""

import asyncio

import pytest


async def async_identity(x: int, delay: float = 0.01) -> int:
    """Returns *x* after a short sleep – placeholder for real async IO."""
    await asyncio.sleep(delay)
    return x


@pytest.mark.asyncio
async def test_async_identity() -> None:
    value = await async_identity(42)
    assert value == 42
