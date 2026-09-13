#!/usr/bin/env python3
"""Phase 20 Script 4: Test Migrator

Updates test files to work with consolidated base classes.
- Updates test imports
- Creates new fixtures for base classes
- Validates test compatibility

Usage:
    python3 scripts/phase20/04-migrate-tests.py \\
        --tests-root tests \\
        --category monitoring \\
        --validate
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import argparse


class TestMigrator:
    """Migrate test files for Phase 20 consolidation."""

    def __init__(self, tests_root: Path):
        self.tests_root = tests_root

    def migrate_category(self, category: str, dry_run: bool = False) -> Dict[str, bool]:
        """Migrate test files for a category.

        Args:
            category: Category name (e.g., "monitoring")
            dry_run: If True, don't write files

        Returns:
            Dict mapping file_path -> success_bool
        """
        results = {}

        # Find test files for category
        test_files = self._find_test_files(category)
        print(f"Found {len(test_files)} test files for {category}")

        for test_file in test_files:
            success = self._migrate_test_file(test_file, dry_run=dry_run)
            results[str(test_file)] = success

        return results

    def _find_test_files(self, category: str) -> List[Path]:
        """Find test files for a category."""
        test_files = []

        for pattern in [f"*{category}*", f"test_{category}*"]:
            matches = list(self.tests_root.rglob(f"{pattern}.py"))
            test_files.extend(matches)

        return list(set(test_files))  # Remove duplicates

    def _migrate_test_file(self, test_file: Path, dry_run: bool = False) -> bool:
        """Migrate a single test file.

        Args:
            test_file: Path to test file
            dry_run: If True, don't write file

        Returns:
            True if file was migrated, False otherwise
        """
        try:
            content = test_file.read_text()
            original = content

            # 1. Update imports for Request/Result classes
            content = re.sub(
                r"from\s+skills\.\w+\.inputs\s+import\s+(\w+Request)",
                "from skills.core.patterns import BaseRequest",
                content,
            )

            content = re.sub(
                r"from\s+skills\.\w+\.inputs\s+import\s+(\w+Result)",
                "from skills.core.patterns import BaseResult",
                content,
            )

            # 2. Update test fixtures if present
            if "def test_" in content or "@pytest.fixture" in content:
                content = self._update_test_fixtures(content)

            # 3. Update assertions for isinstance checks
            content = re.sub(
                r"isinstance\((\w+),\s+\w+Request\)",
                r"isinstance(\1, BaseRequest)",
                content,
            )

            content = re.sub(
                r"isinstance\((\w+),\s+\w+Result\)",
                r"isinstance(\1, BaseResult)",
                content,
            )

            if content == original:
                # No changes made
                return False

            if not dry_run:
                test_file.write_text(content)
                print(f"✓ Migrated tests: {test_file.relative_to(self.tests_root)}")
            else:
                print(f"[DRY RUN] Would migrate: {test_file.relative_to(self.tests_root)}")

            return True

        except Exception as e:
            print(f"Error migrating {test_file}: {e}")
            return False

    def _update_test_fixtures(self, content: str) -> str:
        """Update test fixtures to work with base classes."""

        # Add base class fixtures if not present
        base_fixtures = '''
@pytest.fixture
def base_request_factory():
    """Factory for creating BaseRequest instances in tests."""
    def _make_request(operation: str, **kwargs) -> BaseRequest:
        return BaseRequest(operation=operation, **kwargs)
    return _make_request


@pytest.fixture
def base_result_factory():
    """Factory for creating BaseResult instances in tests."""
    def _make_result(success: bool, **kwargs) -> BaseResult:
        return BaseResult(success=success, **kwargs)
    return _make_result
'''

        if "base_request_factory" not in content and "@pytest.fixture" in content:
            # Insert after first fixture
            insert_pos = content.find("@pytest.fixture")
            if insert_pos > 0:
                next_fixture = content.find("def test_", insert_pos)
                if next_fixture > 0:
                    content = (
                        content[:next_fixture] + base_fixtures + "\n\n" + content[next_fixture:]
                    )

        return content

    def validate_tests(self, category: str = "") -> Tuple[List[str], int]:
        """Validate test imports and structure.

        Args:
            category: Category to validate (empty = all)

        Returns:
            Tuple of (errors, warning_count)
        """
        errors = []
        warnings = 0

        test_files = (
            self._find_test_files(category)
            if category
            else list(self.tests_root.rglob("test_*.py"))
        )

        for test_file in test_files:
            try:
                content = test_file.read_text()

                # Check for unresolved imports
                if "from skills." in content and "core.patterns" not in content:
                    unresolved = re.findall(
                        r"from\s+(skills\.\w+\.inputs)",
                        content,
                    )
                    if unresolved:
                        errors.append(
                            f"{test_file.relative_to(self.tests_root)}: "
                            f"Unresolved import: {unresolved[0]}"
                        )

                # Check for old class references
                old_classes = re.findall(
                    r"\b(\w+Request|\w+Result)\b",
                    content,
                )
                if old_classes and "Request" not in str(old_classes):
                    warnings += 1

            except Exception as e:
                errors.append(f"{test_file}: {e}")

        return errors, warnings


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Migrate test files for Phase 20 consolidation.")
    parser.add_argument(
        "--tests-root",
        default="tests",
        help="Path to tests root directory",
    )
    parser.add_argument(
        "--category",
        default="",
        help="Specific category to migrate (optional)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without writing files",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate test files instead of migrating",
    )

    args = parser.parse_args()

    migrator = TestMigrator(Path(args.tests_root))

    if args.validate:
        print("Validating test files...")
        errors, warnings = migrator.validate_tests(args.category)

        if errors:
            print(f"\n❌ Found {len(errors)} errors:")
            for err in errors:
                print(f"  {err}")

        if warnings:
            print(f"\n⚠️  Found {warnings} potential issues")

        return 1 if errors else 0

    else:
        print("Migrating test files...")
        if args.dry_run:
            print("[DRY RUN MODE - No files will be written]")

        results = migrator.migrate_category(args.category, dry_run=args.dry_run)

        migrated = sum(1 for v in results.values() if v)
        print(f"\n✓ Migrated {migrated} test files")

        if not args.dry_run:
            print(f"Validating test files...")
            errors, warnings = migrator.validate_tests(args.category)

            if errors:
                print(f"\n❌ {len(errors)} validation errors!")
                return 1

            print(f"✓ All test files valid")
            print(f"\nNext: Run pytest to validate consolidation")

        return 0


if __name__ == "__main__":
    sys.exit(main())
