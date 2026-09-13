# Documentation Redundancy Consolidation Plan

**Status**: Ready for implementation  
**Analysis Date**: 2026-08-25  
**Audit Report**: `docs/work/completed/REDUNDANCY_AUDIT_2026-08-25.md`  
**Estimated Effort**: 3–4 hours across 4 phases  

---

## Overview

This plan consolidates documentation redundancy identified in the 2026-08-25 audit. Work is organized into 4 phases, each with clear step-by-step instructions, validation procedures, and rollback paths.

**Key Principle**: Make CLAUDE.md the canonical navigation hub; consolidate link indexes to LINK_MAP.md; eliminate pure redirect files.

---

## Phase 1: Consolidate Navigation Files (CRITICAL)

**Estimated Time**: 1–2 hours  
**Files to Modify**: 5  
**Lines Eliminated**: ~80  
**Risk**: Medium (affects multiple doc entry points)

### Objective
Eliminate duplicate "Quick Links by Role" navigation sections. Make CLAUDE.md the canonical hub; redirect all others there.

### Files Affected
- ✅ KEEP & ENHANCE: `/home/user/it/CLAUDE.md` (canonical hub)
- ❌ DELETE: `/home/user/it/docs/NAVIGATION.md`
- ❌ DELETE: `/home/user/it/docs/INDEX.md`
- ⚠️ MODIFY: `/home/user/it/README.md` (remove duplicate navigation table)
- ⚠️ REFERENCE: `/home/user/it/docs/guides/reference/LINK_MAP.md` (redirect users there)

### Step-by-Step Instructions

#### Step 1.1: Verify CLAUDE.md Contains Complete Navigation
**Location**: `/home/user/it/CLAUDE.md` (lines 9–26)

**Check**:
- [ ] Has "Quick Links by Role" section
- [ ] Contains entries for: New developer, PM, Engineer, Writing code, Code review, Deploying, Security, API, Cost control, File organization, Architecture, IDE, Platform
- [ ] All links point to valid locations

**If incomplete**: Add missing entries before proceeding.

#### Step 1.2: Create Redirect Stubs (Optional)
**Purpose**: Convenience for users who may have old links bookmarked.

**Option A (Minimal)**: Delete files entirely (links will 404, which is fine)  
**Option B (User-friendly)**: Create minimal redirect stubs

**Example redirect stub** (if using Option B):
```markdown
# Documentation Index

→ See [`CLAUDE.md`](../../CLAUDE.md) for navigation by role and task.
```

**Decision**: Choose A or B before proceeding. (Recommended: A for cleaner repo)

#### Step 1.3: Delete Files (or Convert to Stubs)
```bash
# Verify what we're deleting first
git status docs/NAVIGATION.md docs/INDEX.md

# Option A: Delete
git rm docs/NAVIGATION.md docs/INDEX.md

# Option B: Create stubs (if chosen above)
# [Create minimal 3–4 line redirect files]
```

#### Step 1.4: Remove Duplicate Navigation from README.md
**Location**: `/home/user/it/README.md`

**Find and Remove**:
- Search for "Quick Links" section (if exists)
- Remove duplicate role-based navigation table
- Keep only: Quick Start (3–5 commands), Documentation pointer to CLAUDE.md

**Before**:
```markdown
## Quick Links by Role
| Role | Start Here |
|------|-----------|
| New developer | ... |
| Engineer | ... |
[duplicate of CLAUDE.md content]
```

**After**:
```markdown
## Quick Start

1. Clone: `git clone ...`
2. Install: `pip install -r requirements.txt`
3. Test: `pytest tests/`
4. Deploy: `./scripts/deploy.sh`

**→ Full documentation**: See [`CLAUDE.md`](CLAUDE.md) for navigation by role and task.
```

#### Step 1.5: Update Cross-References
**Search for**: Links to deleted files and update them

