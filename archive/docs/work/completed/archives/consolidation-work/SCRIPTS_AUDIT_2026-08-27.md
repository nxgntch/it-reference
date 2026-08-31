# Scripts Directory Audit & Consolidation Plan (2026-08-27)

---

## Executive Summary

**Issue**: Scripts directory has significant organizational issues:
- 9 root-level utility scripts (should be in subdirectories)
- Duplicate/conflicting files (e.g., two `validation.py`, two `syncit.py`)
- 17+ profiling/phase scripts scattered at root (should be in `profiling/` or `phase17/`)
- Complex nested sync structure with duplication
- No shared patterns or base classes (contrary to test infrastructure approach)

**Scope**: Consolidate 45+ scripts into 8 organized categories with improved structure.

---

## Current Structure Analysis

### Root-Level Scripts (19 files - HIGH CLUTTER)

| File | Purpose | Should Go To |
|------|---------|---|
| `validation.py` | ConfigValidator class | `validate/config_validation.py` |
| `cli.py` | CLI interface stub | `cli/interface.py` |
| `docs_generator.py` | DocsGenerator stub | `docs/generator.py` |
| `generateEnvExample.py` | Environment setup | `utils/generate_env.py` |
| `hookOptimizer.py` | Hook optimization | `utils/hook_optimizer.py` |
| `phase17_*.py` (9 files) | Performance profiling | `profiling/phase17/` |
| `parametrization_*.py` (5 files) | Test parametrization metrics | `profiling/parametrization/` |
| `measure_parametrization_perf.py` | Perf measurement | `profiling/parametrization/` |

### sync/ Subdirectory (Complex nesting)

```
sync/
├── autosync.py ...................... Main orchestrator
├── syncit.py ........................ File sync (generic)
├── syncConfig.py .................... Config sync
├── syncClean.py ..................... Cleanup
├── syncMobile.py .................... Mobile sync (unused?)
└── docs/ ............................ Duplicate/nested!
    ├── autosync.py .................. (stub?)
    ├── syncit.py .................... (stub?)
    ├── syncDoc.py ................... Doc sync
    ├── syncConfig.py ................ Config sync (dup!)
    ├── syncClean.py ................ Cleanup (dup!)
    └── syncMobile.py ............... Mobile sync (dup!)
└── repos/ ........................... Multi-repo sync
    ├── daily_sync.py ................ Main orchestrator
    ├── reference_sync.py ............ Ref repo sync
    ├── reference_search.py .......... Ref search
    ├── archive_workflow.py .......... Archive management
    ├── logs_sync.py ................. Logs sync
    └── nxgntch_sync.py .............. Marketplace sync
```

**Problem**: sync/docs/ has near-duplicate files of sync/ (unclear which is authoritative).

### validate/ Subdirectory

```
validate/
├── checkConfigConsistency.py ........ Config checks
├── checkDocLinks.py ................ Link validation
└── checkRedundancy.py .............. Redundancy checks
```

Good organization, but `validation.py` at root competes with this.

### utils/ Subdirectory

```
utils/
├── validation.py ................... Skill validation (different purpose!)
├── startup_profiler.py ............ Startup profiling
├── lazy_load_agents.py ............ Lazy loading
└── lazy_load_skills.py ........... Lazy loading
```

Should include: `generateEnvExample.py`, `hookOptimizer.py`

### coverage/ Subdirectory

```
coverage/
└── reporter.py ................... Coverage reporting
```

Good organization.

---

## Issues Identified

### 1. **Duplicate Files (CRITICAL)**
- `scripts/validation.py` vs `scripts/utils/validation.py` (different purposes!)
- `scripts/sync/syncit.py` vs `scripts/sync/docs/syncit.py` (unclear which is used)
- `scripts/sync/syncConfig.py` vs `scripts/sync/docs/syncConfig.py`
- `scripts/sync/syncClean.py` vs `scripts/sync/docs/syncClean.py`

**Impact**: Maintenance confusion, unclear which version to update.

### 2. **Root-Level Clutter**
- 19 utility/tool scripts at root, should be in subdirectories
- No organization by purpose (performance, generation, validation, sync)

**Impact**: Hard to find scripts, unclear dependencies.

### 3. **Complex Sync Nesting**
- `sync/` has 5 root files PLUS `sync/docs/` with duplicates PLUS `sync/repos/`
- Purpose of sync/docs/ unclear (staging area? outdated?)
- sync/repos/ is well-structured but separate

**Impact**: Duplicate maintenance, unclear sync strategy.

