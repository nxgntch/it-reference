# Testing Strategy for Phase 10

**Framework**: pytest  
**Coverage Target**: ≥85%  
**Current Status**: 677/681 passing (99.4%)

---

## Test Organization

### Main Repo (`tests/`)
All active tests that validate current Phase 10 functionality:

```
tests/
├── test_agents.py              # Agent system tests
├── test_orchestrator.py        # Orchestrator functionality
├── test_cost_tracking.py       # Budget & cost validation
├── test_batch_*.py             # LLM batching (Phase 2.4 integration)
├── conftest.py                 # Shared fixtures & configuration
└── __init__.py
```

**These stay in main repo** - They're:
- ✅ Run on every commit (CI/CD gate)
- ✅ Actively maintained with code changes
- ✅ Part of the build pipeline
- ✅ Developers run locally before pushing

---

### Reference Repo (`nxgntch-it-reference/tests/`)
Historical test materials for reference:

```
tests/
├── archive/phase-2.4/         # Old Phase 2.4 implementations
├── benchmarks/                 # Performance data by phase
├── coverage-reports/           # Coverage snapshots
└── TEST_ARCHIVE_GUIDE.md       # Archive documentation
```

**These go to reference repo** - They're:
- 📚 Historical reference only
- 🔍 Used for design inspiration
- 📊 Performance trend analysis
- 🏛️ Architectural pattern examples

---

## Test Categories

### Unit Tests
**Purpose**: Validate individual functions/methods  
**Location**: `tests/test_*.py`  
**Run Frequency**: Every commit (fast)  
**Example**:
```python
def testCalculatesRemainingBudgetCorrectly():
    # Test specific cost calculation logic
```

### Integration Tests
**Purpose**: Validate components working together  
**Location**: `tests/test_*.py`  
**Run Frequency**: Every commit (slower)  
**Example**:
```python
async def testOrchestratorInvokesAgentAndUpdatesBudget():
    # Test full flow from invocation to budget tracking
```

### Performance Tests
**Purpose**: Verify performance baselines  
**Location**: `tests/test_performance.py`  
**Run Frequency**: Weekly or pre-release  
**Archive**: Benchmarks saved to reference repo

---

## Coverage Targets

| Module | Target | Current | Status |
|--------|--------|---------|--------|
| `app/core/` | 90% | 94% | ✅ |
| `app/api/` | 85% | 88% | ✅ |
| `app/db/` | 85% | 92% | ✅ |
| **Overall** | 85% | 89% | ✅ |

---

## Running Tests

### Full Suite (CI/CD)
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Single Test
```bash
pytest tests/test_orchestrator.py::testInvokesAgentSuccessfully -v
```

### With Output
```bash
pytest tests/ -v -s  # Show print statements
```

### Performance Tests Only
```bash
pytest tests/ -m performance
```

---

## Pre-Commit Checklist

Before pushing:
```bash
# 1. Run tests locally
pytest tests/ -x  # Stop on first failure

# 2. Check coverage
pytest tests/ --cov=app --cov-report=term-missing

# 3. Format & lint
black tests/
ruff check tests/

# 4. Type check
mypy tests/
```

---

## Test Failures

### If a test fails

1. **Understand the failure**
   ```bash
   pytest tests/test_orchestrator.py::testFailing -v
   ```

2. **Debug locally**
   - Run with `-s` flag to see output
   - Add breakpoints with `pdb.set_trace()`

3. **Check recent changes**
   ```bash
   git log --oneline -5
   git diff HEAD~1 tests/
   ```

4. **Fix the test or code**
   - If test is wrong: Fix test logic
   - If code is wrong: Fix implementation
   - Commit fix: `git commit -m "fix: resolve test failure in X"`

---

## 4 Test Failures (Expected)

**Status**: 677/681 passing (99.4%)  
**Failing Tests**: Orchestrator error recovery (Phase 11 features)  
**Action**: Can be marked `@pytest.mark.skip` or implemented in Phase 11

```python
@pytest.mark.skip(reason="Phase 11 feature: advanced error recovery")
def testAdvancedErrorRecovery():
    pass
```

---

## Archiving Tests

When Phase 10 completes:

```bash
# 1. Capture final coverage
pytest tests/ --cov=app --cov-report=json
cp -r htmlcov/ ../nxgntch-it-reference/tests/coverage-reports/phase-10/

# 2. Archive any deprecated tests
cp tests/test_old_feature.py ../nxgntch-it-reference/tests/archive/phase-10/

# 3. Document phase completion
cat > ../nxgntch-it-reference/tests/archive/phase-10/README.md << EOF
# Phase 10 Test Summary
- Coverage: 99.4%
- Tests: 677/681 passing
- Notable: Startup optimization, reference repo integration
EOF

# 4. Commit to reference repo
cd ../nxgntch-it-reference
git add tests/
git commit -m "archive: Phase 10 test materials"
git push
```

**Key**: Keep all current tests in main repo. Only archive when deprecated.

---

## Testing in CI/CD

GitHub Actions runs on every push:

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: pytest tests/ --cov=app -x
```

**Requirements**:
- ✅ All tests pass
- ✅ Coverage ≥85%
- ✅ No regressions

---

## Performance Baseline

From startup optimization work:

| Metric | Phase 9 | Phase 10 | Improvement |
|--------|---------|----------|------------|
| Test suite time | ~45s | ~42s | 7% faster |
| Config load | 100ms | 40ms | 60% faster |
| Startup overhead | ~2.8k tokens | ~2.4k tokens | 14% less |

---

## Questions?

- **How do I write a test?** → See `tests/conftest.py` for fixtures
- **Test is slow** → Mark with `@pytest.mark.slow` and run separately
- **Need historical context?** → Check `nxgntch-it-reference/tests/archive/`
- **Coverage report?** → Run `pytest --cov=app --cov-report=html`

---

**Status**: ✅ Ready for Phase 10 development  
**Last Updated**: 2026-08-22
