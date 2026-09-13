"""Batch migration: Consolidate validators to use base template."""

import logging
import sys
from pathlib import Path

from scripts.utils import find_files, format_success, read_file, write_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate_validators")

VALIDATE_DIR = Path("scripts/validate")


def migrate_validators():
    """Migrate validator classes to use base template."""
    if not VALIDATE_DIR.exists():
        logger.error(f"Directory not found: {VALIDATE_DIR}")
        return False

    migrated = 0
    failed = 0

    py_files = find_files(VALIDATE_DIR, "*.py")

    for filepath in py_files:
        try:
            content = read_file(filepath)

            # Skip base.py or __init__.py
            if filepath.name in ("base.py", "__init__.py"):
                continue

            # Skip if already has base import
            if "BaseValidator" in content:
                logger.debug(f"Already migrated: {filepath.name}")
                continue

            # Skip files without validator patterns
            if "def validate" not in content:
                continue

            # Add import for BaseValidator
            if "import " in content:
                lines = content.split("\n")
                # Find where to insert
                last_import_idx = 0
                for i, line in enumerate(lines):
                    if line.startswith("import ") or line.startswith("from "):
                        last_import_idx = i

                import_line = "from scripts.validate.base import BaseValidator"
                if import_line not in content:
                    lines.insert(last_import_idx + 1, import_line)
                content = "\n".join(lines)

            logger.info(f"Prepared for migration: {filepath.name}")
            write_file(filepath, content)
            migrated += 1

        except Exception as e:
            logger.error(f"Failed to process {filepath.name}: {e}")
            failed += 1

    logger.info(format_success(f"Validator migration: {migrated} prepared, {failed} failed"))
    return failed == 0


if __name__ == "__main__":
    success = migrate_validators()
    sys.exit(0 if success else 1)
