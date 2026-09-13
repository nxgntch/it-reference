---

> ⚠️ **Authoritative source**: See [`docs/rules/performance-benchmarks.md`](../../docs/rules/performance-benchmarks.md) for the official cost model and budget allocation. This guide provides implementation details.

# Phase 8: Configuration Consolidation Guide

**Status**: ✅ COMPLETE  
**Date**: 2026-09-10  
**Effort**: 1-2 hours  
**Files Consolidated**: 8 core + 7 monitoring configs

---

## Summary

**Objective**: Audit, consolidate, and document YAML configuration files across the project.

**Deliverables**:
1. ✅ Configuration inventory & audit
2. ✅ Consolidation strategy (4-layer approach)
3. ✅ Best practices documentation
4. ✅ Validation checklist

**Outcomes**:
- Single source of truth for configuration management
- Clear file dependencies & loading order
- Unified validation strategy
- Reduced configuration drift risk

---

## Configuration Inventory

### Core Runtime Configs (8 files)

| File | Purpose | Scope | Status | Size |
|------|---------|-------|--------|------|
| **unified.yaml** | Consolidated agents + skills | Single source of truth | ✅ Phase 5 | ~500 lines |
| **agents.yaml** | Agent definitions & capabilities | Runtime agents | ✅ Current | ~80 lines |
| **models.yaml** | LLM pricing & tiers | Cost calculation | ✅ Current | ~65 lines |
| **skills.yaml** | Skill registry & assignments | Skill management | ✅ Current | ~200 lines |
| **governance.yaml** | Budget & approval workflows | Cost control | ✅ Current | ~50 lines |
| **orchestration.yaml** | Multi-agent orchestration | Performance tuning | ✅ Current | ~100 lines |
| **routing.yaml** | Routing strategy configuration | Routing behavior | ✅ Phase 2 | ~40 lines |
| **registry.yaml** | Docker registry configuration | DevOps/CI-CD | ✅ Current | ~30 lines |

**Total**: ~1,065 lines of configuration

### Monitoring Configs (7 files)

| File | Location | Purpose | Status |
|------|----------|---------|--------|
| **prometheus.yml** | services/monitoring/ | Metrics collection | ✅ Active |
| **alertmanager.yml** | services/monitoring/ | Alert routing | ✅ Active |
| **alerts.yml** | services/monitoring/ | Alert rules | ✅ Active |
| **loki-config.yml** | services/monitoring/ | Log aggregation | ✅ Active |
| **promtail-config.yml** | services/monitoring/ | Log forwarding | ✅ Active |
| **grafana/dashboards.yml** | services/monitoring/grafana/ | Dashboard config | ✅ Active |
| **grafana/prometheus.yml** | services/monitoring/grafana/ | Datasource config | ✅ Active |

**Note**: Monitoring configs are separate from application configs (different lifecycle, ownership, tooling).

### Scripts Config (1 file)

| File | Purpose |
|------|---------|
| **scripts/config.yaml** | Script execution configuration |

---

## Consolidation Strategy

### Layer 1: File Organization ✅

**Current Structure**:
```
config/
├── agents.yaml           (Agent definitions)
├── models.yaml           (Model pricing)
├── unified.yaml          (Consolidated - Phase 5)
├── governance.yaml       (Budget & approvals)
├── orchestration.yaml    (Orchestration settings)
├── routing.yaml          (Routing strategy)
├── skills.yaml           (Skill registry)
├── registry.yaml         (Docker registry)
└── README.md             (Documentation)
```

**Strengths**:
- Clear separation by concern (agents, models, governance, etc)
- Single directory (`config/`) for all runtime configs
- Each file has clear, focused purpose
- README.md documents loading order

**Improvements Made**:
- ✅ unified.yaml consolidates agents + skills (Phase 5)
- ✅ All timeouts consolidated to orchestration.yaml
- ✅ Clear SSOT (Single Source of Truth) designation

---

### Layer 2: Loading Order & Dependencies ✅

**Startup Sequence** (auto-validated):

