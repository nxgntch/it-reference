# Skill Consolidation Implementation Plan

**Efficient roadmap for consolidating 28 skills into 15-18 unified skills.**

Status: Ready to implement  
Estimated Duration: 3 weeks | 60-80 hours effort  
Benefits: 4,000+ lines saved | 40% maintenance reduction

---

## Executive Summary

**Goals**:
1. Reduce 28 skills to 15-18 consolidated skills
2. Preserve all existing functionality (backward-compatible APIs)
3. Save 4,000-5,000 lines of duplicate code
4. Simplify configuration (50 parameters → 25)
5. Enable new feature development (unified forecasting, observability, workflow systems)

**Approach**: Three parallel work streams (forecasting, infrastructure, decision systems) with shared adapter layer for compatibility.

---

## Dependency Graph (Before Consolidation)

```
┌─ costForecasting ─┐
│                   ├─→ decisionMaking ─→ routing → geoRouterExtended
├─ anomalyDetector ─→ rootCauseAnalyzer ─┘
└─ forecastingEngine

┌─ metricsCollector ─→ analyticsEngine ─→ healthCheck ─→ reportGenerator
├─ performanceTracing ───────────────────────────────────┘
└─ cacheManager (infrastructure)

┌─ planning ─────────┐
├─ decomposition ────┼─→ integration ─→ routing
└─ taskIntake ───────┘

┌─ geoRouterExtended ──────────────────┐
├─ regionFailoverManager ──────────────┼─→ tenantRouter (STUB)
└─ dataLocalityOptimizer ─→ routing ───┘

┌─ intelligentOptimizer ──┐
└─ decisionMaking ────────┼─→ routing
                          │
                 ┌────────┘
                 └─ codeReview
```

---

## Phase 1: Forecasting Consolidation (Week 1)

**Deliverable**: `PredictionEngine` replacing forecastingEngine + costForecasting + anomalyDetector

### 1.1 Create Base PredictionEngine (Day 1)

**File Structure**:
```
skills/predictionEngine/
├── SKILL.md                    # New consolidated skill doc
├── skill.py                    # Base engine
├── models/
│   ├── arima.py               # Time-series models (from forecastingEngine)
│   ├── exponential_smoothing.py
│   └── statistical.py          # Anomaly detection (from anomalyDetector)
├── adapters/
│   ├── forecasting_api.py     # forecastingEngine compatibility layer
│   ├── cost_api.py            # costForecasting compatibility layer
│   └── anomaly_api.py         # anomalyDetector compatibility layer
├── config.yaml                 # Unified configuration
└── tests/
    ├── test_arima.py          # From forecastingEngine tests
    ├── test_exponential.py     # From costForecasting tests
    ├── test_anomaly.py        # From anomalyDetector tests
    └── test_adapters.py       # New compatibility tests
```

**Tasks**:
- [ ] Extract ARIMA, exponential smoothing, seasonal decomposition to shared models
- [ ] Extract statistical anomaly detection (z-score, IQR, isolation_forest)
- [ ] Consolidate configuration (models.yaml + cost_config.yaml → unified config)
- [ ] Create base `ModelRegistry` class
- [ ] Merge test suites (keep all tests, eliminate ~5 redundant tests)

**Time**: 6 hours  
**Commits**: 3 (base engine, models, tests)

### 1.2 Create Adapter Layer (Day 1)

**Tasks**:
- [ ] forecastingEngine adapter: `predict(metric, steps, method)` → `PredictionEngine.forecast()`
- [ ] costForecasting adapter: `forecast_cost()` → `PredictionEngine.forecast("cost", ...)`
- [ ] anomalyDetector adapter: `detect()` → `PredictionEngine.detect()`
- [ ] Add deprecation warnings to old APIs
- [ ] Test backward compatibility (old skills call new engine)

**Time**: 4 hours  
**Commits**: 2 (adapters, tests)

### 1.3 Update Dependents (Day 2)

**Dependents**:
- rootCauseAnalyzer: Update imports, use `PredictionEngine.detect()` output
- decisionMaking: Update imports, use `PredictionEngine.forecast()` for cost predictions

