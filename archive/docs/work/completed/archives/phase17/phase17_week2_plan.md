# Phase 17 Week 2: Implementation Plan (9/1-9/7)

**Focus**: Initiatives 1.1 (Routing) & 1.2 (Batch)  
**Effort**: 44-54 hours (20-24h per initiative)  
**Status**: 🚀 READY TO START

---

## Week 2 Overview

| Day | Initiative | Task | Effort | Owner |
|-----|-----------|------|--------|-------|
| **Mon 9/1** | 1.1 | Analyze routing engine, implement O(1) lookup | 6h | Performance Lead |
| **Tue 9/2** | 1.1 | Add caching, reduce allocations | 6h | Performance Lead |
| **Wed 9/3** | 1.2 | Analyze batch pipeline, implement pre-allocation | 6h | Batch Specialist |
| **Wed 9/3** | 1.2 | Add pipelining, reduce sync overhead | 6h | Batch Specialist |
| **Thu 9/4** | 1.1 | Validation: run tests, measure latency | 6h | QA/Performance |
| **Fri 9/5** | 1.2 | Validation: run tests, measure throughput | 6h | QA/Performance |

---

## Implementation Details

### Initiative 1.1: Routing Engine Latency (Mon-Tue)

**Monday 9/1 - Keyword Lookup Optimization**

Files to modify:
- `app/core/routing.py` (main routing logic)
- `app/core/agents.py` (agent definition)

Changes:
1. Create keyword→team mapping dict (O(1) lookup)
2. Replace current linear search with dict.get()
3. Add inline comments explaining optimization
4. Run quick sanity test

Code skeleton:
```python
# In app/core/routing.py

# BEFORE: O(n) keyword matching
def route_task(task, keywords):
    for keyword in keywords:
        if keyword in task_keywords:
            return team_for_keyword[keyword]
    return default_team

# AFTER: O(1) hash lookup
KEYWORD_TO_TEAM = {
    "budget": "finance_team",
    "latency": "performance_team",
    "patterns": "research_team",
    "cost": "finance_team",
    "performance": "performance_team",
    "metrics": "analytics_team"
}

def route_task(task, keywords):
    # O(1) lookup by primary keyword
    primary_keyword = keywords[0]
    return KEYWORD_TO_TEAM.get(primary_keyword, "default_team")
```

**Tuesday 9/2 - Caching & Allocation Reduction**

Files to modify:
- `app/core/routing.py` (add cache decorator)
- `app/lib/cache.py` (create caching utility if needed)

Changes:
1. Add @lru_cache decorator to routing function
2. Pre-allocate common RoutingResult objects
3. Reuse buffers (no new allocations per request)
4. Add comments on performance implications

Code skeleton:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def route_task_cached(task_type: str, priority: int) -> str:
    # Cached routing decision
    return KEYWORD_TO_TEAM.get(task_type, "default_team")

# Pre-allocate common results
COMMON_RESULTS = {
    "routing_decision": RoutingResult(decision="route", confidence=1.0),
    "default_route": RoutingResult(decision="default", confidence=0.8),
}
```

---

### Initiative 1.2: Batch Processing Efficiency (Wed-Thu)

**Wednesday 9/3 - Pipeline Parallelization**

Files to modify:
- `app/core/batch_processor.py` (batch assembly, formation, processing)
- `app/lib/thread_pool.py` (create pool utility if needed)

Changes:
1. Pre-allocate 10 batch buffers at startup
2. Reuse queue objects (clear instead of recreate)
3. Implement pipelined execution with thread pool
4. Add comments explaining parallelization

Code skeleton:
```python
# In app/core/batch_processor.py

class BatchProcessor:
    def __init__(self):
        # Pre-allocate buffers
        self.batch_buffers = [BatchBuffer() for _ in range(10)]
        self.buffer_queue = queue.Queue(maxsize=10)
        
        # Thread pool for pipelined execution
        self.executor = ThreadPoolExecutor(max_workers=3)
    
    async def process_pipeline(self, tasks):
        # Stage 1: Assembly (parallel)
        future1 = self.executor.submit(self.assemble, tasks)
        
        # Stage 2: Batching (parallel with stage 1's output)
        batch = await future1
        future2 = self.executor.submit(self.form_batches, batch)
        
        # Stage 3: Processing (parallel with stage 2)
        batch_result = await future2
        future3 = self.executor.submit(self.process, batch_result)
        
        # Stage 4: Output
        results = await future3
        return self.output(results)
