"""Phase 8: Batch consolidate validators and doc generators to use get_logger."""

import sys
from pathlib import Path

from scripts.utils import find_files, format_success, read_file, write_file

# Target directories
VALIDATE_DIR = Path("scripts/validate")
DOCS_DIR = Path("scripts/docs")


def consolidate_logger_pattern(content: str) -> tuple[str, bool]:
    """Replace logging.getLogger(__name__) with get_logger(__name__)."""
    if "from scripts.utils import get_logger" not in content:
        return content, False

    # Pattern 1: Plain getLogger call
    if "logger = logging.getLogger(__name__)" in content:
        content = content.replace(
            "logger = logging.getLogger(__name__)", "logger = get_logger(__name__)"
        )
        return content, True

    return content, False


def process_directory(directory: Path, name: str) -> tuple[int, int, int]:
    """Process all Python files in a directory."""
    if not directory.exists():
        print(f"⚠ Directory not found: {directory}")
        return 0, 0, 0

    consolidated = 0
    failed = 0
    skipped = 0

    py_files = find_files(directory, "*.py")

    for filepath in py_files:
        # Skip base.py and __init__.py
        if filepath.name in ("base.py", "__init__.py"):
            continue

        try:
            content = read_file(filepath)

            # Skip if already using get_logger
            if "logger = get_logger(__name__)" in content:
                skipped += 1
                continue

            # Try to consolidate
            new_content, changed = consolidate_logger_pattern(content)

            if changed:
                write_file(filepath, new_content)
                print(f"  ✓ Consolidated: {filepath.name}")
                consolidated += 1
            else:
                skipped += 1

        except Exception as e:
            print(f"  ✗ Failed: {filepath.name}: {e}")
            failed += 1

    return consolidated, failed, skipped


def main():
    """Main entry point for Phase 8 consolidation."""
    print("=" * 70)
    print("PHASE 8: Consolidating Validators & Doc Generators")
    print("=" * 70)
    print()

    print("📋 Processing validators...")
    v_consolidated, v_failed, v_skipped = process_directory(VALIDATE_DIR, "validators")
    print(f"  Result: {v_consolidated} consolidated, {v_skipped} skipped, {v_failed} failed")
    print()

    print("📋 Processing doc generators...")
    d_consolidated, d_failed, d_skipped = process_directory(DOCS_DIR, "doc generators")
    print(f"  Result: {d_consolidated} consolidated, {d_skipped} skipped, {d_failed} failed")
    print()

    # Summary
    total_consolidated = v_consolidated + d_consolidated
    total_failed = v_failed + d_failed
    total_skipped = v_skipped + d_skipped

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✓ Consolidated: {total_consolidated}")
    print(f"✓ Skipped: {total_skipped}")
    print(f"✗ Failed: {total_failed}")
    print()

    if total_failed == 0:
        print(
            format_success(
                f"Phase 8 complete: {total_consolidated} validators/generators consolidated"
            )
        )
        return 0
    else:
        print(f"Phase 8 partial: {total_failed} files need manual review")
        return 1


if __name__ == "__main__":
    sys.exit(main())
