# Configuration Audit Report - Post-Plugin Integration

**Date**: 2026-09-12  
**Auditor**: Configuration & Documentation Audit  
**Scope**: All configurations after adding 3 plugins (ponytail, superpowers, planning-with-files)

---

## Executive Summary

**Status**: ⚠️ **STALE DATA FOUND** - Multiple configuration and documentation files contain outdated skill/capability counts

**Severity**: Medium (data consistency issue, not functional issue)

**Affected Areas**:
- Skill count declarations (26 → 51+)
- Capability declarations (22 → 30+)
- Documentation references
- Agent skill assignments

**Action Items**: 17 files need updates

---

## Detailed Findings

### 1. CRITICAL: Configuration Files (Must Update)

#### 🔴 `.claude/plugin.json` (Line 66)
**Issue**: Says "26" skills total, now 51+
```json
"skills": {
  "total": 26,  // ❌ STALE - should be 51+
```
**Impact**: Plugin metadata incorrect
**Fix**: Update to 51+ and update agent skill counts

---

#### 🔴 `config/skills.yaml` (Line 3)
**Issue**: Header says "26 skills", missing plugin skills
```yaml
# 26 skills: CEO/Org (8), Engineering (8), Research (4), Analytics (4), Documentation (2)
# ❌ STALE - Should be 51+ (30 core + 4 ponytail + 12 superpowers + 1 planning)
```
**Impact**: Skill registry incomplete, doesn't include plugin skills
**Fix**: Update header and add all 17 plugin skills to the registry

---

### 2. DOCUMENTATION: Outdated References (17 files)

#### 🟡 Files Referencing "34 skills" (6 files)
- `docs/guides/agents/ORCHESTRATOR_INTEGRATION.md` (line says 34)
- `docs/guides/development/README.md` (mentions "34 skills")
- `docs/guides/development/SKILL_DEVELOPMENT_HANDBOOK.md` (multiple mentions of "34 skills")
- `docs/guides/reference/ARCHITECTURE_REFERENCE.md` (mentions 34 skills)
- `docs/guides/reference/LINK_MAP.md` (mentions 34 skills)
- `docs/ssot/ARCHITECTURE.md` (mentions 34 skills)

**Issue**: All say "34 skills" (outdated from previous audit)
**Fix**: Update all to "51+ skills (30 core + 17 plugin)"

---

#### 🟡 Files Referencing "28 skills" (6 files)
- `docs/ssot/SSOT_AUDIT.md` (multiple references: lines 28, 40, etc.)
- Various inventory lists

**Issue**: Older count from before plugin integration
**Fix**: Update to "51+ skills"

---

### 3. MISSING: Plugin Skills Not in Core Registry

#### 🔴 `config/skills.yaml` Missing:
**Ponytail Skills (4)**:
- [ ] ponytailMinimalism
- [ ] ponytailReview
- [ ] ponytailAudit
- [ ] ponytailDebt

**Superpowers Skills (12)**:
- [ ] brainstormingViz
- [ ] writingPlans
- [ ] subagentDrivenDevelopment
- [ ] testDrivenDevelopment
- [ ] systematicDebugging
- [ ] requestingCodeReview
- [ ] receivingCodeReview
- [ ] verificationBeforeCompletion
- [ ] usingGitWorktrees
- [ ] dispatchingParallelAgents
- [ ] finishingDevelopmentBranch
- [ ] writingSkills

**Planning-with-Files Skills (1)**:
- [ ] planningWithFiles

**Status**: All 17 should be added to config/skills.yaml

---

### 4. INCOMPLETE: Agent Skill Assignments

#### 🟡 `config/agents.yaml` and `.claude/plugin.json`
**Issue**: Agent skill assignments don't reflect plugin skills

**Current State**:
```json
"agents": [
  {"id": "director", "skills": 11},  // ❌ Should include ponytail, superpowers, planning skills
  {"id": "engineeringManager", "skills": 8},
  {"id": "researchManager", "skills": 7}
]
```

**Fix**: Add plugin skills to appropriate agents:
- Director: brainstormingViz, writingPlans, subagentDrivenDevelopment
- Engineering Manager: ponytailMinimalism, ponytailReview, ponytailAudit
- Research Manager: (planning-with-files integration)

---

### 5. CAPABILITY DECLARATIONS

