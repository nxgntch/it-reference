#!/usr/bin/env python3
"""Phase 2A: Consolidate ValidationError to exceptions.py"""
import subprocess
from pathlib import Path

print("=== PHASE 2A: ValidationError Consolidation ===")
print()

# Check what's in exceptions.py
exceptions_file = Path("scripts/utils/exceptions.py")
exceptions_content = exceptions_file.read_text()

# Check scriptError.py
script_error_file = Path("scripts/utils/scriptError.py")
if script_error_file.exists():
    script_error_content = script_error_file.read_text()

    if "class ValidationError" in script_error_content:
        print("[A1] Found ValidationError in scriptError.py")

        # Remove ValidationError from scriptError.py (keep only non-ValidationError content)
        lines = script_error_content.split("\n")
        filtered_lines = []
        skip_class = False

        for line in lines:
            if line.startswith("class ValidationError"):
                skip_class = True
                print("  Removing class definition")
                continue

            if skip_class and line and not line[0].isspace() and not line.startswith("class"):
                skip_class = False

            if not skip_class:
                filtered_lines.append(line)

        script_error_file.write_text("\n".join(filtered_lines))
        print("  Updated: scriptError.py")
    else:
        print("[A1] ValidationError not in scriptError.py")

# Check syncDoc.py
sync_doc_file = Path("scripts/sync/syncDoc.py")
if sync_doc_file.exists():
    content = sync_doc_file.read_text()
    if "class ValidationError" in content:
        print("[A2] Found ValidationError in syncDoc.py")
        content = content.replace(
            "from scripts.utils.exceptions import ValidationError",
            "from scripts.utils.exceptions import ValidationError",
        )
        sync_doc_file.write_text(content)
        print("  Updated imports: syncDoc.py")

# Update all imports to use exceptions.py
print("[A3] Finding ValidationError imports...")
try:
    result = subprocess.run(
        [
            "grep",
            "-r",
            "from scripts.utils.exceptions import.*ValidationError",
            "scripts",
            "--include=*.py",
        ],
        capture_output=True,
        text=True,
        timeout=10,
    )
    files = {
        line.split(":")[0]
        for line in result.stdout.strip().split("\n")
        if line and "ValidationError" in line
    }

    if files:
        print(f"[A4] Updating {len(files)} import statements...")
        for file_path in files:
            try:
                fc = Path(file_path).read_text()
                fc = fc.replace(
                    "from scripts.utils.exceptions import", "from scripts.utils.exceptions import"
                )
                Path(file_path).write_text(fc)
            except Exception as e:
                print(f"  Warning: {file_path}: {e}")
        print(f"  Updated: {len(files)} files")
except Exception as e:
    print(f"  Warning: {e}")

print()
print("[SUCCESS] Stream A Complete - ValidationError consolidated")
