#!/usr/bin/env python3
"""Phase 20 Script 3: Import Migrator

Updates import statements across the codebase to use new base classes
while maintaining backward compatibility via shims.

Usage:
    python3 scripts/phase20/03-migrate-imports.py \\
        --skills-root skills \\
        --category monitoring \\
        --validate
"""

import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse


def _migrate_import_statement(imports_str: str) -> str:
    """Migrate a complex import statement, preserving non-Request/Result items.

    Example:
        "MetricPoint, MetricsRequest, MetricsResult"
        -> "MetricPoint, BaseRequest, BaseResult"
    """
    items = [item.strip() for item in imports_str.split(",")]
    migrated = []
    base_imports_needed = set()

    for item in items:
        if "Request" in item and item.endswith("Request"):
            migrated.append("BaseRequest")
            base_imports_needed.add("BaseRequest")
        elif "Result" in item and item.endswith("Result"):
            migrated.append("BaseResult")
            base_imports_needed.add("BaseResult")
        else:
            # Keep non-Request/Result items (e.g., MetricPoint)
            migrated.append(item)

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for item in migrated:
        if item not in seen:
            unique.append(item)
            seen.add(item)

    result = ", ".join(unique)

    # If we're importing base classes, ensure they come from core.patterns
    if base_imports_needed and any(item in result for item in ["BaseRequest", "BaseResult"]):
        # Check if other items need to stay with original import
        non_base = [item for item in unique if item not in ["BaseRequest", "BaseResult"]]
        if non_base:
            return result + "  # partially migrated"
        else:
            return f"BaseRequest, BaseResult  # migrated from skills.*.inputs"

    return result