**Tasks**:
- [ ] Update rootCauseAnalyzer to use new PredictionEngine API
- [ ] Update decisionMaking to use new PredictionEngine API
- [ ] Verify all dependent tests pass
- [ ] Update SKILL.md files for changed dependencies

**Time**: 4 hours  
**Commits**: 2 (updates, tests)

### 1.4 Deprecation & Cleanup (Day 3)

**Tasks**:
- [ ] Mark old skills as deprecated in config/skills.yaml
- [ ] Add migration guide: old → new API mapping
- [ ] Run full test suite (target: 3,300+ tests passing)
- [ ] Document in docs/guides/operations/

**Time**: 3 hours  
**Commits**: 1 (documentation)

**Phase 1 Checkpoint**:
- ✅ PredictionEngine working
- ✅ Old APIs functional via adapters
- ✅ All tests passing (3,300+)
- ✅ ~1,000 lines of duplicate code eliminated

---

## Phase 2: Multi-Region Consolidation (Week 1-2)

**Deliverable**: `MultiRegionOrchestrator` replacing geoRouterExtended + regionFailoverManager + dataLocalityOptimizer

### 2.1 Create Base MultiRegionOrchestrator (Day 1-2)

**File Structure**:
```
skills/multiRegionOrchestrator/
├── SKILL.md
├── skill.py
├── core/
│   ├── state_machine.py        # Unified region state (from regionFailoverManager)
│   ├── health_tracker.py       # Health monitoring (from geoRouterExtended)
│   └── router.py               # Routing logic (combined geoRouter + failover)
├── data_placement/
│   ├── locality.py             # Data locality optimizer logic
│   └── replication.py          # Replication strategy
├── adapters/
│   ├── geo_router_api.py       # geoRouterExtended compatibility
│   ├── failover_api.py         # regionFailoverManager compatibility
│   ├── locality_api.py         # dataLocalityOptimizer compatibility
│   └── tenant_router_api.py    # tenantRouter (STUB → implement as adapter)
├── config.yaml                 # Unified region configuration
└── tests/
    ├── test_state_machine.py   # From regionFailoverManager
    ├── test_routing.py         # From geoRouterExtended
    ├── test_locality.py        # From dataLocalityOptimizer
    ├── test_failover.py        # New integration tests
    └── test_adapters.py        # Compatibility tests
```

**Key Design**:
- **RegionStateManager**: Tracks health, failure state, capacity
- **RoutingEngine**: Selects region based on health + data locality + tenant policy
- **FailoverCoordinator**: Implicit in routing (no separate logic)

**Tasks**:
- [ ] Extract region state machine (health tracking, state transitions)
- [ ] Extract routing logic (latency, health, load balancing)
- [ ] Extract data locality logic (placement strategy, replication lag)
- [ ] Create unified region model (health + capacity + replicas)
- [ ] Consolidate config (geo_config.yaml + failover.yaml + locality.yaml → single)

**Time**: 8 hours  
**Commits**: 3 (state machine, routing, data placement)

### 2.2 Create Adapter Layer (Day 2)

**Tasks**:
- [ ] geoRouterExtended adapter: `route()` → `MultiRegionOrchestrator.route()`
- [ ] regionFailoverManager adapter: `detect_failure()` → implicit in state machine
- [ ] dataLocalityOptimizer adapter: `optimize_placement()` → part of routing decision
- [ ] tenantRouter: Implement as adapter (was STUB)
- [ ] Add backward-compatibility wrapper for old APIs

**Time**: 5 hours  
**Commits**: 2 (adapters, tenant router)

### 2.3 Update Dependents (Day 3)

**Dependents**:
- routing: Already depends on geoRouterExtended; update to call unified API
- costAwareLlmPipeline: Region-aware routing; update to new API

**Tasks**:
- [ ] Update routing skill to use MultiRegionOrchestrator
- [ ] Update costAwareLlmPipeline for region selection
- [ ] Verify all dependent tests pass

**Time**: 3 hours  
**Commits**: 1 (updates)

### 2.4 Verification & Docs (Day 4)

