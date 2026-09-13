# Consolidation Execution Guide - CLI & Workflow Agents

This guide shows how to execute the consolidation project using CLI agent commands and multi-agent workflows.

---

## Quick Start

### 1. CLI Agent Commands (Individual Phase Execution)

Run a single phase with a developer:

```bash
# Execute Phase 22 as Marcus
python scripts/consolidation/run_phase.py --phase 22 --developer marcus

# Execute Phase 25 as Sarah
python scripts/consolidation/run_phase.py --phase 25 --developer sarah

# Dry run Phase 27
python scripts/consolidation/run_phase.py --phase 27 --developer alex --dry-run

# List all phases
python scripts/consolidation/run_phase.py --list-phases

# List team members
python scripts/consolidation/run_phase.py --list-developers
```

### 2. Multi-Agent Orchestration Script

Coordinate all 3 developers executing phases in parallel:

```bash
# Validate execution plan (dry run)
python scripts/consolidation/orchestrate_consolidation.py --mode dry-run

# Execute phases sequentially (one at a time)
python scripts/consolidation/orchestrate_consolidation.py --mode sequential

# Execute phases in parallel (all developers simultaneously)
python scripts/consolidation/orchestrate_consolidation.py --mode parallel
```

### 3. Workflow Orchestration (Multi-Agent)

For advanced multi-agent orchestration with automatic task distribution:

```bash
# Run the workflow in Claude Code
/workflow consolidation-execution

# Or invoke from terminal:
claude workflow run consolidation-execution
```

---

## Architecture

### CLI Agent Commands (`run_phase.py`)

**Purpose**: Execute individual consolidation phases with agent oversight

**Features**:
- Single phase execution
- Developer assignment validation
- Dependency checking
- LOC and test targets
- Dry-run mode

**Usage**:
```bash
python run_phase.py --phase <NUM> --developer <NAME> [--dry-run]
```

**Supported Phases**: 22-29
**Supported Developers**: sarah, marcus, alex

### Multi-Agent Orchestrator (`orchestrate_consolidation.py`)

**Purpose**: Coordinate all 8 phases across the 3-person team

**Execution Modes**:

1. **Sequential** - One phase at a time
   ```bash
   python orchestrate_consolidation.py --mode sequential
   ```
   - Phases execute one after another
   - Simpler to debug
   - Takes longer (~5 business days full time)

2. **Parallel** - All developers working simultaneously
   ```bash
   python orchestrate_consolidation.py --mode parallel
   ```
   - All 3 developers execute their phases together
   - Faster completion (3-5 days actual time)
   - Requires good coordination

3. **Dry Run** - Validate without executing (default)
   ```bash
   python orchestrate_consolidation.py --mode dry-run
   ```
   - Checks feasibility
   - Validates team availability
   - No actual execution

### Workflow Orchestration (`.claude/workflows/consolidation_execution.js`)

**Purpose**: Multi-agent workflow for complete consolidation automation

**Phases**:
1. **Setup** (Phase 1) - Initialize branches and health checks
2. **Foundation** (Phase 2) - Day 1-2 work (Phases 22, 23, 24, 27 analysis)
3. **Specialization** (Phase 3) - Day 3 work (Phases 23, 25, 27 specialization + merges)
4. **Completion** (Phase 4) - Day 4-5 work (Phases 26, 28, 29 + final verification)

**Execution**:
```bash
# Run in Claude Code
/workflow consolidation-execution

# Or from command line
claude workflow run consolidation-execution
```

---

## Team Assignments

### Sarah Chen (Team Lead)
- **Role**: Orchestration, Code Review, Architecture
- **Phases**: 24 (Config), 25 (Validators), 29 (Tests)
- **Hours**: 10 hours over 5 days
- **Expertise**: Architecture, Leadership, Decision-making

### Marcus Johnson (Developer 1)
- **Role**: App Core Implementation
- **Phases**: 22 (Batch), 23 (Analytics), 28 (Performance)
- **Hours**: 9.5 hours over 5 days
- **Expertise**: Batch processing, Analytics, Performance optimization

### Alex Patel (Developer 2)
- **Role**: Infrastructure Implementation
- **Phases**: 27 (Sync), 26 (CLI)
- **Hours**: 8.5 hours over 5 days
- **Expertise**: Git operations, Sync systems, Infrastructure

---

## Execution Timeline

### Day 1 (Monday)
- Phase 22: Batch Processing Framework (Marcus)
- Expected: 590 LOC, 150+ tests passing

### Day 2 (Tuesday)
- Phase 23: Analytics (Marcus)
- Phase 24: Configuration (Sarah)
- Phase 27 Analysis: Sync operations (Alex)
- Expected: Phase 22 merged to main, 3 frameworks built

