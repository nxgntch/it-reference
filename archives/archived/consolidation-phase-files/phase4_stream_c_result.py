#!/usr/bin/env python3
"""Phase 4C: Parallel Result Classes Consolidation - Cost Optimized"""
import subprocess
from pathlib import Path

print("=== PHASE 4C: Result Classes Consolidation ===")
print("Optimized for parallel execution\n")

# Create canonical result.py
result_code = '''"""Unified result/response handling for scripts.

Provides consistent Result and SyncResult classes for standardized responses.
"""
from typing import Any, Dict, List, Optional


class Result(dict):
    """Base result class with status tracking."""

    def __init__(self, status: str = "success", **kwargs):
        """Initialize with status and kwargs."""
        super().__init__(status=status, **kwargs)

    @property
    def succeeded(self) -> bool:
        """Check if operation succeeded."""
        return self.get("status") == "success"

    @property
    def failed(self) -> bool:
        """Check if operation failed."""
        return not self.succeeded

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of result."""
        return dict(self)


class SyncResult(Result):
    """Sync operation result with item tracking."""

    def __init__(
        self,
        status: str = "success",
        items: int = 0,
        errors: Optional[List[str]] = None,
        **kwargs,
    ):
        """Initialize sync result."""
        super().__init__(
            status=status, items=items, errors=errors or [], **kwargs
        )

    @property
    def item_count(self) -> int:
        """Get number of items processed."""
        return self.get("items", 0)

    @property
    def error_count(self) -> int:
        """Get number of errors."""
        return len(self.get("errors", []))
'''

print("[C1] Creating canonical result.py...")
result_file = Path("scripts/utils/result.py")
result_file.write_text(result_code)
print(f"  Created: {result_file}")

# Find files with result patterns - single batch grep
print("[C2] Scanning for result handling patterns (batch grep)...")
try:
    result = subprocess.run(
        ["grep", "-r", "-l", "return {", "scripts", "--include=*.py"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    result_files = set(result.stdout.strip().split("\n")) if result.stdout else set()
    result_files.discard("")

    print(f"  Found: {len(result_files)} files using dict returns")

    # Count patterns
    sync_result = 0
    dict_return = 0
    get_summary = 0

    for fpath in result_files:
        try:
            content = Path(fpath).read_text(errors="ignore")
            if "SyncResult" in content:
                sync_result += 1
            if (
                "return {" in content
                and ("status" in content or "success" in content)
            ):
                dict_return += 1
            if "get_summary(" in content:
                get_summary += 1
        except:
            pass

    print(f"  Patterns found:")
    print(f"    - dict returns: {dict_return}")
    print(f"    - SyncResult usage: {sync_result}")
    print(f"    - get_summary methods: {get_summary}")

except Exception as e:
    print(f"  Warning: {e}")

print()
print("[SUCCESS] Stream C Complete - Result classes ready")
