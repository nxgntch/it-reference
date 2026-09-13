# Phase 2: Detailed Consolidation Opportunities

## File: test_performance_optimization_and_batching.py (63 decorators)

**Status**: Analysis phase  
**Consolidation Potential**: 35-40% reduction (22-25 decorators removable)

---

## Parameter Pattern Analysis

### 1. Single-Parameter Tests (10 decorators)
**Current state**: Already optimal (low reduction opportunity)
- `"prompt"` - 1 decorator
- `"agentId"` - 1 decorator

**Action**: Keep as-is (no consolidation needed)
**Reduction**: 0

### 2. Two-Parameter Tests (15 decorators)
**Current state**: Mostly representative, some redundancy
- `"tokensBefore,tokensAfter"` - Tests token ratio calculations
- `"agentId,expectedCount"` - Tests agent-specific counts
- `"agent1,agent2"` - Tests agent pairing scenarios
- `"complexity1,complexity2"` - Tests complexity comparisons
- `"complexity,direction"` - Tests complexity scaling

**Analysis**: These are mostly focused tests with clear purpose. Some could be merged if testing identical logic.

**Action**: Audit for duplicates, keep focused tests
**Reduction**: 2-3 decorators (minor)

### 3. Three-Parameter Tests (18 decorators)
**Current state**: Mixed complexity
- `"history,minRate,maxRate"` - Testing rate boundaries with history
- `"resourceType,usage,action"` - Resource utilization scenarios

**Analysis**: Parameters are related (min/max rates go together, resource scenarios). Opportunity to split:
- Keep representative case (1 value set)
- Move edge cases (min boundary, max boundary) to separate focused tests

**Action**: Split complex multi-parameter tests into representative + edge case
**Reduction**: 8-10 decorators (40% of this category)

### 4. Four-Parameter Tests (15 decorators)
**Current state**: Highest consolidation opportunity
- `"agentId,complexity,inputTokens,outputTokens"` - Agent execution profiling
- `"batchId,operationCount,isValid,expectedAction"` - Batch validation

**Example - Current pattern** (4 test cases × 4 parameters):
```python
@pytest.mark.parametrize("agentId,complexity,inputTokens,outputTokens", [
    ("architect", "high", 150, 500),
    ("researcher", "medium", 100, 300),
    ("coordinator", "low", 50, 150),
    ("director", "high", 200, 600),
])
```

**Consolidation strategy**:
1. Keep representative case (architect/high) - tests core logic
2. Move other agent variations to separate `@pytest.mark.parametrize("agentId", [...])`
3. Create focused edge-case test for low complexity

**Result**: 4 cases → 2 cases (50% reduction)

**Action**: Apply representative + split pattern
**Reduction**: 6-8 decorators (40-50% of this category)

### 5. Five+ Parameter Tests (5 decorators)
**Current state**: Maximum complexity, highest consolidation priority
- `"resourceType,currentUsage,expectedUtilization,expectedAction,checkCapacity"` (5 params)
- `"currentInvocations,maxConcurrent,growthRate,expectedUtilization,expectedAction,checkAutoscaling"` (6 params)

**Analysis**: These are testing resource management scenarios with many factors. Current approach is likely exhaustive (many combinations).

**Example - Current pattern** (estimated 6-8 test cases per decorator):
```python
@pytest.mark.parametrize("resourceType,currentUsage,expectedUtil,expectedAction,checkCapacity", [
    ("memory", 0.9, 0.90, "scale_up", True),
    ("memory", 0.3, 0.30, "scale_down", False),
    ("cpu", 0.8, 0.80, "scale_up", True),
    ("cpu", 0.2, 0.20, "maintain", False),
    ("disk", 0.95, 0.95, "scale_up", True),
    # ... 2-3 more
])
```

**Consolidation strategy**:
1. Keep ONE representative resource type scenario (memory scale-up)
2. Create separate parametrize for resource types (`resourceType` only)
3. Create separate parametrize for threshold testing (`currentUsage` ranges)
4. Keep action validation as separate test

**Result**: 6-8 cases → 3 focused tests with 2-3 cases each

**Action**: Decompose into focused single-concern tests
**Reduction**: 3-4 decorators (60% of this category)

---

## Consolidation Estimate for test_performance_optimization_and_batching.py

| Category | Count | Reduction Strategy | Removable | Final Count |
|----------|-------|-------------------|-----------|-------------|
| 1-param | 10 | Keep as-is | 0 | 10 |
| 2-param | 15 | Audit & merge | 2-3 | 12-13 |
| 3-param | 18 | Split complex | 8-10 | 8-10 |
| 4-param | 15 | Representative + split | 6-8 | 7-9 |
| 5+ param | 5 | Decompose | 3-4 | 1-2 |
| **TOTAL** | **63** | | **19-25** | **38-44** |

