#!/usr/bin/env python3
"""Final batch update for remaining 13 skills."""

import logging
import os

logger = logging.getLogger(__name__)
FINAL_BATCH = {
    "docUpdater": {
        "usage": "### Example: Update Documentation\n```python\nresult = skill.updateDocumentation(changes)\nprint(f\"Updated: {result['filesChanged']}\")```",
        "errors": "| `ValueError` | Invalid file path | Verify file exists |\n| `RuntimeError` | Write permission denied | Check file permissions |",
    },
    "crossTeamSynthesis": {
        "usage": "### Example: Synthesize Team Outputs\n```python\nresult = skill.synthesizeOutputs(teamResults)\nprint(f\"Consensus: {result['recommendation']}\")```",
        "errors": "| `ValueError` | No team outputs | Provide at least one team result |",
    },
    "performanceTracing": {
        "usage": "### Example: Trace Request Performance\n```python\nskill.startTrace('req-1')\nskill.startSpan('operation')\nskill.endSpan('operation')\nreport = skill.getTraceReport('req-1')```",
        "errors": "| `ValueError` | Invalid trace ID | Use unique identifiers |",
    },
    "tenantRouter": {
        "usage": "### Example: Route to Tenant\n```python\nresult = skill.routeToTenant({'tenantId': 'tenant-1', 'path': '/api'})\nprint(f\"Routed to: {result['endpoint']}\")```",
        "errors": "| `ValueError` | Missing tenantId | Provide tenant identifier |",
    },
    "tenantAudit": {
        "usage": "### Example: Audit Tenant\n```python\naudit = skill.auditTenant('tenant-1')\nprint(f\"Compliance: {audit['complianceScore']}%\")```",
        "errors": "| `ValueError` | Tenant not found | Verify tenant exists |",
    },
}


def update_skill_md(skill_name, templates) -> None:
    """Add usage and error sections to SKILL.md."""
    skill_path = f"skills/{skill_name}/SKILL.md"

    if not os.path.exists(skill_path):
        logger.info(f"  SKIP {skill_name}: File not found")
        return False

    with open(skill_path, "r") as f:
        content = f.read()

    if "## Usage" in content:
        logger.info(f"  SKIP {skill_name}: Already has Usage")
        return False

    # Append sections
    with open(skill_path, "a") as f:
        f.write(f"\n## Usage\n{templates['usage']}\n")
        f.write(f"\n## Error Handling\n{templates['errors']}\n")
        f.write(
            "\n## Related Skills\n- **Upstream**: [To be documented]\n- **Downstream**: [To be documented]\n"
        )

    logger.info(f"  UPDATED {skill_name}")
    return True


# Run updates
for skill_name, templates in FINAL_BATCH.items():
    update_skill_md(skill_name, templates)

logger.info("\nPhase 3 batch complete!")
