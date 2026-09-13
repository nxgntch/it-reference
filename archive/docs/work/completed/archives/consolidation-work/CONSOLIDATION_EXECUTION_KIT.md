# Skill Consolidation: 8-Day Execution Kit

**Fast-path execution guide. Start immediately with 6-7 people, 4 parallel tracks, 8-day completion.**

---

## Pre-Execution Checklist (Do This Today)

- [ ] **Approve parallel plan** (sign-off on timeline)
- [ ] **Assign track leads** (4 people):
  - [ ] Track A Lead (Data Science) — Phase 1, 3, 6
  - [ ] Track B Lead (Infrastructure) — Phase 2
  - [ ] Track C Lead (Platform) — Phase 4, 5
  - [ ] Track D Lead (QA/DevOps) — Coordination
- [ ] **Schedule daily standups** — 9 AM, 15 min
- [ ] **Create Slack channel** — #skill-consolidation
- [ ] **Review parallel plan** — All leads read SKILL_CONSOLIDATION_PARALLEL.md
- [ ] **Set up feature branches** — Each track creates branch off main

---

## Day 1: Launch (All Tracks Start Simultaneously)

### Track A Setup (Data Science Lead)
**Responsible**: forecastingEngine + costForecasting + anomalyDetector → PredictionEngine

**Tasks** (Day 1):
- [ ] Create branch: `feat/phase1-predictionengine`
- [ ] Generate consolidated skill structure using automation
- [ ] Extract ARIMA, exponential smoothing, seasonal decomposition
- [ ] Extract statistical anomaly detection (z-score, IQR, isolation_forest)
- [ ] Merge test suites (eliminate 2-3 duplicate tests)
- [ ] Create config consolidation schema

**Commits to make**:
1. `feat(phase1): create PredictionEngine base structure`
2. `feat(phase1): add ARIMA and smoothing models`
3. `feat(phase1): add anomaly detection models`
4. `test(phase1): merge test suites`

**Standup Report**: "PredictionEngine base complete, test suites merged, adapters starting"

---

### Track B Setup (Infrastructure Lead)
**Responsible**: geoRouterExtended + regionFailoverManager + dataLocalityOptimizer → MultiRegionOrchestrator

**Tasks** (Day 1):
- [ ] Create branch: `feat/phase2-multiregionorchestrator`
- [ ] Generate consolidated skill structure
- [ ] Extract region state machine (health tracking, state transitions)
- [ ] Extract routing logic (latency, health, load balancing)
- [ ] Extract data locality logic (placement strategy, replication lag)
- [ ] Create unified region model

**Commits to make**:
1. `feat(phase2): create MultiRegionOrchestrator base`
2. `feat(phase2): add region state machine`
3. `feat(phase2): add routing engine`

**Standup Report**: "MultiRegionOrchestrator state machine complete, routing logic in progress"

---

### Track C Setup (Platform Lead)
**Responsible**: planning + decomposition + integration → WorkflowComposer

**Tasks** (Day 1):
- [ ] Create branch: `feat/phase4-workflowcomposer`
- [ ] Generate consolidated skill structure
- [ ] Create unified task/workflow model
- [ ] Extract phase planning logic
- [ ] Extract decomposition logic (recursive task breakdown)
- [ ] Create test consolidation plan

**Commits to make**:
1. `feat(phase4): create WorkflowComposer base`
2. `feat(phase4): add unified task model`
3. `feat(phase4): add phase planner`

**Standup Report**: "WorkflowComposer base and task model complete, decomposition logic in progress"

---

### Track D Setup (QA/DevOps Lead)
**Responsible**: Shared infrastructure, coordination, integration

**Tasks** (Day 1):
- [ ] Create base adapter framework class
- [ ] Set up config schema validation
- [ ] Create backward-compatibility test suite template
- [ ] Create shared test consolidation patterns
- [ ] Set up coordination spreadsheet (track progress)
- [ ] Document daily merge strategy

**Commits to make**:
1. `feat(shared): add BaseSkillAdapter framework`
2. `feat(shared): add config validation schema`
3. `test(shared): add backward-compatibility patterns`

**Standup Report**: "Adapter framework ready, config validation in place, coordination tracking setup"

---

## Days 2-5: Build Phase (Parallel Execution)

### Day 2: Adapters & Dependencies

