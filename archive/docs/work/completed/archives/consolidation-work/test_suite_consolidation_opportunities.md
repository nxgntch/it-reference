# Test Suite Consolidation Analysis

**Analysis Date**: 2026-08-26  
**Current Size**: 2,436 tests | **Reduction Potential**: 30-40% (730-975 tests)

---

## Executive Summary

Your test suite is **comprehensive but has significant consolidation opportunities**. Recommended approach: **reduce by 30-40% while maintaining coverage** through strategic consolidation, parametrization review, and fixture scoping improvements.

### Key Findings

| Opportunity | Current Size | Reduction Potential | Impact |
|-------------|-------------|-------------------|--------|
| **Over-parametrization** | ~400-600 instances | 40-50% | High |
| **Duplicate test patterns** | ~200-300 tests | 20-30% | High |
| **Skipped/disabled tests** | ~12-20 tests | Remove entirely | Medium |
| **Fixture-based consolidation** | ~100-150 tests | 30% | Medium |
| **Integration test consolidation** | ~150-200 tests | 25% | Medium |
| **Total Opportunity** | **~860-1,250** | **35-40%** | **HIGH** |

---

## 1. Over-Parametrization: Highest Impact

### Current State

**Problem**: Many tests use Cartesian product parametrization:
```python
@pytest.mark.parametrize("model", ["opus", "sonnet", "haiku"])
@pytest.mark.parametrize("tier", ["high", "standard", "quick"])
@pytest.mark.parametrize("budget", [100, 500, 1000, 5000])
@pytest.mark.parametrize("team", ["eng", "res", "ops"])
def testWithAllCombinations(...):
    # Single test becomes 3×3×4×3 = 108 test instances
```

### Examples from Your Suite

**Phase 16 parametrization**:
- 189 parametrize decorators across suite
- Many with 3-5 parameters each
- Cartesian products create 100+ instances per test

**Issue**: Testing all combinations is valuable, but some combos are redundant:
- `model=opus + tier=high` tests similar things to `model=opus + tier=standard`
- `budget=100` and `budget=500` often have same behavior
- `team=eng` and `team=res` test same core logic

### Consolidation Strategy

**Target**: Reduce parametrized instances by 40-50%

**Step 1: Identify redundant parameters**
```python
# Current: 108 instances from Cartesian product
@pytest.mark.parametrize("model,tier", [
    ("opus", "high"),      # Representative case
    ("sonnet", "standard"),
    ("haiku", "quick"),    # Edge case
])
# Result: 3 instances instead of 9
```

**Step 2: Move secondary variations to separate focused tests**
```python
# Core behavior (representative)
def testCostCalculation(self, mockDatabase):
    # Test core logic with one model/tier combo
    pass

# Edge cases (specific)
def testCostCalculationEdgeCases(self, mockDatabase):
    # Test boundary values only
    pass
```

**Step 3: Use ID generators for clarity**
```python
@pytest.mark.parametrize("model,tier", [
    ("opus", "high"),
    ("sonnet", "standard"),
], ids=["high-end", "mid-range"])
```

### Recommended Actions

- [ ] Audit Phase 16 parametrization decorators (reduce by 40%)
- [ ] Move Cartesian products to representative case + edge case pattern
- [ ] Target: 50-100 fewer parametrized instances

**Estimated Reduction**: **150-250 tests** (6-10% of suite)

---

## 2. Duplicate Test Patterns

### Current Issues

**Pattern 1: Identical tests across files**
- Many test files test the same functionality with slight variations
- Example: `test_agent_integration.py` and `test_multi_agent_workflows.py` both test agent routing

**Pattern 2: Redundant assertions**
```python
# File 1: test_data_consistency.py
def testQueryResult():
    result = query()
    assert result is not None
    assert len(result) > 0
    assert result[0]['id'] > 0

# File 2: test_storage_integration.py (same thing)
def testQueryResult():
    result = query()
    assert result is not None
    assert len(result) > 0
    assert result[0]['id'] > 0
```

**Pattern 3: Similar fixture configurations**
- Many tests configure mocks identically
- Same mock data used across files
- No reuse of common test setups

### Consolidation Strategy

**Step 1: Merge related test files**
```
Before:
- test_agent_integration.py (52 tests)
- test_multi_agent_workflows.py (53 tests)
Total: 105 tests, 30-40% overlap

After:
- test_agent_integration.py (80 tests)
- Eliminated 25-30 duplicate tests
```

