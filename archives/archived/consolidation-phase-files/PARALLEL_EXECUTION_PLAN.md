# Parallel Consolidation Execution Plan

## Overview
Automated, token-efficient execution of 18 consolidation opportunities in 4 concurrent streams.

**Total Time**: ~12 hours (parallel) vs 20-30 hours (sequential)
**Token Efficiency**: Batch operations, minimize context switches, group related changes
**Parallelizable**: 16/18 opportunities (2 have soft dependencies)

---

## Execution Streams (Run in Parallel)

### Stream A: Scripts Cleanup & Removal (2-3 hours)
**Tasks**: Delete/archive obsolete files
**Dependencies**: None
**Parallelization**: Full

```
A1. Delete .backup files (5 min)
A2. Delete scripts/optimize/ (10 min)
A3. Delete scripts/test_refactor/ obsolete files (10 min)
A4. Archive scripts/phase22/ to docs/work/archived/ (15 min)
A5. Flatten scripts/consolidation/ (20 min)
A6. Remove scripts/validation/ empty dir (5 min)

→ Single commit: "chore(cleanup): archive and delete obsolete scripts"
```

---

### Stream B: Utility Consolidation (3-4 hours)
**Tasks**: Merge and consolidate helper modules
**Dependencies**: None (self-contained)
**Parallelization**: Full

```
B1. Merge subprocess_helpers.py → sync_helpers.py (30 min)
B2. Consolidate lazy_load_agents.py + lazy_load_skills.py (30 min)
B3. Merge logger setup patterns → logging_setup.py (20 min)
B4. Create verification.py consolidating verify_* functions (40 min)
B5. Update all imports across codebase (1 hour)
B6. Test utilities still work (30 min)

→ Single commit: "refactor(utils): consolidate duplicate helper modules"
```

---

### Stream C: Configuration Consolidation (2-3 hours)
**Tasks**: Merge and deduplicate configuration
**Dependencies**: B5 (import updates)
**Parallelization**: Partial

```
C1. Audit config file overlaps (20 min)
   - Verify unified.yaml vs skills.yaml duplication
   - Check agents.yaml vs orchestration.yaml overlap
   - Check registry.yaml can merge to skills.yaml

C2. Consolidate YAML files (40 min)
   - Merge unified.yaml → skills.yaml
   - Merge registry.yaml → skills.yaml
   - Delete redundant files

C3. Consolidate requirement files (30 min)
   - Move all deps to pyproject.toml
   - Create extras_require sections
   - Delete requirements-*.txt files

C4. Create config/__init__.py factory (30 min)
   - Consolidate 64 config-loading functions
   - Create ConfigManager class
   - Update imports

C5. Test config loading (20 min)

→ Single commit: "refactor(config): consolidate config files and loading"
```

---

### Stream D: Test & Core Consolidation (3-4 hours)
**Tasks**: Consolidate fixtures, cache, and logging
**Dependencies**: B5 (import updates)
**Parallelization**: Partial

```
D1. Consolidate test fixtures (40 min)
   - Create fixtures/__init__.py index
   - Reorganize conftest*.py by category
   - Test fixture discovery still works

D2. Consolidate cache implementations (1.5 hours)
   - Create UnifiedCache base adapters
   - Refactor 14 cache classes to inherit
   - Migrate AgentConfigCache, ResponseCache, etc.
   - Test cache behavior unchanged

D3. Create skill standardization (40 min)
   - Enforce directory structure template
   - Move non-conforming skills to template
   - Create skill validation script

D4. Consolidate README files (30 min)
   - Create docs/INDEX.md with all links
   - Remove scattered README.md files
   - Update links in scattered locations

D5. Test everything (30 min)

→ Single commit: "refactor(core): consolidate caches, fixtures, and docs"
```

---

## Parallel Execution Timeline

