#!/usr/bin/env python3
"""Fix common indentation errors in Python files.
Detects patterns where lines after if/for/while/try etc. aren't indented.
"""

import logging
import re
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)


def fix_indentation_in_file(file_path: Path) -> Tuple[bool, str]:
    """Fix indentation errors in a file by scanning control structures.
    Args:
       file_path: Path to Python file
    Returns:
       Tuple of (modified, message)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return False, f"Error reading: {e}"

    modified = False
    i = 0
    while i < len(lines):
        line = lines[i]
        line.lstrip()

        # Check for control structures ending with colon
        if re.match(
            r"^\s*(if|elif|else|for|while|try|except|finally|with|def|class)\b", line
        ) and line.rstrip().endswith(":"):
            # Scan following lines (may be multiple lines of code)
            i += 1
            while i < len(lines):
                next_line = lines[i]
                next_stripped = next_line.lstrip()

                # Skip blank lines
                if not next_stripped:
                    i += 1
                    continue

                # Skip decorator and docstring lines
                if next_stripped.startswith(("@", '"""', "'''", '"', "'")):
                    i += 1
                    continue

                # Current indentation of control structure
                ctrl_indent = len(line) - len(line.lstrip())
                # Current indentation of next line
                next_indent = len(next_line) - len(next_line.lstrip())

                # If next line has same or less indentation, it's wrong
                if next_indent <= ctrl_indent:
                    # Add indentation (use 3 spaces to match codebase)
                    lines[i] = " " * (ctrl_indent + 3) + next_stripped
                    modified = True
                    # Check if this line also ends with colon (nested structure)
                    if next_stripped.rstrip().endswith(":"):
                        # Skip to end of this block before continuing
                        i += 1
                        continue
                    else:
                        # This line is fixed, move on
                        break
                else:
                    # Properly indented, we're done with this block
                    break

        i += 1

    if modified:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True, "Fixed"
        except Exception as e:
            return False, f"Error writing: {e}"

    return False, "No changes"


def main() -> int:
    """Fix all indentation errors in app directory."""
    files_to_fix = sorted(Path("app").rglob("*.py"))
    fixed_count = 0

    # Multiple passes to handle nested structures
    for _attempt in range(3):
        for file_path in files_to_fix:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    compile(f.read(), str(file_path), "exec")
            except IndentationError:
                modified, _ = fix_indentation_in_file(file_path)
                if modified:
                    fixed_count += 1

    logger.info(f"[DONE] Fixed {fixed_count} files")


if __name__ == "__main__":
    main()