### 4. **Missing Test Infrastructure Patterns**
Tests use:
- Fixtures (dependency injection) → Scripts hardcode paths
- Markers (organization by domain) → Scripts have no tags
- Structured logging → Scripts use basic logging
- Base classes with shared setup → Scripts duplicate code

**Impact**: Scripts harder to maintain and test.

### 5. **Performance Scripts Scattered**
- Phase 17 profiling: 9 separate files at root
- Parametrization: 5 separate files at root
- No shared base class or utility

**Impact**: Hard to run, maintain, or add new profiling scripts.

---

## Consolidation Plan

### New Structure (PROPOSED)

```
scripts/
├── __init__.py
├── cli/ ............................. CLI interface
│   ├── __init__.py
│   └── interface.py ................. Main CLI (from cli.py)
├── docs/ ............................ Documentation
│   ├── __init__.py
│   └── generator.py ................. DocsGenerator (from docs_generator.py)
├── profiling/ ....................... Performance/Profiling tools
│   ├── __init__.py
│   ├── base.py ...................... BaseProfiler (shared patterns)
│   ├── phase17/
│   │   ├── __init__.py
│   │   ├── profiling.py ............. phase17_profiling.py
│   │   ├── gate_closure_validation.py
│   │   ├── concurrency_baseline.py
│   │   └── [etc. - 6 more files]
│   └── parametrization/
│       ├── __init__.py
│       ├── measurement.py ........... measure_parametrization_perf.py
│       ├── dashboard.py ............. parametrization_dashboard.py
│       └── [etc. - 3 more files]
├── sync/ ............................ File/Repo synchronization
│   ├── __init__.py
│   ├── base.py ...................... BaseSyncModule (shared patterns)
│   ├── autosync.py .................. Main orchestrator (KEEP)
│   ├── file_sync.py ................. Generic file sync (from syncit.py)
│   ├── config_sync.py ............... Config sync (from syncConfig.py)
│   ├── cleanup.py ................... Cleanup sync (from syncClean.py)
│   ├── mobile_sync.py ............... Mobile sync (from syncMobile.py)
│   └── repos/ ....................... Multi-repo operations (KEEP STRUCTURE)
│       ├── __init__.py
│       ├── daily_sync.py ............ Main orchestrator
│       ├── reference_sync.py
│       ├── reference_search.py
│       ├── archive_workflow.py
│       ├── logs_sync.py
│       └── nxgntch_sync.py
├── utils/ ........................... Utilities (UPDATED)
│   ├── __init__.py
│   ├── validation.py ................ RENAME: skill_validation.py (clarify purpose)
│   ├── startup_profiler.py .......... KEEP
│   ├── lazy_load_agents.py .......... KEEP
│   ├── lazy_load_skills.py .......... KEEP
│   ├── env_generator.py ............. FROM: generateEnvExample.py
│   └── hook_optimizer.py ............ FROM: hookOptimizer.py
├── validate/ ....................... Configuration validation (KEEP)
│   ├── __init__.py
│   ├── base.py ...................... BaseValidator (shared patterns)
│   ├── config_validator.py .......... FROM: validation.py (root)
│   ├── config_consistency.py ........ FROM: checkConfigConsistency.py
│   ├── doc_links.py ................. FROM: checkDocLinks.py
│   └── redundancy_check.py .......... FROM: checkRedundancy.py
├── coverage/ ....................... Coverage reporting (KEEP)
│   ├── __init__.py
│   └── reporter.py .................. KEEP
├── shell_scripts/ ................... Shell scripts (NEW - organize .sh files)
│   ├── archive-phase.sh
│   ├── daily-sync.sh
│   ├── ref-search.sh
│   ├── release-to-marketplace.sh
│   └── sync-reference-docs.sh
└── README.md ........................ Scripts documentation (NEW)
```

### Key Improvements

#### 1. Base Classes (from test patterns)
```python
# profiling/base.py
class BaseProfiler:
    """Shared profiling infrastructure."""
    
    def __init__(self, output_dir: Path = Path("profiling_output")):
        self.output_dir = output_dir
        self.logger = self._setup_logging()
        self.output_dir.mkdir(exist_ok=True)
    
    def _setup_logging(self):
        """Setup structured logging (like conftest)."""
        return logging.getLogger(self.__class__.__name__)
    
    def saveMetrics(self, name: str, data: dict):
        """Save metrics JSON."""
        output_file = self.output_dir / f"{name}.json"
        output_file.write_text(json.dumps(data, indent=2))
        self.logger.info(f"Saved: {output_file}")

# profiling/phase17/profiling.py
class Phase17Profiler(BaseProfiler):
    """Phase 17 specific profiling."""
    pass
```

