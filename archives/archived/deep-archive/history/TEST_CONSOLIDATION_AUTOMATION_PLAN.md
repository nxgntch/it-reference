# Test Consolidation Automation Plan

**Status**: Planned  
**Created**: 2026-09-01  
**Last Updated**: 2026-09-01  
**Target Completion**: Phase [TBD]

---

## Executive Summary

This plan automates consolidation of 40+ fragmented test files (4,300+ lines of duplicated/related tests) into focused, maintainable test suites. Following successful completion of phase 1 (empty stub removal), this plan targets:

- **13 consolidation operations** across 40+ files
- **~4,300 lines** of redundant/overlapping tests
- **Reduction to ~20 core test files** (from 81)
- **Improved maintainability** and faster test suite execution
- **Zero test coverage loss** (maintain 95% threshold)

---

## Completed Work (Phase 1)

✅ **Empty Stub File Removal** (Baseline complete)
- Deleted 5 completely empty test files (545 empty test functions, 146 empty classes)
- Removed 3 duplicate test methods from test_orchestrator_comprehensive.py
- Consolidated 2 gap coverage files (batch_processor, config_loader)
- **Result**: 2,741 passing tests, 95% coverage maintained

---

## Phase 2: High-Priority Consolidations

### Consolidation 1: Stats Files (High Priority - Smallest)
**Scope**: `test_core_stats_collector.py` → `test_stats_collector.py`

| File | Lines | Test Classes | Action |
|------|-------|--------------|--------|
| test_stats_collector.py | 613 | 12 | MERGE INTO |
| test_core_stats_collector.py | 123 | 6 | **DELETE AFTER MERGE** |
| test_batch_stats_coverage.py | 258 | 2 | **EVALUATE** (may split) |

**Implementation**:
1. Read test_core_stats_collector.py to identify test classes
2. Review test_stats_collector.py coverage
3. Copy unique test classes from test_core_stats_collector.py to test_stats_collector.py
4. Update imports/fixtures as needed
5. Run full test suite to verify
6. Delete test_core_stats_collector.py
7. Commit with message: `test(stats): consolidate core stats tests into stats_collector`

**Expected Outcome**: 123 line reduction, 1 fewer test file

---

### Consolidation 2: Orchestrator Files (High Priority - Related Component)
**Scope**: `test_orchestrator_and_skills.py` → `test_orchestrator_comprehensive.py`

| File | Lines | Test Classes | Action |
|------|-------|--------------|--------|
| test_orchestrator_comprehensive.py | 736 | 21 | MERGE INTO |
| test_orchestrator_and_skills.py | 290 | 6 | **DELETE AFTER MERGE** |

**Implementation**:
1. Read test_orchestrator_and_skills.py (6 classes: Initialization, Dependencies, AgentInit, Invocation, TeamMapping, Accessors)
2. Review test_orchestrator_comprehensive.py for overlaps
3. Insert skills-related tests after core tests (organized by functionality)
4. Update imports and fixtures
5. Run full test suite
6. Delete test_orchestrator_and_skills.py
7. Commit with message: `test(orchestrator): consolidate skills integration tests`

**Expected Outcome**: 290 line reduction, 1 fewer test file, more complete orchestrator coverage

---

### Consolidation 3: Batch Files (Highest Impact)
**Scope**: 3 coverage files → `test_batching.py`

| File | Lines | Action |
|------|-------|--------|
| test_batching.py | 1,408 | MERGE INTO |
| test_batch_execution_coverage.py | 372 | **DELETE AFTER MERGE** |
| test_batch_formation_cache_coverage.py | 331 | **DELETE AFTER MERGE** |
| test_batch_stats_coverage.py | 258 | **EVALUATE** (cross-ref with consolidation 1) |

**Implementation**:
1. Read all three coverage files
2. Identify non-overlapping test classes:
   - test_batch_execution_coverage.py: BatchExecutionMixin, ConcurrentExecution, ResultCollection, ResultAggregation, ErrorHandling
   - test_batch_formation_cache_coverage.py: BatchFormationCache, CacheIntegration, CacheExpiration, CacheEviction, CacheStatistics
3. Append to test_batching.py organized by concern
4. Update imports
5. Run test suite with `pytest tests/test_batching.py -v`
6. Delete coverage files
7. Commit with message: `test(batch): consolidate execution, cache, and coverage tests into batching`

**Expected Outcome**: 961 line reduction, 2 fewer test files, comprehensive batch coverage in single file

---

### Consolidation 4: Config/Cache Files (Medium Priority)
**Scope**: Related config tests consolidation

| File | Lines | Action |
|------|-------|--------|
| test_config_loader.py | 531 | **REVIEW** (primary) |
| test_config_cache_coverage.py | 344 | **MERGE INTO config_loader** |
| test_agent_config_cache_comprehensive.py | 417 | **REVIEW** (agent-specific) |

**Implementation** (if consolidating):
1. Review test_config_cache_coverage.py test classes
2. Check if tests fit into test_config_loader.py scope
3. If yes, merge and delete test_config_cache_coverage.py
4. Keep test_agent_config_cache_comprehensive.py separate (tests agent-specific config behavior)
5. Commit: `test(config): consolidate cache coverage into config loader tests`

**Expected Outcome**: 344 line reduction, 1 fewer test file

---

### Consolidation 5: Metrics Files (Medium Priority - Verify Independence)
**Scope**: `test_metrics_alerts_coverage.py` + `test_metrics_timeseries_coverage.py`

