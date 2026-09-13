# Phase 30-35 Agent Commands Reference

**Advanced consolidation automation for Phases 30-35** — Marketplace, Skills, Monitoring, Error Handling, Logging, Security

This guide covers CLI commands and multi-agent workflows for executing the 6 advanced consolidation phases in parallel.

---

## Quick Start

### Individual Phase Execution

```bash
# Execute Phase 30 (Marketplace) as Marcus
python scripts/consolidation/run_phase.py --phase 30 --developer marcus

# Execute Phase 35 (Security) as Sarah (dry run)
python scripts/consolidation/run_phase.py --phase 35 --developer sarah --dry-run

# List all phases including 30-35
python scripts/consolidation/run_phase.py --list-phases

# List team members
python scripts/consolidation/run_phase.py --list-developers
```

### Parallel Phase Orchestration

```bash
# Validate Phase 30-35 execution plan
python scripts/consolidation/orchestrate_phase_30_plus.py --mode dry-run

# Execute all 6 phases sequentially (slower)
python scripts/consolidation/orchestrate_phase_30_plus.py --mode sequential

# Execute all 6 phases in parallel (faster, Week 1 + Week 2)
python scripts/consolidation/orchestrate_phase_30_plus.py --mode parallel --verbose

# Hybrid execution (balanced approach)
python scripts/consolidation/orchestrate_phase_30_plus.py --mode hybrid --verbose
```

### Multi-Agent Workflow

```bash
# Run Phase 30-35 workflow in Claude Code
/workflow consolidation-phase-30-plus

# Or from terminal
claude workflow run consolidation-phase-30-plus
```

---

## Architecture

### 1. CLI Agent Commands (`run_phase.py`)

**Extended to support Phases 30-35**

#### Usage

```bash
python run_phase.py --phase <NUM> --developer <NAME> [--dry-run]
```

#### Supported Phases (30-35)

| Phase | Name | Developer | Hours | LOC Target | Tests |
|-------|------|-----------|-------|------------|-------|
| 30 | Marketplace | marcus | 10h | 1,350 | 200+ |
| 31 | Skill Management | marcus | 10h | 1,050 | 150+ |
| 32 | Monitoring | sarah | 10h | 1,200 | 180+ |
| 33 | Error Handling | marcus | 10h | 900 | 140+ |
| 34 | Logging | alex | 8h | 800 | 130+ |
| 35 | Security | sarah | 10h | 1,050 | 150+ |

#### Examples

```bash
# Marketplace consolidation
python run_phase.py --phase 30 --developer marcus

# Skills consolidation
python run_phase.py --phase 31 --developer marcus

# Monitoring & Observability
python run_phase.py --phase 32 --developer sarah

# Error Handling & Recovery
python run_phase.py --phase 33 --developer marcus

# Logging & Diagnostics
python run_phase.py --phase 34 --developer alex

# Security & Compliance
python run_phase.py --phase 35 --developer sarah
```

### 2. Multi-Agent Orchestrator (`orchestrate_phase_30_plus.py`)

**Purpose**: Coordinate all 6 phases across 3 developers

#### Execution Modes

**Sequential** - Phases execute one at a time
```bash
python orchestrate_phase_30_plus.py --mode sequential
```
- Week 1: Phases 30, 31, 32
- Week 2: Phases 33, 34, 35
- Takes ~3 weeks full-time
- Better for debugging

**Parallel** - All developers work simultaneously
```bash
python orchestrate_phase_30_plus.py --mode parallel --verbose
```
- Week 1: Phases 30, 32, 34 (Marcus, Sarah, Alex parallel)
- Week 2: Phases 31, 33, 35 (Marcus, Sarah continuing)
- Takes ~2 weeks actual time
- Maximum efficiency

**Hybrid** - Weekly syncs with parallel work
```bash
python orchestrate_phase_30_plus.py --mode hybrid --verbose
```
- Balanced: 4 phases per week
- 2.5 weeks total
- Better team coordination

**Dry Run** - Validate without executing
```bash
python orchestrate_phase_30_plus.py --mode dry-run
```
- Checks team capacity
- Validates dependencies
- No actual execution