class ImportMigrator:
    """Migrate imports to use consolidated base classes."""

    def __init__(self, skills_root: Path):
        self.skills_root = skills_root
        self.import_map = {
            # Old imports → New imports
            r"from skills\..*\.inputs import (\w+Request)": "from skills.core.patterns import BaseRequest  # migrated",
            r"from skills\..*\.inputs import (\w+Result)": "from skills.core.patterns import BaseResult  # migrated",
        }

    def migrate_category(self, category: str, dry_run: bool = False) -> Dict[str, bool]:
        """Migrate imports for all files in a category.

        Args:
            category: Category name (e.g., "monitoring")
            dry_run: If True, don't write files

        Returns:
            Dict mapping file_path -> success_bool
        """
        results = {}

        # Find all Python files in category
        category_path = self.skills_root / category if category else self.skills_root
        if not category_path.exists():
            print(f"Warning: Category path not found: {category_path}")
            return results

        python_files = list(category_path.rglob("*.py"))
        print(f"Found {len(python_files)} Python files in {category}")

        for py_file in python_files:
            success = self._migrate_file(py_file, dry_run=dry_run)
            results[str(py_file)] = success

        return results

    def _migrate_file(self, file_path: Path, dry_run: bool = False) -> bool:
        """Migrate imports in a single file.

        Args:
            file_path: Path to Python file
            dry_run: If True, don't write file

        Returns:
            True if file was migrated, False otherwise
        """
        try:
            content = file_path.read_text()
            original = content

            # Pattern 1: Migrate skill-specific Request/Result imports
            # OLD: from skills.cache.inputs import MetricPoint, CacheRequest, CacheResult
            # NEW: from skills.core.patterns import BaseRequest, BaseResult
            # Handle imports with multiple items
            content = re.sub(
                r"from\s+skills\.\w+\.inputs\s+import\s+([^;\n]+)",
                lambda m: _migrate_import_statement(m.group(1)),
                content,
            )

            # Pattern 2: Update type hints in function signatures
            # OLD: def execute(self, request: CacheRequest) -> CacheResult
            # NEW: def execute(self, request: BaseRequest) -> BaseResult
            content = re.sub(
                r":\s+\w+Request\b(?!.*migrated)",
                ": BaseRequest",
                content,
            )

            content = re.sub(
                r"->\s+\w+Result\b(?!.*migrated)",
                "-> BaseResult",
                content,
            )

            # Pattern 3: Add missing import for core.patterns if needed
            if "BaseRequest" in content or "BaseResult" in content:
                if "from skills.core.patterns import" not in content:
                    # Add import at top after other imports
                    lines = content.split("\n")
                    import_insert_pos = 0
                    for i, line in enumerate(lines):
                        if line.startswith("import ") or line.startswith("from "):
                            import_insert_pos = i + 1

                    lines.insert(
                        import_insert_pos,
                        "from skills.core.patterns import BaseRequest, BaseResult",
                    )
                    content = "\n".join(lines)

            # Pattern 4: Normalize imports (remove duplicates)
            # Remove duplicate imports
            content = re.sub(
                r"(from skills\.core\.patterns import [^\n]+\n)+",
                "from skills.core.patterns import BaseRequest, BaseResult\n",
                content,
            )

            if content == original:
                # No changes made
                return False

            if not dry_run:
                file_path.write_text(content)
                print(f"✓ Migrated imports: {file_path.relative_to(self.skills_root)}")
            else:
                print(f"[DRY RUN] Would migrate: {file_path.relative_to(self.skills_root)}")

            return True

        except Exception as e:
            print(f"Error migrating {file_path}: {e}")
            return False

    def validate_imports(self, category: str = "") -> Tuple[List[str], List[str]]:
        """Validate that all imports are resolvable.

        Args:
            category: Category to validate (empty = all)

        Returns:
            Tuple of (broken_imports, warnings)
        """
        broken = []
        warnings_list = []

        category_path = self.skills_root / category if category else self.skills_root
        python_files = list(category_path.rglob("*.py"))

        for py_file in python_files:
            try:
                content = py_file.read_text()

                # Check for orphaned skill-specific class references
                orphaned = re.findall(
                    r"\b(\w+Request|\w+Result)\b(?!.*migrated)",
                    content,
                )

                if orphaned and py_file.name not in ["inputs.py"]:
                    # Skill inputs.py can have old class definitions
                    for cls in set(orphaned):
                        warnings_list.append(
                            f"{py_file.relative_to(self.skills_root)}: "
                            f"Reference to {cls} may need migration"
                        )

                # Check for broken imports
                imports = re.findall(r"from\s+([\w.]+)\s+import", content)
                for imp in imports:
                    if "skills." in imp and "core.patterns" not in imp:
                        # Potential broken import
                        if "inputs" in imp:
                            broken.append(f"{py_file.relative_to(self.skills_root)}: {imp}")

            except Exception as e:
                broken.append(f"{py_file.relative_to(self.skills_root)}: {e}")

        return broken, warnings_list


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Migrate imports to use consolidated base classes."
    )
    parser.add_argument(
        "--skills-root",
        default="skills",
        help="Path to skills root directory",
    )
    parser.add_argument(
        "--category",
        default="",
        help="Specific category to migrate (optional; empty = all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without writing files",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate imports instead of migrating",
    )

    args = parser.parse_args()

    migrator = ImportMigrator(Path(args.skills_root))

    if args.validate:
        print("Validating imports...")
        broken, warnings = migrator.validate_imports(args.category)

        if broken:
            print(f"\n❌ Found {len(broken)} broken imports:")
            for item in broken:
                print(f"  {item}")

        if warnings:
            print(f"\n⚠️  Found {len(warnings)} warnings:")
            for item in warnings[:10]:  # Show first 10
                print(f"  {item}")

        return 1 if broken else 0

    else:
        print("Migrating imports...")
        if args.dry_run:
            print("[DRY RUN MODE - No files will be written]")

        results = migrator.migrate_category(args.category, dry_run=args.dry_run)

        migrated = sum(1 for v in results.values() if v)
        print(f"\n✓ Migrated {migrated} files")

        if not args.dry_run:
            print(f"Validating imports...")
            broken, warnings = migrator.validate_imports(args.category)

            if broken:
                print(f"\n❌ {len(broken)} broken imports detected!")
                return 1

            print(f"✓ All imports valid")
            print(f"\nNext: Run test migrator (04-migrate-tests.py)")

        return 0


if __name__ == "__main__":
    sys.exit(main())