| File | Lines | Status |
|------|-------|--------|
| test_metrics_alerts_coverage.py | 518 | **KEEP SEPARATE** (distinct concern) |
| test_metrics_timeseries_coverage.py | 499 | **KEEP SEPARATE** (time-series logic) |

**Decision**: Do NOT merge (separate architectural concerns - alerts vs time-series analytics)

---

## Phase 3: Small File Consolidation (Lower Priority)

**15 files < 150 lines** testing different agent skills/workflows:

```
test_taskIntake.py (89)
test_output_consistency.py (97)
test_decisionMaking.py (100)
test_healthCheck.py (102)
test_crossTeamSynthesis.py (112)
test_integration.py (116)
test_planning.py (125)
test_codeGeneration.py (126)
test_reportGenerator.py (128)
test_tenantRouter.py (129)
test_decomposition.py (130)
test_quotaEnforcer.py (130)
test_docUpdater.py (132)
test_performanceTracing.py (147)
```

**Strategy**: Group by domain (not individual consolidations):
- **Agent Skills Tests**: codeGeneration, codeReview, planning, decomposition, crossTeamSynthesis
- **Workflow Tests**: integration, e2e_workflows, multi_agent_workflows
- **Infrastructure Tests**: taskIntake, healthCheck, tenantRouter, tenantAudit

**Action**: Defer to Phase 3.2 (lower priority, requires domain analysis)

---

## Execution Order (Recommended)

### **Week 1: Phase 2 Core (4-5 hours)**
1. **Stats consolidation** (30 min - smallest, lowest risk)
2. **Orchestrator consolidation** (60 min - related component, proven pattern)
3. **Batch consolidation** (90 min - highest impact)
4. **Config/Cache evaluation** (60 min - review before committing)

### **Week 2: Validation & Verification (2-3 hours)**
1. Full test suite run with coverage report
2. Verify all 2,741+ tests pass
3. Confirm 95% coverage threshold maintained
4. Document results in AUDIT.md

### **Future: Phase 3 (Deferred)**
- Small file consolidation (requires domain knowledge)
- Candidate: Include in next optimization cycle

---

## Verification Checklist

For **each consolidation operation**, verify:

- [ ] Source file(s) read and analyzed
- [ ] Test classes identified (no overlaps)
- [ ] Target file ready for merge
- [ ] Imports updated (no missing dependencies)
- [ ] Fixtures consolidated (no duplication)
- [ ] Run `pytest tests/<merged_file>.py -v` → all pass
- [ ] Run `pytest tests/ --cov=app` → coverage ≥ 95%
- [ ] Commit with conventional commit message
- [ ] Push to `claude/repo-testing-egyfjd`
- [ ] Document in CONSOLIDATION_LOG.md

---

## Expected Outcomes

### **Metrics After Phase 2**
| Metric | Before | After | Δ |
|--------|--------|-------|---|
| Test Files | 81 | 75 | -6 |
| Test Lines | 33,842 | ~32,700 | -1,142 |
| Passing Tests | 2,741 | 2,741+ | Same/+5 |
| Coverage | 95% | 95%+ | Maintained |
| Maintenance Burden | High | Lower | ✓ |

### **Quality Improvements**
- ✅ Related tests grouped by component (easier navigation)
- ✅ Reduced file count (from 81 to 75)
- ✅ Single source of truth per component (no duplicates)
- ✅ Faster test suite execution (fewer file I/O operations)
- ✅ Clearer test organization (by domain, not by coverage type)

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Test coverage drops below 95% | Run full coverage report after each consolidation; revert if needed |
| Duplicate test classes | Search for class name in all files before merging; review carefully |
| Missing fixtures/imports | Run tests immediately after merge; fix import errors before commit |
| Merge conflicts | Consolidate one file at a time; push immediately after merge |
| Tests fail after consolidation | Revert commit; analyze root cause; retry with incremental approach |

---

## Automation Script (Optional Future)

Once manual consolidations complete, create Python script to:
1. Scan all test files for duplicate class/function names
2. Identify thin files (< 150 lines, < 3 test classes)
3. Group by component and suggest consolidations
4. Generate merge operations (dry-run mode)

**Target**: Phase 3.2 or later

---

## Related Documents

- **Completed Work**: [Test Consolidation Phase 1 Summary](./TEST_CONSOLIDATION_PHASE1_SUMMARY.md)
- **Current Status**: [AUDIT.md](../../AUDIT.md) (test count, coverage)
- **Git History**: Branch `claude/repo-testing-egyfjd` (consolidation commits)
- **Test Organization**: [testing.md](../../../../docs/rules/testing.md)

---

## How to Use This Plan

1. **For immediate action**: Follow "Execution Order" section
2. **For tracking progress**: Update status of each consolidation below
3. **For future sessions**: Reference this document as SSOT for test consolidation strategy

### Consolidation Progress

- [ ] **Consolidation 1**: Stats files (test_core_stats_collector → test_stats_collector)
- [ ] **Consolidation 2**: Orchestrator files (test_orchestrator_and_skills → test_orchestrator_comprehensive)
- [ ] **Consolidation 3**: Batch files (3 coverage files → test_batching)
- [ ] **Consolidation 4**: Config files (test_config_cache_coverage → test_config_loader)
- [ ] **Phase 2 Complete**: All core consolidations done, coverage verified
- [ ] **Phase 3 Planned**: Small file consolidation (deferred)

---

**Last Updated**: 2026-09-01  
**Next Review**: After Phase 2 completion

