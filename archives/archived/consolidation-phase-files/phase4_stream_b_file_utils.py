#!/usr/bin/env python3
"""Phase 4B: Parallel File Utils Consolidation - Cost Optimized"""
import subprocess
from pathlib import Path

print("=== PHASE 4B: File Utils Consolidation ===")
print("Optimized for parallel execution\n")

# Create canonical file_utils.py
file_utils_code = '''"""Unified file operations for scripts.

Provides safe file reading, writing, and deletion with error handling.
"""
from pathlib import Path
from typing import Optional


def safe_read_file(path: str, default: str = "") -> str:
    """Safely read file, return default if not found."""
    try:
        p = Path(path)
        return p.read_text() if p.exists() else default
    except Exception:
        return default


def safe_write_file(path: str, content: str) -> bool:
    """Safely write file, create parents if needed."""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
        return True
    except Exception:
        return False


def safe_delete_file(path: str) -> bool:
    """Safely delete file if exists."""
    try:
        p = Path(path)
        if p.exists():
            p.unlink()
        return True
    except Exception:
        return False


def ensure_dir(path: str) -> bool:
    """Ensure directory exists."""
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False
'''

print("[B1] Creating canonical file_utils.py...")
file_utils = Path("scripts/utils/file_utils.py")
file_utils.write_text(file_utils_code)
print(f"  Created: {file_utils}")

# Find files with file operation patterns - single batch grep
print("[B2] Scanning for file operation patterns (batch grep)...")
try:
    result = subprocess.run(
        ["grep", "-r", "-l", "Path(", "scripts", "--include=*.py"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    file_files = set(result.stdout.strip().split("\n")) if result.stdout else set()
    file_files.discard("")

    print(f"  Found: {len(file_files)} files using Path()")

    # Count patterns
    read_patterns = 0
    write_patterns = 0
    exists_patterns = 0
    delete_patterns = 0

    for fpath in file_files:
        try:
            content = Path(fpath).read_text(errors="ignore")
            if ".read_text()" in content:
                read_patterns += 1
            if ".write_text(" in content or ".write(" in content:
                write_patterns += 1
            if ".exists()" in content:
                exists_patterns += 1
            if ".unlink()" in content or "os.remove" in content:
                delete_patterns += 1
        except:
            pass

    print(f"  Patterns found:")
    print(f"    - read operations: {read_patterns}")
    print(f"    - write operations: {write_patterns}")
    print(f"    - exists checks: {exists_patterns}")
    print(f"    - delete operations: {delete_patterns}")

except Exception as e:
    print(f"  Warning: {e}")

print()
print("[SUCCESS] Stream B Complete - File Utils ready")