```
1. models.yaml         ← Define LLM pricing first
   └─ Required by: agents.yaml (model references)

2. agents.yaml         ← Define agents
   ├─ Required by: governance.yaml (budget allocation)
   ├─ Required by: unified.yaml (consolidation)
   └─ Required by: skills.yaml (agent assignments)

3. skills.yaml         ← Define skills
   └─ Required by: governance.yaml (team skill allocation)

4. governance.yaml     ← Define budgets & approvals
   ├─ References: orchestration.yaml (timeout values)
   └─ Required by: orchestration (spending limits)

5. orchestration.yaml  ← Define orchestration behavior
   ├─ Consolidates: All timeout values (SSOT)
   └─ Required by: runtime (request handling)

6. routing.yaml        ← Define routing strategy
   ├─ References: agents.yaml (routing targets)
   └─ Optional: Only if custom routing enabled

7. registry.yaml       ← Define Docker registry
   └─ DevOps only: Not required for runtime

8. unified.yaml        ← Consolidated view (Phase 5)
   ├─ Mirrors: agents.yaml + skills.yaml
   └─ Optional: Can be used instead of separate files
```

**Dependency Graph**:
```
models.yaml
  ↓
agents.yaml ──→ governance.yaml ──→ orchestration.yaml
  ↓                   ↓
unified.yaml    routing.yaml
  ↓
skills.yaml
```

---

### Layer 3: Validation Strategy ✅

**Multi-Stage Validation**:

```
Stage 1: Syntax Validation (YAML parsing)
├─ File: Check YAML syntax (json5, strict)
├─ Tool: `python -m yaml` or online validator
└─ Fail: Invalid YAML blocks deployment

Stage 2: Schema Validation
├─ Check: Field types, required fields, ranges
├─ Tool: `pydantic` models or `jsonschema`
└─ Fail: Invalid schema prevents startup

Stage 3: Cross-Reference Validation
├─ Check: Agent references, model references, skill refs
├─ Tool: Custom validation script
└─ Fail: Undefined references prevent startup

Stage 4: Business Logic Validation
├─ Check: Budget caps, timeout reasonableness, SLA targets
├─ Tool: Custom business validation
└─ Warn: May succeed but generate warnings

Stage 5: Consistency Checks
├─ Check: No duplicate definitions, no orphaned configs
├─ Tool: `scripts/validate/checkConfigConsistency.py`
└─ Warn: Informational (doesn't prevent startup)
```

**Automated at Startup**:
```python
# app/startup.py - validateConfiguration()
1. Load all YAML files in order
2. Parse each to Python objects
3. Validate schema (Pydantic)
4. Validate cross-references
5. Validate business rules
6. Log validation results
7. Raise exception if Stage 1-3 fail
8. Log warnings for Stage 4-5
```

---

### Layer 4: Configuration Management Best Practices ✅

#### Adding a New Agent

1. **Update agents.yaml**:
   ```yaml
   - id: newAgent
     name: New Agent
     model: claude-sonnet-5
     description: Agent description
     capabilities:
       - capability1
       - capability2
   ```

2. **Update governance.yaml** (allocate budget):
   ```yaml
   teams:
     NewTeam:
       budget:
         monthly: 500000
   ```

3. **Update skills.yaml** (if agent has skills):
   ```yaml
   newAgent:
     - skill1
     - skill2
   ```

4. **Validate**:
   ```bash
   python -m app.startup.validateConfiguration
   ```

5. **Optional**: Update unified.yaml (Phase 5 consolidation)

#### Adjusting Budget

1. **Update governance.yaml**:
   ```yaml
   teams:
     Engineering:
       budget:
         monthly: 3000000  # ← Change here
   ```

2. **Validate & deploy**

#### Updating Model Pricing

1. **Update models.yaml**:
   ```yaml
   - id: claude-opus-5
     costInput: 0.005   # ← Update pricing
     costOutput: 0.00625
   ```

2. **Validate & deploy**

---

## Consolidation Opportunities

### ✅ Already Done

1. **Unified Configuration** (Phase 5)
   - `unified.yaml` consolidates agents + skills
   - Bidirectional mappings (agent→skills, skill→agents)
   - Single config option for all agent/skill definitions

2. **Timeout Consolidation** (Phase 19.1)
   - All timeouts in `orchestration.yaml` (SSOT)
   - `cache.yaml` references orchestration.yaml
   - `governance.yaml` references orchestration.yaml

3. **Configuration Documentation** (Phase 8)
   - `config/README.md` comprehensive
   - Clear loading order documented
   - Validation checklist provided

### 🔄 Potential Future Improvements

| Opportunity | Effort | Benefit | Priority |
|-------------|--------|---------|----------|
| **Environment-specific overrides** | Medium | Easier multi-env deploys | Low |
| **Hot-reload capability** | Medium | No-downtime config updates | Medium |
| **Config version history** | Small | Audit trail, easy rollback | Low |
| **Consolidated monitoring config** | Medium | Single monitoring hub | Low |
| **Configuration diff tool** | Small | Detect configuration drift | Medium |

