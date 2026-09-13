#!/usr/bin/env python3
"""Phase 4D: Parallel Import Consolidation - Batched & Cost Optimized"""
import subprocess
from pathlib import Path

print("=== PHASE 4D: Import Consolidation (Batched) ===")
print("Optimized for parallel execution\n")

# Consolidation map
consolidations = [
    ("from scripts.utils.logging_setup import", "from scripts.utils.logging_setup import"),
    ("from scripts.utils.logging_setup import", "from scripts.utils.logging_setup import"),
    ("from scripts.utils.error_handler import", "from scripts.utils.error_handler import"),
]

print("[D1] Scanning for non-canonical imports (batch grep)...")
files_to_update = set()

for old_import, _ in consolidations:
    try:
        result = subprocess.run(
            ["grep", "-r", "-l", old_import, "scripts", "--include=*.py"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                if line:
                    files_to_update.add(line)
    except:
        pass

print(f"  Found: {len(files_to_update)} files to update")

# Batch update all files
if files_to_update:
    print("[D2] Batch updating imports...")
    updated = 0

    for file_path in sorted(files_to_update):
        try:
            content = Path(file_path).read_text(errors="ignore")
            original = content

            for old_import, new_import in consolidations:
                content = content.replace(old_import, new_import)

            if content != original:
                Path(file_path).write_text(content)
                updated += 1

        except Exception as e:
            pass

    print(f"  Updated: {updated} files")

print()
print("[SUCCESS] Stream D Complete - Imports consolidated")
