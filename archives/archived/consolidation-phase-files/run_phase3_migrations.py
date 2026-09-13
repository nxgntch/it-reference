"""Phase 3 coordinator: Run all 8 batch migration scripts in parallel."""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("phase3_coordinator")

MIGRATION_SCRIPTS = [
    "migrate_sync_repos.py",
    "migrate_subprocess_calls.py",
    "migrate_doc_generators.py",
    "migrate_validators.py",
    "migrate_cli_commands.py",
    "migrate_logger_setup.py",
    "migrate_consolidation_scripts.py",
    "remove_shims.py",
]

CONSOLIDATION_DIR = Path("scripts/consolidation")


async def run_migration(script_name: str) -> Tuple[str, bool, str]:
    """Run a single migration script."""
    script_path = CONSOLIDATION_DIR / script_name
    logger.info(f"Starting: {script_name}")

    try:
        # Get the project root for PYTHONPATH
        project_root = Path(__file__).parent.parent.parent
        env = os.environ.copy()
        env["PYTHONPATH"] = str(project_root)

        result = await asyncio.create_subprocess_exec(
            sys.executable,
            str(script_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        stdout, stderr = await result.communicate()
        output = stdout.decode().strip()
        error = stderr.decode().strip()

        success = result.returncode == 0

        if success:
            logger.info(f"✅ Completed: {script_name}")
        else:
            logger.error(f"❌ Failed: {script_name}")
            if error:
                logger.error(f"   Error: {error}")

        return script_name, success, output or error

    except Exception as e:
        logger.error(f"❌ Exception in {script_name}: {e}")
        return script_name, False, str(e)


async def run_all_migrations() -> bool:
    """Run all migrations in parallel."""
    logger.info("=" * 70)
    logger.info("Phase 3: Running 8 batch migrations in parallel")
    logger.info("=" * 70)

    # Run all migrations concurrently
    tasks = [run_migration(script) for script in MIGRATION_SCRIPTS]
    results = await asyncio.gather(*tasks)

    # Summary
    logger.info("=" * 70)
    logger.info("Migration Results Summary")
    logger.info("=" * 70)

    passed = 0
    failed = 0

    for script_name, success, output in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{status}: {script_name}")
        if success:
            passed += 1
        else:
            failed += 1
            if output:
                logger.info(f"     {output}")

    logger.info("=" * 70)
    logger.info(f"Total: {passed} passed, {failed} failed out of {len(MIGRATION_SCRIPTS)}")
    logger.info("=" * 70)

    return failed == 0


def main():
    """Main entry point."""
    try:
        success = asyncio.run(run_all_migrations())
        return 0 if success else 1
    except Exception as e:
        logger.error(f"Coordinator failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
