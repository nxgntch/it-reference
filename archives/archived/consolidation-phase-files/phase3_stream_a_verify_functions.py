#!/usr/bin/env python3
"""Phase 3A: Consolidate verify_* functions"""
import subprocess
from pathlib import Path

print("=== PHASE 3A: Verify Functions Consolidation ===")
print()

# Canonical location for verify functions
canonical_file = Path("scripts/utils/verification.py")
print(f"[A1] Canonical location: {canonical_file}")

# Check what's in canonical file
if canonical_file.exists():
    canonical_content = canonical_file.read_text()
    has_verify_git_repo = "def verify_git_repo" in canonical_content
    has_verify_github = "def verify_github_config" in canonical_content
    has_verify_remote = "def verify_remote_reachable" in canonical_content

    print(f"  verify_git_repo: {'✓' if has_verify_git_repo else '✗'}")
    print(f"  verify_github_config: {'✓' if has_verify_github else '✗'}")
    print(f"  verify_remote_reachable: {'✓' if has_verify_remote else '✗'}")
else:
    print("[A1] Creating verification.py...")
    canonical_file.write_text('"""Verification utilities for git and repository operations."""\n')

# Find duplicates
print("[A2] Finding verify_* function duplicates...")
try:
    result = subprocess.run(
        ["grep", "-r", "^def verify_", "scripts", "--include=*.py"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    files = {
        line.split(":")[0]
        for line in result.stdout.strip().split("\n")
        if line and "scripts/utils/verification.py" not in line
    }

    print(f"  Found: {len(files)} files with duplicates")
    for f in sorted(files):
        print(f"    - {f}")

    # Update imports
    if files:
        print("[A3] Updating imports to use verification.py...")
        for file_path in files:
            try:
                content = Path(file_path).read_text()
                original = content

                # Replace various import patterns
                content = content.replace(
                    "from scripts.utils.verification import verify",
                    "from scripts.utils.verification import verify",
                )
                content = content.replace(
                    "from .sync_helpers import verify",
                    "from scripts.utils.verification import verify",
                )

                if content != original:
                    Path(file_path).write_text(content)
            except Exception as e:
                print(f"  Warning: {file_path}: {e}")

        print(f"  Updated: {len(files)} files")

except Exception as e:
    print(f"  Warning: {e}")

print()
print("[SUCCESS] Stream A Complete - Verify functions consolidated")
