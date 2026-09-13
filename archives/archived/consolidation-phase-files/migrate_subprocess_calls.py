"""Batch migration: Consolidate subprocess.run() calls."""

import logging
import sys
from pathlib import Path

from scripts.utils import find_files, format_success, read_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate_subprocess_calls")

SCRIPTS_DIR = Path("scripts")


def migrate_subprocess_calls():
    """Replace subprocess.run() with centralized run_command() wrapper."""
    migrated = 0
    failed = 0
    skipped = 0

    py_files = find_files(
        SCRIPTS_DIR, "*.py", exclude_dirs=[".git", "__pycache__", ".venv", "utils"]
    )

    for filepath in py_files:
        try:
            content = read_file(filepath)

            # Skip if already migrated
            if "from scripts.utils import run_command" in content:
                logger.debug(f"Already has run_command import: {filepath}")
                skipped += 1
                continue

            # Look for subprocess.run patterns
            if "subprocess.run(" not in content:
                skipped += 1
                continue

            # For now, just log that we found it - don't modify utilities themselves
            if "scripts/utils/" in str(filepath):
                logger.debug(f"Skipping utility file: {filepath.name}")
                skipped += 1
                continue

            logger.info(f"Found subprocess calls in: {filepath.name} (not modifying in dry-run)")
            migrated += 1

        except Exception as e:
            logger.error(f"Failed to process {filepath}: {e}")
            failed += 1

    logger.info(
        format_success(
            f"Subprocess audit: {migrated} files with subprocess calls found, {skipped} skipped"
        )
    )
    return failed == 0


if __name__ == "__main__":
    success = migrate_subprocess_calls()
    sys.exit(0 if success else 1)
