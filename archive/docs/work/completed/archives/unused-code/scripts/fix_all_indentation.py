#!/usr/bin/env python3
"""Smart indentation fixer - handles multi-line indentation blocks safely."""

import logging
import re
from pathlib import Path
from typing import Tuple

logger = logging.getLogger(__name__)


def fix_file_indentation(file_path: Path) -> Tuple[bool, str]:
    """Fix indentation in a single file by adjusting blocks after control structures."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception as e:
        return False, f"Read error: {e}"

    modified = False
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip()

        # Check for control structures
        if re.match(r"^\s*(if|elif|else|for|while|try|except|finally|with|def|class)\b", line):
            if line.rstrip().endswith(":"):
                # This line ends with colon, next lines should be indented
                ctrl_indent = len(line) - len(stripped)
                j = i + 1

                # Process subsequent lines that belong to this block
                while j < len(lines):
                    next_line = lines[j]
                    next_stripped = next_line.lstrip()

                    # Skip blank lines
                    if not next_stripped:
                        j += 1
                        continue

                    # Skip lines that are already properly indented
                    next_indent = len(next_line) - len(next_stripped)
                    if next_indent > ctrl_indent:
                        # Already indented, might be part of block
                        j += 1
                        # If this line ends with colon, continue scanning
                        if next_stripped.rstrip().endswith(":"):
                            continue
                        # Otherwise, we've hit an indented line that's part of block
                        if not next_stripped.startswith(("@", "#")):
                            break
                        j += 1
                        continue

                    # Line needs indentation
                    if next_indent <= ctrl_indent and next_stripped:
                        if not next_stripped.startswith(("@", "#")):
                            # Add proper indentation (3 spaces)
                            lines[j] = " " * (ctrl_indent + 3) + next_stripped
                            modified = True
                        j += 1
                    else:
                        # Properly indented or part of next block
                        break

        i += 1

    if modified:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            return True, "Fixed"
        except Exception as e:
            return False, f"Write error: {e}"

    return False, "No changes"


def main() -> int:
    """Fix indentation in all app/ files with errors."""
    app_dir = Path("app")
    fixed = 0
    failed = []

    # Single pass through all files
    for py_file in sorted(app_dir.rglob("*.py")):
        try:
            with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                compile(f.read(), str(py_file), "exec")
        except (IndentationError, SyntaxError):
            # File has error, try to fix it
            ok, _msg = fix_file_indentation(py_file)
            if ok:
                # Verify fix worked
                try:
                    with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
                        compile(f.read(), str(py_file), "exec")
                    logger.info(f"[OK] {py_file.name:40s} - Fixed and verified")
                    fixed += 1
                except Exception:
                    logger.info(f"[FAIL] {py_file.name:40s} - Fixed but still has errors")
                    failed.append(py_file.name)
            else:
                logger.info(f"[SKIP] {py_file.name:40s} - No changes made")

    logger.info(f"\n[DONE] Fixed {fixed} files")
    if failed:
        logger.info(f"[WARN] {len(failed)} files still have errors: {', '.join(failed[:5])}")


if __name__ == "__main__":
    main()