```bash
# Find all references to deleted files
grep -r "docs/NAVIGATION.md\|docs/INDEX.md" . --include="*.md" --include="*.py"

# Replace with CLAUDE.md
# Example:
# OLD: "See [`docs/NAVIGATION.md`](docs/NAVIGATION.md)"
# NEW: "See [`CLAUDE.md`](CLAUDE.md)"
```

**Common locations to check**:
- `.claude/rules/README.md`
- Any files that link to docs/
- Plugin documentation
- Skill documentation

#### Step 1.6: Commit & Validate

**Commit**:
```bash
git add CLAUDE.md README.md docs/
git commit -m "refactor(docs): consolidate navigation to CLAUDE.md

- Make CLAUDE.md canonical navigation hub
- Delete docs/NAVIGATION.md and docs/INDEX.md
- Remove duplicate role-based tables from README.md
- Update cross-references

Fixes redundancy audit findings (category 1)"
```

**Validate**:
- [ ] CLAUDE.md loads and renders correctly
- [ ] README.md quick-start section is clear
- [ ] All cross-references to deleted files have been updated
- [ ] No broken markdown links (check in editor)

---

## Phase 2: Eliminate LINKS_*.md Files (HIGH)

**Estimated Time**: 1 hour  
**Files to Modify**: 7  
**Lines Eliminated**: ~250  
**Risk**: Low (index consolidation, clear rollback path)

### Objective
Keep only LINK_MAP.md; delete all LINKS_*.md variants. Update all references.

### Files Affected
- ✅ KEEP: `/home/user/it/docs/guides/reference/LINK_MAP.md` (master index)
- ❌ DELETE: `LINKS_NAVIGATION.md`
- ❌ DELETE: `LINKS_CORE_DOCS.md`
- ❌ DELETE: `LINKS_REFERENCE.md`
- ❌ DELETE: `LINKS_SKILLS_AGENTS.md`
- ❌ DELETE: `LINKS_ARCHIVE.md`

### Step-by-Step Instructions

#### Step 2.1: Verify LINK_MAP.md is Complete
**Location**: `/home/user/it/docs/guides/reference/LINK_MAP.md`

**Check**:
- [ ] Contains all sections from deleted LINKS_*.md files
- [ ] All links point to valid locations
- [ ] Sections clearly organized (Navigation, Core Docs, Skills, Archive, etc.)

**If incomplete**: Merge missing sections from LINKS_*.md files into LINK_MAP.md before deletion.

#### Step 2.2: Delete LINKS_*.md Files
```bash
# Verify existence
ls docs/guides/reference/LINKS_*.md

# Delete
git rm docs/guides/reference/LINKS_*.md

# Verify they're removed
git status
```

#### Step 2.3: Update All Cross-References
**Search for references**:
```bash
# Find all files that reference deleted LINKS_*.md
grep -r "LINKS_NAVIGATION\|LINKS_CORE_DOCS\|LINKS_REFERENCE\|LINKS_SKILLS_AGENTS\|LINKS_ARCHIVE" . --include="*.md"

# Replace with LINK_MAP.md
# Example:
# OLD: "[See LINKS_CORE_DOCS.md](LINKS_CORE_DOCS.md)"
# NEW: "[See LINK_MAP.md](LINK_MAP.md)"
```

**Common locations to check**:
- `.claude/rules/README.md`
- Skill documentation files
- Architecture guides
- Main documentation files

#### Step 2.4: Verify LINK_MAP.md is Accessible
**Check navigation to ensure easy discovery**:
- [ ] LINK_MAP.md linked from CLAUDE.md
- [ ] LINK_MAP.md linked from NAVIGATION section (or new location)
- [ ] README.md references it as "master reference" if appropriate

#### Step 2.5: Commit & Validate