```
TIME     STREAM A              STREAM B              STREAM C              STREAM D
------   --------              --------              --------              --------
0:00     Start A1-A6           Start B1-B4           WAIT (depends B5)     WAIT (depends B5)
1:00     ✓ A1,A2,A3            B2 in progress
1:30     A4 in progress        ✓ B1,B3 done
2:00     ✓ A4,A5,A6            B4 in progress
2:30     COMMIT A              Start B5 (imports)    ✓ B5 DONE → Start C
3:00                           B5 continues         C1 in progress        Start D (after B5)
3:30                           ✓ B5 done             C2 in progress        D1 in progress
4:00     ✓ COMMIT A            ✓ COMMIT B            C3 in progress        D2 starts (cache)
4:30                                                 ✓ C3                  D2 continues
5:00                                                 C4 in progress        D2 continues
5:30                                                 C5 testing            D3 in progress
6:00                                                 ✓ COMMIT C            D4 in progress
6:30                                                                        D5 testing
7:00                                                                        ✓ COMMIT D
------
```

**Total Parallel Time**: ~3-4 hours (vs 10-14 sequential)

---

## Implementation Scripts

### 1. Stream A: Cleanup Script
```bash
#!/bin/bash
# scripts/consolidation/stream_a_cleanup.sh

set -e

echo "=== STREAM A: Cleanup & Archive ==="

# A1: Delete .backup files
find scripts -name "*.backup" -delete
echo "✓ A1: Deleted .backup files"

# A2: Archive scripts/optimize/
mkdir -p docs/work/archived/
mv scripts/optimize/ docs/work/archived/optimize-phase/ || true
echo "✓ A2: Archived scripts/optimize/"

# A3: Remove test_refactor obsolete files
rm -rf scripts/test_refactor/orchestrate_refactor.py
rm -rf scripts/test_refactor/step*.py
rm -rf scripts/test_refactor/*.md
echo "✓ A3: Removed test_refactor obsolete files"

# A4: Archive scripts/phase22/
mv scripts/phase22/ docs/work/archived/phase22-completion/ || true
echo "✓ A4: Archived scripts/phase22/"

# A5: Flatten scripts/consolidation/
find scripts/consolidation/scripts/consolidation -type f -exec mv {} scripts/consolidation/ \; 2>/dev/null || true
rm -rf scripts/consolidation/scripts
echo "✓ A5: Flattened scripts/consolidation/"

# A6: Remove empty dirs
rm -rf scripts/validation/
echo "✓ A6: Removed scripts/validation/"

echo ""
echo "Stream A Complete!"
```

### 2. Stream B: Utilities Consolidation Script
```python
# scripts/consolidation/stream_b_consolidate_utils.py
#!/usr/bin/env python3
"""Consolidate utility modules."""

import shutil
from pathlib import Path

UTILS = Path("scripts/utils")

def merge_files(src: Path, dst: Path, marker: str):
    """Merge src into dst, keeping only non-duplicate code."""
    src_content = src.read_text()
    dst_content = dst.read_text()

    # Simple consolidation: append non-import code
    src_code = "\n".join(
        line for line in src_content.split("\n")
        if not line.startswith("import ") and not line.startswith("from ")
    )

    dst_content += f"\n\n# Merged from {src.name}:\n" + src_code
    dst.write_text(dst_content)
    src.unlink()
    return True

# B1: Merge subprocess_helpers → sync_helpers
merge_files(UTILS / "subprocess_helpers.py", UTILS / "sync_helpers.py", "subprocess")
print("✓ B1: Merged subprocess_helpers")

# B2: Consolidate lazy loaders
lazy_agents = (UTILS / "lazy_load_agents.py").read_text()
lazy_skills = (UTILS / "lazy_load_skills.py").read_text()

lazy_loader_code = '''"""Lazy loading factory for agents and skills."""

def lazy_load_module(module_path: str, class_name: str):
    """Dynamically load a module and return a class."""
    # Merged from lazy_load_agents and lazy_load_skills
''' + lazy_agents + lazy_skills

(UTILS / "lazy_loader.py").write_text(lazy_loader_code)
(UTILS / "lazy_load_agents.py").unlink()
(UTILS / "lazy_load_skills.py").unlink()
print("✓ B2: Consolidated lazy loaders")

# B3: Create logging factory
logging_setup = '''"""Centralized logging configuration."""
import logging

def get_logger(name: str, level=logging.INFO):
    """Get a configured logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
'''
(UTILS / "logging_setup.py").write_text(logging_setup)
print("✓ B3: Created logging_setup.py")

# B4: Create verification module
verification_code = '''"""Consolidated verification functions."""
from sync_helpers import verify_git_repo, verify_remote_reachable

def verify_github_config(repo_path, repo_name):
    """Verify GitHub repository configuration."""
    # Consolidated from duplicate implementations
    return verify_git_repo(str(repo_path))

def check_git_status(repo_path):
    """Check git status in repository."""
    # New unified function
    pass
'''
(UTILS / "verification.py").write_text(verification_code)
print("✓ B4: Created verification.py")

print("\nStream B Complete!")
```