#### 2. Shared Sync Base
```python
# sync/base.py
class BaseSyncModule:
    """Shared sync infrastructure."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.logger = logging.getLogger(self.__class__.__name__)
        self.filesProcessed = 0
    
    def logAction(self, action: str, path: str):
        """Log sync action."""
        self.logger.info(f"[{'DRY-RUN' if self.dry_run else 'SYNC'}] {action}: {path}")

# sync/file_sync.py
class FileSyncModule(BaseSyncModule):
    """File synchronization."""
    pass
```

#### 3. Fixture-Based Utilities
```python
# utils/fixtures.py (NEW)
"""Fixtures for script operations (like tests/conftest.py)."""

from pathlib import Path

class ScriptFixtures:
    """Reusable path and config fixtures."""
    
    @staticmethod
    def configDir() -> Path:
        return Path(__file__).parent.parent.parent / "config"
    
    @staticmethod
    def agentsDir() -> Path:
        return Path(__file__).parent.parent.parent / "agents"
    
    # ... more fixtures
```

---

## Migration Steps

### Phase 1: Create New Structure (No Changes Yet)
1. Create new directories: `cli/`, `docs/`, `profiling/`, `shell_scripts/`
2. Create `profiling/base.py`, `sync/base.py`, `validate/base.py`
3. Create `utils/fixtures.py` for common paths

### Phase 2: Move & Refactor Scripts (Backward Compatible)
1. Move `scripts/validation.py` → `scripts/validate/config_validator.py`
2. Rename `scripts/utils/validation.py` → `scripts/utils/skill_validation.py`
3. Move phase17 scripts → `scripts/profiling/phase17/`
4. Update imports to use new paths

### Phase 3: Consolidate Sync
1. **DELETE** `scripts/sync/docs/` directory (redundant)
2. Verify `scripts/sync/syncit.py` is correct version, delete duplicate
3. Keep `scripts/sync/repos/` (well-organized, separate concern)

### Phase 4: Update Scripts
1. Add base class inheritance to profiling scripts
2. Use fixtures for path resolution
3. Consolidate common logging/metrics patterns

### Phase 5: Documentation
1. Create `scripts/README.md` with script catalog and usage
2. Add docstrings to each module
3. Update CI/CD references to new paths

---

## Implementation Checklist

### CRITICAL (Do First)
- [ ] Audit imports: Find which validation.py is used where
- [ ] Audit imports: Find which sync/docs files are used
- [ ] Determine if sync/docs/ is active or dead code

### HIGH PRIORITY (Phase 1-2)
- [ ] Create new directory structure
- [ ] Create base classes (BaseProfiler, BaseSyncModule, BaseValidator)
- [ ] Create utils/fixtures.py
- [ ] Move root-level scripts to subdirectories
- [ ] Update all imports
- [ ] Delete duplicate files (sync/docs/*)
- [ ] Rename validation.py files for clarity

### MEDIUM PRIORITY (Phase 3-4)
- [ ] Refactor profiling scripts to use BaseProfiler
- [ ] Refactor sync scripts to use BaseSyncModule
- [ ] Refactor validate scripts to use BaseValidator
- [ ] Add structured logging to all scripts
- [ ] Consolidate common patterns

### LOW PRIORITY (Phase 5)
- [ ] Create scripts/README.md with catalog
- [ ] Add usage examples
- [ ] Update CI/CD references (if any)
- [ ] Performance testing of reorganized scripts

---

## Benefits

| Aspect | Before | After |
|--------|--------|-------|
| **Root-level scripts** | 19 | 0 (all organized) |
| **Easy to find script** | Hard (19 at root) | Easy (organized by category) |
| **Duplicate files** | 6+ conflicts | 0 (consolidated) |
| **Shared patterns** | None (code duplication) | 3 base classes (reusable) |
| **Test integration** | None | Fixtures + fixtures.py |
| **Documentation** | Scattered | scripts/README.md catalog |
| **Maintenance** | Error-prone | Organized by purpose |

---

## Related Documentation

- **File organization rules**: [`.claude/rules/file-organization.md`](../.claude/rules/file-organization.md)
- **Python conventions**: [`.claude/rules/python-conventions.md`](../.claude/rules/python-conventions.md)
- **Test infrastructure**: [`tests/conftest.py`](../tests/conftest.py) (patterns to follow)

---

**Status**: Ready for implementation  
**Created**: 2026-08-27