**Commit**:
```bash
git add docs/guides/reference/
git commit -m "refactor(docs): consolidate link indexes to LINK_MAP.md

- Keep docs/guides/reference/LINK_MAP.md as single master index
- Delete LINKS_NAVIGATION.md, LINKS_CORE_DOCS.md, LINKS_REFERENCE.md, LINKS_SKILLS_AGENTS.md, LINKS_ARCHIVE.md
- Update all cross-references to point to LINK_MAP.md

Fixes redundancy audit findings (category 2)"
```

**Validate**:
- [ ] LINK_MAP.md contains all necessary cross-references
- [ ] No references to deleted files remain
- [ ] LINK_MAP.md is easily discoverable from main docs

---

## Phase 3: Clarify Documentation Scope (MEDIUM)

**Estimated Time**: 1–2 hours  
**Files to Modify**: 5+  
**Lines Eliminated/Refactored**: ~100+  
**Risk**: Low (clarity improvements, no file deletion)

### Objective
Improve clarity by distinguishing IDE vs. Platform contexts; consolidate cost reference materials; clarify SSOT locations.

### Files Affected
- ⚠️ MODIFY: `/home/user/it/docs/guides/development/IDE_SKILLS_INVENTORY.md`
- ⚠️ MODIFY: `/home/user/it/docs/guides/reference/PLATFORM_SKILLS_INVENTORY.md`
- ⚠️ MODIFY: `/home/user/it/docs/guides/reference/COST_REFERENCE.md`
- ⚠️ MODIFY: `/home/user/it/.claude/rules/cost-management.md`
- ⚠️ MODIFY: `/home/user/it/.claude/rules/governance-extensions.md`

### Step-by-Step Instructions

#### Step 3.1: Add Context Headers to Skill Inventories
**File 1**: `/home/user/it/docs/guides/development/IDE_SKILLS_INVENTORY.md`

**Add at top** (after title):
```markdown
> ⚠️ **IDE Development Skills** — These are skills available in Claude Code during development.  
> For **runtime agent skills**, see [`PLATFORM_SKILLS_INVENTORY.md`](../reference/PLATFORM_SKILLS_INVENTORY.md).
```

**File 2**: `/home/user/it/docs/guides/reference/PLATFORM_SKILLS_INVENTORY.md`

**Add at top** (after title):
```markdown
> ⚠️ **Platform Runtime Skills** — These skills run in the nxgntch platform at runtime.  
> For **IDE development skills**, see [`IDE_SKILLS_INVENTORY.md`](../../development/IDE_SKILLS_INVENTORY.md).
```

#### Step 3.2: Add SSOT References to Cost Docs
**File**: `/home/user/it/.claude/rules/cost-management.md`

**Add at top** (after Overview section):
```markdown
### Single Source of Truth (SSOT)

All cost configuration values are authoritative in:
- **Budget Limits**: `config/governance.yaml`
- **Model Pricing**: `config/models.yaml`

These rule files explain **how** costs are enforced and calculated, but actual numbers come from config files.
```

**File**: `/home/user/it/.claude/rules/governance-extensions.md`

**Add similar SSOT note** in Overview or appropriate section.

#### Step 3.3: Consolidate Cost Reference (Choose One Path)

**Decision Point**: How to handle `docs/guides/reference/COST_REFERENCE.md`?

**Option A** (Recommended): Convert to redirect stub
```markdown
# Cost Reference

→ See [Cost Management Rules](.../cost-management.md) for cost enforcement, calculation, and examples.

→ See [Configuration](.../governance.yaml) (SSOT) for current values.
```

**Option B**: Merge substantive content into cost-management.md and delete COST_REFERENCE.md

**Option C**: Keep as-is but add header: "Quick reference; see cost-management.md for full guidance"

**Choose Option**: ___A___ (recommended for cleaner structure)

#### Step 3.4: Update Setup Documentation Scope
**File**: `/home/user/it/docs/guides/development/SETUP_ENVIRONMENT.md`

**Verify** it's a proper redirect (not just a brief mention):
- Should be 2–5 lines only
- Should clearly point to IDE_SETUP.md as canonical

