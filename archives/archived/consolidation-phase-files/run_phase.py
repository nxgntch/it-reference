#!/usr/bin/env python3
"""
CLI Agent Command: Execute a single consolidation phase

Usage:
    python run_phase.py --phase 22 --developer marcus --role dev1
    python run_phase.py --phase 24 --developer sarah --role lead
    python run_phase.py --phase 27 --developer alex --role dev2
"""

import argparse
import sys

# Consolidation phase definitions
PHASES = {
    22: {
        "name": "Batch Processing",
        "focus": "BatchingFramework",
        "assigned_to": "marcus",
        "hours": 2.0,
        "deliverables": ["Framework (150 LOC)", "Components (240 LOC)", "Shims (200 LOC)"],
        "tests_target": 150,
        "dependencies": [],
    },
    23: {
        "name": "Analytics",
        "focus": "AnalyticsEngine",
        "assigned_to": "marcus",
        "hours": 2.0,
        "deliverables": ["Engine (150 LOC)", "8 Analyzers (400+ LOC)"],
        "tests_target": 85,
        "dependencies": [22],
    },
    24: {
        "name": "Configuration",
        "focus": "ConfigurationManager",
        "assigned_to": "sarah",
        "hours": 1.0,
        "deliverables": ["Manager (250 LOC)", "Cache (100 LOC)"],
        "tests_target": 40,
        "dependencies": [],
    },
    25: {
        "name": "Validators",
        "focus": "ValidatorFramework",
        "assigned_to": "sarah",
        "hours": 2.0,
        "deliverables": ["ResultFormatter (80 LOC)", "12 Validator Groups (250 LOC)"],
        "tests_target": 145,
        "dependencies": [],
    },
    26: {
        "name": "CLI & Cache",
        "focus": "CommandBuilder",
        "assigned_to": "alex",
        "hours": 1.5,
        "deliverables": ["CommandBuilder (180 LOC)", "Cache Migration"],
        "tests_target": 100,
        "dependencies": [24],
    },
    27: {
        "name": "Sync Operations",
        "focus": "GitOperations",
        "assigned_to": "alex",
        "hours": 3.5,
        "deliverables": ["GitOperations (100 LOC)", "SyncHandler (200 LOC)", "13 Shims"],
        "tests_target": 120,
        "dependencies": [],
    },
    28: {
        "name": "Performance",
        "focus": "ProfilingFramework",
        "assigned_to": "marcus",
        "hours": 2.5,
        "deliverables": ["ProfilingFramework (150 LOC)", "OptimizationFramework (150 LOC)"],
        "tests_target": 110,
        "dependencies": [],
    },
    29: {
        "name": "Test Utils",
        "focus": "TestFactory",
        "assigned_to": "sarah",
        "hours": 1.0,
        "deliverables": ["TestFactory (180 LOC)", "MockBuilder (150 LOC)"],
        "tests_target": 90,
        "dependencies": [],
    },
    # Phase 30+: Next Wave Consolidations
    30: {
        "name": "Marketplace Module",
        "focus": "MarketplaceFramework",
        "assigned_to": "marcus",
        "hours": 10.0,
        "deliverables": [
            "Framework (100 LOC)",
            "8 Handlers (160 LOC)",
            "Validators (230 LOC)",
            "Cache (80 LOC)",
        ],
        "tests_target": 200,
        "dependencies": [],
    },
    31: {
        "name": "Skill Management",
        "focus": "SkillRegistry",
        "assigned_to": "marcus",
        "hours": 10.0,
        "deliverables": ["Registry (180 LOC)", "Validator (120 LOC)", "Metadata (100 LOC)"],
        "tests_target": 150,
        "dependencies": [],
    },
    32: {
        "name": "Monitoring & Observability",
        "focus": "MonitoringFramework",
        "assigned_to": "sarah",
        "hours": 10.0,
        "deliverables": ["Framework (250 LOC)", "Alerting (180 LOC)", "Diagnostics (150 LOC)"],
        "tests_target": 180,
        "dependencies": [],
    },
    33: {
        "name": "Error Handling & Recovery",
        "focus": "ErrorFramework",
        "assigned_to": "marcus",
        "hours": 10.0,
        "deliverables": ["Framework (150 LOC)", "Retry (120 LOC)", "Recovery (100 LOC)"],
        "tests_target": 140,
        "dependencies": [],
    },
    34: {
        "name": "Logging & Diagnostics",
        "focus": "LoggingFramework",
        "assigned_to": "alex",
        "hours": 8.0,
        "deliverables": ["Framework (150 LOC)", "Structured Data (100 LOC)", "Tracing (100 LOC)"],
        "tests_target": 130,
        "dependencies": [],
    },
    35: {
        "name": "Security & Compliance",
        "focus": "SecurityFramework",
        "assigned_to": "sarah",
        "hours": 10.0,
        "deliverables": ["Framework (200 LOC)", "Compliance (150 LOC)", "Audit (130 LOC)"],
        "tests_target": 150,
        "dependencies": [],
    },
}

DEVELOPERS = {
    "sarah": {"role": "lead", "full_name": "Sarah Chen", "title": "Team Lead"},
    "marcus": {"role": "dev1", "full_name": "Marcus Johnson", "title": "Developer 1"},
    "alex": {"role": "dev2", "full_name": "Alex Patel", "title": "Developer 2"},
}


