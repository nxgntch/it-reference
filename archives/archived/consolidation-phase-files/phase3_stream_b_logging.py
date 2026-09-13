#!/usr/bin/env python3
"""Phase 3B: Consolidate logging utilities"""
import subprocess
from pathlib import Path

print("=== PHASE 3B: Logging Utilities Consolidation ===")
print()

# Canonical location for logging
canonical_file = Path("scripts/utils/logging_setup.py")
print(f"[B1] Canonical location: {canonical_file}")

if canonical_file.exists():
    print("  ✓ logging_setup.py exists")
else:
    print("  ✗ Creating logging_setup.py...")
    canonical_file.write_text(
        '"""Centralized logging configuration.\n\n'
        'Provides get_logger() utility for consistent logging across scripts.\n"""\n'
    )

# Find duplicate get_logger definitions
print("[B2] Finding get_logger() duplicates...")
try:
    result = subprocess.run(
        ["grep", "-r", "^def get_logger", "scripts", "--include=*.py"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    files = {
        line.split(":")[0]
        for line in result.stdout.strip().split("\n")
        if line and "scripts/utils/logging_setup.py" not in line
    }

    if files:
        print(f"  Found: {len(files)} files")
        for f in sorted(files):
            print(f"    - {f}")

        # Update imports
        print("[B3] Updating imports to use logging_setup.py...")
        for file_path in files:
            try:
                content = Path(file_path).read_text()
                original = content

                # Replace various import patterns
                patterns = [
                    ("from scripts.utils.logging_setup import get_logger",
                     "from scripts.utils.logging_setup import get_logger"),
                    ("from .logger import get_logger",
                     "from scripts.utils.logging_setup import get_logger"),
                    ("from scripts.utils.logging_setup import get_logger",
                     "from scripts.utils.logging_setup import get_logger"),
                ]

                for old, new in patterns:
                    content = content.replace(old, new)

                if content != original:
                    Path(file_path).write_text(content)
            except Exception as e:
                print(f"  Warning: {file_path}: {e}")

        print(f"  Updated: {len(files)} files")
    else:
        print("  No duplicates found")

except Exception as e:
    print(f"  Warning: {e}")

print()
print("[SUCCESS] Stream B Complete - Logging utilities consolidated")
