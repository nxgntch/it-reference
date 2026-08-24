# Phase 14: Runtime Operations & Analytics

**Status**: READY TO EXECUTE  
**Duration**: 49 days (7 weeks)  
**Start**: Post-Phase 13 (2026-08-24)  
**Effort**: 49 person-days  
**Priority**: Cost > Performance > Observability > Resilience  
**Target Completion**: 2026-10-12  

---

## Executive Summary

Phase 14 transforms nxgntch from a feature-complete system (Phase 13) into a **production-optimized, observable, and resilient runtime**. Focuses on operational excellence: cost reduction (30-50%), latency optimization (-50%), comprehensive observability, and automatic failure recovery.

Built on the "ACTIVE_PLAN" roadmap (ops/ACTIVE_PLAN.md), Phase 14 is structured as 4 sequential optimization phases with weekly checkpoints and measurable impact per phase.

---

## Phase Dependencies

| Phase | Prerequisite | Status | Impact |
|-------|-------------|--------|--------|
| **Phase 13** | Monitoring & observability | ✅ Complete | Baseline metrics, dashboard system |
| **Phase 12** | Optimization framework | ✅ Complete | ResilienceOptimizer, adaptive tuning |
| **Phase 11** | Error recovery | ✅ Complete | CircuitBreaker, checkpoint system |
| **Phase 14** | All above | ✅ Ready | Will integrate all into unified runtime |

---

## Success Criteria (End of Phase 14)

| Category | Metric | Target | Current |
|----------|--------|--------|---------|
| **Cost** | Monthly API spend | ↓ 30-50% | Baseline (from Phase 13) |
| **Performance** | Invocation latency (p95) | < 200ms | Baseline (establish Week 3) |
| **Throughput** | Concurrent invocations | 100+ | TBD (measure Week 4) |
| **Observability** | Request trace coverage | 100% of requests | 0% (build in Phase 14) |
| **Reliability** | Uptime during partial outages | 99.5% | TBD (validate Week 8) |
| **Error Recovery** | MTTR (Mean Time To Recovery) | < 30 seconds | TBD (measure Week 8) |
| **Documentation** | Ops runbooks complete | 100% | 0% (create in Phase 14) |
| **Test Coverage** | Phase 14 code | ≥ 85% | TBD |

---

## Phase 14.1: Cost Optimization (12 days / Week 1-2)

### Goal
Reduce API spend by 30-50% through intelligent model routing, response caching, and token optimization.

### 14.1.1: Model Routing Strategy (3 days)
**Effort**: 3 days | **Impact**: 15-25% cost reduction

**Tasks**:
- [ ] Profile current invocations: identify tasks suitable for Haiku (classification, summarization)
- [ ] Implement `modelRouter.py`: determine optimal model based on task complexity
- [ ] Add cost estimator: show projected vs optimal cost before execution
- [ ] A/B test: measure quality impact vs cost savings
- [ ] Update `config/governance.yaml` with routing rules
- [ ] Document decision tree in ops guide

**Success Criteria**:
- ✅ Simple tasks routed to Haiku 100% (cost $0.001 vs $0.005)
- ✅ Quality metrics unchanged for Haiku-routed tasks
- ✅ Cost comparison visible in API responses
- ✅ A/B test shows savings without quality loss

**Code Changes**:
- `app/core/modelRouter.py` (new)
- `app/core/orchestrator.py` (+integration)
- `config/governance.yaml` (add routing rules)

---

### 14.1.2: LLM Response Caching (2 days)
**Status**: ✅ **ALREADY COMPLETE** (2026-08-22)

**Already Delivered**:
- ✅ Prompt hash-based caching (SHA256 normalized)
- ✅ CacheEntry with TTL expiration (7-day default)
- ✅ ResponseCache with LRU eviction
- ✅ Orchestrator integration (check cache before execution)
- ✅ 27 comprehensive tests (100% passing)

**Files**: `app/core/responseCache.py`, `tests/testResponseCache.py`

**Revalidate in Phase 14**:
- [ ] Measure cache hit rate on production workload (target: 30%+)
- [ ] Verify TTL expiration working correctly
- [ ] Test LRU eviction under cache pressure
- [ ] Monitor memory impact of cache growth

