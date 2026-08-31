# Phase 17 Week 3: Implementation Plan (9/8-9/14)

**Focus**: Finalize Initiatives 1.1 & 1.2, Begin 1.3 (Token) & 1.4 (Concurrency)  
**Effort**: 48-56 hours (12-14h per initiative)  
**Status**: 🚀 READY TO START

---

## Week 3 Overview

| Day | Initiative | Task | Effort | Owner |
|-----|-----------|------|--------|-------|
| **Mon 9/8** | 1.1 | Capture routing latency baselines & verify optimizations | 4h | Performance Lead |
| **Tue 9/9** | 1.2 | Capture batch throughput baselines & verify optimizations | 4h | Batch Specialist |
| **Wed 9/10** | 1.3 | Analyze token patterns, identify high-usage areas | 5h | Cost Analyst |
| **Wed 9/10** | 1.4 | Establish concurrency baseline metrics | 4h | Scalability Lead |
| **Thu 9/11** | 1.3 | Implement compression algorithm optimizations | 6h | Token Optimizer |
| **Fri 9/12** | 1.4 | Run stress tests, identify bottlenecks | 6h | QA/Scalability |
| **Fri 9/12** | 1.3 | Validation: token reduction achieved | 3h | Cost Analyst |

---

## Implementation Details

### Initiative 1.1: Finalize Routing Optimization (Mon)

**Monday 9/8 - Baseline Capture & Validation**

Status check from Week 2:
- ✅ O(1) keyword lookup implemented
- ✅ LRU cache decorator added
- ✅ Pre-allocated RoutingResult objects
- ✅ Tests passing (10/10)

Tasks:
1. Run benchmarks to capture latency improvements
   ```bash
   pytest tests/test_performance_optimization_and_batching.py::TestRoutingEngineParametrized \
     --benchmark-only -v
   # Capture: p50, p95, p99 latencies
   # Save baseline_after_1_1.json
   ```

2. Compare before/after metrics
   - Expected: ≥20% latency reduction at p95
   - Actual: [to be captured]
   - If < 20%: Identify additional optimization opportunities

3. Verify no regressions in other routing tests
   ```bash
   pytest tests/ -k "routing" --cov=app/core/routing
   # Target: 100% of routing tests passing
   ```

4. Document results in AUDIT.md

**Success Criteria**:
- [ ] Latency baseline captured (before Week 2 work)
- [ ] Latency baseline captured (after Week 2 work)
- [ ] ≥20% reduction verified at p95
- [ ] All routing tests passing (0 regressions)
- [ ] Results documented

---

### Initiative 1.2: Finalize Batch Optimization (Tue)

**Tuesday 9/9 - Baseline Capture & Validation**

Status check from Week 2:
- ✅ Buffer pre-allocation implemented
- ✅ Pipelined execution added
- ✅ Thread pool coordination working
- ✅ Tests passing (10/10)

Tasks:
1. Run load test benchmarks to capture throughput improvements
   ```bash
   pytest tests/test_performance_optimization_and_batching.py::TestLoadTestIntegrationParametrized \
     --benchmark-only -v
   # Capture: ops/sec at different load levels (light/medium/heavy/extreme)
   # Save baseline_after_1_2.json
   ```

2. Compare before/after metrics
   - Expected: ≥25% throughput increase
   - Actual: [to be captured]
   - If < 25%: Investigate synchronization overhead

3. Verify memory efficiency improvements
   - Before: memory allocations per batch
   - After: reduced allocations via pre-allocation
   - Document reduction in garbage collection pressure

4. Verify no regressions
   ```bash
   pytest tests/ -k "batch" --cov=app/core/batch_processor
   # Target: 100% of batch tests passing
   ```

5. Document results in AUDIT.md

**Success Criteria**:
- [ ] Throughput baseline captured (before Week 2 work)
- [ ] Throughput baseline captured (after Week 2 work)
- [ ] ≥25% throughput increase verified
- [ ] All batch tests passing (0 regressions)
- [ ] Memory efficiency improvements documented
- [ ] Results documented

---