### Day 3 (Wednesday)
- Phase 23 Specialization: 8 analyzers (Marcus)
- Phase 25: Validators (Sarah)
- Phase 27 Specialization: GitOperations + Shims (Alex)
- Expected: 5 phases merged, 2,530 LOC removed

### Day 4 (Thursday)
- Phase 26: CLI & Cache (Alex)
- Phase 28: Performance (Marcus)
- Expected: 2 more phases merged

### Day 5 (Friday)
- Phase 29: Test Utils (Sarah)
- Final verification and celebration
- Expected: All 8 phases complete, 5,230 LOC consolidated

---

## Monitoring Execution

### Daily Dashboard

```bash
# View daily status
python scripts/consolidation/daily_dashboard.py

# Output includes:
# - Tests passing (should be 1,611+)
# - Regressions (should be 0)
# - LOC removed so far
# - Phase completion status
# - Team progress
```

### Health Checks

```bash
# Pre-execution validation
python scripts/consolidation/health_check_complete.py

# During execution (hourly)
python scripts/consolidation/health_check_complete.py --hourly
```

### Test Verification

```bash
# Run full test suite
pytest tests/ --cov=app -v

# Should show: 1,611 passing, 0 failing, 0 regressions
```

---

## Common Commands

### Phase Execution

```bash
# Execute a phase with a developer
python run_phase.py --phase 22 --developer marcus

# List available phases
python run_phase.py --list-phases

# List team members
python run_phase.py --list-developers

# Validate phase dependencies
python run_phase.py --phase 23 --developer marcus --dry-run
```

### Orchestration

```bash
# Validate execution plan
python orchestrate_consolidation.py --mode dry-run

# Execute all phases in sequence
python orchestrate_consolidation.py --mode sequential

# Execute all phases in parallel
python orchestrate_consolidation.py --mode parallel

# Verbose output
python orchestrate_consolidation.py --mode parallel --verbose
```

### Monitoring

```bash
# Daily metrics
python scripts/consolidation/daily_dashboard.py

# Health check
python scripts/consolidation/health_check_complete.py

# Test status
pytest tests/ -v --tb=short
```

---

## Success Criteria

### Phase Completion
- ✅ All LOC targets met
- ✅ All tests passing (phase-specific)
- ✅ Code review approved
- ✅ Merged to main
- ✅ 0 regressions

### Project Completion
- ✅ All 8 phases merged
- ✅ 5,230+ LOC consolidated (43% reduction)
- ✅ 1,611 tests passing (100%)
- ✅ 0 regressions across all phases
- ✅ 100% backward compatibility
- ✅ 13 unified frameworks created

### Timeline
- ✅ Completed within 5 days
- ✅ Production ready for deployment

---

## Troubleshooting

### Phase Fails Tests

```bash
# Check test output
pytest tests/test_phase_XX*.py -vv

# Identify the issue
# - Import error? Run migration script
# - Type mismatch? Update type hints
# - Missing test? Add test skeleton

# Re-run tests
pytest tests/test_phase_XX*.py -v
```

### Merge Conflict

```bash
# Check merge status
git status

# Resolve conflicts manually
# Usually in import statements or framework definitions

# Re-run tests after resolution
pytest tests/ -x
```

### Developer Not Available

```bash
# Option 1: Swap with backup developer
python run_phase.py --phase 22 --developer alex  # If Marcus unavailable

# Option 2: Extend timeline
# Instead of 2 weeks, make it 3 weeks

# Option 3: Bring in contractor
# For specialized phases (e.g., Phase 27 git ops)
```

---

## Results

### Expected Outcomes

**Code Consolidation:**
- 5,230 LOC consolidated (43% reduction)
- 13 unified frameworks created
- 8 phases completed successfully

**Quality:**
- 1,611 tests passing (100%)
- 0 regressions
- 100% backward compatibility
- Code review approved

**Timeline:**
- 5 days actual execution
- 9 days faster than planned
- All on schedule

**Team:**
- 3 developers, 27.5 total hours
- Zero blockers
- High morale
- Proven execution

---

## Next Steps

After consolidation complete:

1. **Deploy v1.2.1** to production
2. **Announce completion** to team and stakeholders
3. **Capture lessons learned** for future consolidations
4. **Plan Phase 30+** improvements
5. **Measure impact** over next quarter

---

## Support

For issues during execution:

- Check daily dashboard: `python daily_dashboard.py`
- Run health checks: `python health_check_complete.py`
- Review execution logs: `DAY1_EXECUTION_LOG.md`, etc.
- Contact team lead (Sarah) for escalations

---

**Status**: Ready for execution ✅
**Created**: 2026-09-03
**Updated**: 2026-09-06
