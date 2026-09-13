"""Apply subsystem pytest markers to test modules (one-off maintenance script).
Module-level pytestmark should use subsystem markers only. Scope markers (unit,
integration, security, slow, etc.) stay on individual tests/classes so CI marker
filters stay aligned with main (~235 unit, ~199 integration).
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


ROOT = Path(__file__).resolve().parent.parent / "tests"

# Subsystem markers only — scope markers must not be applied at module level.
FILE_MARKERS: dict[str, list[str]] = {
    "test_agent_and_skills_infrastructure.py": ["agents", "skills"],
    "test_agent_integration.py": ["agents"],
    "test_api_responses.py": ["format"],
    "test_batching.py": ["batching"],
    "test_chaos_engineering.py": ["resilience"],
    "test_cli_and_plugins.py": ["cli"],
    "test_cli_edge_cases.py": ["cli"],
    "test_cli_message_standardization.py": ["cli", "format"],
    "test_config_cache.py": ["config"],
    "test_config_output.py": ["governance", "format"],
    "test_configuration_and_cost_management.py": ["governance", "config"],
    "test_data_consistency.py": ["resilience"],
    "test_distributed_state.py": ["resilience"],
    "test_docs_active_tasks.py": ["docs"],
    "test_docs_audit_validator.py": ["docs"],
    "test_docs_base_generator.py": ["docs"],
    "test_docs_link_map.py": ["docs"],
    "test_docs_optimization.py": ["docs"],
    "test_docs_phase_status.py": ["docs"],
    "test_docs_phase_summary.py": ["docs"],
    "test_documentation_and_orchestration.py": ["orchestration", "docs"],
    "test_documentation_and_sync_pipeline.py": ["sync"],
    "test_documentation_output.py": ["format", "docs"],
    "test_e2e_workflows.py": ["e2e", "resilience"],
    "test_format_integration.py": ["format"],
    "test_html_generator.py": ["format", "docs"],
    "test_llm_processing_and_agent_routing.py": ["agents", "batching", "orchestration"],
    "test_memory_guard.py": ["security"],
    "test_memory_guard_security.py": ["security"],
    "test_metrics_advanced.py": ["observability"],
    "test_metrics_log_parser.py": ["observability"],
    "test_metrics_performance_and_optimization.py": ["observability"],
    "test_metrics_report_generator.py": ["observability", "format"],
    "test_multi_agent_workflows.py": ["orchestration"],
    "test_operations_and_monitoring.py": ["observability", "integration", "slow"],
    "test_output_consistency.py": ["format"],
    "test_performance_benchmarks.py": ["perf"],
    "test_performance_optimization_and_batching.py": ["batching"],
    "test_phase5_integration.py": ["sync"],
    "test_phase5_performance.py": ["sync"],
    "test_phase6_integration.py": ["observability", "cli"],
    "test_schema_validation.py": ["validation"],
    "test_security_owasp.py": ["security"],
    "test_storage_integration.py": ["resilience"],
    "test_sync_autosync.py": ["sync"],
    "test_sync_base_module.py": ["sync"],
    "test_sync_clean.py": ["sync"],
    "test_sync_config.py": ["sync"],
    "test_sync_files.py": ["sync"],
    "test_sync_mcpchat.py": ["sync"],
    "test_sync_optimization.py": ["sync"],
    "test_sync_repos_daily.py": ["sync"],
    "test_sync_repos_reference.py": ["sync"],
    "test_system_resilience_and_optimization.py": ["resilience"],
    "test_validation_and_property_testing.py": ["validation"],
    "test_cli/test_base.py": ["cli"],
    "test_cli/test_interface.py": ["cli"],
    "test_cli/test_profiling.py": ["cli"],
    "test_cli/test_sync.py": ["cli", "sync"],
    "test_cli/test_validation.py": ["cli", "validation"],
}

SKIPIF_FILES = {
    "test_batching.py": 'not HAS_QUERY_BATCHER, reason="QueryBatcher not available"',
    "test_performance_optimization_and_batching.py": (
        'not HAS_QUERY_BATCHER, reason="QueryBatcher not available"'
    ),
}

PYTESTMARK_RE = re.compile(
    r"^pytestmark\s*=\s*(?:\[.*?\]|pytest\.mark\.\w+)\s*$",
    re.MULTILINE,
)


def build_pytestmark_line(markers: list[str], rel: str) -> str:
    """Build pytestmark line with markers and optional skipif.

    Args:
        markers: List of marker names (e.g., ['agents', 'skills'])
        rel: Relative path to test file (for skipif lookup)

    Returns:
        pytestmark assignment string (single marker or bracketed list)
    """
    tokens: list[str] = [f"pytest.mark.{marker}" for marker in markers]
    skipif = SKIPIF_FILES.get(rel)
    if skipif:
        tokens.append(f"pytest.mark.skipif({skipif})")
    if len(tokens) == 1:
        return f"pytestmark = {tokens[0]}"
    inner = ", ".join(tokens)
    return f"pytestmark = [{inner}]"


def patch_file(rel: str, markers: list[str]) -> None:
    """Patch test file with pytestmark line.

    Inserts or replaces pytestmark line in test file, handling docstrings
    and import statements correctly. Adds pytest import if needed.

    Args:
        rel: Relative path to test file
        markers: List of marker names to apply
    """
    path = ROOT / rel
    text = path.read_text()
    new_block = build_pytestmark_line(markers, rel)
    if PYTESTMARK_RE.search(text):
        text = PYTESTMARK_RE.sub(new_block, text, count=1)
    else:
        lines = text.splitlines()
        insert_at = 0
        if lines and (lines[0].startswith('"""') or lines[0].startswith("'''")):
            quote = '"""' if '"""' in lines[0] else "'''"
            insert_at = 1
            while insert_at < len(lines):
                if quote in lines[insert_at]:
                    insert_at += 1
                    break
            insert_at += 1
        while insert_at < len(lines) and lines[insert_at].strip() == "":
            insert_at += 1
        header = "\n".join(lines[:insert_at])
        if "import pytest" not in header:
            lines.insert(insert_at, "import pytest")
            insert_at += 1
            if insert_at < len(lines) and lines[insert_at].strip() != "":
                lines.insert(insert_at, "")
            insert_at += 1
        lines.insert(insert_at, new_block)
        lines.insert(insert_at + 1, "")
        text = "\n".join(lines) + "\n"
    path.write_text(text)
    logger.info(f"OK {rel}: {markers}")


def main() -> None:
    import py_compile

    for rel, markers in sorted(FILE_MARKERS.items()):
        if not (ROOT / rel).exists():
            raise SystemExit(f"Missing file: {rel}")
        patch_file(rel, markers)
        py_compile.compile(str(ROOT / rel), doraise=True)
    logger.info("All files compile.")


if __name__ == "__main__":
    main()