### Initiative 1.3: Token Optimization Phase 1 (Wed-Thu)

**Wednesday 9/10 - Token Usage Analysis**

Files to analyze:
- `app/core/token_optimizer.py` (compression algorithms)
- `app/lib/prompt_templates.py` (prompt definitions)
- Test results from `TestTokenOptimizerIntegrationParametrized`

Tasks:
1. Capture current token usage baseline
   ```bash
   pytest tests/test_performance_optimization_and_batching.py::TestTokenOptimizerIntegrationParametrized \
     --benchmark-only -v -s
   # Capture detailed token counts by:
   # - Agent type (Architect, Researcher, Coordinator)
   # - Prompt style (Verbose, Moderate, Concise)
   # - Prompt length (short, medium, long)
   # Save baseline_token_usage.json
   ```

2. Analyze token consumption patterns
   ```python
   # From test results, identify:
   # 1. Which agent types use most tokens
   # 2. Which prompt styles are most verbose
   # 3. Which prompt lengths exceed expected ranges
   # 4. Redundancy in instructions/examples
   
   # Expected findings:
   # - Verbose architect prompts: 250-300 tokens (reduce to 180-200)
   # - Coordinator templates: 120-150 tokens (reduce to 90-110)
   # - Redundant examples in few-shot: 30-40 tokens per template
   ```

3. Identify optimization targets (ranked by impact)
   - Target 1: Architect verbose prompts (-30 tokens)
   - Target 2: Coordinator instructions (-20 tokens)
   - Target 3: Example redundancy (-15 tokens)

4. Create optimization task list
   ```
   - Remove 1-2 redundant examples from few-shot prompts
   - Consolidate repeated instructions
   - Remove unused context sections
   - Shorten instruction descriptions
   ```

**Thursday 9/11 - Token Optimization Implementation**

Files to modify:
- `app/lib/prompt_templates.py` (template cleanup)
- `app/core/token_optimizer.py` (compression improvements)

Tasks:
1. Implement first round of compression optimizations
   ```python
   # In app/lib/prompt_templates.py
   
   # BEFORE: Architect verbose template (270 tokens)
   ARCHITECT_VERBOSE = """
   You are an expert software architect. 
   Your role is to design systems...
   [Long description]
   [Multiple examples]
   [Detailed guidelines]
   """
   
   # AFTER: Architect optimized template (200 tokens)
   ARCHITECT_OPTIMIZED = """
   You are a software architect. Design systems with:
   - Clear abstractions
   - [Consolidated examples]
   - Performance-first approach
   """
   ```

2. Refine compression algorithms
   - Improve redundancy detection
   - Better instruction consolidation
   - Template variable reuse

3. Run validation tests
   ```bash
   pytest tests/test_performance_optimization_and_batching.py::TestTokenOptimizerIntegrationParametrized \
     -v --benchmark-only
   # Expected: All 6/6 tests still passing
   # Expected: Token reduction ≥10% in first round
   ```

4. Commit changes
   ```
   feat(token): optimize prompt templates and compression algorithms
   
   - Consolidate redundant examples in few-shot prompts
   - Remove unused context sections from templates
   - Improve compression algorithm efficiency
   - Remove 1-2 examples per template (20-30 token reduction)
   
   Baseline: TestTokenOptimizerIntegrationParametrized 6/6 passing
   Target: ≥15% token reduction (will continue in Week 4)
   ```

**Success Criteria**:
- [ ] Token usage baseline captured
- [ ] Optimization targets identified (ranked by impact)
- [ ] First round optimizations implemented
- [ ] ≥10% token reduction achieved
- [ ] All token optimizer tests passing (0 regressions)
- [ ] Changes committed to main

---

### Initiative 1.4: Concurrency Baseline & Assessment (Wed-Fri)

**Wednesday 9/10 - Concurrency Baseline Establishment**

Files to analyze:
- `app/db/session.py` (connection pool configuration)
- `app/core/orchestrator.py` (task execution)
- Load test configuration

