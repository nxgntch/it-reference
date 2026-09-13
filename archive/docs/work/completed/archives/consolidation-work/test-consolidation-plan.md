# Test Consolidation Plan

**Goal**: Reduce test directory from 68 files to ~45 files (34% reduction), improve maintainability.

**Savings Target**: ~1M disk space + clearer test organization

---

## Phase 1: High-Priority Consolidations (Estimated: 600K savings)

### 1. Cost Management Tests → `testCostManagement.py`

**Current files** (3 files, ~100K):
- `testCostAnalysis.py` (32K) - Cost metrics, breakdowns, analysis
- `testCostForecasting.py` (24K) - Forecasting and budget enforcement
- `testConcurrentBudgetTracking.py` (8K) - Concurrent spend tracking

**Strategy**:
1. Create `testCostManagement.py` with structure:
   ```python
   # Section 1: Cost Metrics & Breakdowns (from testCostAnalysis)
   class TestCostMetric
   class TestCostBreakdown
   class TestCostAnalysisResult
   
   # Section 2: Cost Forecasting (from testCostForecasting)
   class TestCostForecast
   class TestBudgetEnforcement
   
   # Section 3: Concurrent Budget Tracking (from testConcurrentBudgetTracking)
   class TestConcurrentBudgetTracker
   ```

2. Delete original 3 files
3. Run tests: `pytest tests/testCostManagement.py -v`

**Benefits**: Single file for all cost operations, easier maintenance

---

### 2. Concurrency Tests → `testConcurrency.py`

**Current files** (5 files, ~80K):
- `testAsyncPatterns.py` (20K) - Async patterns
- `testConcurrentOrchestrator.py` (8K) - Concurrent orchestration
- `testLoadConcurrent.py` (16K) - Load testing
- `testOptimizationExamples.py` (16K) - Optimization examples
- `testPerformanceBaseline.py` (16K) - Performance baselines

**Strategy**:
1. Create `testConcurrency.py`:
   ```python
   # Section 1: Async Patterns
   class TestAsyncPatterns
   
   # Section 2: Concurrent Orchestration
   class TestConcurrentOrchestrator
   
   # Section 3: Load Testing
   class TestLoadTesting
   
   # Section 4: Performance Optimization
   class TestPerformanceOptimization
   class TestPerformanceBaseline
   ```

2. Delete original 5 files
3. Run tests: `pytest tests/testConcurrency.py -v`

**Benefits**: All async/concurrent tests in one place

---

### 3. Configuration Tests → `testConfiguration.py`

**Current files** (4 files, ~90K):
- `testConfigPatterns.py` (19K) - Config loading patterns
- `testConfigSsotVerification.py` (16K) - SSOT verification
- `testCoreValidation.py` (18K) - Core validation
- `testValidation.py` (32K) - Comprehensive validation

**Strategy**:
1. Create `testConfiguration.py`:
   ```python
   # Section 1: Config Loading (from testConfigPatterns)
   class TestConfigLoading
   class TestConfigValidation
   class TestEnvironmentOverrides
   
   # Section 2: SSOT Verification (from testConfigSsotVerification)
   class TestSingleSourceOfTruth
   
   # Section 3: Data Validation (from testValidation)
   class TestInputValidation
   class TestSchemaValidation
   class TestYamlValidation
   ```

2. Delete original 4 files
3. Run tests: `pytest tests/testConfiguration.py -v`

**Note**: This will have ~85 test functions, consider splitting if > 100

---

### 4. Sync Pipeline Tests → `testSyncPipeline.py`

**Current files** (4 files, ~80K):
- `testSyncit.py` (20K) - Sync module
- `testSyncitIntegration.py` (20K) - Sync integration
- `testNxgntchSync.py` (12K) - nxgntch sync
- `testCoreSyncPipeline.py` (18K) - Core sync

**Strategy**:
1. Create `testSyncPipeline.py`:
   ```python
   # Section 1: Core Sync (from testCoreSyncPipeline)
   class TestCoreSyncPipeline
   
   # Section 2: Sync Module (from testSyncit)
   class TestSyncModule
   
   # Section 3: Integration (from testSyncitIntegration)
   class TestSyncIntegration
   
   # Section 4: nxgntch Sync (from testNxgntchSync)
   class TestNxgntchSync
   ```

2. Delete original 4 files
3. Run tests: `pytest tests/testSyncPipeline.py -v`

**Benefits**: All sync-related tests consolidated

---

### 5. Security Tests → `testSecurity.py`

**Current files** (2 files, ~40K):
- `testSecurityPatterns.py` (20K) - Security patterns
- `testSecurityHardening.py` (12K) - Hardening

**Strategy**:
1. Create `testSecurity.py`:
   ```python
   # Section 1: Security Patterns (from testSecurityPatterns)
   class TestSecurityPatterns
   class TestAccessControl
   class TestAuthenticationFlow
   
   # Section 2: Security Hardening (from testSecurityHardening)
   class TestSecurityHardening
   class TestEncryption
   ```

