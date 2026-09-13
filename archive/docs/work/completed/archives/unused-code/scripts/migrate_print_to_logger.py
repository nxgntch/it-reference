#!/usr/bin/env python3
"""Migrate all print() calls to logger.info() for consistent logging.

This script safely replaces print() calls with logger.info() while preserving
docstrings, comments, and intentional string literals containing 'logger.info('.

Usage:
    python scripts/migrate_print_to_logger.py
    python scripts/migrate_print_to_logger.py app/  # specific directory
"""

import re
import sys
from pathlib import Path


def needs_logger_import(content: str) -> bool:
    """Check if file needs logger import."""
    return "logger" not in content or "logger =" not in content


def add_logger_import(content: str) -> str:
    """Add logger import if missing."""
    if "logger =" in content:
        return content

    # Add after initial imports
    lines = content.split("\n")
    import_index = 0
    for i, line in enumerate(lines):
        if line.startswith("import ") or line.startswith("from "):
            import_index = i + 1

    if "import logging" not in content:
        lines.insert(import_index, "import logging")
        import_index += 1

    if "logger =" not in content:
        # Find where to add logger =
        for i in range(import_index, len(lines)):
            if not lines[i].startswith("import ") and not lines[i].startswith("from "):
                lines.insert(i, "\nlogger = logging.getLogger(__name__)\n")
                break

    return "\n".join(lines)


def replace_print_calls(content: str) -> str:
    """Replace logger.info() calls with logger.info()."""
    lines = content.split("\n")
    in_docstring = False
    triple_quote_char = None
    modified = False

    for i, line in enumerate(lines):
        # Track triple-quoted strings
        for match in re.finditer(r'"""|\'\'\' ', line):
            quote = match.group(0)
            if quote == triple_quote_char:
                in_docstring = not in_docstring
                triple_quote_char = None
            elif not in_docstring:
                in_docstring = True
                triple_quote_char = quote

        # Skip lines inside docstrings or comments
        if in_docstring or line.strip().startswith("#"):
            continue

        # Skip lines with >>> (docstring examples)
        if ">>>" in line:
            continue

        # Replace print( with logger.info(
        if "logger.info(" in line:
            original = line
            # Only replace if it's not inside a string literal
            # This is a simple heuristic: replace print( that's not quoted
            if "logger.info(" in line and not (
                "'" in line and "logger.info(" in line.split("'")[1:]
            ):
                line = re.sub(r"print\(", "logger.info(", line)
                if line != original:
                    modified = True
                    lines[i] = line

    return "\n".join(lines), modified


def migrate_file(filepath: Path) -> int:
    """Migrate a single file. Return number of changes."""
    content = filepath.read_text()
    original = content

    # Add logger if needed
    if needs_logger_import(content):
        content = add_logger_import(content)

    # Replace print calls
    content, _modified = replace_print_calls(content)

    if content != original:
        filepath.write_text(content)
        changes = original.count("logger.info(") - content.count("logger.info(")
        return changes
    return 0


def main() -> None:
    """Migrate print statements to logging calls across target directory.

    Usage: python migrate_print_to_logger.py [target_dir]
    """
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/workspace/it")

    total_changes = 0
    files_modified = 0

    for py_file in sorted(target_dir.rglob("*.py")):
        if "__pycache__" in str(py_file):
            continue

        changes = migrate_file(py_file)
        if changes > 0:
            files_modified += 1
            total_changes += changes
            logger.info(f"✓ {py_file.relative_to(target_dir)}: {changes} replacements")

    logger.info(
        f"\n✓ Migration complete: {files_modified} files modified, {total_changes} total replacements"
    )


if __name__ == "__main__":
    main()