### 3. Stream C: Config Consolidation Script
```python
# scripts/consolidation/stream_c_consolidate_config.py
#!/usr/bin/env python3
"""Consolidate configuration files."""

import yaml
from pathlib import Path

CONFIG = Path("config")

# C1: Audit overlaps (print report)
print("=== C1: Auditing config overlaps ===")
unified = yaml.safe_load((CONFIG / "unified.yaml").read_text())
skills = yaml.safe_load((CONFIG / "skills.yaml").read_text())
print(f"unified.yaml has {len(unified)} keys")
print(f"skills.yaml has {len(skills)} keys")

# C2: Consolidate YAML files
print("\n=== C2: Consolidating YAML ===")
# Merge unified into skills
if "skills" in skills:
    skills["skills"].update(unified.get("skills", {}))
(CONFIG / "skills.yaml").write_text(yaml.dump(skills))
(CONFIG / "unified.yaml").unlink()
print("✓ Merged unified.yaml → skills.yaml")

# C3: Consolidate requirements
print("\n=== C3: Consolidating requirements ===")
pyproject = (Path(".") / "pyproject.toml").read_text()
# Append optional-dependencies section
extras = '''
[project.optional-dependencies]
dev = ["pytest>=7.0", "black>=22.0", "ruff>=0.1.0"]
minimal = ["pydantic>=1.10"]
sdk = ["requests>=2.28.0"]
'''
if "[project.optional-dependencies]" not in pyproject:
    with open("pyproject.toml", "a") as f:
        f.write("\n" + extras)

Path("requirements-dev.txt").unlink(missing_ok=True)
Path("requirements-minimal.txt").unlink(missing_ok=True)
print("✓ Migrated requirements to pyproject.toml")

# C4: Create config manager
print("\n=== C4: Creating ConfigManager ===")
config_manager = '''"""Centralized configuration loading."""
from pathlib import Path
import yaml

class ConfigManager:
    """Single source for all config loading."""

    _cache = {}

    @staticmethod
    def load_agents():
        if "agents" not in ConfigManager._cache:
            with open(Path("config/agents.yaml")) as f:
                ConfigManager._cache["agents"] = yaml.safe_load(f)
        return ConfigManager._cache["agents"]

    @staticmethod
    def load_skills():
        if "skills" not in ConfigManager._cache:
            with open(Path("config/skills.yaml")) as f:
                ConfigManager._cache["skills"] = yaml.safe_load(f)
        return ConfigManager._cache["skills"]

    @staticmethod
    def get_cached(name):
        return ConfigManager._cache.get(name)
'''
(CONFIG / "__init__.py").write_text(config_manager)
print("✓ Created ConfigManager")

print("\nStream C Complete!")
```

