#!/usr/bin/env python3
"""Phase 20 Script 1: Pattern Analysis

Analyzes the codebase to identify all duplicate patterns that need consolidation.
Generates a detailed report of consolidation opportunities.

Usage:
    python3 scripts/phase20/01-pattern-analysis.py \\
        --skills-root skills \\
        --output scripts/phase20/patterns-report.json
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import argparse


@dataclass
class PatternInfo:
    """Information about a detected pattern."""

    name: str
    file_path: str
    pattern_type: str  # "Request", "Result", "Pipeline", "Engine", "Exception"
    line_number: int
    fields: List[Tuple[str, str]]  # [(name, type), ...]
    similarity_score: float = 0.0  # 0-100
    consolidation_priority: int = 1  # 1=critical, 2=high, 3=medium


class PatternAnalyzer(ast.NodeVisitor):
    """AST visitor to find duplicate patterns."""

    def __init__(self):
        self.patterns: Dict[str, PatternInfo] = {}
        self.current_file = ""

    def analyze_request_results(self, skills_root: Path) -> Dict[str, PatternInfo]:
        """Scan all skills for Request/Result patterns."""
        patterns = {}

        for skill_dir in sorted(skills_root.rglob("*")):
            if not skill_dir.is_dir():
                continue

            inputs_file = skill_dir / "inputs.py"
            if not inputs_file.exists():
                continue

            self.current_file = str(inputs_file)
            try:
                tree = ast.parse(inputs_file.read_text())
                patterns.update(self._extract_patterns(tree, inputs_file))
            except Exception as e:
                print(f"Warning: Failed to parse {inputs_file}: {e}")

        return patterns

    def _extract_patterns(self, tree: ast.AST, file_path: Path) -> Dict[str, PatternInfo]:
        """Extract pattern info from AST."""
        patterns = {}

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            if "Request" in node.name:
                pattern = self._extract_dataclass_info(node, file_path, "Request")
                if pattern:
                    patterns[f"{file_path}:{node.name}"] = pattern

            elif "Result" in node.name:
                pattern = self._extract_dataclass_info(node, file_path, "Result")
                if pattern:
                    patterns[f"{file_path}:{node.name}"] = pattern

        return patterns

    def _extract_dataclass_info(
        self, node: ast.ClassDef, file_path: Path, pattern_type: str
    ) -> Optional[PatternInfo]:
        """Extract dataclass field information."""
        fields = []

        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                field_name = item.target.id
                field_type = ast.unparse(item.annotation) if item.annotation else "Any"
                fields.append((field_name, field_type))

        if not fields:
            return None

        return PatternInfo(
            name=node.name,
            file_path=str(file_path),
            pattern_type=pattern_type,
            line_number=node.lineno,
            fields=fields,
            similarity_score=100.0,  # Placeholder
            consolidation_priority=1 if pattern_type in ["Request", "Result"] else 2,
        )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze codebase for duplicate patterns to consolidate."
    )
    parser.add_argument(
        "--skills-root",
        default="skills",
        help="Path to skills root directory",
    )
    parser.add_argument(
        "--output",
        default="scripts/phase20/patterns-report.json",
        help="Output file for pattern report",
    )

    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    if not skills_root.exists():
        print(f"Error: Skills root not found: {skills_root}", file=sys.stderr)
        sys.exit(1)

    print(f"Analyzing patterns in {skills_root}...")

    analyzer = PatternAnalyzer()

    # Analyze patterns
    patterns = analyzer.analyze_request_results(skills_root)

    # Group by pattern type
    grouped = {}
    for key, pattern in patterns.items():
        ptype = pattern.pattern_type
        if ptype not in grouped:
            grouped[ptype] = []
        grouped[ptype].append(asdict(pattern))

    report = {
        "total_patterns": len(patterns),
        "by_type": {ptype: len(items) for ptype, items in grouped.items()},
        "patterns": grouped,
        "estimated_loc_reduction": calculate_loc_reduction(patterns),
    }

    # Write report
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    print(f"Report written to {output_path}")
    print(f"Found {len(patterns)} patterns:")
    for ptype, items in grouped.items():
        print(f"  - {ptype}: {len(items)} occurrences")

    return 0


def calculate_loc_reduction(patterns: Dict[str, PatternInfo]) -> Dict[str, int]:
    """Estimate LOC reduction from consolidation."""
    avg_lines_per_pattern = {
        "Request": 50,
        "Result": 50,
        "Pipeline": 200,
        "Engine": 200,
    }

    reduction = {}
    for ptype in avg_lines_per_pattern:
        count = sum(1 for p in patterns.values() if p.pattern_type == ptype)
        reduction[ptype] = count * avg_lines_per_pattern.get(ptype, 50)

    return reduction


if __name__ == "__main__":
    sys.exit(main())