**Track A**:
- [ ] Finish Phase 1.1 (base + models complete)
- [ ] Start Phase 1.2 (adapter layer)
- [ ] Start Phase 3.1 (ObservabilityPipeline base - parallel)

**Track B**:
- [ ] Finish Phase 2.1 (state machine + routing)
- [ ] Start Phase 2.2 (adapters)

**Track C**:
- [ ] Finish Phase 4.1 (base + task model)
- [ ] Start Phase 4.2 (adapters)

**Track D**:
- [ ] Complete adapter framework
- [ ] Start config consolidation tool
- [ ] Validate test merging patterns

---

### Day 3: Integration Begins

**Track A**:
- [ ] Finish Phase 1.2 (adapters)
- [ ] Start Phase 1.3 (update dependents: rootCauseAnalyzer, decisionMaking)
- [ ] Phase 3.1 (continue: collectors + aggregation)

**Track B**:
- [ ] Finish Phase 2.2 (adapters)
- [ ] Start Phase 2.3 (update dependents)

**Track C**:
- [ ] Finish Phase 4.2 (adapters)
- [ ] Start Phase 4.3 (update dependents: routing, taskIntake)

**Track D**:
- [ ] Config consolidation tool ready
- [ ] Validation checkpoints for each track
- [ ] Merge conflict prevention plan review

---

### Day 4: Cleanup & Parallel Start

**Track A**:
- [ ] Finish Phase 1.3 (dependents updated)
- [ ] Phase 1.4 (cleanup & verification)
- [ ] Phase 6 START (RCA plugin integration)
- [ ] Phase 3.2 (ObservabilityPipeline adapters)

**Track B**:
- [ ] Finish Phase 2.3 (dependents)
- [ ] Phase 2.4 START (verification)

**Track C**:
- [ ] Finish Phase 4.3 (dependents)
- [ ] Phase 5.1 START (DecisionEngine base - CAN START after Phase 4.3)

**Track D**:
- [ ] Code review preparation
- [ ] Test suite consolidation in progress
- [ ] Monitor for blocking issues

---

### Day 5: Verification Sprint

**Track A**:
- [ ] Phase 1 verification complete
- [ ] Phase 6 (RCA plugin) in progress
- [ ] Phase 3.3 (ObservabilityPipeline integration) complete

**Track B**:
- [ ] Phase 2.4 verification complete
- [ ] Prepare for code review

**Track C**:
- [ ] Phase 5.1 (DecisionEngine base) complete
- [ ] Phase 5.2 (adapters) in progress

**Track D**:
- [ ] All phases ready for code review
- [ ] Tests consolidated
- [ ] Documentation aggregated
- [ ] Merge strategy finalized

---

## Days 6-7: Code Review & Merge Preparation

### Day 6: Final Code Review Round

**All Tracks**:
- [ ] Phase code review starts (Track D coordinates)
- [ ] Address review feedback
- [ ] Finalize documentation
- [ ] Verify backward compatibility

**Track A**: Phase 1, 3, 6 code review  
**Track B**: Phase 2 code review  
**Track C**: Phase 4, 5 code review  
**Track D**: Cross-track review, integration testing

---

### Day 7: Pre-Merge Validation

**All Tracks**:
- [ ] Rebase branches on latest main
- [ ] Run full test suite locally (3,300+ tests)
- [ ] Verify no performance regression
- [ ] Final documentation check
- [ ] Prepare merge PRs

**Track A**: 3 PRs (Phase 1, 3, 6)  
**Track B**: 1 PR (Phase 2)  
**Track C**: 2 PRs (Phase 4, 5)  
**Track D**: Support PR (shared infrastructure)

---

## Day 8: Coordinated Merge & Verification

### Morning: Merge Window

**Merge Order** (1 hour gaps):
```
09:00 - Track B merges Phase 2 (independent, lowest risk)
10:00 - Track A merges Phase 1 (updates dependents after merge)
11:00 - Track A merges Phase 3 (no dependents)
12:00 - Track C merges Phase 4 (updates routing after merge)
13:00 - Track C merges Phase 5 (depends on Phase 4, safe after)
14:00 - Track A merges Phase 6 (RCA plugin, safe after Phase 1)
15:00 - Track D merges shared infrastructure
```

### Afternoon: Integration Testing

**Track D Leads**:
- [ ] Run full test suite (3,300+ tests) → Target: all passing
- [ ] Benchmark performance (vs baseline)
- [ ] Validate config consolidation
- [ ] Check no import cycles
- [ ] Verify adapters working