**Example**:
```markdown
# Environment Setup

→ Complete setup guide: See [IDE Setup](.../../.claude/IDE/IDE_SETUP.md)
```

#### Step 3.5: Commit & Validate

**Commit**:
```bash
git add docs/guides/ .claude/rules/
git commit -m "docs: clarify scope and SSOT for skill inventories and cost documentation

- Add context headers distinguishing IDE vs Platform skills
- Add SSOT references (config/governance.yaml, config/models.yaml)
- Consolidate cost reference materials
- Verify setup doc redirects are accurate

Improves clarity; fixes redundancy audit findings (categories 3, 5, 6)"
```

**Validate**:
- [ ] Each file clearly states its purpose and context
- [ ] SSOT locations are clearly marked
- [ ] Cross-references between IDE and Platform skills work
- [ ] Readers understand which docs are authoritative

---

## Phase 4: Clean Up Stub Files (LOW)

**Estimated Time**: 30 minutes  
**Files to Modify**: 5  
**Lines Eliminated**: ~100  
**Risk**: Very low (cleanup only, minimal impact)

### Objective
Delete or clearly mark pure redirect files that serve no unique purpose.

### Files Affected
- ❓ DECIDE: `/home/user/it/docs/README.md` (7 lines)
- ❓ DECIDE: `/home/user/it/docs/OPERATIONS.md` (38 lines)
- ❓ DECIDE: `/home/user/it/.claude-plugin/agents/README.md` (34 lines)
- ❓ DECIDE: `/home/user/it/skills/README.md` (6 lines)

### Step-by-Step Instructions

#### Step 4.1: Audit Each Stub File

**File 1**: `/home/user/it/docs/README.md`  
**Review**:
- Does it add unique value, or just redirect?
- Is it used as entry point by users?

**Decision**: 
- [ ] DELETE (pure redirect, use CLAUDE.md instead)
- [ ] KEEP as convenience redirect

**File 2**: `/home/user/it/docs/OPERATIONS.md`  
**Review**:
- Does it add context beyond pointing to guides/operations/?
- Are there any unique sections?

**Decision**:
- [ ] DELETE (pure redirect, use CLAUDE.md instead)
- [ ] KEEP as convenience redirect with short summary

**File 3**: `/home/user/it/.claude-plugin/agents/README.md`  
**Review**:
- Is this the agent inventory, or just links?
- Used by marketplace or local development?

**Decision**:
- [ ] DELETE if redundant with config/agents.yaml and agent docs
- [ ] KEEP if it serves marketplace distribution

**File 4**: `/home/user/it/skills/README.md`  
**Review**:
- Is this the skill directory listing?
- Or just a redirect?

**Decision**:
- [ ] DELETE if pure redirect
- [ ] KEEP as minimal directory guide

#### Step 4.2: Apply Decisions
**For each DELETE decision**:
```bash
git rm <file>
```

**For each KEEP decision** (as convenience redirect):
Ensure file has clear redirect notice at top:
```markdown
# [Original Title]

→ See [Canonical Location](link) for [purpose].
```

#### Step 4.3: Commit & Validate

**Commit**:
```bash
git add docs/ skills/ .claude-plugin/
git commit -m "chore(docs): consolidate redirect stubs

- Delete pure redirect files where canonical sources exist
- Clarify directory purposes
- Reduce documentation clutter

Fixes redundancy audit findings (category 8)"
```

**Validate**:
- [ ] No dangling references to deleted files
- [ ] Remaining redirects are minimal and clear
- [ ] Documentation structure is cleaner

---

## Cross-Phase Validation

After completing each phase (or all 4 phases), perform these checks:

