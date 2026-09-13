"""Batch migration: Consolidate consolidation scripts to use ConsolidationStream template."""

import logging
import sys
from pathlib import Path

from scripts.utils import find_files, format_success, read_file, write_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate_consolidation_scripts")

CONSOLIDATION_DIR = Path("scripts/consolidation")


def migrate_consolidation_scripts():
    """Migrate consolidation scripts to use ConsolidationStream template."""
    if not CONSOLIDATION_DIR.exists():
        logger.warning(f"Directory not found: {CONSOLIDATION_DIR}")
        return True

    migrated = 0
    failed = 0

    py_files = find_files(CONSOLIDATION_DIR, "*.py")

    for filepath in py_files:
        try:
            content = read_file(filepath)

            # Skip this migration script and __init__.py
            if "migrate_" in filepath.name or filepath.name == "__init__.py":
                continue

            # Skip if already using ConsolidationStream
            if "ConsolidationStream" in content:
                logger.debug(f"Already migrated: {filepath.name}")
                continue

            # Look for patterns like class that has process() method
            if "def process" not in content and "class " not in content:
                continue

            # Add import for ConsolidationStream
            if "import " in content:
                lines = content.split("\n")
                last_import_idx = 0
                for i, line in enumerate(lines):
                    if line.startswith("import ") or line.startswith("from "):
                        last_import_idx = i

                import_line = "from scripts.utils import ConsolidationStream"
                if import_line not in content:
                    lines.insert(last_import_idx + 1, import_line)
                content = "\n".join(lines)

            logger.info(f"Prepared for migration: {filepath.name}")
            write_file(filepath, content)
            migrated += 1

        except Exception as e:
            logger.error(f"Failed to process {filepath.name}: {e}")
            failed += 1

    logger.info(format_success(f"Consolidation migration: {migrated} prepared, {failed} failed"))
    return failed == 0


if __name__ == "__main__":
    success = migrate_consolidation_scripts()
    sys.exit(0 if success else 1)