---

### 14.1.3: Token-Level Optimization (2 days)
**Effort**: 2 days | **Impact**: 5-10% cost reduction

**Tasks**:
- [ ] Analyze token patterns from cost tracker (input vs output ratio)
- [ ] Identify verbose prompts (agent system prompts, instructions)
- [ ] Implement `tokenOptimizer.py`: intelligent prompt compression
- [ ] Add token metrics to responses (inputTokens, outputTokens)
- [ ] Create optimization report with compression opportunities

**Success Criteria**:
- ✅ Average input tokens reduced 10-20%
- ✅ No quality degradation on compressed prompts
- ✅ Token metrics visible in invocation responses
- ✅ Optimization report identifies savings opportunities

**Code Changes**:
- `app/core/tokenOptimizer.py` (new)
- `app/core/orchestrator.py` (+token reporting)
- `app/api/admin.py` (/admin/tokens/report endpoint)

---

### 14.1.4: Batch Processing API (3 days)
**Effort**: 3 days | **Impact**: 5% cost reduction + throughput improvement

**Tasks**:
- [ ] Design batch API: `POST /tasks/batch`
- [ ] Implement `taskBatcher.py`: group similar tasks, execute together
- [ ] Measure API call reduction (e.g., 10 tasks → 2 calls)
- [ ] Cost tracking for batch operations
- [ ] Document API and examples in ops guide

**Success Criteria**:
- ✅ Batch endpoint reduces API calls by 50%+
- ✅ Cost per task in batch 30% lower than individual
- ✅ Documented with examples
- ✅ Integration tests validate savings

**Code Changes**:
- `app/core/taskBatcher.py` (new)
- `app/api/routers/tasks.py` (+/tasks/batch endpoint)
- `tests/testTaskBatcher.py` (new, ≥15 tests)

---

### 14.1 Checkpoint (End of Week 2)
**Go-live**: Cost optimization features

**Validation**:
- [ ] All 4 sub-phases complete and tested
- [ ] Estimated cost reduction: 30-50%
- [ ] Baseline metrics established in AUDIT.md
- [ ] Ops guide updated with cost optimization strategies

---

## Phase 14.2: Performance Optimization (9 days / Week 3-4)

### Goal
Reduce latency and increase throughput. Target: invocation latency < 200ms (p95), throughput > 100 concurrent tasks.

### 14.2.1: Connection Pooling & Database (2 days)
**Effort**: 2 days | **Impact**: 20-30% latency reduction

**Tasks**:
- [ ] Verify SQLAlchemy pool configuration (pool_size, max_overflow)
- [ ] Profile slow queries: add logging for queries > 100ms
- [ ] Create database indexes on: `teamId`, `agentId`, `timestamp`, `createdAt`
- [ ] Implement query caching layer: `app/lib/queryCache.py`
- [ ] Add connection pool monitoring to admin API
- [ ] Load test to validate improvements

**Success Criteria**:
- ✅ Database query latency < 50ms (p95)
- ✅ No connection pool exhaustion
- ✅ Slow query log shows improvements
- ✅ Indexes created and tested

**Code Changes**:
- `app/db/session.py` (update pool config)
- `app/lib/queryCache.py` (new)
- `scripts/migrate/add_indexes.py` (new)
- `app/api/admin.py` (/admin/database/stats endpoint)

---

### 14.2.2: Agent Configuration Caching (2 days)
**Effort**: 2 days | **Impact**: 10-15% latency reduction

**Tasks**:
- [ ] Implement in-memory cache for agent definitions (not loaded per invocation)
- [ ] Add invalidation logic: config file watching or version-based
- [ ] Warm up cache on startup
- [ ] Test concurrent access (thread-safe)
- [ ] Add metrics: cache hit rate, load time

**Success Criteria**:
- ✅ Agent definition lookup: < 1ms (from memory)
- ✅ No stale configs in use
- ✅ Cache warm-up completes in < 1s
- ✅ Concurrent safety verified

