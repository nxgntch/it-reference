#!/usr/bin/env python3
"""Phase 2 Consolidation Execution Orchestrator.

Manages automated refactoring of all 5 Phase 2 items:
1. Sync Scripts (1,600 LOC → 900 LOC)
2. Cache Implementations (1,200 LOC → 600 LOC)
3. Validators (550 LOC → 350 LOC)
4. Test Fixtures (1-2 hrs)
5. CLI Bases (100-150 LOC)

Total: 5,050 LOC → 2,515 LOC (50% reduction, 11-15 hours)

Usage:
    python scripts/consolidation/phase2_executor.py [--item 1] [--all] [--dry-run]
"""

import logging
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


@dataclass
class PhaseItem:
    """Configuration for a Phase 2 consolidation item."""

    number: int
    name: str
    script: str
    description: str
    loc_before: int
    loc_after: int
    effort_hours: Tuple[int, int]  # (min, max)
    risk: str

    @property
    def loc_saved(self) -> int:
        """LOC saved by consolidation."""
        return self.loc_before - self.loc_after

    @property
    def reduction_percent(self) -> float:
        """Percentage reduction."""
        if self.loc_before == 0:
            return 0
        return 100 * self.loc_saved / self.loc_before


PHASE_2_ITEMS = [
    PhaseItem(
        number=1,
        name="Sync Scripts",
        script="phase2_item1_sync_scripts.py",
        description="Consolidate 6 sync scripts using RepoSyncBase",
        loc_before=2700,
        loc_after=900,
        effort_hours=(4, 5),
        risk="LOW",
    ),
    PhaseItem(
        number=2,
        name="Cache Implementations",
        script="phase2_item2_cache_consolidation.py",
        description="Refactor 5 cache classes to use GenericCache<T>",
        loc_before=1200,
        loc_after=600,
        effort_hours=(3, 4),
        risk="LOW",
    ),
    PhaseItem(
        number=3,
        name="Validators",
        script="phase2_item3_validator_consolidation.py",
        description="Consolidate validate/ scripts using enhanced BaseValidator",
        loc_before=550,
        loc_after=350,
        effort_hours=(2, 3),
        risk="LOW",
    ),
    PhaseItem(
        number=4,
        name="Test Fixtures",
        script="phase2_item4_test_consolidation.py",
        description="Expand conftest.py factory patterns across test domains",
        loc_before=300,
        loc_after=150,
        effort_hours=(1, 2),
        risk="LOW",
    ),
    PhaseItem(
        number=5,
        name="CLI Bases",
        script="phase2_item5_cli_consolidation.py",
        description="Unify 5 script base classes into single unified base",
        loc_before=250,
        loc_after=100,
        effort_hours=(1, 1),
        risk="LOW",
    ),
]


