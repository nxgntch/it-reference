# Phase 2.3: Async Optimization Plan

**Status**: Ready for Implementation  
**Target Duration**: 2-3 weeks  
**Success Metric**: 15%+ latency reduction under concurrent load  

---

## Executive Summary

Phase 2.3 optimizes async patterns and enables concurrent execution across the agent layer. Current implementation processes one agent at a time and has sequential dependency checks. This phase parallelizes independent operations and makes batch processing fully async for 15-20% latency improvement.

---

## Current Bottlenecks Analysis

### Orchestrator.invoke() - Sequential Execution

**Current Flow:**
```
Budget Check → Idempotency Check → Circuit Breaker → Cache Check → Cost Estimate → Agent Execute
(sequential, blocking on each step)
```

**Issue**: Independent checks execute sequentially. Budget, circuit breaker, and cache checks can run in parallel.

**Impact**: ~20-30ms overhead per invocation (3x 10ms checks running one-by-one)

### Batch Processor - Synchronous

**Current**: All batch methods are blocking (addTaskToBatch, processBatch)
- No concurrent task submission
- Batch processing blocks on individual task completion
- No parallel batch execution

**Impact**: Large batch sizes cause cumulative latency (100 tasks = 100ms+ delay)

### Database Connection Reuse

**Current**: Each async operation gets fresh connection from pool
- Pool is good (20 base + 10 overflow)
- But no connection batching/pipelining
- Related queries don't share connections

**Impact**: Connection pool churn under high load (approaching max_overflow)

### LLM API Calls - Individual Requests

**Current**: executeAgent() makes single LLM call
- No batching of similar requests
- No request pipelining
- Concurrent invocations don't share connection state

**Impact**: LLM API overhead dominates latency for high-concurrency scenarios

---

## Optimization Strategy

### 1. Parallelize Orchestrator Checks (Week 1)

**Goal**: Reduce pre-execution overhead from ~30ms to ~10ms

**Changes**:

```python
# BEFORE: Sequential
budget_ok = await budgetChecker.canSpend(teamId)
idempotent_result = idempotencyTracker.getResult(requestId)
breaker_ok = circuitBreaker.canExecute(agentId)
cache_hit = responseCache.get(task)

# AFTER: Parallel
[budget_ok, idempotent_result, breaker_ok, cache_hit] = await asyncio.gather(
    budgetChecker.canSpend(teamId),
    idempotencyTracker.getResult(requestId),
    circuitBreaker.canExecute(agentId),
    responseCache.get(task)
)
```

**Implementation**:
- Wrap independent checks in async tasks
- Use `asyncio.gather()` for parallel execution
- Short-circuit on failures (idempotent result found, cache hit, etc.)

**Expected Impact**: 20-30ms → 10-15ms per invocation

---

### 2. Make Batch Processor Async (Week 1-2)

**Goal**: Enable concurrent batch submission and processing

**Changes**:

```python
# Add async methods
class BatchProcessor:
    async def addTaskToBatchAsync(self, task: BatchTask) -> Tuple[str, bool]:
        """Async task batching with concurrent queue support."""
        
    async def processBatchAsync(self, batchId: str) -> Dict[str, Any]:
        """Async batch processing with concurrent task execution."""
        
    async def processBatchesAsync(self, batchIds: List[str]) -> List[Dict]:
        """Process multiple batches concurrently."""
```

**Implementation**:
- Add `asyncio.Queue` for pending tasks
- Process batches concurrently with `asyncio.gather()`
- Implement async task grouping with timeout

**Expected Impact**: 100+ task batch from 100ms+ → 30-40ms

---

### 3. Implement Connection Pooling for Batch Queries (Week 2)

**Goal**: Reduce connection pool churn during high concurrency

**Changes**:

```python
class QueryBatcher:
    """Batch related database queries into single connection."""
    
    async def executeBatch(self, queries: List[str]) -> List[Any]:
        """Execute multiple queries in single connection session."""
        # All queries reuse same connection
        # Reduces connection pool contention
        
    async def executeWithConnection(self, operations: List[Callable]) -> List[Any]:
        """Execute multiple operations sharing single session."""
```

**Implementation**:
- Detect related operations (same table, same team, etc.)
- Batch into single session
- Reduce connection pool checkout frequency

**Expected Impact**: Max pool utilization 80%+ → 60-70%

---

### 4. Add Concurrent Agent Invocation Support (Week 2-3)

**Goal**: Support parallel agent execution

**Changes**:

```python
class Orchestrator:
    async def invokeMultiple(
        self, 
        tasks: List[Dict[str, str]]  # [{agentId, task, teamId}, ...]
    ) -> List[Dict[str, Any]]:
        """Invoke multiple agents concurrently."""
        # tasks = [
        #     {"agentId": "architect", "task": "...", "teamId": "eng"},
        #     {"agentId": "ceo", "task": "...", "teamId": "exec"}
        # ]
        
        # Execute all concurrently with shared resource mgmt
        results = await asyncio.gather(
            *[self.invoke(t["agentId"], t["task"], t["teamId"]) 
              for t in tasks],
            return_exceptions=True
        )
```

