# Orphaned Skills Removal Checklist

**Task**: Clean up 6 orphaned Phase 6 skills  
**Time**: ~30 minutes  
**Safety**: High confidence (4 confirmed, 2 conditional)

---

## Step 1: Pre-Removal Verification

### Check what will be removed

```bash
cd /workspace/it
ls -lah skills/ | grep -E "modelChoiceOptimizer|performanceOptimizer|costOptimizationRecommender|phase6Assessment|costDashboard|autoScalingManager"
```

Expected output: All 6 directories exist.

### Verify no active references (beyond known broken ones)

```bash
# Should only find the broken test imports we already know about
grep -r "modelChoiceOptimizer\|performanceOptimizer\|costOptimizationRecommender" \
  app/ tests/ config/ --include="*.py" --include="*.yaml" 2>/dev/null | wc -l
```

Expected: 3 lines (the known broken imports + routing config reference)

---

## Step 2: Investigation (Optional but Recommended)

### Check dashboardConsumer functionality

```bash
grep -A 10 "class Dashboard\|def create_dashboard\|def get_dashboard" \
  skills/dashboardConsumer/*.py | head -30
```

**If it covers cost dashboards**: Remove costDashboard  
**If it doesn't**: Keep costDashboard (for now)

### Check autoScalingManager usage

```bash
grep -r "autoScalingManager\|AutoScalingManager" . --include="*.py" --include="*.yaml" \
  --exclude-dir=.git 2>/dev/null
```

**If used anywhere**: Keep autoScalingManager  
**If only in Phase 6 work**: Remove autoScalingManager

---

## Step 3: Remove Safe Skills (High Confidence)

### Remove 4 definitely safe skills

```bash
# Remove these 4 — very high overlap with registered skills
rm -rf skills/modelChoiceOptimizer
rm -rf skills/performanceOptimizer
rm -rf skills/costOptimizationRecommender
rm -rf skills/phase6Assessment

# Verify they're gone
ls -d skills/model* skills/performance* skills/costOptimization* skills/phase6* 2>&1
```

Expected: "No such file or directory" errors (they're gone ✅)

### Stage the removal

```bash
git add -A
git status  # Should show 4 deletions
```

---

## Step 4: Remove Conditional Skills (If Investigation Confirms)

If investigation showed:
- dashboardConsumer covers cost dashboards → Remove costDashboard
- autoScalingManager not used → Remove autoScalingManager

```bash
# If removing costDashboard:
rm -rf skills/costDashboard

# If removing autoScalingManager:
rm -rf skills/autoScalingManager

# Stage if removed:
git add -A
```

---

## Step 5: Validation

### Fix broken test imports

```bash
# Find broken imports
grep -n "from skills.modelChoiceOptimizer\|from skills.costDashboard" tests/*.py

# Delete or fix the test files
# Option A: Delete broken tests
rm tests/test_optimization_executor.py
rm tests/test_cost_dashboard_and_extensions.py

# Option B: Comment out imports and tests
# (Edit the files and remove the problematic imports/tests)

# Stage the changes:
git add tests/
```

### Fix broken routing config

```bash
# Find the dangling reference
grep -n "performanceOptimizer" config/routing.yaml

# Edit the file and remove the reference:
# vi config/routing.yaml  # Remove the performanceOptimizer section

git add config/routing.yaml
```

### Run validation checks

```bash
# 1. Config validation (should pass)
python config/validate-config.py
# Expected: ✅ Configuration validation PASSED

# 2. Dead code detection (should show 0 orphaned now)
python config/detect-dead-code.py
# Expected: ✅ No dead code detected

# 3. Tests still pass
pytest tests/ -q --tb=short
# Expected: All tests pass or minor failures from removed test files

# 4. No stray references
grep -r "modelChoiceOptimizer\|performanceOptimizer\|costOptimizationRecommender\|phase6Assessment\|costDashboard" \
  app/ skills/ config/ --include="*.py" --include="*.yaml" 2>/dev/null | wc -l
# Expected: 0 lines (no references)
```

---

## Step 6: Commit

```bash
# Commit the cleanup
git commit -m "refactor: remove 4-6 orphaned Phase 6 skills

Removed orphaned skills with high overlap to registered equivalents:
- modelChoiceOptimizer (→ intelligentOptimizer)
- performanceOptimizer (→ intelligentOptimizer + analyticsEngine)
- costOptimizationRecommender (→ costIntelligence)
- phase6Assessment (→ reportGenerator + analyticsEngine)
[- costDashboard (→ dashboardConsumer)]
[- autoScalingManager (if not in production)]

Verified:
- config validation passes
- dead code detection shows 0 orphaned
- no broken cross-references
- test suite passes

Analysis: docs/work/current/ORPHANED_SKILLS_OVERLAP_ANALYSIS.md

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

---

## Step 7: Verification (Final)

```bash
# Confirm everything still works
python config/validate-config.py
python config/detect-dead-code.py
pytest tests/ -q

# Check git log
git log --oneline -3
```

Expected final status:
```
✅ Configuration validation PASSED
   Agents: 6
   Skills: 28 (or 29-30 if keeping conditional ones)
   Models: 3

✅ No dead code detected
```

---

## Checklist

- [ ] Step 1: Pre-removal verification (run grep checks)
- [ ] Step 2: Investigation (check dashboardConsumer + autoScalingManager)
- [ ] Step 3: Remove 4 safe skills
- [ ] Step 3.5: Remove conditional skills (if decision made)
- [ ] Step 4: Fix broken test imports/tests
- [ ] Step 4.5: Fix broken routing config
- [ ] Step 5: Run all validation checks
- [ ] Step 6: Commit with detailed message
- [ ] Step 7: Final verification

**Estimated Time**: 30 minutes  
**Risk Level**: LOW (all removed skills are redundant)  
**Rollback**: `git reset --hard HEAD~1` (reverts the commit)

---

## If Something Goes Wrong

### Tests fail after removal

```bash
# Identify which test is failing
pytest tests/ -v

# Either:
# 1. Comment out the failing test (if it's testing removed skill)
# 2. Update the test to use registered skill instead
# 3. Delete the test if it's orphaned

# Then re-run
pytest tests/ -q
```

### Validation fails

```bash
# Run detailed validation
python config/validate-config.py  # Shows detailed errors
python config/detect-dead-code.py # Shows dead code

# Fix any issues, then re-run
```

### Need to restore

```bash
# Restore last commit (before removal)
git reset --hard HEAD~1

# Or restore specific skills from git history
git checkout HEAD~1 -- skills/modelChoiceOptimizer
git add skills/
git commit -m "restore: temporarily restore modelChoiceOptimizer"
```

---

## Success Criteria

All of these must pass:
- ✅ Config validation passes (0 errors)
- ✅ Dead code detection shows 0 orphaned
- ✅ No dangling references in config
- ✅ All tests pass (or expected deletions)
- ✅ No grep matches for removed skill names

---

## References

- **Analysis**: docs/work/current/ORPHANED_SKILLS_OVERLAP_ANALYSIS.md
- **Validator**: config/validate-config.py
- **Dead Code Detector**: config/detect-dead-code.py
- **Related**: PHASE_7_DEAD_CODE_FINDINGS.md

---

**Time to Execute**: ~30 minutes  
**Confidence Level**: ⭐⭐⭐⭐⭐ (Very High)  
**Difficulty**: Easy (mostly file deletion + validation)