**All Tracks Support**:
- [ ] Pair with Track D on any issues
- [ ] Quick fixes for edge cases
- [ ] Document any surprises

---

## Daily Standup Template (9 AM, 15 min)

```
Track A: [Completed yesterday] | [Blocked by?] | [Today's goal]
Track B: [Completed yesterday] | [Blocked by?] | [Today's goal]
Track C: [Completed yesterday] | [Blocked by?] | [Today's goal]
Track D: [Coordination status] | [Issues to resolve] | [Today's focus]

Blockers: [Any cross-track issues?]
Critical Path: [On track? At risk?]
```

### Example (Day 2 Standup):
```
Track A: Phase 1.1 done, tests merged | None | Finish 1.2, start 3.1
Track B: Phase 2.1 done, state machine works | None | Finish 2.1, start 2.2
Track C: Phase 4.1 done, task model solid | None | Finish 4.1, start 4.2
Track D: Adapter framework ready | None | Config tool, validate merges

Blockers: None
Critical Path: On track (Phase 1 blocks Phase 6 on Day 5 - planned)
```

---

## Track-Specific Checklists

### Track A (Data Science Lead)

**Phase 1: PredictionEngine** (Days 1-4)
- [ ] Base engine structure created
- [ ] ARIMA implementation extracted
- [ ] Exponential smoothing extracted
- [ ] Seasonal decomposition implemented
- [ ] Adapters for all 3 old skills
- [ ] Dependents updated (rootCauseAnalyzer, decisionMaking)
- [ ] Tests merged (target: eliminate 2-3 duplicates)
- [ ] Verified backward compatibility
- [ ] Code review passed
- [ ] **Commit**: `feat(phase1): consolidate forecasting domain`

**Phase 3: ObservabilityPipeline** (Days 2-5)
- [ ] Metrics collection extracted
- [ ] Trace collection (OpenTelemetry) implemented
- [ ] Aggregation logic unified
- [ ] Export layer created (Prometheus, OTel)
- [ ] Adapters for metricsCollector, analyticsEngine, performanceTracing
- [ ] Consumers integrated (healthCheck, reportGenerator)
- [ ] Tests merged
- [ ] Code review passed
- [ ] **Commit**: `feat(phase3): consolidate observability stack`

**Phase 6: RCA Integration** (Days 4-5)
- [ ] rootCauseAnalyzer logic extracted
- [ ] Integrated as plugin into PredictionEngine
- [ ] Anomaly → RCA → recommend pipeline working
- [ ] Backward compatibility verified
- [ ] Code review passed
- [ ] **Commit**: `feat(phase6): integrate RCA into prediction engine`

---

### Track B (Infrastructure Lead)

**Phase 2: MultiRegionOrchestrator** (Days 1-5)
- [ ] Region state machine created
- [ ] Health tracking implemented
- [ ] Routing engine (latency + health aware)
- [ ] Data locality optimizer integrated
- [ ] Adapters for all 3 old skills
- [ ] tenantRouter implemented as adapter
- [ ] Failover scenarios tested
- [ ] Tests merged
- [ ] Code review passed
- [ ] **Commit**: `feat(phase2): consolidate multi-region infrastructure`

**Validation** (Day 5):
- [ ] Region failover scenario works
- [ ] Cross-region routing optimal
- [ ] Data locality respected in decisions
- [ ] No performance regression

---

### Track C (Platform Lead)

**Phase 4: WorkflowComposer** (Days 1-4)
- [ ] Unified task/workflow model created
- [ ] Phase planning extracted
- [ ] Decomposition logic (recursive)
- [ ] Composition/integration extracted
- [ ] Adapters for planning, decomposition, integration
- [ ] taskIntake integrated
- [ ] Tests merged
- [ ] Code review passed
- [ ] **Commit**: `feat(phase4): consolidate workflow composition`

**Phase 5: DecisionEngine** (Days 4-7)
- [ ] Unified scoring framework
- [ ] Rule-based strategy (routing)
- [ ] Heuristic strategy (multi-criteria decisions)
- [ ] ML strategy (intelligentOptimizer)
- [ ] Adapters for all 3 old skills
- [ ] Pluggable strategy switching working
- [ ] Learning feedback loop tested
- [ ] Tests merged
- [ ] Code review passed
- [ ] **Commit**: `feat(phase5): consolidate decision framework`