#### Validation Output

```
TEAM CAPACITY ANALYSIS
─────────────────────
Total hours required:  58.0 hours
Total team capacity:   58.0 hours
Utilization:           100.0%

By Developer:
  ✅ Sarah Chen           20.0h / 20.0h available (100.0%)
  ✅ Marcus Johnson       30.0h / 30.0h available (100.0%)
  ✅ Alex Patel            8.0h / 8.0h available (100.0%)
```

#### Command Reference

```bash
# List all Phase 30-35 phases
python orchestrate_phase_30_plus.py --list-phases

# List team assignments
python orchestrate_phase_30_plus.py --list-team

# Verbose execution (detailed output)
python orchestrate_phase_30_plus.py --mode parallel --verbose
```

### 3. Workflow Orchestration (`.claude/workflows/consolidation_phase_30_plus_execution.js`)

**Purpose**: Multi-agent workflow for complete Phase 30-35 automation

#### 4 Phases

1. **Phase Setup** - Initialize branches and health checks
2. **Wave 1** - Phases 30, 32, 34 (Week 1 parallel execution)
3. **Wave 2** - Phases 31, 33, 35 (Week 2 parallel execution)
4. **Verification** - Integration testing and final validation

#### Execution

```bash
# Run in Claude Code (recommended)
/workflow consolidation-phase-30-plus

# Or from terminal
claude workflow run consolidation-phase-30-plus
```

#### Workflow Features

- **Parallel execution**: All 3 developers work simultaneously in Week 1 and Week 2
- **Automatic validation**: Dependency checking and team capacity validation
- **Metrics collection**: LOC, tests, regressions tracked in real-time
- **Code review**: Automated merge gates and verification
- **Rollback capability**: Can revert any phase if issues detected

---

## Team Assignments

### Sarah Chen (Team Lead)

**Phases**: 32 (Monitoring), 35 (Security)
**Hours**: 20 hours total (2 weeks)

| Phase | Name | Hours | LOC Target | Tests |
|-------|------|-------|------------|-------|
| 32 | Monitoring & Observability | 10h | 1,200 | 180+ |
| 35 | Security & Compliance | 10h | 1,050 | 150+ |

**Responsibilities**:
- Orchestrate concurrent work across Marcus and Alex
- Code review approval for all phases
- Security architecture oversight (Phase 35)
- Daily standups and blocker resolution

### Marcus Johnson (Developer 1)

**Phases**: 30 (Marketplace), 31 (Skills), 33 (Error Handling)
**Hours**: 30 hours total (2 weeks)

| Phase | Name | Hours | LOC Target | Tests |
|-------|------|-------|------------|-------|
| 30 | Marketplace Module | 10h | 1,350 | 200+ |
| 31 | Skill Management | 10h | 1,050 | 150+ |
| 33 | Error Handling & Recovery | 10h | 900 | 140+ |

**Responsibilities**:
- Week 1: Phase 30 (Marketplace consolidation)
- Week 2: Phases 31 (Skills) + 33 (Error Handling) concurrent
- Implement all framework patterns
- Unit test creation and execution

### Alex Patel (Developer 2)

**Phases**: 34 (Logging)
**Hours**: 8 hours total (1.5 weeks)

| Phase | Name | Hours | LOC Target | Tests |
|-------|------|-------|------------|-------|
| 34 | Logging & Diagnostics | 8h | 800 | 130+ |

**Responsibilities**:
- Phase 34: Logging & Diagnostics (Week 1)
- Support Phase 31 (Skills) migration if needed
- Infrastructure optimization after Phase 34
- Performance monitoring

---

## Execution Timeline

### Week 1 (Parallel Execution)

**Monday**
```bash
python run_phase.py --phase 30 --developer marcus  # Marketplace
python run_phase.py --phase 32 --developer sarah   # Monitoring
python run_phase.py --phase 34 --developer alex    # Logging
```

**Tuesday-Thursday**: Continue implementation