Tasks:
1. Establish current concurrency limits
   ```bash
   # Run increasing load to find saturation point
   python -m pytest tests/test_performance_optimization_and_batching.py \
     -k "load" --benchmark-only -v
   
   # Capture for each load level:
   # - Success rate (%)
   # - Latency p50/p95/p99 (ms)
   # - Memory usage (MB)
   # - CPU usage (%)
   # - Error rate (%)
   ```

2. Document baseline metrics
   ```python
   BASELINE_METRICS = {
       "concurrent_tasks_at_1x_load": 100,  # [actual]
       "memory_usage_mb": 300,              # [actual]
       "cpu_usage_percent": 45,             # [actual]
       "error_rate_percent": 0.1,           # [actual]
       "connection_pool_size": 20,          # [actual]
       "thread_pool_size": 10,              # [actual]
   }
   ```

3. Identify bottlenecks at current load
   - Database connection pool saturation?
   - Memory pressure?
   - Lock contention?
   - Thread pool exhaustion?

**Friday 9/12 - Stress Testing & Bottleneck Identification**

Tasks:
1. Run stress tests at 2x current load
   ```bash
   # Run load test with 2x task count
   python -m pytest tests/test_performance_optimization_and_batching.py::TestLoadTestIntegrationParametrized \
     -v -k "2x" --benchmark-only
   
   # Monitor resource usage
   # Expected issues at 2x load:
   # - Connection pool saturation (queued requests)
   # - Memory pressure (possible OOM)
   # - Higher latency (p99 > 2x baseline)
   # - Possible timeouts/errors (> 1%)
   ```

2. Identify top 3 bottlenecks
   ```
   Bottleneck 1: [Symptom] → [Root cause] → [Proposed fix]
   Bottleneck 2: [Symptom] → [Root cause] → [Proposed fix]
   Bottleneck 3: [Symptom] → [Root cause] → [Proposed fix]
   ```

3. Create optimization task list for Week 4
   - Task 4.1a: Increase connection pool size
   - Task 4.1b: Optimize memory allocation
   - Task 4.1c: Tune thread pool size
   - Task 4.1d: Reduce lock contention

4. Document findings in bottleneck report

**Success Criteria**:
- [ ] Current concurrency baseline established
- [ ] 1x load metrics documented (memory, CPU, error rate)
- [ ] Stress test run at 2x load
- [ ] Top 3 bottlenecks identified
- [ ] Root causes understood
- [ ] Optimization task list created
- [ ] Week 4 tasks are clear and scoped

---

### Initiative 1.3: Token Validation (Fri)

**Friday 9/12 - Final Token Optimization Validation**

Tasks:
1. Calculate actual cost savings
   ```python
   baseline_tokens = 150  # avg tokens/task before optimization
   optimized_tokens = 135  # avg tokens/task after Week 3 optimization
   reduction = (baseline_tokens - optimized_tokens) / baseline_tokens * 100
   
   print(f"Token reduction: {reduction:.1f}%")
   # Expected: 10% after Week 3 (15% target in Week 4)
   ```

2. Verify all token optimizer tests passing
   ```bash
   pytest tests/test_performance_optimization_and_batching.py::TestTokenOptimizerIntegrationParametrized \
     -v
   # Target: 6/6 passing
   ```

3. Update AUDIT.md with Week 3 progress

**Success Criteria**:
- [ ] Token reduction measured (expected 10% after Week 3)
- [ ] Cost savings calculated
- [ ] All tests passing
- [ ] Results documented

---

## Testing Strategy

### Unit Tests (existing should pass)
```bash
pytest tests/test_performance_optimization_and_batching.py \
  -k "TestRoutingEngineParametrized or TestLoadTestIntegrationParametrized or TestTokenOptimizerIntegrationParametrized" \
  -v
```

### Performance Baselines
```bash
# Capture new baselines after Week 3
pytest tests/ --benchmark-only --benchmark-compare=baseline_before_week3.json
```

### Stress Tests
```bash
# Run at 1x and 2x load levels
python -m pytest tests/test_performance_optimization_and_batching.py -k "load" --benchmark-only
```

---

## Validation Checklist