```

**Thursday 9/3 - Sync Overhead Reduction**

Files to modify:
- `app/core/batch_processor.py` (reduce locks)
- `app/lib/queue.py` (optimize synchronization)

Changes:
1. Use lock-free queue where possible
2. Replace task-level locks with batch-level locks
3. Reduce condition variable usage
4. Add comments on synchronization strategy

---

## Testing Strategy

### Unit Tests (existing should pass)
```bash
pytest tests/test_performance_optimization_and_batching.py::TestRoutingEngineParametrized -v
pytest tests/test_performance_optimization_and_batching.py::TestLoadTestIntegrationParametrized -v
```

### Performance Baselines
Before implementation:
```bash
python -m pytest [tests] --benchmark-only
# Capture p50, p95, p99 latencies
# Save to baseline_before.json
```

After implementation:
```bash
python -m pytest [tests] --benchmark-only
# Capture new latencies
# Save to baseline_after.json
# Compare: (before - after) / before × 100%
```

### Regression Tests
```bash
pytest tests/ -k "not slow" --cov=app
# Target: ≥85% coverage maintained
# Target: 0 test regressions
```

---

## Validation Checklist

### Mon-Tue (1.1 Routing)
- [ ] Keyword lookup changed from O(n) to O(1)
- [ ] Cache decorator (@lru_cache) added
- [ ] Pre-allocated RoutingResult objects
- [ ] Inline comments explaining optimizations
- [ ] All 10 routing tests still passing
- [ ] p95 latency reduced by ≥20%

### Wed-Thu (1.2 Batch)
- [ ] Buffer pre-allocation implemented
- [ ] Pipelined execution added
- [ ] Thread pool coordination working
- [ ] Lock contention reduced
- [ ] Inline comments on parallelization
- [ ] All 10 batch tests still passing
- [ ] Throughput increased by ≥25%

### Thu-Fri (Validation)
- [ ] Performance benchmarks captured
- [ ] Before/after comparison done
- [ ] No regressions in other tests
- [ ] Code passes linting (black, ruff, mypy)
- [ ] AUDIT.md updated with results
- [ ] Both initiatives commited to main

---

## Code Quality Gates

Before committing each optimization:
```bash
# Format
black app/core/routing.py app/core/batch_processor.py

# Lint
ruff check app/core/routing.py app/core/batch_processor.py

# Type check
mypy app/core/routing.py app/core/batch_processor.py

# Test
pytest tests/test_performance_optimization_and_batching.py -v

# Coverage
pytest tests/ --cov=app --cov-report=term-missing
```

---

## Success Criteria

| Criterion | Target | Acceptance |
|-----------|--------|-----------|
| 1.1 Latency reduction | ≥20% | p95: [before] → [after] |
| 1.2 Throughput increase | ≥25% | ops/sec: [before] → [after] |
| Test regressions | 0 | All tests passing |
| Code quality | Pass all gates | Black, ruff, mypy clean |
| Documentation | Complete | Inline comments, AUDIT.md |

---

## Commit Strategy

**Commit 1 (Mon-Tue 9/2 evening)**:
```
feat(routing): optimize keyword matching and add decision caching

- Replace O(n) linear search with O(1) hash lookup (keyword→team)
- Add @lru_cache on routing decision (1000-entry cache)
- Pre-allocate common RoutingResult objects (reduce allocations)
- Expected: 20-30% latency reduction at p95/p99

Baseline: TestRoutingEngineParametrized 10/10 passing
Target: ≥20% latency reduction across all keywords
```

**Commit 2 (Wed-Thu 9/3-9/4 evening)**:
```
feat(batch): parallelize pipeline and optimize throughput

- Pre-allocate batch buffers (10 reusable buffers)
- Implement pipelined execution with ThreadPoolExecutor
- Reduce inter-stage synchronization overhead
- Use batch-level locks instead of task-level
- Expected: 25-40% throughput improvement

Baseline: TestLoadTestIntegrationParametrized 10/10 passing
Target: ≥25% throughput increase across all load levels
```

---

## References

- **Strategy 1.1**: `docs/work/current/phase17_strategy_1_1_routing.md`
- **Strategy 1.2**: `docs/work/current/phase17_strategy_1_2_batch.md`
- **Baseline Data**: `phase17_baseline.json`
- **Task Breakdown**: `docs/work/planned/phase-17-task-breakdown.md`

---

**Status**: READY FOR IMPLEMENTATION  
**Last Updated**: 2026-08-27