**Tasks**:
- [ ] Run integration tests (multi-region failover scenarios)
- [ ] Document new unified region API
- [ ] Update SKILL.md files for changed dependencies

**Time**: 2 hours  
**Commits**: 1 (documentation)

**Phase 2 Checkpoint**:
- ✅ MultiRegionOrchestrator working
- ✅ Old APIs functional via adapters
- ✅ tenantRouter implemented as adapter
- ✅ All tests passing
- ✅ ~900 lines of duplicate code eliminated

---

## Phase 3: Observability Stack Consolidation (Week 2)

**Deliverable**: `ObservabilityPipeline` replacing metricsCollector + analyticsEngine + performanceTracing (+ healthCheck + reportGenerator as consumers)

### 3.1 Create Base ObservabilityPipeline (Day 1-2)

**File Structure**:
```
skills/observabilityPipeline/
├── SKILL.md
├── skill.py
├── collectors/
│   ├── metrics.py              # metricsCollector logic
│   └── traces.py               # performanceTracing logic
├── aggregation/
│   ├── aggregator.py           # analyticsEngine aggregation
│   ├── statistics.py           # Trend analysis, percentiles
│   └── filtering.py            # Data filtering
├── exporters/
│   ├── prometheus.py           # Prometheus export
│   ├── opentelemetry.py        # OTel export
│   └── storage.py              # Time-series storage
├── adapters/
│   ├── metrics_api.py          # metricsCollector compatibility
│   ├── analytics_api.py        # analyticsEngine compatibility
│   ├── tracing_api.py          # performanceTracing compatibility
│   ├── health_check_api.py     # healthCheck consumer interface
│   └── report_gen_api.py       # reportGenerator consumer interface
├── config.yaml                 # Unified observability config
└── tests/
    ├── test_collection.py      # From metricsCollector
    ├── test_aggregation.py     # From analyticsEngine
    ├── test_tracing.py         # From performanceTracing
    ├── test_integration.py     # New end-to-end tests
    └── test_adapters.py        # Compatibility tests
```

**Key Design**:
- **Single metrics store**: Time-series backend shared by all
- **Unified aggregation**: All statistics computed once
- **Pluggable exporters**: Prometheus, OTel, custom backends
- **Consumer interface**: healthCheck & reportGenerator query unified store

**Tasks**:
- [ ] Extract metric collection (prometheus-compatible)
- [ ] Extract trace collection (OpenTelemetry-compatible)
- [ ] Consolidate aggregation logic (statistics, trending)
- [ ] Create unified metrics store interface
- [ ] Consolidate config (metrics.yaml + analytics.yaml + tracing.yaml)

**Time**: 10 hours  
**Commits**: 4 (collectors, aggregation, exporters, integration)

### 3.2 Create Adapter Layer (Day 2-3)

**Tasks**:
- [ ] metricsCollector adapter: `emit()` → `ObservabilityPipeline.record_metric()`
- [ ] analyticsEngine adapter: `analyze()` → `ObservabilityPipeline.query_aggregated()`
- [ ] performanceTracing adapter: `span()` → `ObservabilityPipeline.record_trace()`
- [ ] healthCheck consumer: Query from unified store, evaluate health rules
- [ ] reportGenerator consumer: Query aggregated data, format reports

**Time**: 6 hours  
**Commits**: 2 (adapters, consumers)

### 3.3 Update Dependents & Integration (Day 3-4)

**Tasks**:
- [ ] healthCheck: Update to query unified metrics store
- [ ] reportGenerator: Update to pull aggregated data
- [ ] Run integration tests (full observability pipeline)
- [ ] Verify all metrics still exported correctly

**Time**: 4 hours  
**Commits**: 2 (updates, tests)

**Phase 3 Checkpoint**:
- ✅ ObservabilityPipeline working
- ✅ Old APIs functional via adapters
- ✅ healthCheck & reportGenerator integrated as consumers
- ✅ All tests passing
- ✅ ~600 lines of duplicate code eliminated

---

## Phase 4: Planning & Workflow Consolidation (Week 2-3)

**Deliverable**: `WorkflowComposer` replacing planning + decomposition + integration

