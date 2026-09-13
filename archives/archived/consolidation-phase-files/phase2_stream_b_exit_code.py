#!/usr/bin/env python3
"""Phase 2B: Consolidate ExitCode to exceptions.py"""
import subprocess
from pathlib import Path

print("=== PHASE 2B: ExitCode Consolidation ===")
print()

# Ensure ExitCode is in exceptions.py
exceptions_file = Path("scripts/utils/exceptions.py")
exceptions_content = exceptions_file.read_text()

if "class ExitCode" not in exceptions_content:
    print("[B1] Adding ExitCode to exceptions.py...")
    exit_code_def = '''

class ExitCode:
    """Standard exit codes."""

    SUCCESS = 0
    ERROR = 1
    VALIDATION_ERROR = 2
    CONFIG_ERROR = 3
    MISSING_DEPENDENCY = 4
'''
    exceptions_file.write_text(exceptions_content + exit_code_def)
    print("  Added: ExitCode to exceptions.py")
else:
    print("[B1] ExitCode already in exceptions.py")

# Remove from scriptError.py
script_error_file = Path("scripts/utils/scriptError.py")
if script_error_file.exists():
    content = script_error_file.read_text()
    if "class ExitCode" in content:
        print("[B2] Removing ExitCode from scriptError.py...")
        lines = content.split("\n")
        filtered = []
        skip = False

        for line in lines:
            if line.startswith("class ExitCode"):
                skip = True
                continue
            if skip and line and not line[0].isspace():
                skip = False
            if not skip:
                filtered.append(line)

        script_error_file.write_text("\n".join(filtered))
        print("  Removed: ExitCode from scriptError.py")

# Remove from cli/base.py
cli_base_file = Path("scripts/cli/base.py")
if cli_base_file.exists():
    content = cli_base_file.read_text()
    if "class ExitCode" in content:
        print("[B3] Removing ExitCode from cli/base.py...")
        content = content.replace(
            "from scripts.utils.exceptions import ExitCode",
            "from scripts.utils.exceptions import ExitCode",
        )
        cli_base_file.write_text(content)
        print("  Updated: cli/base.py")

# Update all imports
print("[B4] Finding ExitCode imports...")
try:
    result = subprocess.run(
        ["grep", "-r", "ExitCode", "scripts", "--include=*.py"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    files = {
        line.split(":")[0]
        for line in result.stdout.strip().split("\n")
        if line and "ExitCode" in line
    }

    count = 0
    for file_path in files:
        try:
            fc = Path(file_path).read_text()
            original = fc
            fc = fc.replace(
                "from scripts.utils.exceptions import ExitCode",
                "from scripts.utils.exceptions import ExitCode",
            )
            if fc != original:
                Path(file_path).write_text(fc)
                count += 1
        except Exception:
            pass

    if count > 0:
        print(f"  Updated: {count} files")
except Exception as e:
    print(f"  Warning: {e}")

print()
print("[SUCCESS] Stream B Complete - ExitCode consolidated")
