#!/usr/bin/env python3
"""Phase 20 Script 2: Shim Generator

Generates backward-compatible shim classes that allow old skill code to work
with new base classes. Shims inherit from base classes but preserve old names.

Usage:
    python3 scripts/phase20/02-generate-shims.py \\
        --pattern-report scripts/phase20/patterns-report.json \\
        --skills-root skills \\
        --output-dir skills \\
        --category monitoring
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse
from dataclasses import dataclass


@dataclass
class PatternToShim:
    """Mapping from detected pattern to shim code."""

    skill_name: str
    skill_dir: Path
    old_class_name: str
    pattern_type: str  # "Request" or "Result"
    fields: List[tuple]  # [(name, type), ...]


class ShimGenerator:
    """Generate backward-compatible shim classes."""

    def __init__(self, skills_root: Path):
        self.skills_root = skills_root

    def generate_for_category(self, category: str, patterns: Dict) -> Dict[str, str]:
        """Generate shims for all patterns in a category.

        Returns:
            Dict mapping file_path -> generated_shim_code
        """
        shims = {}

        for pattern_type in ["Request", "Result"]:
            if pattern_type not in patterns["patterns"]:
                continue

            for pattern in patterns["patterns"][pattern_type]:
                file_path = pattern["file_path"]

                # Filter by category if specified
                if category and category not in file_path:
                    continue

                skill_name = self._extract_skill_name(file_path)
                shim_code = self._generate_shim(
                    old_class_name=pattern["name"],
                    pattern_type=pattern_type,
                    fields=pattern["fields"],
                    skill_name=skill_name,
                )

                file_key = file_path
                if file_key not in shims:
                    shims[file_key] = []
                shims[file_key].append(shim_code)

        return shims

    def _extract_skill_name(self, file_path: str) -> str:
        """Extract skill name from file path."""
        parts = file_path.split("/")
        if len(parts) >= 3:
            return parts[2]  # skills/category/skillName
        return "unknown"

    def _generate_shim(
        self, old_class_name: str, pattern_type: str, fields: List[tuple], skill_name: str
    ) -> str:
        """Generate a single shim class."""

        if pattern_type == "Request":
            return self._generate_request_shim(old_class_name, fields, skill_name)
        else:
            return self._generate_result_shim(old_class_name, fields, skill_name)

    def _generate_request_shim(
        self, old_class_name: str, fields: List[tuple], skill_name: str
    ) -> str:
        """Generate Request shim code."""

        # Extract fields that aren't in BaseRequest
        base_fields = {
            "operation",
            "metadata",
            "timeout_ms",
            "retry_count",
            "skill_name",
            "request_id",
            "created_at",
        }
        extra_fields = [f for f in fields if f[0] not in base_fields]

        extra_fields_code = ""
        if extra_fields:
            for field_name, field_type in extra_fields:
                extra_fields_code += f"    {field_name}: {field_type} = None\n"

        template = f'''"""[DEPRECATED] {old_class_name} - Use BaseRequest from skills.core.patterns

This is a backward-compatibility shim. The {skill_name} skill should migrate to BaseRequest.
See Phase 20 consolidation plan: scripts/phase20/README.md
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List
from skills.core.patterns import BaseRequest
import warnings


@dataclass
class {old_class_name}(BaseRequest):
    """[DEPRECATED] Use BaseRequest instead.

    This class exists for backward compatibility during Phase 20 consolidation.
    New code should use BaseRequest from skills.core.patterns.request.

    Deprecation Timeline:
    - Now: Backward-compatible shim active (inherits from BaseRequest)
    - Phase 21 (8 weeks): Shims removed from codebase
    """

