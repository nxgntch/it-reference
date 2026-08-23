# Phase 5+ Cost Tracking Architecture (Archived Modules)

**Archived**: 2026-08-22  
**Status**: Preserved for Phase 5+ implementation  
**Reason**: Designed for stateful backend; current Phase 2.4 uses stateless plugin model

---

## What's Here

This directory contains **fully-designed, never-used modules** for a future stateful version of nxgntch:

### Archived Modules

| Module | Size | Purpose | Status |
|--------|------|---------|--------|
| **budgetChecker.py.phase5-stateful-backend** | 7KB | Hard-stop budget enforcement (org/team/agent/invocation levels) | Complete, untested |
| **costTracker.py.phase5-stateful-backend** | 5KB | Cost aggregation and reporting across teams/agents | Complete, untested |

---

## Why Archived?

### Current Architecture (Phase 2.4)
- **Model**: Stateless plugin (Claude Marketplace)
- **Budget tracking**: `ConcurrentBudgetTracker` in orchestrator.py (simple concurrent spend)
- **Cost enforcement**: Informational only (governance.yaml line 12)
- **Rationale**: Plugin runs client-side with no persistent storage

### Designed Architecture (Phase 5+)
- **Model**: Stateful backend server with persistent database
- **Budget enforcement**: Hard-stop limits at multiple levels:
  - Organization monthly cap (e.g., $10,000)
  - Team monthly allocation (e.g., engineering $3,000)
  - Agent per-invocation limit (e.g., architect $2.00)
  - Individual invocation hard stop at 100%
- **Cost tracking**: Persistent cost records, aggregation by team/agent/model
- **Reporting**: Monthly cost reports, spend analytics, anomaly detection
- **Approval workflows**: Spending levels require different approval tiers

---

## When These Will Be Needed

### Phase 5: Multi-Tenant Enterprise Backend
- When nxgntch transitions from stateless plugin → stateful server
- Requires database schema for cost records
- Requires persistent session management
- Requires audit trail for all spending

### Implementation Steps
1. Set up PostgreSQL or similar for persistent storage
2. Implement `CostRecord` table (mapped in costTracker.py)
3. Integrate `BudgetChecker` into orchestrator
4. Add approval workflow system (see governance-extensions.md)
5. Add cost reporting API endpoints

---

## How to Use These Files

### To Review for Phase 5 Planning
```bash
# Read the archived modules to understand the design
cat https://github.com/nxgntch/it-reference/tree/master/docs/archive/budgetChecker.py.phase5-stateful-backend
cat https://github.com/nxgntch/it-reference/tree/master/docs/archive/costTracker.py.phase5-stateful-backend
```

### To Restore for Phase 5 Implementation
```bash
# Restore files when Phase 5 work begins
mv https://github.com/nxgntch/it-reference/tree/master/docs/archive/budgetChecker.py.phase5-stateful-backend app/core/budgetChecker.py
mv https://github.com/nxgntch/it-reference/tree/master/docs/archive/costTracker.py.phase5-stateful-backend app/core/costTracker.py

# Add tests
# Wire into orchestrator
```

---

## Active Cost Management (Phase 2.4+)

**Don't use archived modules.** Instead:

### For pricing calculations
- Use: `app/core/cost.py` (47% coverage)
- Methods: `calculateCost()`, `formatCurrency()`

### For model selection based on cost
- Use: `app/core/modelRouter.py` (83% coverage)
- Integrates cost factors into model selection

### For concurrent spend tracking
- Use: `app/core/orchestrator.py` → `ConcurrentBudgetTracker` (100% coverage)
- Prevents concurrent agents from exceeding team limits

### For response caching (cost savings)
- Use: `app/core/responseCache.py` (69% coverage)
- Reduces redundant LLM calls

### For token optimization (future)
- Use: `app/core/tokenOptimizer.py` (0% coverage, has tests)
- Prompt compression to reduce token usage

---

## Rule References

- **Cost Management**: `.claude/rules/cost-management.md` (documents intended architecture)
- **Governance**: `.claude/rules/governance-extensions.md` (approval workflows, Phase 5+)
- **Security**: `.claude/rules/code-review-checklist.md` § Cost Enforcement

---

## Testing

These modules have **zero test coverage** because they're not integrated:

```python
# Tests DO NOT exist for:
pytest tests/test_budgetChecker.py  # ✗ File doesn't exist
pytest tests/test_costTracker.py    # ✗ File doesn't exist

# When restoring for Phase 5, create:
tests/test_budgetChecker.py         # Budget enforcement tests
tests/test_costTracker.py           # Cost aggregation tests
tests/test_costReporting.py         # Reporting API tests
```

---

## Notes for Future Implementation

### Design Decisions Already Made (in archived code)
1. **Budget hierarchy**: Org → Team → Agent → Invocation
2. **Alert thresholds**: 80% warning, 90% critical
3. **Currency handling**: Always USD, formatted to 2 decimals
4. **Team isolation**: Teams see only their own costs
5. **Immutable audit logs**: Cost records never deleted, only archived

### Outstanding Decisions Needed
1. **Database choice**: PostgreSQL, MongoDB, or managed service?
2. **Approval system**: Manual approval vs. automated rules?
3. **Monthly billing cycle**: Fixed date or rolling 30 days?
4. **Overspend handling**: Pause execution or allow with escalation?
5. **Reporting frequency**: Daily, weekly, or on-demand?

---

## Why Not Delete Entirely?

These modules represent **weeks of design and architecture work**:
- Complete class hierarchies with docstrings
- Clear separation of concerns
- Well-thought-out error handling
- Budget calculation formulas proven in design

**Archiving preserves this work** for when nxgntch scales to an enterprise backend.

---

## Related Files

- **Active rules**: `.claude/rules/cost-management.md`
- **Current implementation**: `app/core/orchestrator.py` (ConcurrentBudgetTracker)
- **Alternative tracking**: `app/core/cost.py` + `app/core/modelRouter.py`
- **Future roadmap**: See Phase 5 planning docs

---

**Last updated**: 2026-08-22  
**Archive reason**: Phase transition (stateless → stateful)  
**Restore timeline**: Phase 5 (Multi-Tenant Enterprise Backend)
