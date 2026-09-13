#!/usr/bin/env python3
"""Phase 2C: Consolidate ConfigValidationError and SkillValidationError"""
from pathlib import Path

print("=== PHASE 2C: ConfigValidationError/SkillValidationError ===")
print()

exceptions_file = Path("scripts/utils/exceptions.py")
exceptions_content = exceptions_file.read_text()

# Ensure both are in exceptions.py
if "class ConfigValidationError" not in exceptions_content:
    print("[C1] Adding ConfigValidationError to exceptions.py...")
    msg = "\n\nclass ConfigValidationError(ValidationError):\n"
    msg += '    """Configuration validation failed."""\n    pass\n'
    exceptions_content += msg
    exceptions_file.write_text(exceptions_content)

if "class SkillValidationError" not in exceptions_content:
    print("[C2] Adding SkillValidationError to exceptions.py...")
    exceptions_content = exceptions_file.read_text()
    msg = "\n\nclass SkillValidationError(ValidationError):\n"
    msg += '    """Skill validation failed."""\n    pass\n'
    exceptions_content += msg
    exceptions_file.write_text(exceptions_content)

# Remove from scriptError.py
script_error_file = Path("scripts/utils/scriptError.py")
if script_error_file.exists():
    content = script_error_file.read_text()

    for class_name in ["ConfigValidationError", "SkillValidationError"]:
        if f"class {class_name}" in content:
            print(f"[C3] Removing {class_name} from scriptError.py...")
            lines = content.split("\n")
            filtered = []
            skip = False

            for line in lines:
                if f"class {class_name}" in line:
                    skip = True
                    continue
                if skip and line and not line[0].isspace():
                    skip = False
                if not skip:
                    filtered.append(line)

            content = "\n".join(filtered)

    script_error_file.write_text(content)

print()
print("[SUCCESS] Stream C Complete - Validation errors consolidated")
