#!/usr/bin/env python3
"""Phase 3C: General import consolidation"""
import subprocess
from pathlib import Path

print("=== PHASE 3C: Import Consolidation ===")
print()

# Common import consolidations
consolidations = [
    ("from scripts.utils.logging_setup import", "from scripts.utils.logging_setup import"),
    ("from scripts.utils.logging_setup import", "from scripts.utils.logging_setup import"),
    ("from scripts.utils.sync_helpers import verify",
     "from scripts.utils.verification import verify"),
]

print("[C1] Finding files with non-canonical imports...")
files_to_update = set()

for old_import, _ in consolidations:
    try:
        result = subprocess.run(
            ["grep", "-r", old_import, "scripts", "--include=*.py"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        for line in result.stdout.strip().split("\n"):
            if line:
                file_path = line.split(":")[0]
                files_to_update.add(file_path)
    except Exception:
        pass

print(f"  Found: {len(files_to_update)} files to update")

if files_to_update:
    print("[C2] Updating imports...")
    for file_path in sorted(files_to_update):
        try:
            content = Path(file_path).read_text()
            original = content

            for old_import, new_import in consolidations:
                content = content.replace(old_import, new_import)

            if content != original:
                Path(file_path).write_text(content)
                print(f"  ✓ {file_path}")

        except Exception as e:
            print(f"  ✗ {file_path}: {e}")

print()
print("[SUCCESS] Stream C Complete - Imports consolidated")
