# Infrastructure Cleanup Action Plan

**Date**: 2026-09-02  
**Status**: 🟡 IN PROGRESS (Phase 1 ✅ Complete, Phase 2-3 Planned)  
**Effort**: ~20 hours across 3 phases  
**Priority**: CRITICAL (Blocks Phase 8 full deployment, context bloat management)

---

## Executive Summary

Comprehensive infrastructure cleanup to address:
- **Documentation sprawl**: 134 files in `docs/work/`, unclear current state
- **Duplicate skill docs**: 3 skills with conflicting SKILL.md + README.md
- **Validation clutter**: Python scripts scattered in `config/` instead of `scripts/`
- **Test fragmentation**: 6 conftest files, 3 testing guides, untracked `__init__.py`
- **No runtime config validation**: YAML configs not validated at startup
- **Git disorganization**: No release tags, unclear branch strategy

**Goal**: Clean, organized infrastructure with clear ownership, proper structure, and documentation.

---

## Phase 1: Structural Fixes ✅ COMPLETE

**Completed 2026-09-02 21:00 UTC**

### Phase 1.1: Python Package Structure
- ✅ Created `skills/cost/__init__.py`
- ✅ Created `skills/monitoring/__init__.py`
- ✅ Created `skills/performance/__init__.py`
- ✅ Created `skills/remediation/__init__.py`
- ✅ Created `metrics/__init__.py`
- ✅ Created `logs/__init__.py`

**Impact**: 6 files created, proper module initialization for Phase 8 components

### Phase 1.2: Import Fixes
- ✅ Fixed late import in `config/drift_detector.py` (datetime)
- ✅ Reorganized imports per PEP8
- ✅ Removed duplicate import

**Impact**: Code quality improved, PEP8 compliance

### Phase 1.3: Logging Infrastructure
- ✅ Created `logs/` directory structure
- ✅ Created `logs/automation/` for cron jobs
- ✅ Updated `scripts/automation/phase8_automation_setup.sh`
- ✅ Changed logging from `/tmp` to persistent `logs/automation/`

**Impact**: Persistent logging, audit trail, production-ready automation

### Phase 1.4: Metrics Infrastructure
- ✅ Created `metrics/` directory with `__init__.py`
- ✅ Documented all metrics files (7 JSON files)
- ✅ Established centralized metrics storage

**Impact**: Single source of truth for all Phase 8 metrics

### Phase 1.5: Documentation
- ✅ Created `INFRASTRUCTURE_CLEANUP_REPORT.md` (Phase 1 status)
- ✅ Created `INFRASTRUCTURE_CLEANUP_ACTION_PLAN.md` (this file)

**Deliverables**: 9 files modified/created, 480 LOC added

**Git Commit**: `Infrastructure cleanup: organize Phase 8 components`

---

## Phase 2: Consolidation & Deduplication (PLANNED)

**Estimated**: 2-3 days (40-60 hours)  
**Start**: After Phase 1 validation  
**Parallel**: Can run alongside Phase 8 testing

### Phase 2.1: Documentation Archival (CRITICAL)

**Current State**: `docs/work/` has 134 files (47 completed phases + planning + specs)

**Action**: Archive historical documentation
```
docs/work/completed/
  ├── PHASE_1_PLAN.md ──────────┐
  ├── PHASE_1_SUMMARY.md        │
  ├── [44 more files]           ├──→ archive to:
  └── PHASE_20_FINAL.md         │     docs/work/archived/phases-1-20.tar.gz
                                │     docs/work/archived/PHASES_1_20_INDEX.md
                                └─
```

**Deliverables**:
- [ ] Consolidate 47 phase files into `docs/work/archived/phases-1-20/`
- [ ] Create `PHASES_1_20_INDEX.md` for reference
- [ ] Reduce `docs/work/current/` to 5 key documents:
  - AUDIT.md (metrics)
  - PHASE_8_IMPLEMENTATION_LOG.md
  - PHASE_8_AUTOMATED_OPERATIONS_PLAN.md
  - INFRASTRUCTURE_CLEANUP_REPORT.md
  - INFRASTRUCTURE_CLEANUP_ACTION_PLAN.md (this file)

**Impact**: Reduce clutter by 47 files, clarify current state, improve context window

**Effort**: 2-3 hours

---

### Phase 2.2: Testing Documentation Consolidation (HIGH PRIORITY)

**Current State**: 3 overlapping files
- `docs/guides/development/TESTING_PATTERNS.md` (100 lines)
- `docs/guides/development/FIXTURE_GUIDE.md` (743 lines)
- `docs/guides/development/FIXTURE_PATTERNS.md` (506 lines)

