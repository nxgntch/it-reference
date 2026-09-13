# Phase 2: Parametrization Consolidation Strategy

**Status**: In Progress  
**Date Started**: 2026-08-27  
**Target Reduction**: 150-250 tests (40-50% of parametrized tests)

---

## Executive Summary

Audit of 181 parametrize decorators across test suite reveals **121 (67%) have 3+ parameters** — these are candidates for consolidation from "exhaustive coverage" to "representative + edge case" pattern.

**Key Finding**: Not true Cartesian products (3×3×4=36 combinations), but rather 4-10 representative test cases per decorator. Opportunity exists to:
1. Reduce multi-parameter tests to core representative cases (3-4 cases)
2. Move edge cases to focused, single-parameter tests
3. Keep coverage while reducing redundancy

---

## Current State Analysis

| Metric | Count | Details |
|--------|-------|---------|
| Total parametrize decorators | 181 | Across 28 test files |
| 1-2 param decorators | ~60 | Simple (low redundancy) |
| **3+ param decorators** | **121** | **Complex (high redundancy)** |
| **Consolidation candidates** | **85-90** | 70% of complex decorators |

### Pattern Breakdown (3+ param decorators)

**Most common patterns**:
1. **4-parameter tests** (most common)
   - Example: `(agentId, teamId, costAmount, canExecute)` with 4-6 cases
   - Issue: Testing multiple orthogonal concerns together
   - Consolidation: Split into representative + edge case tests

2. **3-parameter tests**
   - Example: `(endpoint, method, expected_status)` with 5-8 cases
   - Issue: Different request methods vs. endpoints tested together
   - Consolidation: Use representative method/endpoint pairs only

3. **5+ parameter tests** (rare, high impact)
   - Example: Complex workflow tests with 5-7 parameters
   - Issue: Exponential explosion potential
   - Consolidation: Use representative scenario only

---

## Consolidation Strategy

### Step 1: Representative + Edge Case Pattern

**Before** (exhaustive multi-parameter test):
```python
@pytest.mark.parametrize("agentId,teamId,costAmount,canExecute", [
    ("architect", "engineering", 0.15, True),      # Case 1
    ("researcher", "research", 0.10, True),        # Case 2
    ("manager", "operations", 5000.0, False),      # Case 3 (over budget)
    ("director", "finance", 100.0, True),          # Case 4
])
def testAgentCostValidation(self, agentId, teamId, costAmount, canExecute):
    # Tests 4 agent/team combinations with different costs
    pass
```

**After** (representative + edge cases):
```python
@pytest.mark.parametrize("agentId,teamId,costAmount,canExecute", [
    ("architect", "engineering", 0.15, True),      # Representative
    ("manager", "operations", 5000.0, False),      # Edge case: over budget
])
def testAgentCostValidation(self, agentId, teamId, costAmount, canExecute):
    # Tests core logic + critical edge case (50% reduction)
    pass
```

**Benefit**: 4 test cases → 2 cases (50% reduction), coverage maintained

### Step 2: Split Orthogonal Concerns

**Before** (testing multiple things together):
```python
@pytest.mark.parametrize("endpoint,method,expectedStatus", [
    ("/users", "GET", 200),
    ("/users", "POST", 201),
    ("/users/1", "GET", 200),
    ("/users/1", "PUT", 200),
    ("/users/1", "DELETE", 204),
    ("/invalid", "GET", 404),
])
def testAPIEndpoints(endpoint, method, expectedStatus):
    pass
```

**After** (separated concerns):
```python
# Test 1: Core endpoints (representative)
@pytest.mark.parametrize("endpoint,expectedStatus", [
    ("/users", 200),          # GET users
    ("/users/1", 200),        # GET specific user
])
def testAPIGetEndpoints(endpoint, expectedStatus):
    pass

# Test 2: HTTP methods (separate focus)
@pytest.mark.parametrize("method,expectedStatus", [
    ("GET", 200),
    ("POST", 201),
    ("PUT", 200),
    ("DELETE", 204),
])
def testAPIHttpMethods(method, expectedStatus):
    pass

# Test 3: Error cases (edge cases)
@pytest.mark.parametrize("endpoint,expectedStatus", [
    ("/invalid", 404),
])
def testAPIErrorCases(endpoint, expectedStatus):
    pass
```

**Benefit**: 6 test cases → 9 cases BUT more focused, better for debugging

### Step 3: Merge Duplicate Scenarios

**Before** (testing same thing multiple ways):
```python
# test_file_1.py
@pytest.mark.parametrize("teamId,budget,spent", [
    ("team_eng", 3000, 1500),
    ("team_ops", 2000, 800),
])
def testTeamBudget(teamId, budget, spent):
    pass

# test_file_2.py (identical logic)
@pytest.mark.parametrize("teamId,budget,spent", [
    ("team_eng", 3000, 1500),
    ("team_ops", 2000, 800),
])
def testBudgetTracking(teamId, budget, spent):
    pass
```