### General Checks
```bash
# Find any remaining dead links
grep -r "docs/INDEX.md\|docs/NAVIGATION.md\|LINKS_" . --include="*.md" | grep -v "docs/work/completed"

# Check for trailing stub redirects that could be removed
find docs/ -name "*.md" -exec sh -c 'lines=$(wc -l < "$1"); if [ "$lines" -lt 10 ]; then echo "$1 ($lines lines)"; fi' _ {} \;

# Verify all key docs are still accessible
grep -r "CLAUDE.md\|LINK_MAP.md\|IDE_SETUP.md" . --include="*.md" | grep -c "^" # Should have hits
```

### Documentation Integrity
- [ ] No broken internal links (check in markdown editor)
- [ ] No references to deleted files
- [ ] All role-based quick links point to CLAUDE.md
- [ ] AUDIT.md is referenced as SSOT for metrics
- [ ] Cost config points to governance.yaml and models.yaml

### Git History
- [ ] Each phase committed separately with clear message
- [ ] Commits reference redundancy audit categories
- [ ] No unrelated changes in commits

---

## Rollback Path

If issues arise, rollback is simple:

```bash
# After Phase 1:
git revert <Phase1CommitHash>

# After Phase 2:
git revert <Phase2CommitHash>

# After Phase 3:
git revert <Phase3CommitHash>

# After Phase 4:
git revert <Phase4CommitHash>
```

Each phase is independent, so rolling back one doesn't affect others (mostly).

---

## Success Criteria

**Phase 1 Complete** ✅
- [ ] CLAUDE.md is canonical navigation hub
- [ ] docs/NAVIGATION.md and docs/INDEX.md deleted
- [ ] No duplicate role-based navigation tables
- [ ] All cross-references updated

**Phase 2 Complete** ✅
- [ ] LINK_MAP.md is single master index
- [ ] All LINKS_*.md files deleted
- [ ] All references point to LINK_MAP.md
- [ ] No documentation referring to deleted link indexes

**Phase 3 Complete** ✅
- [ ] Skill inventories have context headers
- [ ] Cost docs reference SSOT (config files)
- [ ] Setup documentation scope is clear
- [ ] Readers understand IDE vs Platform distinction

**Phase 4 Complete** ✅
- [ ] Pure redirect stubs removed (or clearly marked)
- [ ] Documentation structure is cleaner
- [ ] No dangling references

**Overall Success** ✅
- [ ] ~630 lines of redundancy eliminated
- [ ] 3–4 hours of work completed
- [ ] Documentation is clearer and better organized
- [ ] Single source of truth for each concept
- [ ] All validation checks pass

---

## Running This Plan

### For Next Session

**Recommended approach**:

1. **Session Setup**: Copy this plan to scratchpad or visible area
2. **Phase 1**: Follow step-by-step instructions, commit
3. **Phase 2**: Complete after Phase 1 passes validation
4. **Phase 3**: Complete before Phase 4 (builds on previous changes)
5. **Phase 4**: Final cleanup after all phases

### Quick Start Commands

```bash
# At start of session:
# 1. Read this plan
# 2. Review audit report: docs/work/completed/REDUNDANCY_AUDIT_2026-08-25.md
# 3. Start with Phase 1:

# Phase 1 checklist:
# - [ ] Verify CLAUDE.md has complete navigation
# - [ ] Delete docs/NAVIGATION.md docs/INDEX.md
# - [ ] Remove duplicate table from README.md
# - [ ] Update cross-references
# - [ ] Commit with message

# After Phase 1:
pytest tests/ --cov=app  # Verify no code broke
grep -r "docs/NAVIGATION\|docs/INDEX" . --include="*.md"  # Verify no refs remain
```

---

## References

- **Audit Report**: `docs/work/completed/REDUNDANCY_AUDIT_2026-08-25.md`
- **File Organization Guidelines**: `.claude/rules/file-organization.md`
- **CLAUDE.md**: Main navigation hub (canonical after Phase 1)
- **LINK_MAP.md**: Master reference index (after Phase 2)

---

**Plan Status**: Ready for implementation  
**Last Updated**: 2026-08-25  
**Next Step**: Assign to future session and begin Phase 1