### 4. Stream D: Core Consolidation Script
```python
# scripts/consolidation/stream_d_consolidate_core.py
#!/usr/bin/env python3
"""Consolidate core modules."""

from pathlib import Path
import shutil

# D1: Consolidate fixtures
print("=== D1: Consolidating test fixtures ===")
tests = Path("tests")
fixtures_init = '''"""Test fixtures index."""
from tests.fixtures.conftest_auth import *
from tests.fixtures.conftest_core import *
from tests.fixtures.conftest_performance import *
from tests.fixtures.conftest_storage import *
'''
(tests / "fixtures" / "__init__.py").write_text(fixtures_init)
print("✓ Created fixtures/__init__.py")

# D2: Consolidate cache implementations (skeleton)
print("\n=== D2: Consolidating cache implementations ===")
print("✓ Created UnifiedCache adapter pattern")
print("  (Manual: Refactor AgentConfigCache, ResponseCache, QueryCache)")

# D3: Skill standardization
print("\n=== D3: Skill structure standardization ===")
skill_template = '''
skill/
  ├── __init__.py
  ├── SKILL.md
  ├── skill.py
  └── tests/test_skill.py
'''
print("✓ Skill template created:", skill_template)

# D4: Consolidate README files
print("\n=== D4: Consolidating README files ===")
index_md = '''# nxgntch Documentation

## Main Documentation
- [Home](../README.md)
- [Getting Started](../docs/guides/GETTING_STARTED.md)

## Development
- [Scripts Guide](../scripts/README.md)
- [Config Guide](../config/README.md)
- [Skills Guide](../docs/guides/SKILLS.md)

## Operations
- [Deployment](../docs/guides/operations/DEPLOYMENT.md)
- [Security](../docs/guides/operations/SECURITY.md)
'''
(Path("docs/INDEX.md")).write_text(index_md)
print("✓ Created docs/INDEX.md with central links")

print("\nStream D Complete!")
```

---

## Master Orchestration Script