class Phase2Executor:
    """Execute Phase 2 consolidation items."""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.results: Dict[str, Dict] = {}
        self.start_time = datetime.now()

    def print_header(self) -> None:
        """Print execution header."""
        logger.info("=" * 70)
        logger.info("PHASE 2: CONSOLIDATION EXECUTION ORCHESTRATOR")
        logger.info("=" * 70)
        logger.info(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Dry run: {self.dry_run}")
        logger.info(f"Verbose: {self.verbose}")
        logger.info("=" * 70)

    def print_summary(self) -> None:
        """Print summary table of all items."""
        logger.info("\nPHASE 2 CONSOLIDATION ITEMS:")
        logger.info("-" * 90)
        logger.info(
            f"{'#':<2} {'Item':<20} {'LOC Before':<12} {'LOC After':<12} {'Saved':<10} {'Risk':<6}"
        )
        logger.info("-" * 90)

        total_before = 0
        total_after = 0

        for item in PHASE_2_ITEMS:
            total_before += item.loc_before
            total_after += item.loc_after
            logger.info(
                f"{item.number:<2} {item.name:<20} {item.loc_before:<12} {item.loc_after:<12} "
                f"{item.loc_saved:<10} {item.risk:<6}"
            )

        logger.info("-" * 90)
        total_saved = total_before - total_after
        total_percent = 100 * total_saved / total_before if total_before > 0 else 0
        logger.info(
            f"{'TOTAL':<4} {'':<16} {total_before:<12} {total_after:<12} "
            f"{total_saved:<10} ({total_percent:.1f}%)"
        )
        logger.info("-" * 90)

    def execute_item(self, item: PhaseItem) -> bool:
        """Execute a single consolidation item.

        Args:
            item: Phase 2 item to execute

        Returns:
            True if successful
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"ITEM {item.number}: {item.name}")
        logger.info(f"{'='*70}")
        logger.info(f"Description: {item.description}")
        logger.info(
            f"LOC Reduction: {item.loc_before} → {item.loc_after} ({item.reduction_percent:.1f}%)"
        )
        logger.info(f"Effort: {item.effort_hours[0]}-{item.effort_hours[1]} hours")
        logger.info(f"Risk: {item.risk}")

        script_path = Path(__file__).parent / item.script

        if not script_path.exists():
            logger.warning(f"Script not found: {script_path}")
            logger.info("Creating placeholder script...")
            return False

        # Execute the consolidation script
        cmd = [sys.executable, str(script_path)]
        if self.dry_run:
            cmd.append("--dry-run")
        if self.verbose:
            cmd.append("--verbose")

        logger.info(f"\nExecuting: {' '.join(cmd)}")

        try:
            result = subprocess.run(
                cmd,
                capture_output=False,
                text=True,
                timeout=600,  # 10 minutes per item
            )

            success = result.returncode == 0
            self.results[item.name] = {
                "success": success,
                "exit_code": result.returncode,
            }

            if success:
                logger.info(f"✓ {item.name} consolidation completed successfully")
            else:
                logger.error(f"✗ {item.name} consolidation failed (exit code {result.returncode})")

            return success
        except subprocess.TimeoutExpired:
            logger.error(f"✗ {item.name} consolidation timed out")
            self.results[item.name] = {"success": False, "error": "timeout"}
            return False
        except Exception as e:
            logger.error(f"✗ {item.name} consolidation error: {e}")
            self.results[item.name] = {"success": False, "error": str(e)}
            return False

    def execute_all(self) -> bool:
        """Execute all Phase 2 items.

        Returns:
            True if all successful
        """
        self.print_header()
        self.print_summary()

        logger.info("\nExecuting consolidations...")
        all_success = True

        for item in PHASE_2_ITEMS:
            if not self.execute_item(item):
                all_success = False

        self.print_final_report()
        return all_success

    def execute_item_by_number(self, item_number: int) -> bool:
        """Execute a specific item by number.

        Args:
            item_number: Item number (1-5)

        Returns:
            True if successful
        """
        self.print_header()

        matching_items = [item for item in PHASE_2_ITEMS if item.number == item_number]
        if not matching_items:
            logger.error(f"Item {item_number} not found")
            return False

        item = matching_items[0]
        logger.info(f"Executing Item {item_number}: {item.name}\n")

        return self.execute_item(item)

    def print_final_report(self) -> None:
        """Print final execution report."""
        duration = (datetime.now() - self.start_time).total_seconds() / 3600

        logger.info("\n" + "=" * 70)
        logger.info("PHASE 2 EXECUTION REPORT")
        logger.info("=" * 70)
        logger.info(f"Duration: {duration:.1f} hours")
        logger.info(f"Items executed: {len(self.results)}")
        logger.info(f"Successful: {sum(1 for r in self.results.values() if r.get('success'))}")
        logger.info(f"Failed: {sum(1 for r in self.results.values() if not r.get('success'))}")

        if self.results:
            logger.info("\nResults:")
            for item_name, result in self.results.items():
                status = "✓" if result.get("success") else "✗"
                logger.info(f"  {status} {item_name}")

        logger.info("\n" + "=" * 70)
        if all(r.get("success") for r in self.results.values()):
            logger.info("✓ All consolidations completed successfully!")
        else:
            logger.info("⚠ Some consolidations failed or were skipped")
        logger.info("=" * 70)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Phase 2 Consolidation Execution Orchestrator")
    parser.add_argument(
        "--item",
        type=int,
        choices=range(1, 6),
        help="Execute specific item (1-5)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Execute all items",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without applying",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    executor = Phase2Executor(dry_run=args.dry_run, verbose=args.verbose)

    if args.all or (not args.item):
        return 0 if executor.execute_all() else 1
    elif args.item:
        return 0 if executor.execute_item_by_number(args.item) else 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