**Code Changes**:
- `app/lib/agentConfigCache.py` (new)
- `app/core/orchestrator.py` (use cache)
- `app/startup.py` (warm-up on startup)

---

### 14.2.3: Async Optimization (3 days)
**Effort**: 3 days | **Impact**: Throughput +30%

**Tasks**:
- [ ] Audit `orchestrator.py` and critical paths for blocking operations
- [ ] Convert file I/O to async (aiofiles)
- [ ] Convert external API calls to async (httpx.AsyncClient)
- [ ] Add concurrent task execution (semaphore-based concurrency limiting)
- [ ] Load testing: measure throughput improvement (tasks/second)
- [ ] Verify no resource exhaustion (memory, file handles)

**Success Criteria**:
- ✅ No blocking I/O in critical paths
- ✅ Throughput: 100+ concurrent invocations
- ✅ Memory usage stable under load
- ✅ Load tests validate +30% throughput

**Code Changes**:
- `app/core/orchestrator.py` (async audit + fixes)
- `app/core/fileHandler.py` (async file ops)
- `scripts/load_test.py` (new, concurrent workload)

---

### 14.2.4: Observability for Performance (2 days)
**Effort**: 2 days | **Impact**: Enables future optimization

**Tasks**:
- [ ] Add latency tracking at key checkpoints: routing, execution, cost calculation
- [ ] Implement histogram metrics: agent latency, DB query time, LLM call time
- [ ] Create performance breakdown dashboard
- [ ] Identify bottlenecks (where time is spent)
- [ ] Document findings in AUDIT.md

**Success Criteria**:
- ✅ Latency breakdown visible per component
- ✅ Bottlenecks identified and ranked
- ✅ Performance metrics in admin API
- ✅ Dashboard shows per-agent latency

**Code Changes**:
- `app/lib/metrics.py` (timing decorators)
- `app/api/admin.py` (/admin/metrics/performance endpoint)
- `app/lib/timings.py` (histogram tracking)

---

### 14.2 Checkpoint (End of Week 4)
**Go-live**: Performance optimizations

**Validation**:
- [ ] All 4 sub-phases complete and tested
- [ ] Latency baseline established: < 200ms (p95)
- [ ] Throughput baseline: 100+ concurrent tasks
- [ ] Bottlenecks identified and documented

---

## Phase 14.3: Observability & Debugging (14 days / Week 5-7)

### Goal
Complete visibility into runtime behavior. Enable rapid diagnosis of issues.

### 14.3.1: Distributed Tracing (4 days)
**Effort**: 4 days | **Impact**: Complete request flow visibility

**Tasks**:
- [ ] Verify request ID propagation (from Phase 13)
- [ ] Add span tracking: routing → execution → cost calculation
- [ ] Export traces to structured logs (JSON format)
- [ ] Implement trace correlation: link agent → sub-agent calls
- [ ] Create trace viewer endpoint: `/admin/traces/search?requestId=X`
- [ ] Document tracing architecture

**Success Criteria**:
- ✅ Every request has unique trace ID
- ✅ All sub-operations linked to parent trace
- ✅ Full execution path visible in trace viewer
- ✅ Trace format documented

