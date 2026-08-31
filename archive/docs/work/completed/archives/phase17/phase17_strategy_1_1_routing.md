# Phase 17 Initiative 1.1: Routing Engine Latency Optimization

**Goal**: Reduce routing decision latency by 20-30%  
**Baseline**: TestRoutingEngineParametrized passing (10/10 tests)  
**Target**: ≥20% latency reduction across all 6 task keywords  
**Week**: 2 (9/1-9/7)  
**Effort**: 20-24 hours

---

## Current Baseline Status

**Test Results**: 10/10 PASSING ✅
- `designTask` routing: PASS
- `analysisTask` routing: PASS
- `coordinationTask` routing: PASS
- `deploymentTask` routing: PASS
- Keyword routing (budget, latency, patterns, cost, performance, metrics): All PASS

**Baseline Metrics to Capture**:
- Current p50 latency per task type (TBD)
- Current p95 latency per task type (TBD)
- Current p99 latency per task type (TBD)
- Average latency per keyword (TBD)

---

## Optimization Strategy

### Phase 1.1.1: Analyze Current Implementation

**Hot Path Identification**:
1. Profile routing engine with TestRoutingEngineParametrized data
2. Identify keyword matching algorithm (likely linear search O(n))
3. Measure CPU/memory usage per routing decision
4. Identify object creation overhead

**Method**:
```python
# In Week 2, add profiling decorators to routing engine
import cProfile
import pstats

@profile_routing_decision
def routeTask(task: Task, keywords: List[str]) -> Agent:
    # Current implementation
    pass
```

**Target Latency Distribution**:
- p50: Current baseline → baseline (no degradation expected)
- p95: Reduce by 20%
- p99: Reduce by 25%

---

### Phase 1.1.2: Optimization Implementation

**Optimization 1: Replace Linear Search with O(1) Lookup**

*Current (likely)*:
```python
# O(n) keyword matching
for keyword in keywords:
    if keyword in task_keywords:
        return team_for_keyword[keyword]
```

*Target*:
```python
# O(1) hash lookup
keyword_map = {
    "budget": "finance_team",
    "latency": "performance_team",
    "patterns": "research_team",
    "cost": "finance_team",
    "performance": "performance_team",
    "metrics": "analytics_team"
}
return keyword_map.get(keywords[0], default_team)
```

**Expected Gain**: 50-70% reduction for keyword matching

---

**Optimization 2: Cache Routing Decisions**

*Approach*:
- Cache routing decisions by task fingerprint
- Use LRU cache with 1000-entry limit
- Invalidate on keyword/team config changes

*Implementation*:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def routeTaskCached(task_type: str, priority: int) -> str:
    # Routing logic
    return agent_id
```

**Expected Gain**: 30-40% for repeated task patterns

---

**Optimization 3: Reduce Object Creation**

*Current (likely)*:
- Creates new RoutingResult objects for each decision
- Creates temporary keyword lists
- Allocates new Team objects

*Target*:
- Pre-allocate common result objects
- Reuse keyword list buffers
- Reference existing Team objects (no allocation)

**Expected Gain**: 10-20% reduction in allocation overhead

---

### Phase 1.1.3: Validation & Benchmarking

**Re-run Tests**:
```bash
pytest tests/test_performance_optimization_and_batching.py::TestRoutingEngineParametrized -v --durations=10
```

**Measure Results**:
- p50 latency (should be stable)
- p95 latency (target: -20%)
- p99 latency (target: -25%)
- All 6 keyword types (budget, latency, patterns, cost, performance, metrics)

**Success Criteria**:
- [ ] All 10 tests still passing (no regressions)
- [ ] p95 latency reduced by ≥20%
- [ ] p99 latency reduced by ≥20%
- [ ] Routing accuracy unchanged (decisions still correct)
- [ ] No new memory leaks

**Fallback Strategy**:
If target not met:
1. Profile hottest 10% of operations
2. Focus optimization on that slice
3. Consider async routing for parallelization (Week 3+)

---

## Implementation Checklist

**Week 2 Monday-Tuesday (9/1-9/3)**: Implementation
- [ ] Analyze current routing implementation
- [ ] Implement O(1) keyword lookup (Opt 1)
- [ ] Add routing decision cache (Opt 2)
- [ ] Reduce object allocation (Opt 3)
- [ ] Write inline comments explaining optimizations

**Week 2 Thursday-Friday (9/4-9/5)**: Validation
- [ ] Run TestRoutingEngineParametrized with profiling
- [ ] Measure p50/p95/p99 latencies
- [ ] Verify no regressions in accuracy
- [ ] Update benchmark data
- [ ] Commit optimized code

---

## Code Quality Requirements

- [ ] All changes documented with inline comments
- [ ] No deprecated methods used
- [ ] Variable names follow camelCase convention
- [ ] Functions ≤50 lines
- [ ] Test coverage maintained (≥85%)
- [ ] Follows `.claude/rules/coding-style.md`

---

## Metrics to Track

After implementation, update AUDIT.md:

```
Initiative 1.1 Results:
- Routing latency p95: [before] ms → [after] ms ([percentage]% reduction)
- Routing latency p99: [before] ms → [after] ms ([percentage]% reduction)
- Test pass rate: 10/10 (100%)
- Regressions: 0
```

---

## References

- **Baseline**: `phase17_baseline.json` → routing.tests_passed = 10/10
- **Test Class**: `TestRoutingEngineParametrized` (10 tests, 6 keywords)
- **Phase 16 Archive**: `docs/work/completed/phase-16-archive/README.md`
- **Task Breakdown**: `docs/work/planned/phase-17-task-breakdown.md` § 1.1

---

**Status**: READY FOR WEEK 2 IMPLEMENTATION  
**Last Updated**: 2026-08-27
