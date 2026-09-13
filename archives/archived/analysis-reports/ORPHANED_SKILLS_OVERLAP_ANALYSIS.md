# Orphaned Skills: Overlap Analysis & Recommendations

**Analysis Date**: 2026-09-02  
**Scope**: 6 orphaned Phase 6 skills vs. 32 registered skills  
**Recommendation**: Remove 4, consider 2

---

## Summary

| Skill | Overlap Level | Redundancy | Safe to Remove? |
|-------|---------------|-----------|-----------------|
| **costDashboard** | Medium | Partial (dashboardConsumer exists) | ⚠️ CAUTION |
| **modelChoiceOptimizer** | High | High (intelligentOptimizer covers) | ✅ YES |
| **performanceOptimizer** | High | High (intelligentOptimizer covers) | ✅ YES |
| **costOptimizationRecommender** | Very High | Very High (costIntelligence covers) | ✅ YES |
| **autoScalingManager** | Low | Low (no registered equivalent) | ⚠️ KEEP IF NEEDED |
| **phase6Assessment** | Medium | Medium (meta-skill, integration) | ✅ YES |

---

## Detailed Analysis

### 1. costDashboard ⚠️ CAUTION

**Purpose**: Real-time cost monitoring dashboard with team spend, budget status, trends, anomalies.

**Registered Equivalent**: 
- **dashboardConsumer** — "Consult executive, operations, and metrics dashboards for context-aware decision making"
- **reportGenerator** — "Automated report generation and scheduling"
- **costIntelligence** — "Analyze cost implications... provides forecasting and recommendations"

**Overlap Assessment**:
- dashboardConsumer suggests dashboard *consumption* (reading dashboards), not *creation*
- costDashboard is about *creating* cost-specific dashboards
- reportGenerator might handle some reporting, but costDashboard is more real-time
- costIntelligence handles analysis, not visualization

**Verdict**: **PARTIAL OVERLAP** — dashboardConsumer overlaps in intent but seems different in scope
- dashboardConsumer = read/consume existing dashboards
- costDashboard = create/display cost dashboards

**Recommendation**: 
- ❌ **REMOVE if** dashboardConsumer provides cost dashboard functionality
- ✅ **KEEP if** costDashboard adds real-time visualization costIntelligence doesn't provide
- **Action**: Check dashboardConsumer implementation first before deleting

---

### 2. modelChoiceOptimizer ✅ YES - REMOVE

**Purpose**: Model selection optimization, evaluates cost/performance trade-offs for model choice.

**Registered Equivalent**:
- **intelligentOptimizer** — "ML-driven resource optimization with reinforcement learning feedback"

**Overlap Assessment**:
- intelligentOptimizer explicitly handles "resource optimization"
- Model choice is a core resource optimization decision
- Reinforcement learning in intelligentOptimizer would include model selection
- High overlap in capability

**Verdict**: **HIGHLY REDUNDANT**

**Recommendation**: ✅ **REMOVE** — intelligentOptimizer already covers model choice optimization
- Both do ML-driven optimization
- No unique functionality in modelChoiceOptimizer that intelligentOptimizer doesn't cover
- Safe to delete

---

### 3. performanceOptimizer ✅ YES - REMOVE

**Purpose**: Hot path identification, caching recommendations, parallelization analysis, cost-aware optimization.

**Registered Equivalent**:
- **intelligentOptimizer** — "ML-driven resource optimization"
- **analyticsEngine** — "Advanced analytics and metric correlation analysis"
- **forecastingEngine** — "Time-series forecasting"

**Overlap Assessment**:
- intelligentOptimizer: "parameter tuning" includes performance tuning
- analyticsEngine: "metric correlation" is core to finding hot paths
- performanceOptimizer is a Phase 6 component (performance profiling work)
- Its functionality (caching, parallelization) is pattern-matching that intelligentOptimizer would handle

**Verdict**: **HIGHLY REDUNDANT**