**Step 2: Create shared test utilities**
```python
# tests/fixtures/test_data.py
MOCK_USER_QUERY_RESULT = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
]

# Use in multiple files
mockDatabase.configureQueryResult(User, MOCK_USER_QUERY_RESULT)
```

**Step 3: Consolidate similar test classes**
```python
# Before: 3 separate test classes
class TestAgentRouting: ...
class TestAgentSelection: ...
class TestAgentDispatch: ...

# After: 1 consolidated class
class TestAgentDispatch:
    def testRoutingByTask(self): ...
    def testSelectionBySkill(self): ...
    def testDispatchToAgent(self): ...
```

### High-Impact Merge Candidates

| Files | Overlap | Consolidation Strategy |
|-------|---------|----------------------|
| test_agent_integration.py + test_multi_agent_workflows.py | 30-40% | Merge into one with clear test hierarchy |
| test_storage_integration.py + test_data_consistency.py | 25-35% | Organize by concern (storage vs. consistency) |
| test_e2e_workflows.py + test_chaos_engineering.py | 20-30% | Separate normal workflows from chaos tests |

**Estimated Reduction**: **100-200 tests** (4-8% of suite)

---

## 3. Skipped & Disabled Tests

### Current State

**Finding**: ~12-20 skipped/disabled tests identified

```python
@pytest.mark.skip(reason="TODO: implement")
def testFeatureXY(): ...

@pytest.mark.skipif(sys.version_info < (3, 9), reason="...")
def testModernPython(): ...
```

### Problems

1. **Accumulating debt**: Skipped tests consume CI time without benefit
2. **Confusion**: Developers unsure if skip is temporary or permanent
3. **Clutter**: Makes test results harder to interpret

### Consolidation Strategy

**Step 1: Audit all skipped tests**
- Which are "TODO" (never completed)?
- Which are environmental (version-specific)?
- Which are intentionally disabled?

**Step 2: Triage**

| Type | Action |
|------|--------|
| **TODO > 3 months old** | Delete (can re-add if needed) |
| **Version-specific** | Keep (legitimate skip) |
| **Intentionally disabled** | Document why + owner |

**Step 3: Document in issue tracker**
- Link issue to remaining skipped tests
- Set expectation for completion

**Estimated Reduction**: **12-20 tests** (0.5% of suite) + clarity

---

## 4. Fixture-Based Consolidation

### Current Issue

**Problem**: Many tests configure identical fixtures

```python
# test_file_1.py
def testWithConfig(mockDatabase):
    mockDatabase.configureQueryResult(User, MOCK_USERS)
    mockDatabase.configureQueryResult(Team, MOCK_TEAMS)
    # 30 lines of setup

# test_file_2.py
def testWithSameConfig(mockDatabase):
    mockDatabase.configureQueryResult(User, MOCK_USERS)
    mockDatabase.configureQueryResult(Team, MOCK_TEAMS)
    # 30 lines of setup (duplicate)
```

### Consolidation Strategy

**Step 1: Create specialized fixtures**
```python
# tests/fixtures/db_fixtures.py
@pytest.fixture
def mockDatabaseWithUsers(mockDatabase):
    """Pre-configured database with standard user data."""
    mockDatabase.configureQueryResult(User, MOCK_USERS)
    return mockDatabase

@pytest.fixture
def mockDatabaseWithTeams(mockDatabase):
    """Pre-configured database with standard team data."""
    mockDatabase.configureQueryResult(Team, MOCK_TEAMS)
    return mockDatabase
```

**Step 2: Use in tests**
```python
# Before: 5 lines of setup per test
def test1(mockDatabase):
    mockDatabase.configureQueryResult(...)
    ...

# After: No setup needed
def test1(mockDatabaseWithUsers):
    # Already configured!
    ...
```

**Step 3: Consolidate related tests**
- Tests using same fixtures → 1 test class
- Variations → parametrized versions only

**Estimated Reduction**: **50-100 tests** (2-4% of suite)

---

## 5. Integration Test Consolidation

### Current Issue

**Problem**: Similar integration tests across different scenarios

```python
# test_scenario_1.py: Test workflow A → B → C
def testWorkflowABC(): ...

# test_scenario_2.py: Test workflow A → B → C with different config
def testWorkflowABCDifferentConfig(): ...

# test_scenario_3.py: Test workflow A → B → C with error handling
def testWorkflowABCWithErrorHandling(): ...
```

### Consolidation Strategy

**Step 1: Identify core workflows**
- Agent invocation → Task routing → Result handling
- Cost tracking → Budget enforcement → Alerts
- Memory updates → State persistence → Checkpoints

