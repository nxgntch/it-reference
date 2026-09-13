# Phase 30-35 Agent Commands - Quick Reference

**One-page guide for executing Phase 30-35 consolidation (6 phases, 2 weeks, 6,350 LOC reduction)**

---

## Three Ways to Execute Phase 30-35

### Option 1: Single Phase Execution

Run individual phases one at a time:

```bash
# Phase 30 - Marketplace (Marcus)
python run_phase.py --phase 30 --developer marcus

# Phase 31 - Skills (Marcus)
python run_phase.py --phase 31 --developer marcus

# Phase 32 - Monitoring (Sarah)
python run_phase.py --phase 32 --developer sarah

# Phase 33 - Error Handling (Marcus)
python run_phase.py --phase 33 --developer marcus

# Phase 34 - Logging (Alex)
python run_phase.py --phase 34 --developer alex

# Phase 35 - Security (Sarah)
python run_phase.py --phase 35 --developer sarah
```

### Option 2: Orchestrated Execution (Recommended)

Run all 6 phases with automatic team coordination:

```bash
# Validate plan (dry run)
python orchestrate_phase_30_plus.py --mode dry-run

# Execute in parallel (Week 1 + Week 2, 2 weeks total)
python orchestrate_phase_30_plus.py --mode parallel --verbose

# Execute sequentially (3 weeks, easier to debug)
python orchestrate_phase_30_plus.py --mode sequential

# Hybrid mode (balanced, 2.5 weeks)
python orchestrate_phase_30_plus.py --mode hybrid --verbose
```

### Option 3: Workflow Orchestration (Multi-Agent)

Let Claude orchestrate all phases with automatic validation:

```bash
# Run in Claude Code
/workflow consolidation-phase-30-plus

# Or from terminal
claude workflow run consolidation-phase-30-plus
```

---

## Team & Phases

| Developer | Phases | Total Hours | Week 1 | Week 2 |
|-----------|--------|-------------|--------|--------|
| **Marcus** | 30, 31, 33 | 30h | Phase 30 | Phases 31 + 33 |
| **Sarah** | 32, 35 | 20h | Phase 32 | Phase 35 |
| **Alex** | 34 | 8h | Phase 34 | (Support) |

---

## Targets

| Phase | Name | Before | After | Reduction | Tests |
|-------|------|--------|-------|-----------|-------|
| 30 | Marketplace | 2,000 | 1,350 | 32.5% | 200+ |
| 31 | Skills | 1,500 | 1,050 | 30.0% | 150+ |
| 32 | Monitoring | 1,800 | 1,200 | 33.3% | 180+ |
| 33 | Errors | 1,400 | 900 | 35.7% | 140+ |
| 34 | Logging | 1,200 | 800 | 33.3% | 130+ |
| 35 | Security | 1,600 | 1,050 | 34.4% | 150+ |
| **TOTAL** | **6 phases** | **9,500** | **6,350** | **33.2%** | **950+** |

---

## Execution Checklist

### Pre-Execution

- [ ] `python orchestrate_phase_30_plus.py --mode dry-run` (validate)
- [ ] `python health_check_complete.py` (health check)
- [ ] All 1,611 tests passing
- [ ] Team briefing complete

### Week 1 (Parallel)

- [ ] Phase 30 (Marcus): 1,350 LOC, 200+ tests
- [ ] Phase 32 (Sarah): 1,200 LOC, 180+ tests
- [ ] Phase 34 (Alex): 800 LOC, 130+ tests
- [ ] Merge all 3 phases to main
- [ ] `pytest tests/ -v` (full test verification)

### Week 2 (Parallel)

- [ ] Phase 31 (Marcus): 1,050 LOC, 150+ tests
- [ ] Phase 33 (Marcus): 900 LOC, 140+ tests
- [ ] Phase 35 (Sarah): 1,050 LOC, 150+ tests
- [ ] Merge all 3 phases to main
- [ ] `pytest tests/ -v` (full test verification)

### Post-Execution

- [ ] Final integration tests: 950+ tests passing
- [ ] Performance validation
- [ ] Backward compatibility: 100%
- [ ] Documentation complete
- [ ] Production ready for v1.3.0

---

## Quick Commands

### List & Validate

```bash
python run_phase.py --list-phases           # List all phases (22-35)
python run_phase.py --list-developers       # List team
python orchestrate_phase_30_plus.py --list-phases  # List 30-35 only
python orchestrate_phase_30_plus.py --list-team    # List team
```

### Monitor Execution

```bash
python daily_dashboard.py                   # View daily metrics
python health_check_complete.py             # Pre-execution validation
python health_check_complete.py --hourly    # During-execution checks
```

### Verify Phases

```bash
pytest tests/test_phase_30*.py -v           # Phase 30 tests
pytest tests/test_phase_35*.py -v           # Phase 35 tests
pytest tests/ --cov=app -v                  # Full suite (1,611 tests)
```

---

## Execution Time Estimates

| Mode | Week 1 | Week 2 | Total | Best For |
|------|--------|--------|-------|----------|
| **Parallel** | Simultaneous | Simultaneous | 2 weeks | Maximum efficiency |
| **Hybrid** | 3 phases | 3 phases | 2.5 weeks | Balanced |
| **Sequential** | 2 phases | 2 phases | 3 weeks | Debugging |

---

## Success Criteria

- ✅ All 6 phases completed and merged
- ✅ 6,350 LOC consolidated (33.2% reduction)
- ✅ 950+ new tests passing
- ✅ 0 regressions (1,611 total tests passing)
- ✅ 100% backward compatibility
- ✅ 6 frameworks created
- ✅ Production ready

---

## Troubleshooting

| Issue | Command | Solution |
|-------|---------|----------|
| Phase fails | `pytest test_phase_XX.py -vv` | Fix issue, re-run tests |
| Merge conflict | `git status` | Resolve, re-test |
| Dev unavailable | `run_phase.py --phase XX --developer ALT` | Use backup dev |
| Tests fail | `pytest tests/ -x` | Check imports, types |

---

## Resources

- **Full Guide**: `PHASE_30_PLUS_AGENT_COMMANDS.md`
- **Roadmap**: `CONSOLIDATION_PHASE_30_PLUS_ROADMAP.md`
- **Phase 30 Exec**: `CONSOLIDATION_PHASE_30_EXECUTION_GUIDE.md`
- **Team Charter**: `CONSOLIDATION_TEAM_CHARTER.md`

---

**Status**: Ready for execution ✅
**Timeline**: 2 weeks (parallel) | 3 weeks (sequential)
**LOC Target**: 9,500 → 6,350 (33.2% reduction)
**Test Target**: 950+ tests | 0 regressions
**Frameworks**: 6 unified frameworks