**Implementation**:
- Accept list of tasks
- Execute with `asyncio.gather()`
- Shared budget tracking across concurrent invocations
- Shared circuit breaker state

**Expected Impact**: 5 sequential tasks (500ms) → 5 concurrent tasks (120-150ms)

---

### 5. Implement LLM Call Batching (Week 3)

**Goal**: Batch similar LLM requests

**Changes**:

```python
class LLMBatcher:
    """Batch similar LLM requests for efficiency."""
    
    async def batchCall(
        self, 
        prompts: List[str], 
        model: str
    ) -> List[str]:
        """Execute batch of LLM calls."""
        # Groups similar prompts
        # Sends to LLM API with batch optimization
```

**Implementation**:
- Detect similar prompts (complexity, length, agent)
- Group into batch request
- Use Anthropic batch API if available
- Fall back to concurrent individual calls

**Expected Impact**: Varies by workload (10-20% on batch-heavy)

---

## Implementation Schedule

| Week | Task | Deliverable |
|------|------|-------------|
| **1** | Parallelize orchestrator checks + async batch processor | Updated orchestrator.py, batchProcessor.py with async methods |
| **2** | Connection batching + concurrent invocation support | QueryBatcher class, orchestrator.invokeMultiple() |
| **3** | LLM call batching + load testing | LLMBatcher class, performance benchmarks |

---

## Success Criteria

### Performance Metrics

- [ ] Agent invocation latency reduced by ≥15% under concurrent load (p95 latency)
- [ ] Connection pool utilization stays <70% under 50 concurrent invocations
- [ ] Batch processing latency: 100 tasks completed in <50ms
- [ ] No deadlocks or race conditions under concurrent execution
- [ ] Memory usage stable (no leaks under sustained concurrent load)

### Code Quality

- [ ] All new async methods have docstrings explaining concurrency model
- [ ] Test coverage for concurrent scenarios (5+ concurrent invocations)
- [ ] Load test with 50+ concurrent tasks demonstrates improvement
- [ ] No blocking operations in async code paths
- [ ] All tests pass (existing + new concurrency tests)

### Validation

```bash
# Load test: 50 concurrent agent invocations
pytest tests/test_concurrent_orchestrator.py -v

# Latency baseline
pytest tests/test_performance.py --benchmark

# Connection pool under load
python scripts/perf/pool_stress_test.py --concurrent=50 --duration=60s
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|-----------|
| Race conditions in shared state | Medium | High | Comprehensive concurrent testing, use asyncio primitives |
| Connection pool starvation | Low | High | Monitor pool metrics, set conservative overflow limits |
| Deadlock in circular dependencies | Low | High | Code review async lock acquisition order |
| Performance regression | Low | Medium | Baseline all metrics before + after |

---

## Rollback Plan

If Phase 2.3 introduces regressions:

1. **Revert async changes**: Restore synchronous batch processor
2. **Keep pooling**: Connection pooling improvements are safe to keep
3. **Disable concurrent invocation**: Fallback to single-agent invoke()
4. **Root cause analysis**: Identify specific async pattern causing issue

```bash
git revert <async-commits>  # Revert orchestrator async changes
git keep <pooling-commits>   # Keep connection pool improvements
```

---

## Dependencies

- Phase 2.1 (Connection Pooling) - ✅ Complete
- Phase 2.2 (Agent Config Caching) - ✅ Complete
- Phase 3 Security (OWASP) - Not blocking (can parallelize)

---

## Files to Modify

1. `app/core/orchestrator.py` - Parallelize checks, add invokeMultiple()
2. `app/core/batchProcessor.py` - Add async methods
3. `app/db/session.py` - Add QueryBatcher for connection batching
4. `tests/test_concurrent_orchestrator.py` - New: concurrent testing
5. `tests/test_batch_async.py` - New: async batch testing
6. `scripts/perf/pool_stress_test.py` - New: connection pool stress test

---

## Next Steps

1. **Approve Plan** - Get team sign-off on scope and timeline
2. **Week 1 Kickoff** - Start with orchestrator parallelization
3. **Daily Standups** - Quick sync on blocker resolution
4. **Weekly Reviews** - Performance metrics, load test results
5. **Phase Completion** - All success criteria met + documentation updated

---

## References

- **Phase 2 Overview**: Integration (Agent Layer) optimization
- **Phase 2.1**: Database connection pooling (complete)
- **Phase 2.2**: Agent configuration caching (complete)
- **Phase 3**: Security hardening (next)
- **Performance Goals**: Latency baseline in AUDIT.md