**Action**: Merge into single reference
```
TESTING_PATTERNS.md (concise, general)
  └── Reference: "See FIXTURE_REFERENCE.md for fixtures"

FIXTURE_REFERENCE.md (comprehensive, replaces GUIDE + PATTERNS)
  ├── Best practices (from PATTERNS)
  ├── Common patterns (from GUIDE)
  ├── Examples (from both)
  └── Troubleshooting
```

**Deliverables**:
- [ ] Merge FIXTURE_GUIDE.md + FIXTURE_PATTERNS.md → FIXTURE_REFERENCE.md
- [ ] Keep TESTING_PATTERNS.md (concise overview)
- [ ] Archive old files to `docs/guides/reference/archived/`
- [ ] Update `../../docs/rules/` references to point to FIXTURE_REFERENCE.md

**Impact**: Clearer testing guidance, single source of truth for fixtures

**Effort**: 2-3 hours

---

### Phase 2.3: Skill Documentation Consolidation (HIGH PRIORITY)

**Current State**: 3 skills with duplicate docs
- `docs/guides/skills/ 409L + README.md 177L)
- `docs/guides/skills/ 175L + README.md 352L)
- `docs/guides/skills/ 392L + README.md 358L)

**Action**: Pick SKILL.md as authoritative, consolidate

**For each skill**:
- [ ] Review both docs (SKILL.md vs README.md)
- [ ] Keep SKILL.md as authoritative (matches convention)
- [ ] Merge any unique content from README.md into SKILL.md
- [ ] Delete README.md
- [ ] Archive to `skills/[skill]/deprecated/README.md.archive`

**Deliverables**:
- [ ] `docs/guides/skills/` (consolidated)
- [ ] `docs/guides/skills/` (consolidated)
- [ ] `docs/guides/skills/` (consolidated)
- [ ] 3 README.md files archived

**Impact**: Clear documentation ownership, reduced maintenance burden

**Effort**: 3-4 hours

---

### Phase 2.4: Validation Scripts Reorganization (HIGH PRIORITY)

**Current State**: Python scripts in `config/` directory
- `config/validate-config.py` (8872 lines) — YAML validation
- `config/detect-dead-code.py` (7481 lines) — Code analysis
- `config/drift_detector.py` (6164 lines) — Config drift detection

**Issue**: These belong in `scripts/validation/`, not with configs

**Action**: Move to proper location
```
config/                         scripts/
├── validate-config.py    ──→   ├── validation/
├── detect-dead-code.py   ──→   │   ├── validate-config.py
├── drift_detector.py     ──→   │   ├── detect-dead-code.py
│                               │   └── drift_detector.py
└── [YAML configs]              ├── validate_skill_docs.py (already in scripts/)
                                └── [other scripts]
```

**Also in `config/`**: duplicate `validate-config.py` exists

**Deliverables**:
- [ ] Create `scripts/validation/` directory
- [ ] Move 3 Python files from `config/` to `scripts/validation/`
- [ ] Update imports in Phase 8 automation scripts
- [ ] Update `config/.gitignore` if needed
- [ ] Remove duplicate validation files

**Also address**: Remove duplicate validation in `scripts/validate_skill_docs.py`

**Impact**: Clear separation of concerns, proper organization

**Effort**: 2-3 hours

---

### Phase 2.5: Conftest Consolidation (MEDIUM PRIORITY)

**Current State**: 6 conftest files
- `tests/conftest.py` (main)
- `tests/conftest_auth.py` (authentication)
- `tests/conftest_core.py` (core functionality)
- `tests/conftest_parametrize.py` (parametrization)
- `tests/conftest_performance.py` (performance tests)
- `tests/conftest_storage.py` (database/storage)

**Action**: Consolidate with modular imports

**Structure**:
```
tests/
├── conftest.py (main, imports from fixtures/)
├── fixtures/
│   ├── auth_fixtures.py (from conftest_auth.py)
│   ├── core_fixtures.py (from conftest_core.py)
│   ├── parametrize_fixtures.py (from conftest_parametrize.py)
│   ├── performance_fixtures.py (from conftest_performance.py)
│   └── storage_fixtures.py (from conftest_storage.py)
└── conftest_*.py (archived/removed)
```

**Deliverables**:
- [ ] Create modular fixture files in `tests/fixtures/`
- [ ] Update `conftest.py` to import all fixtures
- [ ] Delete individual `conftest_*.py` files
- [ ] Update fixture references in tests
- [ ] Verify all imports still work

**Impact**: Cleaner test structure, easier to maintain

**Effort**: 4-5 hours

---

### Phase 2.6: Git Release Tags (MEDIUM PRIORITY)

**Current State**: No git tags; version only in code/docs

**Action**: Create retroactive release tags

```bash
git tag -a v1.0.0 -m "Phase 1 Complete: Foundational infrastructure"
git tag -a v1.1.0 -m "Phase 2-3: Network & cost routing"
git tag -a v1.2.0 -m "Phase 4-5: Optimization & consolidation"
git tag -a v1.3.0 -m "Phase 6-7: Validation & automation"
git tag -a v2.0.0 -m "Phase 8: Automated operations"
```

**Deliverables**:
- [ ] Create v1.0.0 - v2.0.0 tags
- [ ] Push tags to origin
- [ ] Document tag strategy in `../../docs/rules/git-workflow.md`
- [ ] Update README.md with version reference

**Impact**: Clear version history, release management

**Effort**: 1-2 hours

---

### Phase 2.7: Agent Directory Consolidation (MEDIUM PRIORITY)

**Current State**: 3 agent locations
- `/agents/` (3 files)
- `/.claude/agents/` (0 files, likely empty)
- `/.claude-plugin/agents/` (1 directory)

**Issue**: Unclear which is authoritative; potential inconsistencies

**Action**: Use `config/agents.yaml` as single source of truth

**Deliverables**:
- [ ] Review all 3 agent locations
- [ ] Consolidate unique definitions into `config/agents.yaml`
- [ ] Remove redundant agent files/dirs
- [ ] Document agent management in `config/README.md`
- [ ] Add validator to check agent consistency

**Impact**: Single source of truth, consistent agent definitions

**Effort**: 2-3 hours

---

## Phase 3: Long-Term Infrastructure (PLANNED)

**Estimated**: 1-2 weeks (80-120 hours)  
**Start**: After Phase 2 completion  
**Priority**: MEDIUM (Quality improvement, not blocking)

### Phase 3.1: Runtime Config Validation

**Action**: Add Pydantic schema validation to app startup

```python
# app/core/config/validators.py
from pydantic import BaseModel, ValidationError