**Friday**:
```bash
# Merge Week 1 phases
python run_phase.py --phase 30 --developer marcus --dry-run  # Validate
# Then merge Phase 30, 32, 34 to main

# Run full test suite
pytest tests/ -v --cov=app
```

### Week 2 (Parallel Execution)

**Monday**
```bash
python run_phase.py --phase 31 --developer marcus  # Skills
python run_phase.py --phase 33 --developer marcus  # Error Handling
python run_phase.py --phase 35 --developer sarah   # Security
```

**Tuesday-Thursday**: Continue implementation

**Friday**:
```bash
# Merge Week 2 phases
# Then run final verification
pytest tests/ -v --cov=app
python daily_dashboard.py
```

---

## Consolidation Targets

### LOC Reduction

| Phase | Name | Before | Target | Reduction |
|-------|------|--------|--------|-----------|
| 30 | Marketplace | 2,000 | 1,350 | 32.5% |
| 31 | Skills | 1,500 | 1,050 | 30.0% |
| 32 | Monitoring | 1,800 | 1,200 | 33.3% |
| 33 | Error Handling | 1,400 | 900 | 35.7% |
| 34 | Logging | 1,200 | 800 | 33.3% |
| 35 | Security | 1,600 | 1,050 | 34.4% |
| **TOTAL** | **6 Phases** | **9,500** | **6,350** | **33.2%** |

### Test Coverage

- **Target**: 950+ tests across all phases
- **Phase 30**: 200+ tests (marketplace handlers, validators, cache)
- **Phase 31**: 150+ tests (skill registry, validation)
- **Phase 32**: 180+ tests (monitoring, alerting, diagnostics)
- **Phase 33**: 140+ tests (error handlers, retry, recovery)
- **Phase 34**: 130+ tests (logging, tracing, structured data)
- **Phase 35**: 150+ tests (security, compliance, audit)

### Quality Gates

- ✅ All tests passing (1,611+ total)
- ✅ 0 regressions
- ✅ 100% backward compatibility
- ✅ Code review approved
- ✅ Documentation complete

---

## Monitoring & Verification

### Daily Status

```bash
# View daily metrics
python scripts/consolidation/daily_dashboard.py

# Output shows:
# - Tests passing
# - Regressions
# - LOC consolidated so far
# - Phase completion status
# - Team progress
```

### Health Checks

```bash
# Pre-execution validation
python scripts/consolidation/health_check_complete.py

# During execution (hourly)
python scripts/consolidation/health_check_complete.py --hourly

# Post-execution verification
python scripts/consolidation/verify_phase_complete.py --phase 30
```

### Test Verification

```bash
# Run full test suite
pytest tests/ --cov=app -v

# Phase-specific tests
pytest tests/test_phase_30*.py -v
pytest tests/test_phase_31*.py -v
pytest tests/test_phase_35*.py -v
```

---

## Common Issues & Solutions

### Phase Fails Tests

**Symptom**: `pytest tests/test_phase_30*.py` shows failures

**Solution**:
```bash
# Check test output
pytest tests/test_phase_30*.py -vv

# Identify issue:
# - Import error? Run migration script
# - Type mismatch? Update type hints
# - Missing test? Add test skeleton

# Re-run after fix
pytest tests/test_phase_30*.py -v
```

### Merge Conflict

**Symptom**: `git merge` shows conflicts

**Solution**:
```bash
# Check merge status
git status

# Resolve conflicts manually
# Usually in imports or framework definitions

# Re-run tests after resolution
pytest tests/ -x
```

### Team Member Unavailable

**Symptom**: Developer cannot work on assigned phase

**Solution**:
```bash
# Option 1: Swap assignments
python run_phase.py --phase 31 --developer alex  # If Marcus unavailable

# Option 2: Extend timeline
# Instead of 2 weeks, make it 3 weeks

# Option 3: Bring in contractor
# For specialized phases (e.g., Phase 35 security)
```

---

## Success Criteria

### Phase-Level

For each phase (30-35):
- ✅ LOC target met (within 10%)
- ✅ All tests passing (100%)
- ✅ Code review approved
- ✅ Merged to main
- ✅ 0 regressions