#### 🟡 `.claude/plugin.json` (Lines 40-62)
**Current**: 22 capabilities listed
**Missing**: 
- ponytail-specific capabilities (code-minimalism, decision-ladder-review)
- superpowers-specific capabilities (brainstorming, planning, SDD)
- planning-with-files-specific capabilities (persistent-planning, recovery)

**Fix**: Expand capabilities array to include:
- code-minimalism
- decision-ladder-review
- code-debt-minimalism
- brainstorming-specification
- planning-decomposition
- subagent-driven-development
- code-review-workflow
- test-driven-development
- persistent-planning
- context-reset-recovery
- hook-based-lifecycle

---

### 6. MISSING DATA

#### Hook Configuration
**Issue**: `.claude/plugin.json` mentions hooks (lines 74-77) but incomplete
**Missing**:
- PostToolUse hook details for planning-with-files
- PreToolUse hook for planning validation
- PreCompact hook for plan persistence
- Hook latency specifications

**Reference**: Should point to `skills/planning-with-files/hooks.json` for complete hook config

---

## Summary Table

| Category | Item | Current | Correct | Status |
|----------|------|---------|---------|--------|
| Skill Count | `.claude/plugin.json` | 26 | 51+ | 🔴 Stale |
| Skill Count | `config/skills.yaml` | 26 | 51+ | 🔴 Stale |
| Skill Count | Documentation (6 files) | 34 | 51+ | 🟡 Stale |
| Skill Count | SSOT_AUDIT.md (6 refs) | 28 | 51+ | 🟡 Stale |
| Plugin Skills | `config/skills.yaml` | 0 | 17 | 🔴 Missing |
| Agent Skills | `config/agents.yaml` | 26 | 51+ | 🟡 Incomplete |
| Capabilities | `.claude/plugin.json` | 22 | 30+ | 🟡 Incomplete |
| Hooks | `.claude/plugin.json` | 2 | 5+ | 🟡 Incomplete |

---

## Recommended Fix Order

**Priority 1 (Functional)**:
1. Add 17 plugin skills to `config/skills.yaml`
2. Update skill counts in `.claude/plugin.json`
3. Update agent skill assignments in `config/agents.yaml`

**Priority 2 (Documentation)**:
4. Update 12 documentation files with correct skill counts
5. Add plugin-specific capabilities to `.claude/plugin.json`
6. Complete hook configuration references

**Priority 3 (Polish)**:
7. Verify all cross-references in SSOT files
8. Update README files mentioning skill counts

---

## Files Needing Updates

### Configuration Files (3)
- [ ] `.claude/plugin.json` - Update skill count, capabilities, agent assignments
- [ ] `config/skills.yaml` - Add 17 plugin skills, update header
- [ ] `config/agents.yaml` - Update agent skill assignments

### Documentation Files (12)
- [ ] `docs/guides/agents/ORCHESTRATOR_INTEGRATION.md`
- [ ] `docs/guides/development/README.md`
- [ ] `docs/guides/development/SKILL_DEVELOPMENT_HANDBOOK.md`
- [ ] `docs/guides/reference/ARCHITECTURE_REFERENCE.md`
- [ ] `docs/guides/reference/LINK_MAP.md`
- [ ] `docs/ssot/ARCHITECTURE.md`
- [ ] `docs/ssot/SSOT_AUDIT.md` (6 references)

### Reference Files (2)
- [ ] `README.md` (if it mentions skill counts)
- [ ] `CHANGELOG.md` (if needed)

---

## Impact Assessment

**Functional Impact**: ⚠️ Low
- Configurations still work (code is backward compatible)
- Plugin skills are available even if not in registry

**Documentation Impact**: 🔴 High
- Misleading information to developers
- Incorrect inventory counts
- Confusion about available skills

**Consistency Impact**: 🔴 High
- SSOT claims to be authoritative but has stale data
- Multiple sources of truth conflict
- Maintenance burden increases

---

## Recommendations

1. **Immediate**: Update `.claude/plugin.json` and `config/skills.yaml` with correct counts
2. **Short-term**: Add all 17 plugin skills to runtime registry
3. **Medium-term**: Update all 12 documentation files
4. **Long-term**: Implement automated configuration validation to catch count drift

---

## Next Steps

1. Review this report
2. Approve fix recommendations
3. Execute Priority 1 fixes (should take ~30 min)
4. Update documentation files
5. Re-run audit to verify

**Estimated Fix Time**: ~45 minutes for all fixes

