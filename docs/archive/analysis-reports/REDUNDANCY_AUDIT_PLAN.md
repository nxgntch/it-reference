# Redundancy Audit & Consolidation Plan

**Branch**: `claude/redundancy-audit-q231cc`  
**Status**: Planning Phase  
**Created**: 2026-09-02  
**Target Completion**: 2026-09-15 (2 weeks)

---

## Summary of Findings

| Category | Issues | LOC Impact | Effort |
|----------|--------|-----------|--------|
| **Configuration Redundancy** | 21 violations | — | 8-12 hours |
| **Orphaned Code** | 5 skills | 1,187 LOC | 2-3 hours |
| **Session Memory Waste** | MCP + archives | ~75k tokens | 4-6 hours |
| **Documentation Duplication** | IDE/Runtime overlap | — | 3-4 hours |
| **Total** | **31 items** | **1,187 LOC** | **17-25 hours** |

---

## TIER 1: CRITICAL (Week 1) — 5-7 hours

### 1.1: Configuration SSOT Violations (9 critical issues)
**Status**: Partially fixed (PR #284 draft)  
**Remaining Work**: Verify, test, merge

| Issue | File | Current Fix | Action | Effort |
|-------|------|-------------|--------|--------|
| Model versioning conflict | `startup-critical.yaml` | Aligned with agents.yaml | ✅ DONE (PR #284) | 0 |
| Skill name mismatch | `agents.yaml` line 41 | "anomalyDetector" → registry | ✅ DONE (PR #284) | 0 |
| GPT fallback policy violation | `routing.yaml` line 299 | Removed GPT references | ✅ DONE (PR #284) | 0 |
| Version mismatch | `plugin.json` | Unified to 1.1.0 | ✅ DONE (PR #284) | 0 |
| Model tier gap | `agents.yaml` line 106-108 | Added "high" tier for Opus | ✅ DONE (PR #284) | 0 |
| Duplicate tier mapping | `orchestration.yaml` | Removed + SSOT reference | ✅ DONE (PR #284) | 0 |
| Agent skill references | Multiple lines | Updated to registry | ✅ DONE (PR #284) | 0 |
| Timeout duplicates | `cache.yaml` | Removed with SSOT note | ✅ DONE (PR #284) | 0 |
| Undocumented skills | `skills.yaml` | Registered 3 director skills | ✅ DONE (PR #284) | 0 |

**Deliverables**:
- [ ] Review PR #284 for completeness
- [ ] Run validation: `config/validate-all.sh` or equivalent
- [ ] Verify zero broken skill references (grep verification)
- [ ] Merge PR #284 to main
- [ ] Update AUDIT.md with completion status

**Success Criteria**:
- ✅ All 9 CRITICAL issues closed
- ✅ config/validate-all.sh passes
- ✅ 3,044+ tests still passing
- ✅ Zero new config inconsistencies

**Effort**: 2-3 hours (review + validation + merge)

---

### 1.2: Orphaned Code Removal (5 skill files)
**Status**: Identified, not yet removed  
**Action**: Delete + verify no references

| File | Size | References | Action | Effort |
|------|------|-----------|--------|--------|
| `skills/agents/cacheEffectiveness.py` | 235 LOC | 0 verified | Delete | 10m |
| `skills/agents/latencyAnalyzer.py` | 237 LOC | 0 verified | Delete | 10m |
| `skills/agents/loadManagementOptimizer.py` | 288 LOC | 0 verified | Delete | 10m |
| `skills/agents/modelRoutingOptimizer.py` | 183 LOC | 0 verified | Delete | 10m |
| `skills/agents/reliabilityAssessor.py` | 244 LOC | 0 verified | Delete | 10m |

**Verification Steps**:
```bash
# Re-verify no references before deletion
grep -r "cacheEffectiveness\|latencyAnalyzer\|loadManagementOptimizer\|modelRoutingOptimizer\|reliabilityAssessor" app/ tests/ scripts/ skills/ config/ --exclude-dir=agents

# After deletion, run tests to confirm no breakage
pytest tests/ --cov=app -q
```

**Deliverables**:
- [ ] Re-verify zero references for all 5 files (before deletion)
- [ ] Delete all 5 skill files
- [ ] Run full test suite
- [ ] Verify config consistency (no orphaned refs in agents.yaml)
- [ ] Commit: "refactor: remove 5 orphaned skill implementations (1,187 LOC)"

**Success Criteria**:
- ✅ 5 files deleted
- ✅ grep verification returns zero matches
- ✅ 3,044+ tests still passing
- ✅ No config references remain

**Effort**: 2-3 hours (verification + deletion + testing)

---

## TIER 2: HIGH (Week 1-2) — 6-10 hours

### 2.1: HIGH Priority Configuration Issues (4 items)
**Status**: Identified, not yet fixed  
**Action**: Implement fixes beyond PR #284

| Issue | Location | Fix | Complexity | Effort |
|-------|----------|-----|-----------|--------|
| Timeout duplicate removal | `cache.yaml` | Remove acknowledged duplicates | Low | 30m |
| Cost tier consolidation | agents.yaml + orchestration.yaml | Single source (agents.yaml) | Medium | 1h |
| Policy enforcement gap | routing.yaml | Verify no deprecated references | Low | 30m |
| Test model validation | orchestration.yaml | Verify all referenced models exist | Low | 30m |

**Deliverables**:
- [ ] Audit `cache.yaml` for timeout duplicates (add SSOT comment)
- [ ] Consolidate cost tier mapping to `agents.yaml` only
- [ ] Audit `routing.yaml` for deprecated/GPT model references
- [ ] Validate all models in orchestration.yaml exist in agents.yaml
- [ ] Create HIGH_PRIORITY_CONFIG_FIXES.md documenting changes
- [ ] Commit: "refactor: consolidate configuration SSOT violations"

**Success Criteria**:
- ✅ Zero duplicate definitions
- ✅ Single source for tiers, timeouts, policies
- ✅ All model references valid
- ✅ Config validation passes

**Effort**: 2-3 hours

---

### 2.2: Skill Registry Completion (IDE/Runtime Parity)
**Status**: Partial (from Phase 10 consolidation)  
**Action**: Verify merged skills have consistent naming

| Skill Pair | IDE Version | Runtime Version | Status | Action |
|-----------|-----------|-------------|--------|--------|
| code-review | Enhanced in PR #… | codeReview v1.1 | ✅ Merged | Verify naming consistency |
| documentation-auditor | Merged | docReviewer v1.1 | ✅ Merged | Update cross-refs |
| docOptimizer | Merged | docUpdater v1.1 | ✅ Merged | Document relationship |

**Deliverables**:
- [ ] Audit `.claude/skills/` IDE implementations for references to removed skills
- [ ] Update PLATFORM_SKILLS_INVENTORY.md with v1.1 versions
- [ ] Document IDE→Runtime mapping in skills/README.md
- [ ] Verify config/skills.yaml lists only active skills

**Success Criteria**:
- ✅ No stale IDE skill references
- ✅ Merged pairs documented with mapping
- ✅ Inventory reflects current state
- ✅ Zero duplicates across IDE/Runtime

**Effort**: 2 hours

---

## TIER 3: MEDIUM (Week 2) — 4-6 hours

### 3.1: Documentation Deduplication
**Status**: Identified (from Phase 5 cleanup)  
**Action**: Consolidate IDE/Runtime guides

| Issue | Location | Status | Action | Effort |
|-------|----------|--------|--------|--------|
| IDE vs Runtime skill docs | `.claude/skills/` + `skills/` | Duplicated content | Create unified reference | 1h |
| Testing guide archives | `docs/guides/development/` | Split across files | Consolidate to single SSOT | 1h |
| Configuration guide overlap | Multiple files | Scattered examples | Create `config/README.md` guide | 1h |
| Deployment docs redundancy | `docs/guides/operations/` | Multiple versions | Create single DEPLOYMENT.md | 1h |

**Deliverables**:
- [ ] Create `docs/guides/SKILL_DEVELOPMENT.md` (IDE + Runtime unified)
- [ ] Create `config/CONFIGURATION_GUIDE.md` (centralized config reference)
- [ ] Audit & consolidate deployment documentation
- [ ] Update LINK_MAP.md with dedup results
- [ ] Add redirect comments to archived/redundant docs

**Success Criteria**:
- ✅ Single source for each topic
- ✅ Cross-references updated
- ✅ Archived docs marked as superseded
- ✅ LINK_MAP reflects consolidation

**Effort**: 3-4 hours

---

### 3.2: Session Memory Optimization (Token Savings)
**Status**: Partially done (15k tokens saved in Phase 5)  
**Remaining**: MCP tools (~50-60k tokens)

| Tool Set | Status | Tokens | Action | Effort |
|----------|--------|--------|--------|--------|
| Figma MCP | Unused | 15-20k | Disable via MCP allowlist | 30m |
| Notion MCP | Unused | 15-20k | Disable via MCP allowlist | 30m |
| Context7 | Unused | 15-20k | Disable via MCP allowlist | 30m |
| Large reference docs | Archived in Phase 5 | 15k saved | Verify archived → docs/guides/ | 30m |

**Deliverables**:
- [ ] Document disabled MCP tools in `.claude/MCP_TOOLS_MANIFEST.md`
- [ ] Test session startup with MCP disabling (if platform supports)
- [ ] Measure token usage before/after
- [ ] Update AUDIT.md with token savings results
- [ ] Document in dev guide: "MCP tools disabled for session optimization"

**Success Criteria**:
- ✅ MCP tools disabled (if platform supports allowlists)
- ✅ Session memory reduced by 50-60k tokens
- ✅ Startup time not impacted
- ✅ Token usage documented in AUDIT.md

**Effort**: 2 hours (mostly waiting on platform support)

---

## TIER 4: OPTIONAL ENHANCEMENTS (After Tier 1-3)

### 4.1: Configuration Schema Validation
**Add to TIER 3 if time permits** — Creates durable consistency checks

**Goal**: Prevent future configuration SSOT violations

**Actions**:
- [ ] Create `config/schema.json` (jsonschema for all YAML configs)
- [ ] Add pre-commit hook: `validate-config.sh`
- [ ] Document in CLAUDE.md under Development section

**Effort**: 4-6 hours (one-time investment, high ROI)

---

### 4.2: Dead Code Detection Automation
**Add to TIER 3 if time permits** — Ongoing maintenance

**Goal**: Catch future orphaned code early

**Actions**:
- [ ] Add to CI: unused import detection (ruff rule)
- [ ] Add to CI: unused function detection (grep + custom script)
- [ ] Document in `../../docs/rules/coding.md`

**Effort**: 3-4 hours

---

## Minimal Action Plan

**Start here. Do these in order.**

1. **Merge PR #284** (30 min)
   - Review for completeness
   - Run: `pytest tests/ -q` → confirm 3,044+ pass
   - Merge to main

2. **Delete 5 orphaned skills** (30 min)
   ```bash
   rm skills/agents/cacheEffectiveness.py
   rm skills/agents/latencyAnalyzer.py
   rm skills/agents/loadManagementOptimizer.py
   rm skills/agents/modelRoutingOptimizer.py
   rm skills/agents/reliabilityAssessor.py
   pytest tests/ -q  # confirm still pass
   git commit -m "refactor: remove 5 orphaned skills (1,187 LOC)"
   ```

3. **Fix 4 HIGH config issues** (1 hour)
   - Remove timeout duplicates from `cache.yaml` (add SSOT note)
   - Consolidate cost tiers to `agents.yaml` only
   - Verify no GPT references in `routing.yaml`
   - Validate model references in `orchestration.yaml`

4. **Deduplicate docs** (1.5 hours)
   - Create `docs/guides/SKILL_DEVELOPMENT.md` (IDE + Runtime unified)
   - Create `config/CONFIGURATION_GUIDE.md` (centralized config reference)
   - Update `LINK_MAP.md` to reflect consolidation

5. **Disable unused MCP tools** (30 min)
   - Add notes to `.claude/MCP_TOOLS_MANIFEST.md` listing disabled tools
   - Wait for platform MCP allowlist support to activate

**Total effort: ~4 hours of active work**  
**Test suite: Run after each step to catch breakage immediately**

---

## Success Criteria (Overall)

| Category | Target | Verification |
|----------|--------|---------------|
| **Configuration** | Zero SSOT violations | config-validate.sh passes |
| **Code Quality** | 1,187 LOC orphaned removed | grep finds zero references |
| **Tests** | 3,044+ tests passing | pytest runs clean |
| **Memory** | 75k token savings | MCP tools disabled + AUDIT.md updated |
| **Documentation** | No duplication | LINK_MAP reflects consolidation |
| **Security** | Policy compliance | No deprecated models in routing |

---

## Dependencies & Risks

### Dependencies
- **PR #284 merge** blocks Tier 1.1 completion
- **Config validation script** needed for Tier 1.1 verification
- **Platform MCP allowlist support** needed for Tier 3.2 full benefit

### Risks
- **Incomplete grep verification** could leave stale references → Mitigate: Double-check before deletion
- **Test breakage** if orphaned skills have hidden dependencies → Mitigate: Run full test suite after each deletion
- **Config file conflicts** if merging PRs in parallel → Mitigate: Serialize config changes

---

## Rollback Plan

If issues arise:

1. **Config changes**: Revert specific PR or re-run config fixes
2. **Deleted files**: Restore from git history (`git checkout HEAD~ -- <file>`)
3. **Tests broken**: Identify affected test, add to skip list, investigate

**Abort condition**: If any Tier 1 test fails after changes, pause and investigate before continuing.

---

## Tracking & Handoff

**This Plan**:
- [ ] Create branch: `claudy/redundancy-consolidation-phase1` for Tier 1-2 work
- [ ] Link to GitHub issues if applicable
- [ ] Update AUDIT.md weekly with progress
- [ ] Final commit message: "fix: redundancy audit consolidation (Tier 1-3, 21 issues)"

**Deliverables Checklist**:
- [ ] Tier 1.1: Config SSOT — PR merged + tests passing
- [ ] Tier 1.2: Orphaned code — 5 files deleted + zero references
- [ ] Tier 2.1: HIGH config — consolidated + validated
- [ ] Tier 2.2: Skills parity — IDE/Runtime aligned
- [ ] Tier 3.1: Docs dedup — LINK_MAP updated
- [ ] Tier 3.2: Memory optimization — tokens saved documented

---

## References

- **Audit findings**: AUDIT.md (line 1504-1712)
- **SSOT violations detail**: AUDIT.md line 1597-1712
- **Orphaned code detail**: AUDIT.md line 1504-1594
- **PR #284**: Configuration consolidation (in draft)
- **Phase 10**: Skills consolidation baseline
- **Phase 5**: Initial memory optimization

---

**Last Updated**: 2026-09-02  
**Owner**: (you)  
**Status**: 🟡 Planning → Ready for execution