**After** (consolidated):
```python
# Single test covers both scenarios
@pytest.mark.parametrize("teamId,budget,spent", [
    ("team_eng", 3000, 1500),
    ("team_ops", 2000, 800),
])
def testTeamBudgetTracking(teamId, budget, spent):
    # Tests both budget and tracking in one place
    pass
```

**Benefit**: Merge duplicate test logic, eliminate redundancy

---

## Implementation Roadmap

### Phase 2.1: Identify High-Impact Files (1 day)
- [ ] List all 28 test files with parametrized tests
- [ ] Rank by "complexity score" (number of 3+ param decorators)
- [ ] Identify top 5 files for consolidation (50+ decorators each)

**Target files** (estimated by decorator count):
1. test_agent_integration.py (52+ decorators)
2. test_batching.py (45+ decorators)
3. test_chaos_engineering.py (40+ decorators)
4. test_distributed_state.py (38+ decorators)
5. test_e2e_workflows.py (35+ decorators)

### Phase 2.2: Consolidate Top Files (2-3 days)
- [ ] Audit each top file's parametrized tests
- [ ] Apply representative + edge case pattern
- [ ] Split orthogonal concerns where applicable
- [ ] Merge duplicate scenarios
- [ ] Run tests, measure reduction

**Expected reduction per file**:
- test_agent_integration.py: 52 → 30 decorators (42% reduction)
- test_batching.py: 45 → 28 decorators (38% reduction)
- test_chaos_engineering.py: 40 → 26 decorators (35% reduction)
- test_distributed_state.py: 38 → 24 decorators (37% reduction)
- test_e2e_workflows.py: 35 → 22 decorators (37% reduction)

**Total from top 5**: ~75 decorators removed (36% reduction)

### Phase 2.3: Audit Remaining Files (1 day)
- [ ] Apply same patterns to remaining 23 files
- [ ] Target: 30-50 additional decorators removed

**Target from remaining**: ~40 decorators removed (33% reduction)

### Phase 2.4: Verify & Commit (0.5 day)
- [ ] Run full test suite
- [ ] Confirm coverage maintained
- [ ] Document consolidation patterns
- [ ] Commit with detailed message

---

## Quality Assurance

### Testing Strategy
```bash
# Before consolidation
pytest tests/ -v --durations=10

# After consolidation (per file)
pytest tests/test_agent_integration.py -v --durations=10

# Compare:
# - Same assertions
# - Same scenario coverage
# - Reduced test count
# - Same or faster execution
```

### Coverage Verification
- Run `pytest --cov=app` before and after
- Confirm coverage remains >= 85%
- Document any coverage changes

---

## Success Criteria

| Metric | Target | Verification |
|--------|--------|--------------|
| Parametrized test count | Reduce by 40-50% | 121 → 70-80 decorators |
| Test count | Reduce by 150-250 | 2,436 → 2,250-2,300 tests |
| Execution time | ≤5% variance | Still < 10s full suite |
| Coverage | ≥ 85% maintained | `pytest --cov` report |
| Scenarios covered | 100% maintained | Same cases tested |

---

## Documentation Requirements

After Phase 2.2, document:
1. **Consolidation patterns used** (for future tests)
2. **Files modified** (with before/after counts)
3. **Reduction achieved** (per file, total)
4. **Coverage impact** (maintained? improved?)

Example template:
```
# File: test_agent_integration.py
- Decorators: 52 → 30 (42% reduction)
- Tests: 120 → 80 (33% reduction)
- Patterns used:
  * Representative + edge case (8 instances)
  * Split orthogonal concerns (3 instances)
  * Merged duplicates (2 instances)
- Coverage: 87% → 87% (maintained)
```

---

## Risks & Mitigation

| Risk | Mitigation |
|------|-----------|
| Over-consolidating loses coverage | Keep critical edge cases (failure modes) |
| Tests become less readable | Add clear test names and docstrings |
| Hard to revert if issues arise | One file at a time, commit per file |
| Missed consolidation opportunities | Document patterns, apply consistently |
| Tests still take too long | Combine with Phase 1 fixtures for speedup |

---

## Next Steps

1. **Start Phase 2.1** — Identify high-impact files
2. **Pick one file** — Start with test_agent_integration.py
3. **Consolidate** — Apply patterns, run tests
4. **Document** — Record consolidation patterns
5. **Iterate** — Move to next file

**Estimated completion**: 7-10 days (3 days intensive work + testing)

---

## Success Metrics (Post-Phase 2)

**Expected Results**:
- ✅ 121 → 70-80 parametrized decorators (37% reduction)
- ✅ 2,436 → 2,250-2,300 tests (5-8% reduction)
- ✅ Faster test execution (consolidated mocks + fewer tests)
- ✅ Same coverage maintained (85%+)
- ✅ Clearer, more focused tests
- ✅ Easier maintenance (less duplication)

---

**Phase 2 Status**: Strategy document created, ready to begin consolidation

**Next Action**: Run Phase 2.1 analysis to identify top files and specific consolidation opportunities
