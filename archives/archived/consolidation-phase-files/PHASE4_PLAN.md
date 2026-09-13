# Phase 4: Parallel Utility Consolidation Plan

**Cost Efficiency Strategy:**
- ✅ 4 independent parallel streams (zero dependencies)
- ✅ Batch file operations (single read/write per file)
- ✅ Reuse Phase 1-3 patterns for automation
- ✅ Import updates done once (Stream D)
- ✅ Single validation pass per stream
- ✅ Automated commit creation

**Timeline:** ~18 minutes total (vs 60+ sequential)
**Token Efficiency:** ~25% reduction vs Phase 3 (optimized grep patterns)
**Lines Saved:** ~330 LOC
**Files Updated:** 136 (overlapping coverage)

---

## Parallel Streams

### Stream A: Error Handler Consolidation
**Target:** `scripts/utils/error_handler.py`
**Task:** Consolidate error logging patterns
**Files:** 39 files
**Time:** 5-7 minutes
**LOC Saved:** ~80

**Operations:**
1. Create canonical error_handler.py
2. Extract error patterns from 29 files (except/pass)
3. Extract error patterns from 34 files (logger.error)
4. Extract error patterns from 7 files (self.log_error)
5. Create unified error helpers

---

### Stream B: File Utils Consolidation
**Target:** `scripts/utils/file_utils.py`
**Task:** Consolidate file operations
**Files:** 69 files
**Time:** 6-8 minutes
**LOC Saved:** ~150

**Operations:**
1. Create canonical file_utils.py
2. Extract Path() patterns (67 files)
3. Extract read patterns (22 files)
4. Extract write patterns (33 files)
5. Extract delete patterns (8 files)
6. Create unified file helpers

---

### Stream C: Result Classes Consolidation
**Target:** `scripts/utils/result.py`
**Task:** Consolidate result/response handling
**Files:** 28 files
**Time:** 4-5 minutes
**LOC Saved:** ~100

**Operations:**
1. Create canonical result.py
2. Extract dict result patterns (13 files)
3. Extract SyncResult patterns (1 file)
4. Extract get_summary patterns (4 files)
5. Create unified Result class hierarchy

---

### Stream D: Import Consolidation
**Target:** All files using error/file/result patterns
**Task:** Update all imports to canonical locations
**Files:** 136 files (overlapping)
**Time:** 3-4 minutes
**LOC Saved:** ~0 (refactoring only)

**Operations:**
1. Update imports from scattered error_handler locations
2. Update imports from scattered file_utils locations
3. Update imports from scattered result locations
4. Verify no dangling imports

---

## Cost Efficiency Optimizations

### 1. Batch Operations
```
Per Stream:
  - Single pass grep (all files at once)
  - Batch file reads (consolidated per stream)
  - Batch file writes (only if changed)
  - Single validation per module
```

### 2. Reusable Patterns
```
From Phase 1-3:
  ✓ Grep-based file discovery
  ✓ Set operations for dedup
  ✓ Path.read_text() for safe reads
  ✓ Subprocess.run for batch operations
```

### 3. Execution Strategy
```
Timeline:
  T+0m:  Start all 4 streams in parallel
  T+3m:  Stream C (Result) completes → Start Stream D prep
  T+5m:  Stream A (Error) completes
  T+8m:  Stream B (File) completes → All ready for import update
  T+9m:  Stream D (Imports) final pass
  T+18m: All streams done, ready for commits
```

### 4. Token Efficiency
```
Phase 3: ~15 tokens/file checked
Phase 4: ~8 tokens/file checked (optimized grep)
Savings: ~42% reduction from smart batching
```

---

## Parallel Dependencies

```
Independent (can start immediately):
  Stream A → Error Handler [39 files]
  Stream B → File Utils [69 files]
  Stream C → Result [28 files]

Dependent (after A, B, C complete):
  Stream D → Import updates [136 files]
```

**No blocking:** All streams operate on different files and modules

---

## Risk Mitigation

### Anti-Risks
- ✓ No circular imports (separate modules)
- ✓ Backward compatible (can run with old + new)
- ✓ Staged rollout (one stream at a time if needed)
- ✓ Full rollback possible (git reset)

### Test Strategy
```
After each stream:
  1. Check for syntax errors
  2. Verify imports resolve
  3. No circular dependencies
  4. File counts match expected

Before commit:
  1. Pre-commit hooks pass
  2. No duplicate definitions remain
  3. All old locations cleaned
```

---

## Execution Checklist

- [ ] Create error_handler.py
- [ ] Create file_utils.py  
- [ ] Create result.py
- [ ] Stream A: Extract error patterns
- [ ] Stream B: Extract file patterns
- [ ] Stream C: Extract result patterns
- [ ] Stream D: Update all imports
- [ ] Pre-commit validation
- [ ] Create commits (3 commits)
- [ ] Git push

---

## Expected Output

```
3 New Consolidation Modules:
  ✓ scripts/utils/error_handler.py (80 LOC)
  ✓ scripts/utils/file_utils.py (150 LOC)
  ✓ scripts/utils/result.py (100 LOC)

3 Git Commits:
  ✓ Create utility modules
  ✓ Consolidate error handling
  ✓ Consolidate file ops & results
  
Import Updates:
  ✓ 136 files updated
  ✓ 0 broken imports
  ✓ 0 circular dependencies

Metrics:
  Lines saved: ~330 LOC
  Execution time: ~18 min
  Token cost: ~42% reduced
  Risk level: MEDIUM → LOW (with staging)
```

---

**Ready to execute Phase 4?** ✓
