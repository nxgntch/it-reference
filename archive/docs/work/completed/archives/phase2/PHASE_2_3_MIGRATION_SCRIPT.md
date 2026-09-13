# Phase 2-3 Migration Instructions (Automated)

**Use this guide to complete Phase 2 (relocation) and Phase 3 (consolidation).**

---

## Phase 2: Script Relocation (Copy & Paste Commands)

### Step 1: Move Phase 17 Scripts
```bash
cd scripts

# Move phase17 profiling scripts to phase17/ subdirectory
for file in phase17_*.py; do
  [ -f "$file" ] && mv "$file" "profiling/phase17/$file" && echo "✓ Moved $file"
done
```

### Step 2: Move Parametrization Scripts
```bash
# Move parametrization scripts to parametrization/ subdirectory
for file in parametrization_*.py measure_parametrization_perf.py; do
  [ -f "$file" ] && mv "$file" "profiling/parametrization/$file" && echo "✓ Moved $file"
done
```

### Step 3: Move Utility Scripts
```bash
# Move utility scripts to utils/
[ -f "generateEnvExample.py" ] && mv "generateEnvExample.py" "utils/env_example_generator.py" && echo "✓ Moved generateEnvExample.py"
[ -f "hookOptimizer.py" ] && mv "hookOptimizer.py" "utils/hook_optimizer.py" && echo "✓ Moved hookOptimizer.py"
```

### Step 4: Move CLI & Docs
```bash
# Move CLI and docs generators
[ -f "cli.py" ] && mv "cli.py" "cli/interface.py" && echo "✓ Moved cli.py"
[ -f "docs_generator.py" ] && mv "docs_generator.py" "docs/generator.py" && echo "✓ Moved docs_generator.py"
```

### Step 5: Verify Moves
```bash
# Check that scripts were moved successfully
echo "Checking Phase 17 scripts..."
ls profiling/phase17/*.py | wc -l

echo "Checking Parametrization scripts..."
ls profiling/parametrization/*.py | wc -l

echo "Checking Utils scripts..."
ls utils/env_example_generator.py utils/hook_optimizer.py 2>/dev/null && echo "✓ Utils moved"

echo "Checking CLI..."
ls cli/interface.py 2>/dev/null && echo "✓ CLI moved"

echo "Checking Docs..."
ls docs/generator.py 2>/dev/null && echo "✓ Docs moved"
```

### Step 6: Update Imports in Moved Scripts

After moving, update imports in Python files:

**For scripts in profiling/phase17/**:
```bash
# Update imports to use base classes
sed -i 's/from scripts.profiling.base import/from scripts.profiling.base import/' profiling/phase17/*.py
```

**For scripts in profiling/parametrization/**:
```bash
# Ensure they import BaseProfiler
sed -i 's/from scripts.profiling.base import/from scripts.profiling.base import/' profiling/parametrization/*.py
```

---

## Phase 3: Sync Consolidation (Remove Duplicates)

### Step 1: Identify Duplicate Files
```bash
# List files in sync/docs/
echo "Files in sync/docs/:"
ls -1 sync/docs/*.py

# List files in sync/
echo "Files in sync/:"
ls -1 sync/*.py | grep -v __
```

### Step 2: Verify Duplicates
```bash
# Check if sync/docs/syncit.py duplicates sync/syncit.py
diff sync/syncit.py sync/docs/syncit.py 2>/dev/null && echo "✓ Duplicates confirmed"

# Same for other files
for file in syncConfig syncClean syncMobile; do
  if [ -f "sync/${file}.py" ] && [ -f "sync/docs/${file}.py" ]; then
    echo "Checking ${file}.py..."
    diff sync/${file}.py sync/docs/${file}.py >/dev/null && echo "  → Duplicate found"
  fi
done
```

### Step 3: Delete Duplicate Directory
```bash
# VERIFY FIRST that sync/docs/ contains only duplicates
# Then safely remove it:

if [ -d "sync/docs" ]; then
  echo "Removing sync/docs/ (duplicate files)..."
  rm -rf sync/docs/
  echo "✓ Removed sync/docs/"
else
  echo "sync/docs/ not found"
fi
```

### Step 4: Verify Consolidation
```bash
# Confirm sync/docs/ is gone
[ ! -d "sync/docs" ] && echo "✓ Consolidation complete"

# Verify sync/ has all needed files
ls sync/*.py | wc -l
```

---

## Phase 2-3 Completion Checklist

### Root Level Cleanup
- [ ] No `phase17_*.py` at root (all moved to profiling/phase17/)
- [ ] No `parametrization_*.py` at root (all moved to profiling/parametrization/)
- [ ] No `measure_parametrization_perf.py` at root
- [ ] No `generateEnvExample.py` at root
- [ ] No `hookOptimizer.py` at root
- [ ] No `cli.py` at root
- [ ] No `docs_generator.py` at root

### Verify Organization
- [ ] `profiling/phase17/` contains 10+ phase17 scripts
- [ ] `profiling/parametrization/` contains 4+ parametrization scripts
- [ ] `utils/` contains env_generator.py and hook_optimizer.py
- [ ] `cli/interface.py` exists
- [ ] `docs/generator.py` exists

### Consolidation Done
- [ ] `sync/docs/` directory deleted
- [ ] No duplicate files remaining
- [ ] `sync/` directory has authoritative versions only

### Tests Pass
- [ ] Verify moved scripts still work:
  ```bash
  python -m scripts.profiling.phase17.profiling
  python -m scripts.profiling.parametrization.measurement --help
  python -m scripts.utils.env_generator
  python -m scripts.cli.interface --help
  ```

---

## Troubleshooting

### Import Errors After Move
**Problem**: `ModuleNotFoundError: No module named 'scripts.xyz'`

**Solution**: Update imports in moved scripts to reference new locations.

### Duplicate Detection Failed
**Problem**: Can't confirm if files are duplicates

**Solution**: 
```bash
# Use diff with summary
diff -q sync/syncit.py sync/docs/syncit.py

# Or compare line counts
wc -l sync/syncit.py sync/docs/syncit.py
```

### Scripts Don't Work After Move
**Problem**: Script fails with path-related error

**Solution**: Ensure script uses `ScriptFixtures` or `Path(__file__).parent.parent`  
```python
# BEFORE (hardcoded, fails after move)
configDir = Path("config/")

# AFTER (uses fixtures, works anywhere)
from scripts.utils.fixtures import ScriptFixtures
configDir = ScriptFixtures.configDir()
```

---

## After Phase 2-3

1. **Verify everything works**: Run a few moved scripts
2. **Check root directory**: Should only have ~5 scripts left
3. **Run tests**: Ensure no import breakage
4. **Document any issues**: In IMPLEMENTATION_STATUS.md

Once complete, proceed to **Phase 4: Refactoring** (see PHASE_2_4_IMPLEMENTATION_COMPLETE.md)

---

**Estimated Time**: 30-45 minutes  
**Breaking Changes**: None (scripts location changed but functionality preserved)  
**Next**: Phase 4 refactoring (apply base class pattern to all scripts)