def get_phase_info(phase: int) -> dict:
    """Get phase information."""
    if phase not in PHASES:
        raise ValueError(f"Phase {phase} not found. Valid phases: {list(PHASES.keys())}")
    return PHASES[phase]


def check_dependencies(phase: int) -> bool:
    """Check if all dependencies for this phase are met."""
    phase_info = get_phase_info(phase)
    dependencies = phase_info.get("dependencies", [])

    if not dependencies:
        return True

    print(f"\n📋 Checking dependencies for Phase {phase}...")
    for dep_phase in dependencies:
        dep_info = get_phase_info(dep_phase)
        print(f"  ✓ Phase {dep_phase} ({dep_info['name']}) - required")

    return True


def validate_assignment(phase: int, developer: str) -> bool:
    """Validate that the developer is assigned to this phase."""
    phase_info = get_phase_info(phase)
    assigned_to = phase_info["assigned_to"]

    if developer.lower() not in DEVELOPERS:
        raise ValueError(f"Unknown developer: {developer}")

    if developer.lower() != assigned_to:
        print(
            f"⚠️  Warning: Phase {phase} is assigned to {assigned_to}, but {developer} is executing it"
        )
        return False

    return True


def execute_phase(phase: int, developer: str, dry_run: bool = False) -> dict:
    """Execute a consolidation phase."""
    phase_info = get_phase_info(phase)
    dev_info = DEVELOPERS[developer.lower()]

    print(f"\n{'='*70}")
    print(f"CONSOLIDATION PHASE {phase} EXECUTION")
    print(f"{'='*70}\n")

    print(f"📍 Phase:        {phase} - {phase_info['name']}")
    print(f"👤 Developer:    {dev_info['full_name']} ({dev_info['role']})")
    print(f"🎯 Focus:        {phase_info['focus']}")
    print(f"⏱️  Estimated:    {phase_info['hours']} hours")
    print(f"📊 Target Tests: {phase_info['tests_target']}+")

    print("\n📦 Deliverables:")
    for deliverable in phase_info["deliverables"]:
        print(f"   • {deliverable}")

    # Check dependencies
    check_dependencies(phase)

    # Validate assignment
    is_assigned = validate_assignment(phase, developer)

    if dry_run:
        print(f"\n✅ DRY RUN - Phase {phase} execution plan validated")
        return {"status": "dry_run", "phase": phase, "developer": developer}

    print(f"\n🚀 Executing Phase {phase}...")
    print(f"   $ python scripts/consolidation/phase_{phase}_execute.py --developer {developer}")

    return {
        "status": "executing",
        "phase": phase,
        "developer": developer,
        "assigned": is_assigned,
        "deliverables": phase_info["deliverables"],
        "tests_target": phase_info["tests_target"],
    }


def list_phases() -> None:
    """List all available phases."""
    print("\n📋 CONSOLIDATION PHASES\n")
    print(f"{'Phase':<8} {'Name':<25} {'Framework':<25} {'Assigned':<12} {'Hours':<8}")
    print("─" * 80)

    for phase_num, phase_info in sorted(PHASES.items()):
        print(
            f"{phase_num:<8} {phase_info['name']:<25} {phase_info['focus']:<25} "
            f"{phase_info['assigned_to']:<12} {phase_info['hours']:<8.1f}"
        )

    print("\n💡 Tip: Run a phase with: python run_phase.py --phase 22 --developer marcus")


def list_developers() -> None:
    """List all developers."""
    print("\n👥 CONSOLIDATION TEAM\n")
    print(f"{'Name':<20} {'Role':<12} {'ID':<10}")
    print("─" * 42)

    for dev_id, dev_info in DEVELOPERS.items():
        print(f"{dev_info['full_name']:<20} {dev_info['role']:<12} {dev_id:<10}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Execute consolidation phases as CLI agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute Phase 22 as Marcus
  python run_phase.py --phase 22 --developer marcus

  # Execute Phase 25 as Sarah (with validation)
  python run_phase.py --phase 25 --developer sarah

  # Dry run Phase 27
  python run_phase.py --phase 27 --developer alex --dry-run

  # List all available phases
  python run_phase.py --list-phases

  # List all developers
  python run_phase.py --list-developers
        """,
    )

    parser.add_argument("--phase", type=int, help="Phase number to execute (22-29)")
    parser.add_argument("--developer", help="Developer executing the phase (sarah, marcus, alex)")
    parser.add_argument("--dry-run", action="store_true", help="Validate without executing")
    parser.add_argument("--list-phases", action="store_true", help="List all available phases")
    parser.add_argument("--list-developers", action="store_true", help="List all developers")

    args = parser.parse_args()

    try:
        if args.list_phases:
            list_phases()
            return 0

        if args.list_developers:
            list_developers()
            return 0

        if not args.phase:
            parser.print_help()
            return 1

        if not args.developer:
            print("❌ Error: --developer is required")
            return 1

        result = execute_phase(args.phase, args.developer, args.dry_run)
        print(f"\n✅ Phase {args.phase} ready for execution\n")
        return 0

    except ValueError as e:
        print(f"❌ Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n⚠️  Execution cancelled")
        return 1


if __name__ == "__main__":
    sys.exit(main())