class AgentsSchema(BaseModel):
    id: str
    model: str
    skills: list[str]
    # ... validation rules

class SkillsSchema(BaseModel):
    id: str
    purpose: str
    # ... validation rules

class ConfigValidator:
    def load_and_validate(self):
        # Load YAML
        # Validate against schema
        # Raise on validation error
        pass
```

**Deliverables**:
- [ ] Create `app/core/config/validators.py` with Pydantic schemas
- [ ] Update app startup to validate configs
- [ ] Add error messages for config violations
- [ ] Test validation with bad configs

**Impact**: Catch config errors at startup, prevent silent failures

**Effort**: 4-6 hours

---

### Phase 3.2: Skill Registry Validator

**Action**: Add tool to verify consistency between `config/skills.yaml` and `/skills/` filesystem

```bash
python scripts/validation/validate_skill_registry.py
```

**Output**:
```
Skill Registry Validation:
  ✅ monitoring: defined in config, found in filesystem
  ✅ remediation: defined in config, found in filesystem
  ❌ oldSkill: defined in config, NOT FOUND in filesystem (orphaned)
  ❌ newSkill: found in filesystem, NOT DEFINED in config (unregistered)
```

**Deliverables**:
- [ ] Create `scripts/validation/validate_skill_registry.py`
- [ ] Add to pre-commit hooks or CI
- [ ] Document in `scripts/validation/README.md`

**Impact**: Prevent skill registration drift

**Effort**: 2-3 hours

---

### Phase 3.3: Skills Directory Reorganization

**Action**: Organize 38+ skills into functional groups

```
skills/
├── core/                    # Base classes, utilities
├── cost/                    # Cost monitoring & optimization
│   ├── costDashboard/
│   ├── costForecasting/
│   ├── costIntelligence/
│   └── costAwareLlmPipeline/
├── monitoring/              # Health & performance monitoring
│   ├── healthCheck/
│   ├── healthMonitoring/
│   ├── metricsCollector/
│   └── monitoring/ (Phase 8)
├── optimization/            # Performance & resource optimization
│   ├── autoScalingManager/
│   ├── cacheManager/
│   └── performance/ (Phase 8)
├── routing/                 # Request routing & orchestration
│   ├── tenantRouter/
│   ├── routing/
│   └── regionFailoverManager/
├── security/                # Security & validation
│   ├── crossTeamSynthesis/
│   ├── codeReview/
│   └── tenantAudit/
└── [utilities & integration]/
```

**Deliverables**:
- [ ] Create logical grouping structure
- [ ] Move skills into appropriate directories
- [ ] Update imports in dependent skills
- [ ] Update documentation references
- [ ] Update `config/skills.yaml` paths if needed

**Impact**: Better organization, clearer dependencies

**Effort**: 6-8 hours

---

### Phase 3.4: Documentation Structure Refactor

**Action**: Clarify and organize `docs/` hierarchy

```
docs/
├── INDEX.md (main entry point)
├── guides/
│   ├── development/         # Developer guides
│   ├── operations/          # Operational guides
│   ├── architecture/        # Architecture docs
│   ├── reference/           # API/config reference
│   └── agents/              # Agent documentation
├── work/
│   ├── archived/            # Historical phases 1-20
│   │   └── phases-1-20/
│   └── current/             # Only 5 current docs
├── api/                     # Auto-generated API docs
└── examples/                # Example usage
```

**Deliverables**:
- [ ] Restructure docs layout
- [ ] Create clear INDEX.md
- [ ] Archive historical docs
- [ ] Auto-generate API documentation
- [ ] Update internal links

**Impact**: Clearer documentation, better onboarding

**Effort**: 4-5 hours

---

## Summary of Changes

### By Category

| Category | Phase 1 ✅ | Phase 2 (Planned) | Phase 3 (Planned) | Total |
|----------|---------|-------------------|-------------------|-------|
| **Files Created** | 6 | ~15 | ~10 | ~31 |
| **Files Deleted** | 0 | ~8 | ~5 | ~13 |
| **Files Modified** | 2 | ~20 | ~30 | ~52 |
| **Lines Changed** | 480 | ~5,000 | ~8,000 | ~13,480 |
| **Documentation** | 2 docs | 5 docs | 3 docs | 10 docs |

### By Impact

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| **Documentation files** | 134 in `docs/work/` | ~50 (40 archived) | -40% |
| **Conftest files** | 6 | 1 | -83% |
| **Duplicate docs** | 3 skills | 0 | -100% |
| **Script locations** | 3 (scripts/, config/, .claude/) | 2 | -33% |
| **Config validation** | None | Runtime validation | ✅ New |
| **Release tags** | 0 | 5 tags | ✅ New |

---

## Timeline & Milestones

```
Phase 1: Structural Fixes
  ├─ 2026-09-02 21:00 UTC ✅ COMPLETE (9 files, 480 LOC)
  └─ Commit: Infrastructure cleanup

