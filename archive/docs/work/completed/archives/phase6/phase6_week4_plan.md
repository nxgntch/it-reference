# Phase 6 Week 4: Advanced Metrics & Script Optimization

**Status**: ACTIVE (2026-08-27 onwards) | **Target**: 14 hours | **Tests**: +16 new tests

---

## Overview

Week 4 focuses on expanding metrics capabilities and optimizing critical scripts using performance data from Week 3 baselines.

**Current State**:
- ✅ ReportGenerator fully functional
- ✅ Performance baselines captured via CLIProfiler
- ✅ Caching infrastructure ready
- ⏳ Advanced metrics features needed
- ⏳ Sync scripts optimization needed
- ⏳ Doc generator optimization needed

**Goals**:
1. Add time-series metrics storage
2. Optimize sync scripts (target: 30% faster)
3. Optimize doc generators (target: 20% faster)
4. Maintain 100% test pass rate

---

## Task Breakdown (14 hours total)

### Task 1: Advanced Metrics (6 hours)

**What**: Extend ReportGenerator with time-series analysis and alerts

**Subtasks**:
1. **Time-Series Storage** (2 hours)
   - Implement MetricsTimeSeries class
   - Store daily/hourly metrics snapshots
   - Query metrics by date range
   - Export for analysis/visualization

2. **Trend Detection & Alerts** (2 hours)
   - Detect anomalies (sudden cost spikes)
   - Calculate moving averages
   - Identify trend reversals
   - Generate alert conditions

3. **Comparative Analysis** (2 hours)
   - Week-over-week comparison
   - Month-over-month comparison
   - Seasonal patterns detection
   - Year-over-year forecasting foundation

**Tests**: +8 new tests  
**Files**: `app/analytics/metricsTimeSeries.py`, `app/analytics/metricsAlerts.py`

---

### Task 2: Sync Scripts Optimization (6 hours)

**What**: Optimize repository sync scripts using profiling insights

**Subtasks**:
1. **Parallel File Processing** (2 hours)
   - Multi-threaded file operations
   - Batch file reads (reduce I/O)
   - Stream large files instead of loading to memory
   - Target: 30% improvement

2. **Connection Pooling** (2 hours)
   - Reuse connections across operations
   - Implement connection cache
   - Reduce handshake overhead
   - Connection timeout management

3. **Caching Integration** (2 hours)
   - Use FileConfigCache for parsed repos
   - Cache file hashes
   - Skip unchanged files
   - Measure cache impact

**Tests**: +5 new tests  
**Files**: Extend `scripts/sync/base.py` with optimizations

---

### Task 3: Doc Generator Optimization (2 hours)

**What**: Optimize documentation generation using cache and batching

**Subtasks**:
1. **Batch Metadata Extraction** (1 hour)
   - Extract frontmatter in parallel
   - Cache parsed metadata
   - Reduce file I/O (group reads)
   - Target: 20% improvement

2. **Cache Integration** (1 hour)
   - Cache generated doc content
   - Hash-based invalidation (FileConfigCache)
   - Skip unchanged documents
   - Measure cache hit rate

**Tests**: +3 new tests  
**Files**: Extend `scripts/docs/generator.py` with optimizations

---

## Implementation Order

**Sequential** (Task 1 → Task 2 → Task 3):
1. Start with advanced metrics (self-contained)
2. Then optimize sync (uses metrics for validation)
3. Finally doc generator (uses cache from sync work)

---

## Success Criteria

**By end of Week 4**:
- [ ] Time-series metrics working with date range queries
- [ ] Trend detection identifying anomalies accurately
- [ ] Sync scripts 30% faster (verified with baseline comparison)
- [ ] Doc generators 20% faster (verified with baseline comparison)
- [ ] Cache hit rate >50% for common operations
- [ ] 16+ new tests passing
- [ ] No regressions in existing tests

---

## Performance Targets

| Component | Current | Target | Improvement |
|-----------|---------|--------|-------------|
| Sync scripts | 100% | 70% | 30% faster |
| Doc generators | 100% | 80% | 20% faster |
| Cache hit rate | N/A | >50% | High reuse |
| Metrics queries | - | <100ms | Fast reporting |

---

## Testing Strategy

**Unit Tests** (12+ tests):
- Time-series storage and queries
- Trend detection algorithms
- Parallel processing correctness
- Cache invalidation

**Integration Tests** (4+ tests):
- End-to-end sync with caching
- Doc generation with cache
- Metrics with alerts
- Performance comparison (before/after)

---

## Files to Create/Modify

**Create**:
- `app/analytics/metricsTimeSeries.py` - Time-series storage
- `app/analytics/metricsAlerts.py` - Alert generation

**Modify**:
- `scripts/sync/base.py` - Add parallel + cache
- `scripts/docs/generator.py` - Add batch + cache
- `scripts/profiling/phase6/cli_profiling.py` - Add comparison

---

## Validation Plan

**Baseline Comparison**:
1. Run profiler on current code (get Week 3 baseline)
2. Implement optimizations
3. Run profiler again
4. Compare: (baseline - optimized) / baseline = % improvement

**Cache Validation**:
1. Measure cache hit rate
2. Verify correctness (cache doesn't mask bugs)
3. Check memory usage
4. Confirm TTL expiration works

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Parallelization bugs | Use thread-safe structures; extensive testing |
| Cache invalidation issues | FileConfigCache hash validation; manual tests |
| Performance regress | Baseline comparison; rollback if needed |
| Memory issues | Profile memory usage; add memory limits |

---

## Dependencies

- Week 3 baselines captured (CLIProfiler results)
- ConfigCache/FileConfigCache working (tested)
- LogParser functional (tested)

---

**Status**: READY TO START | **Priority**: HIGH | **Effort**: 14 hours (3.5 days at 4hr/day)