---

## Key Findings

### Strengths ✅

1. **Well-organized**: Clear separation by concern (agents, models, governance)
2. **Documented**: README.md explains loading order and best practices
3. **Consolidated**: Unified.yaml and timeout consolidation reduce duplication
4. **Validated**: Startup validation catches configuration errors
5. **Dependency aware**: Loading order respects cross-file dependencies
6. **Clear SSOT**: Single source of truth clearly marked (orchestration.yaml for timeouts)
7. **DevOps separation**: Docker registry config separate from runtime config
8. **Monitoring isolated**: Monitoring configs in services/, not mixed with app config

### Areas for Improvement

1. **No hot-reload**: Configuration changes require restart
2. **No versioning**: No history of configuration changes
3. **No environment-specific overrides**: Single config file per environment
4. **No configuration drift detection**: Manual verification needed
5. **Monitoring consolidation**: 7 monitoring configs not centrally documented

---

## Metrics

| Metric | Value | Status |
|--------|-------|--------|
| **Core runtime configs** | 8 files | ✅ Audited |
| **Monitoring configs** | 7 files | ✅ Identified |
| **Total lines of configuration** | ~1,065 | ✅ Documented |
| **Loading order defined** | 8 stages | ✅ Clear |
| **Validation stages** | 5 stages | ✅ Comprehensive |
| **Files with SSOT designation** | 2 | ✅ Clear |

---

## Related Documentation

### Existing Guides

- **Runtime Configuration**: `config/README.md` (comprehensive)
- **Configuration Schema**: `config/SCHEMA.md` (SSOT for field definitions)
- **Cost Management**: `docs/guides/operations/COST_MANAGEMENT.md` (budget config)
- **Governance Policies**: `docs/guides/operations/GOVERNANCE.md` (spending approvals)

### Phase 8 Documentation

- **CI/CD Hub**: `.github/README.md` (10 workflows documented)
- **CI/CD Consolidation Guide**: `docs/work/completed/phase8/CI_CD_CONSOLIDATION_GUIDE.md`
- **Configuration Consolidation Guide**: This file

---

## Implementation Checklist

- [x] **Audit**: All 8 config files examined
- [x] **Inventory**: Created table of all files
- [x] **Dependencies**: Mapped loading order
- [x] **Validation**: Documented 5-stage validation
- [x] **Best practices**: Common tasks documented
- [x] **Findings**: Identified strengths + opportunities

### Integration Points

- [ ] Link from `config/README.md` → Phase 8 documentation
- [ ] Add to `docs/INDEX.md` → Configuration section
- [ ] Cross-reference from CI/CD guide

---

## Next Steps

### Immediate (This Week)

1. Share Phase 8 documentation with team
2. Update `docs/INDEX.md` with links to Phase 8 guides

### Short-term (Next 2 Weeks)

1. Evaluate hot-reload capability (effort vs benefit)
2. Create configuration drift detection script
3. Document environment-specific overrides strategy

### Medium-term (Next Month)

1. Implement configuration versioning
2. Create centralized monitoring configuration hub
3. Add configuration diff tool for change review

---

## Appendix: Quick Reference

### Configuration Files SSOT

| Aspect | File | Note |
|--------|------|------|
| **Model pricing** | models.yaml | ← Check here for LLM costs |
| **Agent definitions** | agents.yaml | ← Single agent source |
| **Skill registry** | skills.yaml | ← All skills defined here |
| **Budget allocation** | governance.yaml | ← Spending limits enforced |
| **Timeouts** | orchestration.yaml | ← SSOT for all timeouts |
| **Routing rules** | routing.yaml | ← Delegation logic |
| **Docker registry** | registry.yaml | ← Container registry config |
| **Consolidated view** | unified.yaml | ← Phase 5 consolidation |

### Validation Commands

```bash
# Syntax check
python -c "import yaml; yaml.safe_load(open('config/models.yaml'))"

# Full validation
python -m app.startup.validateConfiguration

# Schema validation
pydantic-validate config/

# Check config consistency
python scripts/validate/checkConfigConsistency.py --verbose
```

### Environment Variables

```bash
# Required at startup
export NXGN_CONFIG_DIR="config/"

# Optional
export LOG_LEVEL="INFO"
export ENVIRONMENT="production"
```

---

**Last Updated: 2026-09-10  
**Configuration Consolidation Status**: ✅ COMPLETE  
**Total Configuration Lines**: ~1,065  
**Validation Stages**: 5  
**SSOT Files**: 2 (orchestration.yaml, agents.yaml)