### Mon-Tue (1.1 & 1.2 Finalization)
- [ ] Routing latency baseline captured & documented
- [ ] ≥20% latency reduction verified
- [ ] Batch throughput baseline captured & documented
- [ ] ≥25% throughput increase verified
- [ ] No regressions in existing tests
- [ ] Results added to AUDIT.md

### Wed-Thu (1.3 Token)
- [ ] Token usage baseline captured
- [ ] High-usage patterns identified
- [ ] First round optimizations implemented
- [ ] ≥10% token reduction achieved
- [ ] Token optimizer tests passing (6/6)
- [ ] Cost savings calculated

### Wed-Fri (1.4 Concurrency)
- [ ] Concurrency baseline established
- [ ] 1x load metrics documented
- [ ] Stress test at 2x load completed
- [ ] Top 3 bottlenecks identified
- [ ] Root causes understood
- [ ] Optimization task list for Week 4 created

---

## Code Quality Gates

Before committing each optimization:
```bash
# Format
black app/lib/prompt_templates.py app/core/token_optimizer.py

# Lint
ruff check app/core/routing.py app/core/batch_processor.py \
  app/lib/prompt_templates.py app/core/token_optimizer.py

# Type check
mypy app/core/routing.py app/core/batch_processor.py \
  app/lib/prompt_templates.py app/core/token_optimizer.py

# Test
pytest tests/test_performance_optimization_and_batching.py -v

# Coverage
pytest tests/ --cov=app --cov-report=term-missing
```

---

## Success Criteria

| Criterion | Target | Acceptance |
|-----------|--------|-----------|
| 1.1 Routing finalized | ≥20% reduction | Verified & documented |
| 1.2 Batch finalized | ≥25% increase | Verified & documented |
| 1.3 Token (Week 3) | ≥10% reduction | On track to 15% in Week 4 |
| 1.4 Concurrency baseline | Full documentation | Bottlenecks identified |
| Test regressions | 0 | All tests passing |
| Code quality | Pass all gates | Black, ruff, mypy clean |

---

## Commit Strategy

**Commit 1 (Mon 9/8 afternoon)**:
```
docs(phase17): week 3 finalization metrics for initiatives 1.1 & 1.2

- Routing latency reduction: [% achieved] (target: ≥20%)
- Batch throughput increase: [% achieved] (target: ≥25%)
- Baseline metrics captured and documented
- No regressions in 1.1 or 1.2 optimization
```

**Commit 2 (Thu 9/11 evening)**:
```
feat(token): optimize prompt templates and compression algorithms

- Consolidate redundant examples in few-shot prompts
- Remove unused context sections from templates
- Improve compression algorithm efficiency
- Reduce architect templates by 60-70 tokens
- Reduce coordinator templates by 20-30 tokens

Baseline: TestTokenOptimizerIntegrationParametrized 6/6 passing
Target: ≥15% token reduction (10% achieved in Week 3, 5% more in Week 4)
```

**Commit 3 (Fri 9/12 afternoon)**:
```
docs(phase17): week 3 concurrency assessment and bottleneck analysis

- Current concurrency baseline established
- Stress testing completed at 1x and 2x load
- Top 3 bottlenecks identified with root causes
- Optimization task list for Week 4 created
- On track for 2x concurrency capacity in Week 4
```

---

## References

- **Strategy 1.1**: `docs/work/current/phase17_strategy_1_1_routing.md`
- **Strategy 1.2**: `docs/work/current/phase17_strategy_1_2_batch.md`
- **Strategy 1.3**: `docs/work/current/phase17_strategy_1_3_token.md`
- **Strategy 1.4**: `docs/work/current/phase17_strategy_1_4_concurrency.md`
- **Week 2 Plan**: `phase17_week2_plan.md`
- **Task Breakdown**: `docs/work/planned/phase-17-task-breakdown.md`

---

**Status**: READY FOR IMPLEMENTATION  
**Last Updated**: 2026-08-26  
**Next**: Week 4 (9/15-9/21) - Complete 1.3, Intensive 1.4, Begin Validation