**Code Changes**:
- `app/lib/tracing.py` (trace context, span tracking)
- `app/middleware/tracingMiddleware.py` (request ID propagation)
- `app/api/admin.py` (/admin/traces/* endpoints)

---

### 14.3.2: Metrics & Dashboards (5 days)
**Effort**: 5 days | **Impact**: Real-time system visibility

**Metrics to Implement**:
- Agent invocation latency (p50, p95, p99)
- Request throughput (invocations/sec)
- Error rate (by agent, by error type)
- Cost distribution (by team, by agent, by model)
- Cache hit rate
- Database connection pool usage
- Memory usage (garbage collection, peaks)
- Circuit breaker state changes
- Retry rate and backoff distribution

**Tasks**:
- [ ] Implement metrics collection: `app/metrics.py`
- [ ] Export to Prometheus format (or simple JSON)
- [ ] Create dashboard: real-time HTML view or Grafana integration
- [ ] Configure alerting: anomalies on latency/error spikes
- [ ] Document dashboard usage

**Success Criteria**:
- ✅ Metrics available in real-time
- ✅ Alerts trigger on anomalies
- ✅ Dashboard shows system health
- ✅ Historical metrics retained (1-month rolling window)

**Code Changes**:
- `app/metrics.py` (collection)
- `app/api/admin.py` (/admin/metrics/current endpoint)
- `scripts/dashboard.html` (simple web dashboard)
- `config/alerting.yaml` (alert thresholds)

---

### 14.3.3: Structured Logging (2 days)
**Effort**: 2 days | **Impact**: Searchable, analyzable logs

**Tasks**:
- [ ] Convert all logs to JSON format (timestamp, level, component, message, context)
- [ ] Add context fields: requestId, agentId, teamId, userId, traceId
- [ ] Standardize log levels: DEBUG (dev), INFO (events), WARNING (issues), ERROR (failures)
- [ ] Configure log rotation (daily, retention 30 days)
- [ ] Centralize logs (file or simple aggregation)

**Success Criteria**:
- ✅ All logs JSON-formatted
- ✅ Easily searchable (grep or log viewer)
- ✅ Context fields consistent across codebase
- ✅ No sensitive data in logs (hashed tokens, redacted PII)

**Code Changes**:
- `app/core/logging.py` (JSON formatter, context manager)
- Update all logger calls to use structured format
- `config/logging.yaml` (logging configuration)

---

### 14.3.4: Admin Observability API (3 days)
**Effort**: 3 days | **Impact**: Ops visibility

**Endpoints to Implement**:
- `GET /admin/system/health` - overall system status
- `GET /admin/metrics/current` - real-time metrics snapshot
- `GET /admin/traces/search?requestId=X` - find trace by ID
- `GET /admin/agents/status` - agent health and load
- `GET /admin/cache/stats` - cache effectiveness
- `GET /admin/database/stats` - connection pool and slow queries
- `GET /admin/logs/recent?level=ERROR` - recent errors
- `GET /admin/alerts/active` - active alerts

**Tasks**:
- [ ] Implement all 8 endpoints
- [ ] Each returns JSON with visualization hints
- [ ] Add response schema documentation
- [ ] Implement access control (admin token required)

**Success Criteria**:
- ✅ All key metrics available via API
- ✅ Ops can diagnose issues without logs directly
- ✅ Response schemas documented
- ✅ Examples provided for each endpoint

**Code Changes**:
- `app/api/routers/admin.py` (expand existing or create new file)
- `app/api/schemas.py` (add response schemas)

---

### 14.3 Checkpoint (End of Week 7)
**Go-live**: Observability infrastructure

**Validation**:
- [ ] All 4 sub-phases complete and tested
- [ ] Dashboard live and showing real-time data
- [ ] Alerting working and tested
- [ ] Ops guide updated with observability tools

---

## Phase 14.4: Reliability & Resilience (14 days / Week 8+)

### Goal
System survives failures gracefully. Automatic recovery where possible.

### 14.4.1: Circuit Breaker Pattern (3 days)
**Effort**: 3 days | **Impact**: Prevent cascading failures

**Tasks**:
- [ ] Implement circuit breaker for external APIs (Anthropic, external calls)
- [ ] States: CLOSED (normal), OPEN (failing, reject), HALF_OPEN (testing recovery)
- [ ] Configurable thresholds: 5 failures → OPEN, retry after 30s → HALF_OPEN
- [ ] Fallback behavior: cache, degraded mode, or error response
- [ ] Metrics: track state changes, failure rates
- [ ] Configuration in `config/governance.yaml`

**Success Criteria**:
- ✅ External failures don't crash system
- ✅ Automatic recovery when service recovers
- ✅ Metrics track circuit breaker state changes
- ✅ Fallback behavior tested

**Code Changes**:
- `app/lib/circuitBreaker.py` (implementation, likely already exists from Phase 11)
- Integration into LLM client and external requests
- Configuration in `config/governance.yaml`

---

### 14.4.2: Retry Logic with Exponential Backoff (2 days)
**Effort**: 2 days | **Impact**: Transient failure recovery

**Tasks**:
- [ ] Implement retry on transient errors: timeout, rate limit, 5xx
- [ ] Backoff strategy: 1s, 2s, 4s, 8s, 16s max
- [ ] Jitter to prevent thundering herd (randomize within range)
- [ ] Max retries: 3 per request (configurable)
- [ ] Logging of retries for analysis

**Success Criteria**:
- ✅ Transient failures retried transparently
- ✅ No unnecessary retries (fail fast on permanent errors)
- ✅ Jitter prevents load spikes
- ✅ Retry metrics tracked

**Code Changes**:
- `app/lib/retryPolicy.py` (likely already exists from Phase 11)
- Integration into LLM client
- Configuration in `config/governance.yaml`

---

### 14.4.3: Graceful Degradation (3 days)
**Effort**: 3 days | **Impact**: Partial service availability

**Tasks**:
- [ ] Identify critical vs optional functionality
  - Critical: agent execution, cost tracking, auth
  - Optional: advanced features, caching, analytics
- [ ] Implement feature flags: `FEATURE_CACHING_ENABLED`, `FEATURE_ANALYTICS_ENABLED`
- [ ] Disable optional features if dependencies fail
- [ ] Return reduced response if full response unavailable
- [ ] Logging of degradation events

**Success Criteria**:
- ✅ System operates with reduced feature set on partial outage
- ✅ Users notified of degradation
- ✅ Automatic recovery when dependencies restore
- ✅ Degradation transparent to critical operations

**Code Changes**:
- Feature flags in `config/features.yaml`
- Graceful error handling in critical paths
- Middleware to detect dependency failures

---

### 14.4.4: Error Recovery & Checkpoint (4 days)
**Effort**: 4 days | **Impact**: Long-running operation resilience

**Tasks**:
- [ ] Implement checkpoints (likely exists from Phase 11)
- [ ] State serialization: save state after each step
- [ ] Recovery: resume from checkpoint on failure
- [ ] Audit trail: log recovery attempts
- [ ] Testing: chaos engineering, simulated failures

**Success Criteria**:
- ✅ Long operations survive mid-execution failures
- ✅ Recovery automatic and transparent
- ✅ No duplicate work on recovery
- ✅ Audit trail of recovery events

**Code Changes**:
- Checkpoint system in `app/core/state.py` (likely exists)
- Recovery logic in orchestrator
- Chaos testing in `tests/testResilience.py`

---

### 14.4.5: Load Shedding (2 days)
**Effort**: 2 days | **Impact**: System stability under extreme load

**Tasks**:
- [ ] Monitor queue depth and response latency
- [ ] When latency exceeds threshold: reject low-priority requests (gracefully)
- [ ] Return 503 Service Unavailable with retry-after header
- [ ] Prioritize high-value or low-cost tasks
- [ ] Metrics for rejected requests

**Success Criteria**:
- ✅ System doesn't collapse under extreme load
- ✅ Graceful rejection instead of timeout cascades
- ✅ Core functionality remains responsive
- ✅ Priority-based shedding working

**Code Changes**:
- Load monitor in middleware
- Priority-based request filtering
- Metrics for load shedding decisions

---

### 14.4 Checkpoint (End of Week 8)
**Go-live**: Resilience infrastructure

**Validation**:
- [ ] All 5 sub-phases complete and tested
- [ ] Chaos testing validates recovery
- [ ] MTTR (Mean Time To Recovery) < 30s
- [ ] Uptime metrics show improvement

---

## Phase 14 Timeline & Execution

### Weekly Checkpoint Cadence

| Week | Phases | Deliverable | Go-Live |
|------|--------|-------------|---------|
| **Week 1-2** | 14.1 (Cost) | Model routing + caching + tokens + batch | ✅ Cost optimization |
| **Week 3-4** | 14.2 (Performance) | DB + caching + async + observability | ✅ Performance baseline |
| **Week 5-7** | 14.3 (Observability) | Tracing + metrics + logging + admin API | ✅ Observability live |
| **Week 8** | 14.4 (Resilience) | Circuit breaker + retry + degradation + recovery | ✅ Resilience |

### Daily Standup Structure
- **What was done** (commits, tests added)
- **What's blocking** (dependencies, decisions)
- **Next day focus** (specific tasks)
- **Metrics** (tests passing, test coverage, build time)

### Testing at Each Phase
- Unit tests for new components (target: ≥85% coverage)
- Integration tests with existing system
- Load testing (Phase 14.2+)
- Staging environment validation
- Metrics comparison: before/after

### Documentation
- Update `CLAUDE.md` with runtime improvements
- Document new APIs, configs, and admin endpoints
- Create ops runbook: troubleshooting, common issues
- Update `.claude/WORKFLOWS.md` with new batch API
- Add performance tuning guide

---

## Success Metrics (Phase 14 Completion)

### Cost Metrics
- [ ] API spend reduced by 30-50%
- [ ] Cost per invocation: $0.002-0.003 (from baseline)
- [ ] Cache hit rate: ≥30% on repeated queries
- [ ] Token optimization: 10-20% reduction in input tokens

### Performance Metrics
- [ ] Invocation latency (p95): < 200ms
- [ ] Throughput: 100+ concurrent invocations
- [ ] Database query latency: < 50ms (p95)
- [ ] Cache lookup: < 1ms

### Observability Metrics
- [ ] Request trace coverage: 100%
- [ ] Dashboard uptime: 99.9%
- [ ] Log volume: < 100 MB/day (for 1000 invocations/day)
- [ ] Alert accuracy: > 90% (low false positive rate)

### Reliability Metrics
- [ ] System uptime: 99.5% (including partial outages)
- [ ] MTTR (Mean Time To Recovery): < 30 seconds
- [ ] Error recovery success rate: > 95%
- [ ] Graceful degradation: core services always available

### Code Quality
- [ ] Test coverage: ≥ 85% (all Phase 14 code)
- [ ] All tests passing (100% pass rate)
- [ ] Black/Ruff/mypy passing
- [ ] No security issues (OWASP review complete)

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Cache pollution | Memory exhaustion | LRU eviction, TTL enforcement, monitoring |
| Async refactoring bugs | Production outages | Thorough testing, staging validation, gradual rollout |
| Observability overhead | Latency increase | Sampling logs (not all), async metrics collection |
| Retry storms | Cascading failures | Jitter, circuit breaker, rate limiting |
| Feature flag debt | Code complexity | Clear deprecation timeline, regular cleanup |

---

## Integration Checklist

- [ ] All Phase 14 code merged to main
- [ ] AUDIT.md updated with Phase 14 metrics
- [ ] CLAUDE.md updated with phase completion
- [ ] Ops guide updated with new features
- [ ] Team trained on observability tools
- [ ] Runbooks documented
- [ ] Production deployment tested in staging
- [ ] Baseline metrics established for next phase

---

## Success Definition

**Phase 14 is COMPLETE when:**

1. ✅ All 4 sub-phases (Cost, Performance, Observability, Resilience) delivered and tested
2. ✅ All 49 days of effort completed with 100% test coverage
3. ✅ Production metrics show:
   - 30-50% cost reduction
   - Latency < 200ms (p95)
   - 100+ concurrent tasks
   - 99.5% uptime with automatic recovery
4. ✅ Complete observability: traces, metrics, logs, dashboards
5. ✅ Ops team trained and runbooks documented
6. ✅ Code review passed (2+ reviewers)
7. ✅ Staging environment validation complete
8. ✅ AUDIT.md updated with all Phase 14 metrics

---

## References

- **Active Plan**: `ops/ACTIVE_PLAN.md` (49-day detailed roadmap)
- **Cost Management**: `.claude/rules/cost-management.md`
- **Performance**: `.claude/rules/fastapi-patterns.md`
- **Security**: `.claude/rules/security.md`
- **Phase Gates**: `.claude/rules/phase-gates.md`
- **Phase 13 Completion**: `AUDIT.md` § Phase 13

---

## Status

**Phase 14 Plan**: ✅ **APPROVED** (2026-08-23)  
**Ready to Execute**: 2026-08-24  
**Estimated Completion**: 2026-10-12  
**Owner**: Runtime optimization team  

Next Step: Start Phase 14.1 (Model Routing Strategy)