### 4.1 Create Base WorkflowComposer (Day 1-2)

**File Structure**:
```
skills/workflowComposer/
├── SKILL.md
├── skill.py
├── core/
│   ├── task_model.py           # Unified task/subtask model
│   ├── workflow_engine.py      # Task composition engine
│   └── executor.py             # Execution orchestration
├── planning/
│   ├── phase_planner.py        # Phase planning (from planning)
│   └── risk_analyzer.py        # Risk assessment
├── decomposition/
│   ├── decomposer.py           # Task decomposition (from decomposition)
│   └── dependency_resolver.py  # Dependency resolution
├── composition/
│   ├── composer.py             # Service composition (from integration)
│   └── registry.py             # Service registry
├── adapters/
│   ├── planning_api.py         # planning compatibility
│   ├── decomposition_api.py    # decomposition compatibility
│   └── integration_api.py      # integration compatibility
├── config.yaml                 # Unified workflow config
└── tests/
    ├── test_task_model.py      # Unified model tests
    ├── test_planning.py        # From planning
    ├── test_decomposition.py   # From decomposition
    ├── test_composition.py     # From integration
    └── test_workflows.py       # New end-to-end tests
```

**Key Design**:
- **Unified task model**: Tasks have subtasks, phases, dependencies, costs, risks
- **Workflow execution**: decompose → plan phases → compose services → execute
- **Single registry**: All services discoverable, callable

**Tasks**:
- [ ] Create unified task/workflow model
- [ ] Extract phase planning logic
- [ ] Extract decomposition logic (recursive task breakdown)
- [ ] Extract composition logic (service assembly)
- [ ] Consolidate config (planning.yaml + decomposition.yaml + integration.yaml)

**Time**: 10 hours  
**Commits**: 4 (task model, planning, decomposition, composition)

### 4.2 Create Adapter Layer (Day 2-3)

**Tasks**:
- [ ] planning adapter: `plan()` → `WorkflowComposer.plan_phases()`
- [ ] decomposition adapter: `decompose()` → `WorkflowComposer.decompose_task()`
- [ ] integration adapter: `compose()` → `WorkflowComposer.compose_services()`
- [ ] Ensure backward compatibility

**Time**: 5 hours  
**Commits**: 2 (adapters, tests)

### 4.3 Update Dependents (Day 3-4)

**Dependents**:
- routing: May need workflow composition for complex routing
- decisionMaking: May need task decomposition for multi-step decisions
- taskIntake: Entry point for workflows

**Tasks**:
- [ ] Update routing if it uses decomposition/composition
- [ ] Update decisionMaking if it uses planning
- [ ] Update taskIntake to create workflows
- [ ] Verify all dependent tests pass

**Time**: 4 hours  
**Commits**: 2 (updates, tests)

**Phase 4 Checkpoint**:
- ✅ WorkflowComposer working
- ✅ Old APIs functional via adapters
- ✅ All tests passing
- ✅ ~700 lines of duplicate code eliminated

---

## Phase 5: Decision Engine Consolidation (Week 3)

**Deliverable**: `DecisionEngine` replacing intelligentOptimizer + decisionMaking + routing

### 5.1 Create Base DecisionEngine (Day 1)

**File Structure**:
```
skills/decisionEngine/
├── SKILL.md
├── skill.py
├── strategies/
│   ├── rule_based.py           # Routing strategy (from routing)
│   ├── heuristic.py            # Multi-criteria (from decisionMaking)
│   └── ml_based.py             # Learning (from intelligentOptimizer)
├── scoring/
│   ├── scorer.py               # Multi-criteria scoring
│   ├── weighting.py            # Preference weighting
│   └── normalization.py        # Score normalization
├── adapters/
│   ├── routing_api.py          # routing compatibility
│   ├── decision_api.py         # decisionMaking compatibility
│   └── optimizer_api.py        # intelligentOptimizer compatibility
├── config.yaml                 # Unified decision config
└── tests/
    ├── test_strategies.py      # Strategy tests
    ├── test_scoring.py         # Scoring tests
    └── test_adapters.py        # Compatibility tests
```