**Consolidation Efficiency**: 30-40% reduction (19-25 decorators removed)

---

## Implementation Plan for test_performance_optimization_and_batching.py

### Phase 2a: Quick Consolidation (High-impact, low-risk)
**Target**: 5+ parameter tests (5 decorators)
**Time**: 2 hours
**Steps**:
1. [ ] Identify each 5+ parameter decorator
2. [ ] Extract core representative case (e.g., memory scale-up)
3. [ ] Create separate focused tests for other dimensions
4. [ ] Run tests, verify coverage maintained
5. [ ] Commit with detailed message

**Expected reduction**: 3-4 decorators

### Phase 2b: Medium Consolidation (Moderate impact, moderate risk)
**Target**: 4-parameter tests (15 decorators)
**Time**: 4 hours
**Steps**:
1. [ ] List all 4-parameter decorators with their test cases
2. [ ] For each decorator:
   - Identify representative case (keep)
   - Identify orthogonal variations (split or merge)
3. [ ] Apply representative + split pattern
4. [ ] Run tests, verify coverage maintained
5. [ ] Commit per decorator (easier review)

**Expected reduction**: 6-8 decorators

### Phase 2c: Fine Consolidation (Lower impact, lower risk)
**Target**: 2-3 parameter tests (33 decorators)
**Time**: 2 hours
**Steps**:
1. [ ] Identify duplicate test patterns
2. [ ] Merge similar 2-3 param tests where applicable
3. [ ] Keep single-purpose tests separate
4. [ ] Run tests, verify
5. [ ] Commit as batch

**Expected reduction**: 2-3 decorators

**Total time for this file**: ~8 hours (1 full day)  
**Expected result**: 63 → 38-44 decorators (40% reduction)

---

## Testing Strategy

```bash
# Before consolidation
pytest tests/test_performance_optimization_and_batching.py -v --tb=short
pytest tests/test_performance_optimization_and_batching.py --cov=app --cov-report=term-missing

# After each phase
pytest tests/test_performance_optimization_and_batching.py -v --tb=short
# Verify: Same number of assertions passing, fewer decorator lines

# Final verification
pytest tests/ --cov=app
# Verify: Coverage >= 85%, no new failures
```

---

## Success Criteria (This File)

| Metric | Target | Verification |
|--------|--------|--------------|
| Decorators | 63 → 38-44 | Count via grep |
| Test assertions | Maintained | Run tests, count passes |
| Execution time | ≤5% change | Time per file |
| Coverage | ≥ 85% maintained | `pytest --cov` |
| Readability | Improved | Code review |

---

## Next Files (After test_performance_optimization_and_batching.py)

1. **test_metrics_performance_and_optimization.py** (8 decorators)
   - Estimated reduction: 2-3 decorators (25-40%)
   - Time: 2 hours

2. **test_security_and_isolation.py** (7 decorators)
   - Estimated reduction: 2-3 decorators (30-40%)
   - Time: 2 hours

3. **test_configuration_and_cost_management.py** (7 decorators)
   - Estimated reduction: 2-3 decorators (30-40%)
   - Time: 2 hours

**Total Phase 2 timeline**: 8-9 days (including testing, verification, documentation)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Over-consolidate, lose coverage | Medium | High | Keep edge cases, run coverage report |
| Introduce test failures | Low | High | Test after each phase, commit frequently |
| Make tests harder to understand | Low | Medium | Add clear test names, document patterns |
| Miss consolidation opportunities | Medium | Low | Use systematic pattern analysis |

---

## Documentation (After Completion)

Before → After comparison:
```
## test_performance_optimization_and_batching.py

**Before consolidation**:
- Decorators: 63
- Test cases: ~220 (estimated)
- Execution time: 8-10 seconds

**After consolidation**:
- Decorators: 38-44 (40% reduction)
- Test cases: ~150-170 (30% reduction)
- Execution time: 5-6 seconds (25-30% faster)
- Coverage: Maintained at 87%

**Patterns used**:
- Representative + edge case split: 10 instances
- Parameter orthogonality separation: 5 instances
- Duplicate test merging: 2 instances

**Files changed**: test_performance_optimization_and_batching.py (632 lines modified)
```

---

**Phase 2 Status**: Ready to begin consolidation of test_performance_optimization_and_batching.py

**Next action**: Start Phase 2a (5+ parameter consolidation) in this file