---

### Track D (QA/DevOps Lead)

**Shared Infrastructure**:
- [ ] BaseSkillAdapter framework created
- [ ] Config schema validation implemented
- [ ] Backward-compatibility patterns documented
- [ ] Test consolidation patterns created
- [ ] Config migration tool ready

**Coordination** (All 8 Days):
- [ ] Daily standup facilitation
- [ ] Track progress monitoring
- [ ] Merge conflict prevention
- [ ] Code review support
- [ ] Cross-track issue resolution
- [ ] Test suite management

**Pre-Merge** (Days 6-7):
- [ ] All code reviewed
- [ ] Integration test plan prepared
- [ ] Merge strategy locked in
- [ ] Rollback plan ready

**Merge Day** (Day 8):
- [ ] Orchestrate merge sequence
- [ ] Monitor test suite
- [ ] Quick-fix any issues
- [ ] Final verification pass

---

## Success Metrics (End of Day 8)

✅ **By End of Day**:
- [ ] 6 phases merged (Phase 1, 2, 3, 4, 5, 6)
- [ ] 3,300+ tests passing
- [ ] No performance regression (benchmarks passed)
- [ ] Zero critical issues post-merge
- [ ] ~4,000 lines of duplicate code eliminated
- [ ] All adapter layers working (backward compatibility 100%)

✅ **Verification**:
- [ ] Full test suite run: All passing
- [ ] Perf benchmarks: No regression
- [ ] Config consolidation: 50+ params → 25 params
- [ ] Documentation: All updated
- [ ] Dependent skills: All updated and tested

---

## Risk Handling

**If Track Falls Behind**:
- Other track(s) stop parallel work to help
- Example: Track A helps Track C catch up on Day 4
- Adjust merge schedule accordingly

**If Merge Conflict Arises**:
- Track D resolves immediately (coordinated merge window prevents most)
- Each phase waits 1 hour gap = time to fix conflicts
- Have merge conflict resolution protocol ready

**If Performance Regression Detected**:
- Day 8 afternoon: Investigate specific phase
- Likely culprit: New consolidation layer overhead
- Solution: Optimize caching, model loading
- Target: Fix within 1 hour, re-verify

**If Tests Fail Post-Merge**:
- Track lead + Track D pair on fix
- Likely issue: Adapter API mismatch or import cycle
- Solution: Quick adapter adjustment or re-export
- Target: All tests green within 2 hours

---

## Tools & Resources

**For Track Leads**:
- [SKILL_CONSOLIDATION_PLAN.md](SKILL_CONSOLIDATION_PLAN.md) — Detailed phase plans
- [SKILL_CONSOLIDATION_PARALLEL.md](SKILL_CONSOLIDATION_PARALLEL.md) — Parallel execution strategy
- `scripts/consolidation/consolidator.py` — Automation framework

**Shared**:
- Slack channel: #skill-consolidation (daily standup, quick asks)
- Spreadsheet: Track progress (Track D maintains)
- Git branches: Feature branches per track
- PR reviews: Use standard checklist from code-review skill

---

## Example Day 1 Terminal Session

```bash
# Track A Lead starts
git checkout -b feat/phase1-predictionengine
python scripts/consolidation/consolidator.py generate \
  --skill predictionEngine \
  --from forecastingEngine,costForecasting,anomalyDetector \
  --output skills/

# Verify structure created
ls -la skills/predictionEngine/
# → SKILL.md, skill.py, __init__.py, adapters/, tests/

# Extract models and commit
git add skills/predictionEngine/
git commit -m "feat(phase1): create PredictionEngine base structure"

# Report in standup
echo "✅ PredictionEngine base created, proceeding to extract models"
```

---

## Sign-Off

**Ready to execute with team sign-off on**:
- [ ] Parallel plan approved
- [ ] Track leads assigned and onboarded
- [ ] Daily standup scheduled
- [ ] Slack channel created
- [ ] Feature branches created per track
- [ ] Day 1 tasks understood and distributed

**Execution begins**: [Date]  
**Expected completion**: [Date + 8 days]  
**All phases in production by**: [Date + 10 days] (with 2-day buffer)

---

**Document**: CONSOLIDATION_EXECUTION_KIT.md  
**Status**: Ready to Launch  
**Next Step**: Assign track leads and hit Day 1 start button
