"""Batch migration: Remove camelCase shims and backward-compat aliases."""

import logging
import re
import sys
from pathlib import Path

from scripts.utils import format_success, read_file, write_file

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("remove_shims")

BASE_FILES = [
    Path("scripts/base.py"),
    Path("scripts/validate/base.py"),
    Path("scripts/sync/base.py"),
    Path("scripts/docs/base.py"),
    Path("scripts/profiling/base.py"),
    Path("scripts/cli/base.py"),
]


def remove_shims():
    """Remove camelCase shims and backward-compat aliases from base classes."""
    removed = 0
    failed = 0

    for filepath in BASE_FILES:
        if not filepath.exists():
            logger.warning(f"Base file not found: {filepath}")
            continue

        try:
            content = read_file(filepath)

            # Track shim patterns to remove
            # Pattern: def camelCaseMethod(self, ...): pass  # alias for snake_case_method
            shim_pattern = (
                r"\n    def [a-z][a-zA-Z]+\(self.*?\):[^\n]*# (?:alias|shim|backward|compat)"
            )

            matches = re.finditer(shim_pattern, content)
            match_count = len(list(matches))

            if match_count > 0:
                # Remove shim methods - simple approach: remove lines with alias/shim comments
                lines = content.split("\n")
                filtered_lines = [
                    line
                    for line in lines
                    if not (
                        "# alias" in line
                        or "# shim" in line
                        or "# backward" in line
                        or "# compat" in line
                    )
                ]

                new_content = "\n".join(filtered_lines)

                if new_content != content:
                    logger.info(f"Removed {match_count} shims from {filepath.name}")
                    write_file(filepath, new_content)
                    removed += match_count

        except Exception as e:
            logger.error(f"Failed to process {filepath}: {e}")
            failed += 1

    logger.info(format_success(f"Shim removal: {removed} removed, {failed} failed"))
    return failed == 0


if __name__ == "__main__":
    success = remove_shims()
    sys.exit(0 if success else 1)