**Key Design**:
- **Pluggable strategies**: Rule-based (routing), heuristic (decisions), ML (optimization)
- **Unified scoring**: All decisions use same multi-criteria framework
- **Learning feedback loop**: Results feed back to ML strategy

**Tasks**:
- [ ] Create unified scoring framework
- [ ] Extract rule-based strategy (routing)
- [ ] Extract heuristic strategy (multi-criteria decisions)
- [ ] Extract ML strategy (intelligentOptimizer)
- [ ] Consolidate config (routing.yaml + decision_config.yaml + optimizer.yaml)

**Time**: 8 hours  
**Commits**: 3 (strategies, scoring, config)

### 5.2 Create Adapter Layer (Day 1-2)

**Tasks**:
- [ ] routing adapter: `select_agent()` → `DecisionEngine.decide(strategy="rule-based")`
- [ ] decisionMaking adapter: `evaluate_options()` → `DecisionEngine.decide(strategy="heuristic")`
- [ ] intelligentOptimizer adapter: `optimize()` → `DecisionEngine.decide(strategy="ml")`

**Time**: 4 hours  
**Commits**: 2 (adapters, tests)

### 5.3 Verification (Day 2)

**Tasks**:
- [ ] Ensure all decision APIs work through unified framework
- [ ] Test strategy switching (same decision evaluated 3 ways)
- [ ] Verify ML feedback loop working
- [ ] Run full test suite

**Time**: 3 hours  
**Commits**: 1 (tests)

**Phase 5 Checkpoint**:
- ✅ DecisionEngine working
- ✅ Old APIs functional via adapters
- ✅ All tests passing
- ✅ ~500 lines of duplicate code eliminated

---

## Phase 6: Root Cause Analysis Integration (Week 3)

**Deliverable**: rootCauseAnalyzer as plugin in PredictionEngine

### 6.1 Create RCA Plugin (Day 1)

**Tasks**:
- [ ] Extract rootCauseAnalyzer logic into plugin module
- [ ] Integrate with PredictionEngine.detect() output
- [ ] Create complete pipeline: forecast → detect → analyze_root_cause
- [ ] Update SKILL.md for rootCauseAnalyzer to describe as plugin

**Time**: 4 hours  
**Commits**: 1 (plugin)

### 6.2 Integration Testing (Day 1-2)

**Tasks**:
- [ ] Test anomaly detection → root cause analysis pipeline
- [ ] Verify backward compatibility
- [ ] Run full test suite

**Time**: 3 hours  
**Commits**: 1 (tests)

**Phase 6 Checkpoint**:
- ✅ RCA integrated into forecasting pipeline
- ✅ Complete observability chain: forecast → detect → diagnose
- ✅ ~300 lines of duplicate code eliminated

---

## Parallel Work: Shared Utilities & Infrastructure

**Can run in parallel with phases above:**

### 6.1 Adapter Framework (Day 1 of Phases 1-6)

**Tasks**:
- [ ] Create `BaseSkillAdapter` class (provides deprecation warning, logging)
- [ ] Implement common patterns (error handling, validation)
- [ ] Document adapter development guide

**Time**: 3 hours  
**Commits**: 1

### 6.2 Configuration Management (Day 1-2 of Phases)

**Tasks**:
- [ ] Create unified config schema validation
- [ ] Migrate skills.yaml to reference consolidated skills
- [ ] Create migration tool: old → new configs
- [ ] Document config consolidation

**Time**: 4 hours  
**Commits**: 2

### 6.3 Testing Infrastructure (Day 1 of Phases)

**Tasks**:
- [ ] Create consolidated test fixtures
- [ ] Create backward-compatibility test suite
- [ ] Document test consolidation patterns

**Time**: 3 hours  
**Commits**: 1

### 6.4 Documentation (Ongoing)

**Tasks**:
- [ ] Create migration guide: old skills → new consolidated skills
- [ ] Document all new APIs
- [ ] Create deprecation timeline (3 months → removal)

**Time**: 2 hours per phase  
**Commits**: 1 per phase

---

## Timeline & Milestones