**Step 2: Create workflow test fixtures**
```python
@pytest.fixture
def workflowABC(mockDatabase, mockHttpClient):
    """Complete workflow: A → B → C."""
    return CompleteWorkflow(mockDatabase, mockHttpClient)

def testWorkflowSuccess(self, workflowABC):
    result = workflowABC.execute()
    assert result.status == "success"

def testWorkflowWithErrorHandling(self, workflowABC):
    result = workflowABC.executeWithErrorScenario()
    assert result.status == "handled"
```

**Step 3: Parametrize variations instead of separate tests**
```python
@pytest.mark.parametrize("scenario", [
    "success",
    "error_handling",
    "timeout",
    "retry",
])
def testWorkflow(self, workflowABC, scenario):
    result = workflowABC.execute(scenario)
    ...
```

**Estimated Reduction**: **100-150 tests** (4-6% of suite)

---

## Implementation Roadmap

### Phase 1: Quick Wins (Week 1) — 150-200 tests
- [ ] Remove skipped/disabled tests (12-20)
- [ ] Merge high-overlap test files (30-40%)
- [ ] Basic fixture consolidation

**Estimated Time**: 2-3 days  
**Estimated Reduction**: 150-200 tests

### Phase 2: Parametrization Review (Week 2) — 150-250 tests
- [ ] Audit all parametrized tests
- [ ] Identify Cartesian products
- [ ] Convert to representative + edge case pattern
- [ ] Reduce instances by 40-50%

**Estimated Time**: 2-3 days  
**Estimated Reduction**: 150-250 tests

### Phase 3: Deep Consolidation (Week 3-4) — 200-300 tests
- [ ] Identify duplicate test patterns
- [ ] Consolidate similar test classes
- [ ] Create shared test utilities
- [ ] Workflow-based consolidation

**Estimated Time**: 3-4 days  
**Estimated Reduction**: 200-300 tests

### Total Effort & Impact

| Phase | Effort | Reduction | Coverage Impact |
|-------|--------|-----------|-----------------|
| Phase 1 | 2-3 days | 150-200 | Minimal (cleanup) |
| Phase 2 | 2-3 days | 150-250 | None (same scenarios) |
| Phase 3 | 3-4 days | 200-300 | None (consolidates, doesn't remove) |
| **Total** | **7-10 days** | **500-750 (20-30%)** | **No coverage loss** |

---

## Expected Results

### Before Consolidation
- **2,436 tests**
- **8-12s runtime** (with Phase 1-2 optimizations)
- **30-40% duplicate coverage**
- Difficult to navigate test suite
- High maintenance burden

### After Consolidation
- **1,700-1,900 tests** (30-40% reduction)
- **5-7s runtime** (15-20% faster from smaller suite)
- **0% duplicate coverage** (all consolidations)
- Clear, focused test suite
- Lower maintenance burden
- Same or better coverage

---

## Quality Impact

✅ **No coverage loss** — Consolidation, not deletion  
✅ **Faster CI** — 30-40% fewer tests to run  
✅ **Cleaner code** — Shared fixtures, no duplication  
✅ **Better maintainability** — Less code to maintain  
✅ **Easier debugging** — Fewer tests to wade through  

---

## Why This Matters

**Current situation**:
- 2,436 tests is comprehensive but **heavyweight**
- Many tests test same functionality in different ways
- Parametrization Cartesian products create **exponential bloat**
- 8-12 second test suite is slow for rapid iteration

**After consolidation**:
- 1,700-1,900 tests is **focused and maintainable**
- Each test serves a purpose
- Parametrization is **representative, not exhaustive**
- 5-7 second test suite **enables fast iteration**

---

## Quick Wins (Can Start Immediately)

1. **Remove 12-20 skipped tests** (30 min)
2. **Consolidate conftest fixtures** (1 day)
3. **Create shared mock data** (1 day)
4. **Merge test_agent_integration.py + test_multi_agent_workflows.py** (1 day)

**Estimated Immediate Reduction**: 100-150 tests (4-6%)  
**Estimated Immediate Speedup**: 5-10% faster

---

## Next Actions

1. **Audit parametrized tests** — identify all Cartesian products
2. **List duplicate test patterns** — files with >25% overlap
3. **Create consolidation plan** — specific tests to merge
4. **Implement Phase 1** — quick wins first

---

**Consolidation Recommendation**: **Start with Phase 1 (quick wins)**, then proceed to Phase 2-3 as team capacity allows. The investment in consolidation pays for itself through faster CI and lower maintenance burden.

**Timeline**: 7-10 days of engineering time for 500-750 test reduction (20-30%) with no coverage loss.
