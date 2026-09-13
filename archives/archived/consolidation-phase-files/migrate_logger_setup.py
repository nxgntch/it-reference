"""Batch migration: Centralize logger initialization."""

import logging
import sys
from pathlib import Path

from scripts.utils import find_files, format_success, read_file, write_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate_logger_setup")

SCRIPTS_DIR = Path("scripts")


def migrate_logger_setup():
    """Migrate all logger initialization to use centralized get_logger()."""
    migrated = 0
    failed = 0

    py_files = find_files(SCRIPTS_DIR, "*.py")

    for filepath in py_files:
        try:
            content = read_file(filepath)

            # Skip files without logging
            if "logging.basicConfig" not in content and "logging.getLogger" not in content:
                continue

            # Skip if already uses get_logger
            if "from scripts.utils import get_logger" in content:
                logger.debug(f"Already migrated: {filepath.name}")
                continue

            # Add import for get_logger if using logging
            if "import logging" in content or "from logging import" in content:
                lines = content.split("\n")
                last_import_idx = 0
                for i, line in enumerate(lines):
                    if line.startswith("import ") or line.startswith("from "):
                        last_import_idx = i

                import_line = "from scripts.utils import get_logger"
                if import_line not in content:
                    lines.insert(last_import_idx + 1, import_line)
                content = "\n".join(lines)

                logger.info(f"Added get_logger import: {filepath.name}")
                write_file(filepath, content)
                migrated += 1

        except Exception as e:
            logger.error(f"Failed to process {filepath.name}: {e}")
            failed += 1

    logger.info(format_success(f"Logger migration: {migrated} updated, {failed} failed"))
    return failed == 0


if __name__ == "__main__":
    success = migrate_logger_setup()
    sys.exit(0 if success else 1)
