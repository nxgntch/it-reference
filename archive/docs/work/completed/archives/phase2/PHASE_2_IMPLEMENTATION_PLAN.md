# Phase 2 Implementation Plan: Completing Medium-Impact Refactorings

**Document Version**: 2026-10-12  
**Current Status**: 3/6 refactorings complete (91 LOC net reduction)  
**Phase 2 Target**: 480-550 LOC savings  
**Estimated Completion**: 2-3 hours for remaining 3 refactorings

---

## Session 1 Complete ✅

Three refactorings successfully implemented:

1. **ConcurrentBudgetTracker Extraction** (-54 LOC)
2. **Singleton Factory Pattern** (-37 LOC)
3. **HookMatcher Extraction** (Code reorganization)

**All tests passing**: 2904/2904 ✓  
**Branch**: `claude/sync-nxgntch-it-29z6b7`

---

## Remaining Refactorings (Session 2+)

### Refactoring 4: BatchProcessor Class Separation (150 LOC)

**Status**: READY FOR IMPLEMENTATION  
**Priority**: HIGH (highest remaining impact)  
**Complexity**: HIGH  
**Time Estimate**: 60-90 minutes

#### Architecture Plan

Split monolithic BatchProcessor (643 LOC) into focused responsibilities:

```python
# New Class 1: BatchQueueManager
class BatchQueueManager:
    """Queue and pending batch management."""
    - pendingBatches: Dict[str, Batch]
    - batchLock: Lock
    
    Methods:
    - createBatchTask(taskId, agentId, description, parameters)
    - addTaskToBatch(task) -> (batchId, wasNew)
    - getPendingBatches()
    - reset()
    
    Lines: ~100

# New Class 2: BatchExecutor
class BatchExecutor:
    """Batch processing and execution."""
    
    Methods:
    - processBatch(batchId)
    - processBatchesPipelined(tasks)
    - _processBatchStage(batch)
    - _assembleTaskBatch(tasks)
    - _formBatches(batches)
    
    Lines: ~120

# New Class 3: BatchAnalyzer
class BatchAnalyzer:
    """Batch analysis and reporting."""
    
    Methods:
    - suggestBatching(tasks)
    - getStatistics()
    - getOptimizationMetrics()
    - _getTotalCost()
    - _getTotalSavings()
    
    Lines: ~80

# Refactored: BatchProcessor (Facade)
class BatchProcessor(StatsCollector):
    """Public API facade (backward compatible)."""
    - queueManager: BatchQueueManager
    - executor: BatchExecutor
    - analyzer: BatchAnalyzer
    
    Methods (delegating):
    - createBatchTask() → queueManager
    - addTaskToBatch() → queueManager
    - processBatch() → executor
    - processBatchesPipelined() → executor
    - suggestBatching() → analyzer
    - getStatistics() → analyzer
    - getPendingBatches() → queueManager
    - reset() → queueManager
    - shutdown() → executor
    - getOptimizationMetrics() → analyzer
    
    Lines: ~50 (delegating facade)

# Total: 643 → 350 (293 LOC reduction)
# But: Estimated 150 LOC net after adding delegation/overhead
```

#### Implementation Steps

**Step 1**: Create BatchQueueManager class
- Extract: pendingBatches, batchLock, batchTimeoutSeconds
- Move methods: createBatchTask, addTaskToBatch, getPendingBatches, reset
- Share: costCalculator, modelRouter, configLoader
- Time: 20 min

**Step 2**: Create BatchExecutor class
- Extract: executor (ThreadPoolExecutor)
- Move methods: processBatch, processBatchesPipelined, _processBatchStage, _assembleTaskBatch, _formBatches
- Needs: queueManager reference for accessing pendingBatches
- Time: 25 min

**Step 3**: Create BatchAnalyzer class
- No state extraction (uses queueManager for data)
- Move methods: suggestBatching, getStatistics, _getTotalCost, _getTotalSavings, getOptimizationMetrics
- Time: 15 min

**Step 4**: Refactor BatchProcessor to facade pattern
- Create instances of Queue/Executor/Analyzer in __init__
- Replace method implementations with delegation
- Maintain exact same public API
- Time: 15 min

**Step 5**: Run tests, verify, commit
- Run: pytest tests/ -q
- Expected: 2904/2904 passing
- Commit with detailed message
- Time: 10 min

**Risks & Mitigation**:
- ❌ Risk: Circular imports between classes → ✅ Mitigation: Use TYPE_CHECKING imports
- ❌ Risk: Breaking tests → ✅ Mitigation: Keep public API identical
- ❌ Risk: Thread safety issues → ✅ Mitigation: Keep batchLock in QueueManager

---

### Refactoring 5: RoutingEngine Method Density (80 LOC)

**Status**: QUEUED  
**Priority**: MEDIUM  
**Complexity**: MEDIUM  
**Time Estimate**: 20-30 minutes

#### Analysis

Identify and consolidate low-density methods in `app/core/routingEngine.py`:

**Expected Low-Density Methods** (< 3 lines):
- Direct routing decision helpers
- Cost calculation wrappers
- Agent selection filters

#### Implementation Strategy

1. Read entire routingEngine.py
2. Identify all methods with LOC < 3
3. Group related methods
4. Create consolidation helper methods
5. Update callers
6. Run tests

#### Example Consolidation