2. Delete original 2 files
3. Run tests: `pytest tests/testSecurity.py -v`

---

### 6. Resilience Tests → `testResilience.py`

**Current files** (4 files, ~68K):
- `testResiliencePatterns.py` (16K) - Patterns
- `testResilienceOptimization.py` (16K) - Optimization
- `testResilienceMonitoring.py` (20K) - Monitoring
- `testResilienceStress.py` (16K) - Stress testing

**Strategy**:
1. Create `testResilience.py`:
   ```python
   # Section 1: Resilience Patterns
   class TestResiliencePatterns
   
   # Section 2: Optimization
   class TestResilienceOptimization
   
   # Section 3: Monitoring
   class TestResilienceMonitoring
   
   # Section 4: Stress Testing
   class TestStressTesting
   ```

2. Delete original 4 files
3. Run tests: `pytest tests/testResilience.py -v`

---

### 7. Validation Tests → `testDataValidation.py`

**Current files** (2 files, ~48K):
- `testValidationPatterns.py` (16K) - Patterns
- (Already consolidated some into testConfiguration.py above)

**Strategy**:
- Merge remaining validation tests into `testConfiguration.py`
- Or keep as `testDataValidation.py` if data-specific

---

## Phase 2: Archive Candidates (Estimated: 200K savings)

### Archive (move to `.archive/tests/` for reference)

1. **`testFixturePatterns.py`** (20K)
   - Better as documentation in conftest.py or docs/
   - Move fixture examples to conftest.py docstrings

2. **`testPropertyBased.py`** (12K)
   - Merge property-based tests into domain-specific test files
   - Or keep if property-based testing is critical

3. **`testPerformanceProfiling.py`** (16K)
   - Covered by testPerformanceBaseline.py
   - Keep only if profiling-specific

4. **`testHookOptimization.py`** (8K)
   - Covered by testHookExecutor.py
   - Merge remaining tests into testHookExecutor.py

5. **`testMocking.py`** (8K)
   - Better as documentation/patterns in conftest.py
   - Move to conftest.py as fixture examples

6. **`testIntermediateSkills.py`** (8K)
   - Merge into testSkillsModules.py

---

## Phase 3: Minor Consolidations (Estimated: 150K savings)

### Merge into existing files

| Source | Destination | Reason |
|--------|-------------|--------|
| testAgentConfigCache.py | testAgentsModule.py | Agent-related |
| testIntermediateSkills.py | testSkillsModules.py | Skills-related |
| testHookOptimization.py | testHookExecutor.py | Hook-related |
| testPluginManifest.py | testSkillsModules.py | Plugin/skill related |

---

## Implementation Order

### Week 1 (High Priority)
1. Phase 1.1: Cost Management → testCostManagement.py
2. Phase 1.2: Concurrency → testConcurrency.py
3. Phase 1.3: Configuration → testConfiguration.py

### Week 2 (Medium Priority)
4. Phase 1.4: Sync Pipeline → testSyncPipeline.py
5. Phase 1.5: Security → testSecurity.py
6. Phase 1.6: Resilience → testResilience.py

### Week 3 (Low Priority)
7. Phase 2: Archive candidates
8. Phase 3: Minor consolidations

---

## Merge Checklist (Per Consolidation)

For each consolidation:

- [ ] Create new consolidated file
- [ ] Copy all test classes from source files
- [ ] Add section comments separating original source
- [ ] Update imports (ensure all imports from original files)
- [ ] Run tests: `pytest tests/newFile.py -v` → All pass
- [ ] Check coverage: `pytest tests/newFile.py --cov` → ≥85%
- [ ] Update conftest.py fixtures if needed
- [ ] Delete original source files
- [ ] Commit: `chore(tests): consolidate X tests into testY.py`
- [ ] Push to branch

---

## Risk Mitigation

### Before merging files:
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] Check coverage: `pytest tests/ --cov=app`
- [ ] Search for file imports: `grep -r "import.*testOldFile" tests/`
- [ ] Verify no tests reference deleted files

### Rollback plan:
- Keep merged files in separate branch until verified
- Tag git commit before deletions
- If issues arise, revert with: `git revert <commit-hash>`

---

## Estimated Results

| Metric | Before | After | Savings |
|--------|--------|-------|---------|
| Test files | 68 | ~43 | -25 files |
| Test file size | 1.3M | ~0.7M | -600K (46%) |
| Test functions | ~1200 | ~1200 | Same (no loss) |
| Coverage | ≥85% | ≥85% | Same (maintained) |

---

## Alternative: Just Delete?

**Not recommended** because:
- Tests still provide value (not duplicative)
- Consolidation preserves all test coverage
- Improves maintainability (tests grouped by domain)
- Easier to navigate with fewer files

---

## Questions to Answer Before Starting

1. Should we keep `testFixturePatterns.py` or move to conftest.py?
2. Is property-based testing (testPropertyBased.py) actively used?
3. Are there specific files you want to keep separate?
4. Should archived tests stay for reference or be fully deleted?