### Project-Level

For Phase 30-35 completion:
- ✅ All 6 phases merged
- ✅ 6,350+ LOC consolidated (33.2% reduction)
- ✅ 950+ tests passing
- ✅ 0 regressions across all phases
- ✅ 100% backward compatibility
- ✅ 6 unified frameworks created
- ✅ All documentation complete

### Timeline

- ✅ Completed within 2 weeks (parallel)
- ✅ Production ready for v1.3.0 release
- ✅ Ready for Phase 36+ planning

---

## Advanced Usage

### Custom Phase Execution

```bash
# Execute phase with custom LOC target
python run_phase.py --phase 30 --developer marcus --loc-target 1200

# Execute with extended hours
python run_phase.py --phase 32 --developer sarah --hours 12
```

### Orchestration with Custom Config

```bash
# Execute with custom execution plan
python orchestrate_phase_30_plus.py --mode parallel --phases 30,32,34 --skip 31,33,35

# Generate execution report
python orchestrate_phase_30_plus.py --mode dry-run --generate-report
```

### Workflow with Custom Parameters

```bash
# Run workflow with extended timeline
/workflow consolidation-phase-30-plus --timeline extended

# Run with specific team
/workflow consolidation-phase-30-plus --team marcus,sarah,alex
```

---

## Results Expected

### Code Consolidation

- **Before**: 9,500 LOC across 6 areas (marketplace, skills, monitoring, error, logging, security)
- **After**: 6,350 LOC consolidated into 6 unified frameworks
- **Reduction**: 3,150 LOC (33.2% reduction)

### Frameworks Created

1. **MarketplaceFramework** (570 LOC) - Handles all marketplace operations
2. **SkillRegistry** (400 LOC) - Centralized skill management
3. **MonitoringFramework** (580 LOC) - Unified monitoring and alerting
4. **ErrorFramework** (370 LOC) - Error handling and recovery
5. **LoggingFramework** (350 LOC) - Structured logging and tracing
6. **SecurityFramework** (480 LOC) - Security and compliance

### Quality

- **Tests**: 950+ new tests + 1,611 existing = 2,561 total passing
- **Regressions**: 0 across all phases
- **Backward Compatibility**: 100% (no breaking changes)
- **Coverage**: 99%+ across all frameworks

### Timeline

- **Actual Execution**: 2 weeks (parallel, Week 1 + Week 2)
- **Planned Duration**: 3 weeks (sequential)
- **Time Saved**: 1 week (33% faster with parallelization)

---

## Next Steps After Phase 30-35

1. **Deploy v1.3.0** to production with all 6 frameworks
2. **Measure impact** — LOC reduction, test coverage, maintainability
3. **Plan Phase 36+** — Next wave of consolidations
4. **Capture lessons learned** — Document best practices
5. **Schedule Phase 40** — Final strategic consolidation

---

## Support & Resources

### Documentation

- **Phase 30 Execution**: `CONSOLIDATION_PHASE_30_EXECUTION_GUIDE.md`
- **Phase 30-35 Roadmap**: `CONSOLIDATION_PHASE_30_PLUS_ROADMAP.md`
- **Team Charter**: `CONSOLIDATION_TEAM_CHARTER.md`
- **Team Resources**: `CONSOLIDATION_TEAM_RESOURCES.md`

### Monitoring

- Daily dashboard: `python scripts/consolidation/daily_dashboard.py`
- Health checks: `python scripts/consolidation/health_check_complete.py`
- Phase verification: `python scripts/consolidation/verify_phase_complete.py`

### Contact

For issues or blockers:
- **Team Lead**: Sarah Chen (sarah@nxgntch.com)
- **Dev 1**: Marcus Johnson (marcus@nxgntch.com)
- **Dev 2**: Alex Patel (alex@nxgntch.com)

---

**Status**: Ready for execution ✅
**Created**: 2026-09-05
**Phase Range**: 30-35
**Execution Mode**: Parallel (2 weeks)
**LOC Consolidation Target**: 6,350 (33.2% reduction)