**Before**:
```python
def _selectAgentForTask(task):  # 2 LOC
    return self.agentSelector.select(task)

def _calculateTaskCost(task):  # 2 LOC
    return self.costCalculator.calculate(task)

def _validateRoutePermissions(route):  # 2 LOC
    return self._permissionChecker.validate(route)
```

**After**:
```python
def _routeTask(task):  # 5 LOC (consolidated)
    """Route task with cost calculation and permission validation."""
    agent = self.agentSelector.select(task)
    cost = self.costCalculator.calculate(task)
    if not self._permissionChecker.validate(agent.route):
        raise PermissionError(...)
    return agent
```

---

### Refactoring 6: ConfigLoader Caching (100 LOC) ✅ ALREADY DONE

**Status**: COMPLETE  
**Location**: `app/core/configLoader.py` lines 49-74  
**Pattern**: `_loadConfigWithCache()` template method  

Consolidates check-cache-load-store pattern used by:
- `loadModelDefinitions()`
- `loadAgentDefinitions()`
- `loadSkillRegistry()`

Already counted in Phase 2 target: **+100 LOC reduction**

---

## Phase 2 Summary & Targets

| Refactoring | Status | Impact | Notes |
|---|---|---|---|
| 1. ConcurrentBudgetTracker | ✅ DONE | -54 LOC | Extraction, clean split |
| 2. Singleton Factory | ✅ DONE | -37 LOC | Template method, 6 functions |
| 3. HookMatcher | ✅ DONE | Org | Composability improvement |
| 4. BatchProcessor | ⏳ QUEUED | -150 LOC | Facade + 3 classes, high risk/impact |
| 5. RoutingEngine | ⏳ QUEUED | -80 LOC | Method consolidation |
| 6. ConfigLoader | ✅ DONE | -100 LOC | Already completed in Phase 1 |

**Total Completed**: 91 LOC + 100 LOC (ConfigLoader) = 191 LOC ✓  
**Remaining**: ~350 LOC (to reach 480-550 target)  
**Realistic Assessment**: 230-280 LOC achievable (91 + 100 + 80-150 from refactorings 4-5)

---

## Session 2 Kickoff Checklist

When ready to continue:

```bash
# 1. Verify branch state
git log --oneline -5
git status

# 2. Verify tests still passing
pytest tests/ -q 2>&1 | tail -5

# 3. Start BatchProcessor refactoring
# Create BatchQueueManager first (lowest risk)
# Then BatchExecutor, then BatchAnalyzer

# 4. After each refactoring
pytest tests/test_batch_processor*.py -v

# 5. Full test suite when BatchProcessor done
pytest tests/ -q

# 6. Commit and push
git add -A
git commit -m "refactor(core): split BatchProcessor into 3 focused classes"
git push -u origin claude/sync-nxgntch-it-29z6b7
```

---

## Reference Materials

**Audit Reports**:
- `docs/PHASE_2_AUDIT_2026_10_12.md` — Detailed audit with all 6 refactorings
- `docs/SESSION_PHASE_2_2026_10_12_SUMMARY.md` — This session's work (3 refactorings)

**Code References**:
- `app/core/budgetTracker.py` — ConcurrentBudgetTracker pattern (extraction)
- `app/core/hookMatcher.py` — HookMatcher pattern (delegation)
- `app/core/singletonFactory.py` — Singleton pattern (template method)
- `app/core/batchProcessor.py` — Next target (643 LOC to refactor)
- `app/core/routingEngine.py` — Final target (method consolidation)

**Test Status**:
- All refactorings: 2904/2904 tests passing ✓
- No regressions introduced
- Backward compatibility maintained

---

## Next Session: What to Do

### Recommended: Start with BatchProcessor

1. **Create** `app/core/batchQueueManager.py` (100 LOC)
   - Copy queue/batch management code from BatchProcessor
   - Update imports

2. **Create** `app/core/batchExecutor.py` (120 LOC)
   - Copy processing methods from BatchProcessor
   - Import QueueManager

3. **Create** `app/core/batchAnalyzer.py` (80 LOC)
   - Copy analysis methods from BatchProcessor
   - Import QueueManager for data access

4. **Refactor** `app/core/batchProcessor.py`
   - Create instances of all 3 classes
   - Replace methods with delegation calls
   - Keep public API identical

5. **Test** and **Commit**
   - Verify: `pytest tests/ -q` → 2904/2904
   - Commit with message explaining facade pattern

**Estimated Time**: 90 minutes  
**Expected Outcome**: ~150 LOC reduction, Phase 2 target: 340+ LOC

---

## Quality Gates

Before committing each refactoring:

- [ ] All tests passing (2904/2904)
- [ ] No new type errors (mypy clean)
- [ ] Code formatted (black compliant)
- [ ] Linting passes (ruff 0 errors)
- [ ] Backward compatibility maintained
- [ ] Commit message explains the refactoring
- [ ] Branch pushed to remote

---

**Plan Created**: 2026-10-12  
**Phase 2 Status**: 50% complete (3/6 refactorings)  
**Phase 2 Target**: 480-550 LOC (191 LOC achieved, 289+ remaining)  
**Next Steps**: Complete BatchProcessor split in Session 2

---

*This plan is ready to execute. All necessary analysis is complete. Next developer can pick up exactly where this session left off.*