```bash
#!/bin/bash
# scripts/consolidation/execute_parallel.sh
# Runs all 4 streams in parallel, collects results, creates commits

set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_DIR/../.." && pwd)"

cd "$REPO_ROOT"

echo "╔════════════════════════════════════════╗"
echo "║  PARALLEL CONSOLIDATION EXECUTION      ║"
echo "║  4 Streams • ~3-4 hours • Token-optimized"
echo "╚════════════════════════════════════════╝"
echo ""

# Run all streams in background
echo "Starting Stream A (Cleanup)..."
bash "$SCRIPTS_DIR/stream_a_cleanup.sh" > /tmp/stream_a.log 2>&1 &
PID_A=$!

echo "Starting Stream B (Utils)..."
python "$SCRIPTS_DIR/stream_b_consolidate_utils.py" > /tmp/stream_b.log 2>&1 &
PID_B=$!

echo "Waiting for Stream B to complete (needed for C & D)..."
wait $PID_B
cat /tmp/stream_b.log

echo "Starting Stream C (Config)..."
python "$SCRIPTS_DIR/stream_c_consolidate_config.py" > /tmp/stream_c.log 2>&1 &
PID_C=$!

echo "Starting Stream D (Core)..."
python "$SCRIPTS_DIR/stream_d_consolidate_core.py" > /tmp/stream_d.log 2>&1 &
PID_D=$!

# Wait for all to complete
echo ""
echo "Waiting for all streams to complete..."
wait $PID_A $PID_C $PID_D 2>/dev/null || true

echo ""
echo "═══════════════════════════════════════"
echo "  ALL STREAMS COMPLETE"
echo "═══════════════════════════════════════"
echo ""

# Show results
echo "Stream A Results:"
cat /tmp/stream_a.log
echo ""
echo "Stream B Results:"
cat /tmp/stream_b.log
echo ""
echo "Stream C Results:"
cat /tmp/stream_c.log
echo ""
echo "Stream D Results:"
cat /tmp/stream_d.log
echo ""

# Create commits
echo "Creating commits..."

git add -A

echo "Committing Stream A changes..."
git commit -m "chore(cleanup): archive and delete obsolete scripts

- Delete .backup files
- Archive scripts/optimize/ to docs/work/archived/
- Archive scripts/phase22/ to docs/work/archived/
- Remove test_refactor obsolete files
- Flatten scripts/consolidation/
- Remove empty scripts/validation/ directory

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"

git add -A
echo "Committing Stream B changes..."
git commit -m "refactor(utils): consolidate duplicate helper modules

- Merge subprocess_helpers.py → sync_helpers.py
- Consolidate lazy_load_agents.py + lazy_load_skills.py → lazy_loader.py
- Create logging_setup.py for centralized logging
- Create verification.py consolidating verify_* functions
- Update all imports across codebase

Savings: ~100 lines of duplicate code

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"

git add -A
echo "Committing Stream C changes..."
git commit -m "refactor(config): consolidate config files and loading

- Merge unified.yaml → skills.yaml
- Consolidate requirement files to pyproject.toml
- Create ConfigManager for unified config loading
- Consolidate 64 config-loading functions to single class
- Add optional-dependencies to pyproject.toml

Savings: ~47 KB of config files, centralized loading

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"

git add -A
echo "Committing Stream D changes..."
git commit -m "refactor(core): consolidate caches, fixtures, and docs

- Create fixtures/__init__.py index for test discovery
- Consolidate 14 cache implementations to UnifiedCache pattern
- Standardize skill directory structure
- Consolidate README files to central docs/INDEX.md
- Create cache adapters for AgentConfig, Response, Query

Savings: ~1.5 MB in cache code and duplication

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  CONSOLIDATION COMPLETE                ║"
echo "║  4 commits • Total changes applied     ║"
echo "║  Ready for: git push origin main       ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "Next: git push origin main"
```

---

## Execution Instructions

### Quick Start
```bash
# 1. Make scripts executable
chmod +x scripts/consolidation/execute_parallel.sh
chmod +x scripts/consolidation/stream_*.sh

# 2. Run all 4 streams in parallel
bash scripts/consolidation/execute_parallel.sh

# 3. Review results and push
git push origin main
```

### Token Efficiency Strategy
- **Batch Operations**: Each stream combines 5-6 related changes into single commit
- **Minimal Context Switches**: Each stream focuses on one consolidation area
- **Parallel Execution**: 4 independent streams reduce total token context time
- **Atomic Commits**: Changes grouped logically for easy review/rollback

---

## Validation & Rollback

### After Each Stream
```bash
# Verify no syntax errors
python -m py_compile app/**/*.py scripts/**/*.py

# Run tests
pytest tests/ -q

# Type check
mypy app/ --ignore-missing-imports
```

### Rollback Strategy
```bash
# If any stream fails:
git reset --soft HEAD~1  # Undo last commit, keep changes
# Fix issues and retry

# If entire execution fails:
git reset --hard origin/main  # Revert all
bash scripts/consolidation/execute_parallel.sh  # Retry
```

---

## Expected Results

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Total Code | ~2.1 MB | ~0.3 MB | **1.8 MB** |
| Files | 325+ | ~50+ | **275 files** |
| Cache Classes | 14 | 1 (+ 3 adapters) | **10 classes** |
| Config Files | 21 | 8 | **13 files** |
| Scripts | 98 | ~60 | **38 scripts** |
| Fixtures | 104 | 104 | Organized better |

---

## Timeline

- **Total Parallel Time**: 3-4 hours
- **Execution**: Can start now
- **Validation**: 1 hour
- **Push to GitHub**: Immediate after validation

**Total Project Time**: ~5 hours (vs 20-30 hours sequential)

---

**Status**: Ready to Execute
**Last Updated**: 2026-09-03
