# Phase 3c: Rollout - Consolidation Expansion

**Status**: IN PROGRESS  
**Date**: 2026-08-26  
**Target**: Apply consolidation pattern to additional test files

---

## Overview

Phase 3c expands the test consolidation pattern from Phase 3a (`test_documentation_and_sync_pipeline.py`) to additional test files across the codebase.

**Goal**: Consolidate 20-30 tests from 2-3 additional test files using the proven pattern.

---

## Candidate Test Files

### Analysis: Consolidation Opportunities

#### 1. **test_config_output.py** (525 lines) — PRIMARY TARGET

**Class-based organization** with clear consolidation candidates:

| Class | Methods | Pattern | Opportunity |
|-------|---------|---------|-------------|
| TestYAMLConfigOutput | 3 | File I/O (parse, validate, preserve) | ✅ HIGH |
| TestJSONConfigOutput | 3 | File I/O (parse, data types, special chars) | ✅ HIGH |
| TestConfigSchemaValidation | 3 | Validation (agent, model, governance schemas) | ✅ HIGH |
| TestConfigMigration | 3 | State transition (v1→v2, preserve, rollback) | ✅ MEDIUM |
| TestConfigExport | 3 | File export (yaml, json, roundtrip) | ✅ MEDIUM |
| TestConfigValidation | 4 | Validation rules (budget, model, skills, thresholds) | ✅ MEDIUM |
| TestConfigEnvironmentVariables | 2 | Env var handling (path, override) | ✅ LOW |

**Estimated Consolidation**: 21 tests → 7 parametrized tests (~67% reduction)  
**Estimated Time**: 3-4 hours (4-5 hours/group @ 5-6 tests per class)

#### 2. **test_api_responses.py** (473 lines) — SECONDARY TARGET

**Tests HTTP response handling** - good consolidation candidates expected

#### 3. **test_schema_validation.py** (605 lines) — FUTURE TARGET

**Schema validation tests** - likely high consolidation potential

---

## Phase 3c Execution Plan

### Stage 1: Test & Validate (30 minutes)
- [ ] Analyze test_config_output.py structure
- [ ] Identify consolidation patterns
- [ ] Document 7 consolidation groups
- [ ] Estimate consolidation effort

### Stage 2: High-Priority Consolidations (2-3 hours)
- [ ] Consolidate TestYAMLConfigOutput (3→1)
- [ ] Consolidate TestJSONConfigOutput (3→1)
- [ ] Consolidate TestConfigSchemaValidation (3→1)
- [ ] Run integration tests after each consolidation

### Stage 3: Medium-Priority Consolidations (1-2 hours)
- [ ] Consolidate TestConfigMigration (3→1)
- [ ] Consolidate TestConfigExport (3→1)
- [ ] Consolidate TestConfigValidation (4→1)
- [ ] Run integration tests

### Stage 4: Wrap-up (30 minutes)
- [ ] Consolidate TestConfigEnvironmentVariables (2→1)
- [ ] Final integration testing (all tests pass)
- [ ] Document metrics

---

## Team Training Materials

### Quick Start (5 minutes)
```
Phase 3 Consolidation Pattern:

✅ 1. Identify tests with similar names
✅ 2. Read original test logic
✅ 3. Design @pytest.mark.parametrize table
✅ 4. Write unified test function
✅ 5. Verify all scenarios pass
✅ 6. Commit with metrics

Result: N individual tests → 1 parametrized test
Reduction: ~30-40% code lines
```

### Pattern Template (Copy-Paste)
```python
@pytest.mark.parametrize(
    "scenario,setup,expectedChecks",
    [
        ("scenario1", lambda cfg: cfg, [("field", value1)]),
        ("scenario2", lambda cfg: modifyConfig(cfg), [("field", value2)]),
    ],
    ids=["scenario1", "scenario2"],
)
@pytest.mark.unit
def testConsolidatedName(config_fixture, scenario, setup, expectedChecks):
    """Consolidated parametrized test."""
    cfg = setup(config_fixture)
    result = Function(cfg)
    
    for checkType, expectedValue in expectedChecks:
        assert result[checkType] == expectedValue
```

### Reference Materials
- **Adoption Guide**: `docs/work/current/phase3b_adoption_guide.md`
- **Pattern Examples**: `tests/test_documentation_and_sync_pipeline.py` (30 parametrized tests)
- **Metrics**: Phase 3 achieved 39% code reduction across 65 tests

---

## Success Criteria

- [ ] 20+ tests consolidated from test_config_output.py
- [ ] 0 regressions in integration testing
- [ ] Code reduction: 25-40% (target ~35%)
- [ ] All commits follow pattern (5-minute commits)
- [ ] Metrics documented
- [ ] Team feedback gathered

---

## Expected Outcomes

### Code Reduction
| File | Before | After | Reduction |
|------|--------|-------|-----------|
| test_config_output.py | 525 lines | ~400 lines | ~125 lines (24%) |
| test_api_responses.py | 473 lines | ~350 lines | ~123 lines (26%) |
| TOTAL | ~1000 lines | ~750 lines | ~250 lines (25%) |

### Learning Objectives
- [x] Pattern proven effective on Phase 3a
- [ ] Pattern applied to new file type (class-based tests)
- [ ] Team competency with consolidation
- [ ] Metrics tracking established

---

## Timeline

**Estimated**: 4-6 hours total (spread across sessions)

| Stage | Time | Deliverable |
|-------|------|------------|
| 1. Analysis | 30 min | Consolidation groups identified |
| 2. High-priority | 2-3 h | 9 tests consolidated (3 classes) |
| 3. Medium-priority | 1-2 h | 10 tests consolidated (3 classes) |
| 4. Wrap-up | 30 min | Metrics documented |

---

## Notes

### Why test_config_output.py?
1. **Clear structure**: Class-based organization
2. **Homogeneous tests**: Each class tests same domain
3. **Manageable size**: 525 lines (~100 lines per class)
4. **Good learning opportunity**: Demonstrates pattern on different test style
5. **Low risk**: Not on critical path

### Class-based Tests Consolidation
Class-based tests can be consolidated at the method level:
- Each test method → scenario in parametrized test
- Fixture/setup code → shared `self` or fixture parameter
- Assertion logic → generalized check loop

---

## Resources

### Documentation
- **Phase 3b Adoption Guide**: `docs/work/current/phase3b_adoption_guide.md`
- **Phase 3 Summary**: `docs/work/current/phase3_complete.md`
- **Example Consolidations**: `tests/test_documentation_and_sync_pipeline.py`

### Tools & Commands
```bash
# Analyze file
grep -E "def test|class Test" tests/test_config_output.py

# Run specific test class
pytest tests/test_config_output.py::TestYAMLConfigOutput -v

# Run all tests in file
pytest tests/test_config_output.py -v

# Check consolidation results
git diff HEAD~1 tests/test_config_output.py | grep -c "^-"  # lines removed
```

---

**Ready to start Phase 3c consolidations. Next: Consolidate TestYAMLConfigOutput (3→1 test)**