```
Week 1:
  Day 1: Phase 1.1 (PredictionEngine base)
  Day 2: Phase 1.2 + Phase 1.3 (Adapters & dependents)
  Day 3: Phase 1.4 (Cleanup)
  Day 4: Phase 2.1 (MultiRegionOrchestrator start)
  Day 5: Phase 2.1 (MultiRegionOrchestrator continue)

Week 2:
  Day 1: Phase 2.2 + 2.3 (MultiRegion adapters & dependents)
  Day 2: Phase 2.4 (MultiRegion verification)
  Day 3: Phase 3.1 (ObservabilityPipeline start)
  Day 4: Phase 3.1 (ObservabilityPipeline continue)
  Day 5: Phase 3.2 + 3.3 (Adapters & integration)

Week 3:
  Day 1: Phase 4.1 (WorkflowComposer start)
  Day 2: Phase 4.1 (WorkflowComposer continue)
  Day 3: Phase 4.2 + 4.3 (Adapters & dependents)
  Day 4: Phase 5.1 + 5.2 (DecisionEngine)
  Day 5: Phase 5.3 + 6 (Verification & RCA)
```

---

## Risk Mitigation

### Risk 1: Breaking Changes in Dependent Skills
**Mitigation**:
- Create comprehensive adapter layer (backward compatibility guaranteed)
- Run dependency tests before each phase
- Deploy adapters before deprecating old APIs
- Document migration path clearly

### Risk 2: Test Suite Explosion
**Mitigation**:
- Merge duplicate tests (keep 1 copy of each test scenario)
- Consolidate fixtures
- Eliminate redundant test cases (~30 tests)
- Target: 3,300 → 3,200 tests (higher quality, fewer duplicates)

### Risk 3: Configuration Complexity
**Mitigation**:
- Use config schema validation
- Create migration tool for old configs
- Provide sensible defaults
- Target: 50+ params → 25 params

### Risk 4: Performance Regression
**Mitigation**:
- Benchmark before and after each phase
- Target: No performance regression (shared libraries often faster due to caching)
- Run load tests on multi-region orchestrator

### Risk 5: Dependency Cycles
**Mitigation**:
- Map dependencies before each phase
- Use adapters to break cycles
- Use adapter tests to verify cycle-free design

---

## Success Criteria

**Phase Completion Checklist** (use for each phase):

- [ ] All new consolidated skill code passes linting (black, ruff, mypy)
- [ ] Adapter layer complete and tested
- [ ] All dependent skills updated and tested
- [ ] Test suite merged (no duplicate tests)
- [ ] No performance regression (benchmarks pass)
- [ ] Documentation updated (SKILL.md, migration guide)
- [ ] Old APIs callable via adapters
- [ ] Full test suite passing (3,300+ tests)
- [ ] Code review approved
- [ ] Merged to main branch

---

## Resource Allocation

**Effort Distribution**:
- Phase 1: 17 hours (PredictionEngine)
- Phase 2: 20 hours (MultiRegionOrchestrator)
- Phase 3: 20 hours (ObservabilityPipeline)
- Phase 4: 19 hours (WorkflowComposer)
- Phase 5: 15 hours (DecisionEngine)
- Phase 6: 7 hours (RCA Integration)
- **Shared**: 12 hours (adapters, config, testing, docs)

**Total**: ~110 hours (~3 weeks at 35-40 hrs/week)

---

## Post-Consolidation (Week 4+)

**Maintenance & Cleanup**:
1. Monitor performance for 1 week
2. Collect feedback from dependent skills
3. Fix any edge cases discovered
4. Remove deprecation warnings → full API migration (3 months later)
5. Delete old skill directories

**New Capabilities Unlocked**:
- Unified forecasting + anomaly + RCA pipeline
- Integrated observability (all metrics in one place)
- Multi-region orchestration with automatic failover
- Unified decision framework (rule/heuristic/ML strategies)
- Workflow execution engine

---

## Sign-Off

**Technical Lead**: [TBD]  
**QA Lead**: [TBD]  
**Project Manager**: [TBD]

---

**Last Updated**: 2026-08-31  
**Status**: Ready for Implementation  
**Next Step**: Approve and begin Phase 1