Phase 2: Consolidation & Deduplication (2-3 days)
  ├─ Day 1: Documentation archival + Testing docs merge
  ├─ Day 2: Skill docs consolidation + Script reorganization
  ├─ Day 3: Conftest consolidation + Release tags
  └─ Commits: 5-6 commits across tasks

Phase 3: Long-Term Infrastructure (1-2 weeks)
  ├─ Week 1: Config validation + Skill registry validator
  ├─ Week 2: Skills reorganization + Docs refactoring
  └─ Commits: 4-5 commits across tasks

Total Effort: ~20 hours across 3 phases
```

---

## Dependencies & Prerequisites

### Phase 2 Dependencies
- Phase 1 ✅ COMPLETE
- All Phase 8 components tested (estimated 2026-09-04)

### Phase 3 Dependencies
- Phase 2 ✅ COMPLETE
- No Phase 8 development in-flight
- Ability to test with bad configs

---

## Success Criteria

| Criterion | Phase 1 | Phase 2 | Phase 3 | Overall |
|-----------|---------|---------|---------|---------|
| **Documentation sprawl** | - | Reduced 40% | Resolved | ✅ |
| **Duplicate docs** | - | Resolved | - | ✅ |
| **Script organization** | 50% | 80% | 100% | ✅ |
| **Config validation** | - | - | Implemented | ✅ |
| **Release tags** | - | Implemented | - | ✅ |
| **Test consolidation** | - | 50% | 100% | ✅ |
| **Skill organization** | - | - | Improved | ✅ |

---

## Quick Reference

### Phase 1 Completed
```bash
# View Phase 1 changes
git show HEAD --stat

# Check new directories
ls -la logs/ metrics/
```

### Phase 2 Actions (When Ready)
```bash
# Archive documentation
mv docs/work/completed docs/work/archived/phases-1-20

# Move validation scripts
mv config/*.py scripts/validation/

# Consolidate conftest
pytest --collect-only  # Verify imports work
```

### Phase 3 Actions (When Ready)
```bash
# Validate configs
python scripts/validation/validate_skill_registry.py

# Check runtime validation
python -c "from app.core.config import load_and_validate; load_and_validate()"
```

---

## Notes

- **Parallel Work**: Phase 2 can run in parallel with Phase 8 testing (Days 2-4)
- **Risk**: Low risk; mostly organizational changes, no logic changes
- **Rollback**: Git commits allow easy rollback if issues arise
- **Testing**: No new tests needed; existing tests should pass after changes

---

## Owner & Status

- **Owner**: Infrastructure Cleanup Initiative
- **Lead**: Claude Haiku 4.5
- **Status**: Phase 1 ✅ COMPLETE, Phase 2-3 Planned
- **Last Updated**: 2026-09-02 21:00 UTC
- **Next Review**: 2026-09-04 (after Phase 2 starts)

---

**This document is the single source of truth for infrastructure cleanup activities.**
