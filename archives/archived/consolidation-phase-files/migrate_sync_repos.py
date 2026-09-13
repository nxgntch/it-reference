"""Batch migration: Sync repo orchestrator consolidation."""

import logging
import sys
from pathlib import Path
from scripts.utils import (
    MultiRepoSyncOrchestrator,
    find_files,
    read_file,
    write_file,
    format_success,
    format_error,
    get_logger,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate_sync_repos")

SYNC_REPO_DIR = Path("scripts/sync/repos")
SYNC_FILES = [
    "daily_sync.py",
    "logs_sync.py",
    "nxgntch_sync.py",
    "archive_workflow.py",
    "reference_sync.py",
    "full_sync_orchestrator.py",
]


def migrate_sync_repos():
    """Migrate sync repo scripts to use MultiRepoSyncOrchestrator."""
    if not SYNC_REPO_DIR.exists():
        logger.error(f"Directory not found: {SYNC_REPO_DIR}")
        return False

    migrated = 0
    failed = 0

    for filename in SYNC_FILES:
        filepath = SYNC_REPO_DIR / filename
        if not filepath.exists():
            logger.warning(f"File not found: {filepath}")
            failed += 1
            continue

        try:
            content = read_file(filepath)

            # Check if already migrated
            if "MultiRepoSyncOrchestrator" in content:
                logger.info(f"Already migrated: {filename}")
                continue

            # Add import if not present
            if "from scripts.utils import MultiRepoSyncOrchestrator" not in content:
                import_line = (
                    "from scripts.utils import MultiRepoSyncOrchestrator\n"
                )
                if "import" in content:
                    # Insert after last import
                    lines = content.split("\n")
                    last_import_idx = 0
                    for i, line in enumerate(lines):
                        if line.startswith("import ") or line.startswith("from "):
                            last_import_idx = i
                    lines.insert(last_import_idx + 1, import_line.strip())
                    content = "\n".join(lines)
                else:
                    content = import_line + content

            logger.info(f"Migrated: {filename}")
            write_file(filepath, content)
            migrated += 1

        except Exception as e:
            logger.error(f"Failed to migrate {filename}: {e}")
            failed += 1

    logger.info(format_success(f"Migration complete: {migrated} migrated, {failed} failed"))
    return failed == 0


if __name__ == "__main__":
    success = migrate_sync_repos()
    sys.exit(0 if success else 1)
