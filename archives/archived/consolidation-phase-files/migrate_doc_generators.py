"""Batch migration: Consolidate doc generators to use DocumentGenerator template."""

import logging
import sys
from pathlib import Path

from scripts.utils import find_files, format_success, read_file, write_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate_doc_generators")

DOCS_DIR = Path("scripts/docs")


def migrate_doc_generators():
    """Migrate doc generator classes to use DocumentGenerator template."""
    if not DOCS_DIR.exists():
        logger.error(f"Directory not found: {DOCS_DIR}")
        return False

    migrated = 0
    failed = 0

    py_files = find_files(DOCS_DIR, "*.py")

    for filepath in py_files:
        try:
            content = read_file(filepath)

            # Skip base.py or __init__.py
            if filepath.name in ("base.py", "__init__.py"):
                continue

            # Skip if already migrated
            if (
                "DocumentGenerator" in content
                or "from scripts.utils import DocumentGenerator" in content
            ):
                logger.debug(f"Already migrated: {filepath.name}")
                continue

            # Skip files without generator patterns
            if "class " not in content or "def generate" not in content:
                continue

            # Add import for DocumentGenerator
            if "import " in content:
                lines = content.split("\n")
                import_line = "from scripts.utils import DocumentGenerator"
                # Insert after last import
                last_import_idx = 0
                for i, line in enumerate(lines):
                    if line.startswith("import ") or line.startswith("from "):
                        last_import_idx = i
                lines.insert(last_import_idx + 1, import_line)
                content = "\n".join(lines)

            logger.info(f"Prepared for migration: {filepath.name}")
            write_file(filepath, content)
            migrated += 1

        except Exception as e:
            logger.error(f"Failed to process {filepath.name}: {e}")
            failed += 1

    logger.info(format_success(f"Doc generator migration: {migrated} prepared, {failed} failed"))
    return failed == 0


if __name__ == "__main__":
    success = migrate_doc_generators()
    sys.exit(0 if success else 1)