{extra_fields_code}
    def __post_init__(self):
        """Call parent initialization and emit deprecation warning."""
        super().__post_init__()
        warnings.warn(
            f"{{self.__class__.__name__}} is deprecated. "
            "Use BaseRequest from skills.core.patterns instead. "
            "See scripts/phase20/README.md for migration guide.",
            DeprecationWarning,
            stacklevel=2
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "{old_class_name}":
        """Create instance from dictionary (API compatibility)."""
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return super().to_dict()
'''
        return template

    def _generate_result_shim(
        self, old_class_name: str, fields: List[tuple], skill_name: str
    ) -> str:
        """Generate Result shim code."""

        # Extract fields that aren't in BaseResult
        base_fields = {
            "success",
            "data",
            "error",
            "error_code",
            "status",
            "latency_ms",
            "request_id",
            "metadata",
            "timestamp",
        }
        extra_fields = [f for f in fields if f[0] not in base_fields]

        extra_fields_code = ""
        if extra_fields:
            for field_name, field_type in extra_fields:
                extra_fields_code += f"    {field_name}: {field_type} = None\n"

        template = f'''"""[DEPRECATED] {old_class_name} - Use BaseResult from skills.core.patterns

This is a backward-compatibility shim. The {skill_name} skill should migrate to BaseResult.
See Phase 20 consolidation plan: scripts/phase20/README.md
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional
from skills.core.patterns import BaseResult
import warnings


@dataclass
class {old_class_name}(BaseResult):
    """[DEPRECATED] Use BaseResult instead.

    This class exists for backward compatibility during Phase 20 consolidation.
    New code should use BaseResult from skills.core.patterns.result.

    Deprecation Timeline:
    - Now: Backward-compatible shim active (inherits from BaseResult)
    - Phase 21 (8 weeks): Shims removed from codebase
    """

{extra_fields_code}
    def __post_init__(self):
        """Call parent initialization and emit deprecation warning."""
        super().__post_init__()
        warnings.warn(
            f"{{self.__class__.__name__}} is deprecated. "
            "Use BaseResult from skills.core.patterns instead. "
            "See scripts/phase20/README.md for migration guide.",
            DeprecationWarning,
            stacklevel=2
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "{old_class_name}":
        """Create instance from dictionary (API compatibility)."""
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return super().to_dict()
'''
        return template

    def write_shims(self, shims: Dict[str, List[str]], dry_run: bool = False) -> Dict[str, bool]:
        """Write shim files to disk.

        Args:
            shims: Dict mapping file_path -> [shim_codes]
            dry_run: If True, don't write files, just show what would happen

        Returns:
            Dict mapping file_path -> success_bool
        """
        results = {}

        for file_path, shim_codes in shims.items():
            file_obj = Path(file_path)

            if not file_obj.exists():
                print(f"Warning: File not found (shim not written): {file_path}")
                results[file_path] = False
                continue

            # Append shim code to existing file
            content = file_obj.read_text()

            # Check if shims already present
            if "[DEPRECATED]" in content:
                print(f"Note: Shims already present in {file_path}")
                results[file_path] = True
                continue

            shim_block = "\n# ===== PHASE 20 BACKWARD-COMPATIBILITY SHIMS =====\n"
            shim_block += "\n".join(shim_codes)

            if not dry_run:
                file_obj.write_text(content + shim_block)
                print(f"✓ Shims written: {file_path}")
            else:
                print(f"[DRY RUN] Would write shims to: {file_path}")

            results[file_path] = True

        return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate backward-compatible shim classes for Phase 20 consolidation."
    )
    parser.add_argument(
        "--pattern-report",
        default="scripts/phase20/patterns-report.json",
        help="Path to pattern analysis report",
    )
    parser.add_argument(
        "--skills-root",
        default="skills",
        help="Path to skills root directory",
    )
    parser.add_argument(
        "--output-dir",
        default="skills",
        help="Output directory (same as skills-root for in-place updates)",
    )
    parser.add_argument(
        "--category",
        default="",
        help="Filter to specific category (optional)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without writing files",
    )

    args = parser.parse_args()

    # Load pattern report
    report_path = Path(args.pattern_report)
    if not report_path.exists():
        print(f"Error: Pattern report not found: {report_path}", file=sys.stderr)
        print(f"Run: python3 scripts/phase20/01-pattern-analysis.py first", file=sys.stderr)
        sys.exit(1)

    with open(report_path) as f:
        patterns = json.load(f)

    print(f"Loading patterns from {report_path}")
    print(f"Found {patterns['total_patterns']} patterns")

    # Generate shims
    generator = ShimGenerator(Path(args.skills_root))
    shims = generator.generate_for_category(args.category, patterns)

    print(f"Generated shims for {len(shims)} files")

    # Write shims
    if args.dry_run:
        print("[DRY RUN MODE - No files will be written]")

    results = generator.write_shims(shims, dry_run=args.dry_run)

    success_count = sum(1 for v in results.values() if v)
    print(f"\n✓ Successfully processed {success_count}/{len(results)} files")

    if not args.dry_run:
        print(f"\nShims written. Next: Run import migrator (03-migrate-imports.py)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
