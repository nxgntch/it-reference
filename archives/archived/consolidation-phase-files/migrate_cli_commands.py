"""Batch migration: Consolidate CLI commands to use CommandRegistry."""

import logging
import sys
from pathlib import Path

from scripts.utils import find_files, format_success, read_file, write_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate_cli_commands")

CLI_DIR = Path("scripts/cli")


def migrate_cli_commands():
    """Migrate CLI command classes to use CommandRegistry pattern."""
    if not CLI_DIR.exists():
        logger.error(f"Directory not found: {CLI_DIR}")
        return False

    migrated = 0
    failed = 0

    py_files = find_files(CLI_DIR, "*.py")

    for filepath in py_files:
        try:
            content = read_file(filepath)

            # Skip base files or already migrated
            if filepath.name in ("base.py", "__init__.py") or "CommandRegistry" in content:
                continue

            # Skip files without command patterns
            if "def register_commands" not in content and "def execute_command" not in content:
                continue

            # Add import for CommandRegistry
            if "import " in content:
                lines = content.split("\n")
                last_import_idx = 0
                for i, line in enumerate(lines):
                    if line.startswith("import ") or line.startswith("from "):
                        last_import_idx = i

                import_line = "from scripts.utils import CommandRegistry"
                if import_line not in content:
                    lines.insert(last_import_idx + 1, import_line)
                content = "\n".join(lines)

            logger.info(f"Prepared for migration: {filepath.name}")
            write_file(filepath, content)
            migrated += 1

        except Exception as e:
            logger.error(f"Failed to process {filepath.name}: {e}")
            failed += 1

    logger.info(format_success(f"CLI command migration: {migrated} prepared, {failed} failed"))
    return failed == 0


if __name__ == "__main__":
    success = migrate_cli_commands()
    sys.exit(0 if success else 1)
