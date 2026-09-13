#!/usr/bin/env python3
"""Final push to 100% coverage."""

import logging
import os

logger = logging.getLogger(__name__)
# Get all skill directories
skill_dirs = [
    d
    for d in os.listdir("skills")
    if os.path.isdir(f"skills/{d}")
    and d not in ["archived-stubs", "__pycache__", "agents", "integration", "planning"]
]

# Check each skill for completeness
incomplete = []
complete = []

for skill in sorted(skill_dirs):
    skill_md = f"skills/{skill}/SKILL.md"
    if os.path.exists(skill_md):
        with open(skill_md, "r") as f:
            content = f.read()

        has_usage = "## Usage" in content or "### Example" in content
        has_errors = "## Error Handling" in content or "| Error |" in content
        has_links = "## Related Skills" in content or "Related" in content

        if has_usage and has_errors and has_links:
            complete.append(skill)
        else:
            missing = []
            if not has_usage:
                missing.append("Usage")
            if not has_errors:
                missing.append("Errors")
            if not has_links:
                missing.append("Links")
            incomplete.append((skill, missing))

logger.info(f"Complete: {len(complete)}/28 skills")
for s in complete:
    logger.info(f"  [DONE] {s}")

logger.info(f"\nIncomplete: {len(incomplete)}/28 skills")
for s, missing in incomplete:
    logger.info(f"  [NEED {','.join(missing)}] {s}")

completion_pct = (len(complete) / 28) * 100
logger.info(f"\nTotal: {completion_pct:.0f}% complete ({len(complete)}/28)")