**Recommendation**: ✅ **REMOVE** — intelligentOptimizer + analyticsEngine cover this functionality
- Performance optimization is resource optimization (intelligentOptimizer's domain)
- Hot path analysis is pattern correlation (analyticsEngine's domain)
- No unique value beyond what's registered

---

### 4. costOptimizationRecommender ✅ YES - REMOVE

**Purpose**: Actionable cost optimization recommendations (model alternatives, resource utilization, batch optimization, cost impact).

**Registered Equivalent**:
- **costIntelligence** — "Analyze cost implications... provides cost forecasting and optimization recommendations"
- **intelligentOptimizer** — "ML-driven resource optimization"

**Overlap Assessment**:
- costIntelligence *explicitly* provides "optimization recommendations"
- costOptimizationRecommender does cost optimization recommendations
- This is a **direct duplicate** in purpose
- High redundancy

**Verdict**: **VERY HIGHLY REDUNDANT**

**Recommendation**: ✅ **REMOVE** — costIntelligence already provides this exact function
- costIntelligence handles cost analysis + recommendations
- costOptimizationRecommender is redundant
- Safe to delete without loss of functionality

---

### 5. autoScalingManager ⚠️ CONDITIONAL KEEP

**Purpose**: Real-time scaling decisions (up/down/maintain) based on load, latency, budget, predictions. Cost-aware scaling with SLA compliance.

**Registered Equivalent**:
- ❌ **No direct equivalent found**
- Possibly: **intelligentOptimizer** (optimization) or **analyticsEngine** (predictions)

**Overlap Assessment**:
- autoScaling is infrastructure-level operation
- intelligentOptimizer is general resource optimization (higher-level)
- autoScalingManager is specialized for Kubernetes/infrastructure scaling
- **Low overlap** — fills a unique niche

**Verdict**: **UNIQUE FUNCTIONALITY**

**Recommendation**: ⚠️ **CONDITIONAL**
- ✅ **KEEP if** this is used in production (autoScaling is important for cost control)
- ❌ **REMOVE if** it's only Phase 6 experimental work and not actively needed
- **Action**: Check if autoScalingManager is used in any agent workflows or just Phase 6 experiments

---

### 6. phase6Assessment ✅ YES - REMOVE

**Purpose**: Meta-skill, unified interface to Phase 6 components (profiler, auto-scaler, analytics, baselines). Provides assessment + optimization reporting + baseline tracking.

**Registered Equivalent**:
- **reportGenerator** — "Automated report generation and scheduling"
- **analyticsEngine** — "Advanced analytics and metric correlation"
- **intelligentOptimizer** — "Optimization recommendations"

**Overlap Assessment**:
- phase6Assessment is a *wrapper* around Phase 6 tools
- It provides assessment, reporting, and roadmap planning
- These functions are covered by reportGenerator + analyticsEngine + intelligentOptimizer
- It's a meta-coordination skill, not a core functional skill

**Verdict**: **PARTIALLY REDUNDANT**

**Recommendation**: ✅ **REMOVE** — Higher-level skills (agent coordination) handle this
- Core functions are covered by reportGenerator + analyticsEngine
- phase6Assessment was a Phase 6-specific wrapper
- Not needed if Phase 6 components are integrated into main flow
- Safe to delete

---

## Action Plan

### Immediate Remove (Safe, High Confidence)

```bash
# Remove these 3 — very high overlap with registered skills
rm -r skills/modelChoiceOptimizer
rm -r skills/performanceOptimizer
rm -r skills/costOptimizationRecommender
```

**Why safe**: Registered skills (intelligentOptimizer, analyticsEngine, costIntelligence) already provide this functionality.

### Likely Remove (Moderate Confidence)

```bash
# Remove this 1 — meta-skill, wrapper around others
rm -r skills/phase6Assessment
```

**Why safe**: reportGenerator + analyticsEngine handle the core functions.

### Conditional (Requires Investigation)

**costDashboard**:
- Check if dashboardConsumer implementation covers cost dashboards
- If yes: remove
- If no (dashboardConsumer is generic): consider keeping OR create minimal version in dashboardConsumer

**autoScalingManager**:
- Check if used in production agent workflows
- Check if intelligentOptimizer covers scaling decisions
- If Phase 6 experimental only: remove
- If used in production: keep and register

---

## Testing After Removal

After removing skills, run:

```bash
# 1. Validate config (no broken references)
python config/validate-config.py

# 2. Detect remaining dead code
python config/detect-dead-code.py

# 3. Verify tests still pass
pytest tests/ -q

# 4. Check no broken imports
grep -r "modelChoiceOptimizer\|performanceOptimizer\|costOptimizationRecommender\|phase6Assessment" app/ tests/ config/ --include="*.py" --include="*.yaml"
```

Expected result: All checks pass with 0 orphaned skills.

---

## Overlap Summary by Function

| Function | Orphaned Skill | Registered Equivalent | Verdict |
|----------|---|---|---|
| Cost tracking | costIntelligence | costIntelligence | ✅ Covered |
| Cost dashboards | costDashboard | dashboardConsumer (?) | ⚠️ Check |
| Cost recommendations | costOptimizationRecommender | costIntelligence | ✅ Covered (Remove) |
| Model selection | modelChoiceOptimizer | intelligentOptimizer | ✅ Covered (Remove) |
| Performance tuning | performanceOptimizer | intelligentOptimizer + analyticsEngine | ✅ Covered (Remove) |
| Scaling decisions | autoScalingManager | intelligentOptimizer (?) | ⚠️ Check |
| Assessment/reporting | phase6Assessment | reportGenerator + analyticsEngine | ✅ Covered (Remove) |

---

## Recommendation Summary

**Conservative Approach** (Safest):
- Remove: modelChoiceOptimizer, performanceOptimizer, costOptimizationRecommender, phase6Assessment
- Keep: costDashboard, autoScalingManager (investigate both)
- Expected result: 2 skills remain (need re-registration)

**Aggressive Approach** (Maximum cleanup):
- Remove: All 6
- Assumption: All functionality covered by registered skills
- Risk: Might lose specialized functionality

**Recommended Approach** (Balanced):
1. Remove 4 safe ones immediately (modelChoiceOptimizer, performanceOptimizer, costOptimizationRecommender, phase6Assessment)
2. Investigate costDashboard (check dashboardConsumer implementation)
3. Investigate autoScalingManager (check if used in production)
4. Re-register costDashboard OR autoScalingManager if still needed

---

## References

- **Registered Skills**: config/skills.yaml (32 total)
- **Orphaned Skills**: skills/{costDashboard,performanceOptimizer,...}/
- **Dead Code Detector**: config/detect-dead-code.py
- **Config Validator**: config/validate-config.py

---

**Last Updated**: 2026-09-02  
**Author**: Phase 7 Analysis  
**Next Step**: Implement recommended removals + run tests
