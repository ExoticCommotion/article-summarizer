import asyncio
import subprocess
import sys

from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

# --- Constants ---
OUTPUT_DIR = "outputs"
ENTRYPOINT = "src/backend/app/cli.py"


async def run_cli_test() -> None:
    """Run a CLI-based test."""
    logger.info("=== Running CLI Test ===")

    # Example: Run CLI script with example args
    result = subprocess.run(
        [sys.executable, ENTRYPOINT, "--example-string", "hello", "--example-flag"],
        capture_output=True,
        text=True,
    )

    logger.info("CLI output:\n%s", result.stdout)
    assert result.returncode == 0, "CLI did not exit cleanly"
    assert "hello" in result.stdout.lower(), "Expected output not found"
    assert "example-flag" in result.stdout.lower(), "Expected flag usage not confirmed"

    logger.info("✅ CLI test passed.")


if __name__ == "__main__":
    asyncio.run(run_cli_test())
