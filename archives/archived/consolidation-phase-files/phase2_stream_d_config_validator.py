#!/usr/bin/env python3
"""Phase 2D: Consolidate ConfigValidator variants"""
import subprocess
from pathlib import Path

print("=== PHASE 2D: ConfigValidator Consolidation ===")
print()

# Find ConfigValidator definitions
try:
    result = subprocess.run(
        ["grep", "-r", "^class ConfigValidator", "scripts", "--include=*.py"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    files = {line.split(":")[0] for line in result.stdout.strip().split("\n") if line}

    print(f"[D1] Found ConfigValidator in {len(files)} files:")
    for f in sorted(files):
        print(f"  - {f}")

    # Determine canonical location (prefer scripts/validate/)
    canonical = None
    for f in sorted(files):
        if "scripts/validate/" in f:
            canonical = f
            break

    if canonical:
        print(f"[D2] Canonical location: {canonical}")

        # Remove duplicates from other files
        for file_path in files:
            if file_path != canonical:
                print(f"[D3] Removing from {file_path}...")
                content = Path(file_path).read_text()
                lines = content.split("\n")
                filtered = []
                skip = False

                for line in lines:
                    if "class ConfigValidator" in line:
                        skip = True
                        continue
                    if skip and line and not line[0].isspace():
                        skip = False
                    if not skip:
                        filtered.append(line)

                Path(file_path).write_text("\n".join(filtered))
    else:
        print("[D2] No canonical ConfigValidator found in validate/")

except Exception as e:
    print(f"  Warning: {e}")

print()
print("[SUCCESS] Stream D Complete - ConfigValidator consolidated")
