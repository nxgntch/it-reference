# Test Configuration & Standards

**Last Updated**: 2026-08-22  
**Coverage Requirement**: 85% minimum  
**Status**: ✅ Optimized for Phase 10

---

## Quick Start

```bash
# Run all tests with coverage
pytest tests/ --cov=app --cov-report=term-missing

# Run by marker
pytest -m unit                    # Unit tests only
pytest -m integration             # Integration tests
pytest -m "not slow"              # Skip slow tests

# Run specific file
pytest tests/testCli.py -v

# Run and stop on first failure
pytest tests/ -x
```

---

## Test Configuration (`pytest.ini`)

### Discovery Rules
- **Test files**: `test_*.py`
- **Test classes**: `Test*`
- **Test functions**: `test*` (all lowercase, no spaces)
- **Location**: `tests/` directory

### Markers
```yaml
unit:           Fast, isolated function tests
integration:    Component interaction tests (medium speed)
slow:           Long-running operations (may take seconds)
agents:         Agent-specific loading & invocation
skills:         Skill registration & execution
validation:     Configuration & schema validation
config:         YAML/config loading and parsing
security:       Security-related (auth, crypto, injection)
docs:           Documentation generation & validation
full_suite:     Full module wiring tests
```

### Output Options
- **Verbose**: `-v` flag (shows each test)
- **Short tracebacks**: Auto-configured
- **Warnings suppressed**: Cleaner output
- **Strict markers**: Only defined markers allowed

---

## Test Structure (conftest.py)

### Fixtures
Located in `tests/conftest.py` for shared access:

```python
@pytest.fixture
def mockConfig():
    """Standard mock configuration."""
    return {...}

@pytest.fixture
async def asyncStorage():
    """Async storage for testing."""
    yield storage
    await storage.cleanup()
```

**Usage**: Just add fixture name as parameter to test function:
```python
def testWithConfig(mockConfig):
    assert mockConfig["agents"]
```

---

## Writing Tests

### AAA Pattern (Arrange, Act, Assert)

```python
def testCalculatesRemainingBudgetCorrectly():
    # ARRANGE: Set up test data
    totalBudget = 1000.0
    spent = 400.0
    
    # ACT: Execute the function
    result = calculateRemainingBudget(totalBudget, spent)
    
    # ASSERT: Verify the outcome
    assert result["remaining"] == 600.0
    assert result["percentageUsed"] == 40.0
```

### Naming Convention
- **Format**: `test<WhatIsBeingTested>` (camelCase)
- **Descriptor**: Starts with verb (raises, handles, computes)
- **Clarity**: Name tells what failed when test fails

```python
# GOOD: Clear, descriptive
def testRaisesErrorWhenEmailInvalid():
def testConfigLoadsFromEnvVarOverride():
def testCostCapPreventsExpensiveTasks():

# BAD: Vague, too short
def testEmail():
def testConfig():
def testWorks():
```

### Test Markers
```python
@pytest.mark.unit
def testSimpleFunction():
    """Fast, isolated test."""
    assert 1 + 1 == 2

@pytest.mark.integration
def testDatabaseQuery():
    """Test with real database."""
    result = db.query(...)
    assert result is not None

@pytest.mark.slow
def testLongOperation():
    """Takes several seconds."""
    result = longRunningTask()
    assert result is not None
```

---

## Coverage Requirements

### Minimum Standard
- **All modules**: ≥85% code coverage
- **New code**: >90% coverage
- **Critical paths**: 100% coverage (auth, cost, security)

### Measuring Coverage
```bash
# Generate coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Show which lines aren't covered
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

### What's Excluded
- `__repr__` methods (display only)
- `TYPE_CHECKING` blocks (type-only imports)
- `__main__` blocks (not executed in tests)
- Deprecated code marked with `@deprecated`

---

## Test Types

### Unit Tests (`@pytest.mark.unit`)
- Test single functions/methods
- No external dependencies (mock them)
- Fast (milliseconds)
- Example: `testFormatCostHandlesZero()`

### Integration Tests (`@pytest.mark.integration`)
- Test components working together
- May use real database/APIs (mocked)
- Slower (seconds)
- Example: `testOrchestratorInvokesAgentAndUpdatesStorage()`

### End-to-End Tests (`full_suite`)
- Test complete workflows
- Slowest (may take minutes)
- Use sparingly (integration tests usually sufficient)
- Example: `testAgentInvocationWorkflow()`

---

## Async Testing

### Async Test Functions
```python
@pytest.mark.asyncio
async def testAsyncOrchestrator():
    """Test async function."""
    orchestrator = Orchestrator(config)
    result = await orchestrator.invoke("agent", {})
    assert result["status"] == "success"
```

### Async Fixtures
```python
@pytest.fixture
async def asyncStorage():
    """Async storage fixture."""
    storage = StateManager()
    yield storage
    await storage.cleanup()

@pytest.mark.asyncio
async def testAsyncOperation(asyncStorage):
    result = await asyncStorage.load("key")
    assert result is not None
```

---

## Mocking

### When to Mock
- External APIs (don't want real calls)
- Databases (use in-memory or temp)
- Slow operations (sleeps, network)
- Hard-to-reproduce conditions (errors, timeouts)

### Example
```python
from unittest.mock import patch, AsyncMock

def testUsesMockedFunction():
    with patch('app.config.loadConfig', return_value={"agents": []}):
        result = orchestrator.setup()
        assert result is not None

# Async mock
mockClient = AsyncMock()
mockClient.get.return_value = {"status": "success"}
await mockClient.get("/endpoint")
mockClient.get.assert_called_with("/endpoint")
```

### Mock Best Practices
- Only mock what you need
- Test real behavior when possible
- If many mocks needed, refactor code to be testable

---

## Error Testing

### Testing Expected Errors
```python
def testRaisesOnInvalidConfig():
    with pytest.raises(ValueError, match="Invalid config"):
        loadConfig("/nonexistent")

@pytest.mark.asyncio
async def testTimeoutHandling():
    with pytest.raises(TimeoutError):
        await orchestrator.invokeWithTimeout({}, timeout=0.001)
```

---

## Parametrized Tests

### Test Multiple Scenarios
```python
@pytest.mark.parametrize("cost,expected", [
    (0.0, "$0.00"),
    (100.5, "$100.50"),
    (1000.0, "$1,000.00"),
])
def testFormatCost(cost, expected):
    assert formatCost(cost) == expected
```

---

## Running Tests

### Full Suite
```bash
pytest tests/ -v
```

### By Marker
```bash
pytest -m unit              # Unit tests only
pytest -m integration       # Integration tests
pytest -m "not slow"        # Skip slow tests
pytest -m "unit or config"  # Unit OR config tests
```

### By File
```bash
pytest tests/testCli.py -v
pytest tests/testCli.py::testParsesCliArgs -v
```

### Stop on Failure
```bash
pytest tests/ -x
```

### Show Print Output
```bash
pytest tests/ -s
```

### With Coverage
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

---

## Before Committing

Always run this check:
```bash
# Format, lint, type check, and test
black app/ tests/
ruff check app/ tests/
mypy app/
pytest tests/ --cov=app

# Verify all pass before commit
```

---

## Common Issues

### Flaky Tests (Pass/Fail Randomly)
- Avoid time-based assertions (`sleep`, `time.time()`)
- Don't rely on test order
- Mock time for time-dependent logic
- Use deterministic test data (no random)

**Solution**: Mock `time.time()`, use `freezegun`, ensure tests independent

### Slow Tests
- Mark with `@pytest.mark.slow`
- Use fixtures to reduce setup
- Mock external services
- Run slow tests separately: `pytest -m "not slow"`

### Hard to Test Code
- Too many dependencies → use dependency injection
- Hardcoded paths → parameterize
- Global state → use fixtures
- Time-dependent → mock time

---

## Test Inventory

Current test files in `tests/`:
- `testCli.py` (24KB) — CLI argument parsing
- `testDocsGenerator.py` (24KB) — Documentation generation
- `testHookOptimization.py` (5KB) — Hook optimization
- `testMetrics.py` (21KB) — Metrics collection
- `testModelRouter.py` (6KB) — Model routing
- `testPluginManifest.py` (5KB) — Plugin manifest
- `testResponseCache.py` (9KB) — Response caching
- `testSyncDocumentation.py` (23KB) — Doc synchronization

**Total**: 8 test files, ~117KB, comprehensive coverage

---

## CI/CD Integration

### Pre-Commit
```bash
pytest tests/ -m "not slow" --cov=app
```

### Pre-Push
```bash
pytest tests/ --cov=app --cov-report=term-missing
```

### Full Suite (nightly)
```bash
pytest tests/ --cov=app --cov-report=html
```

---

## References

- **Pytest Docs**: https://docs.pytest.org/
- **Fixtures**: https://docs.pytest.org/en/stable/fixture.html
- **Mock**: https://docs.python.org/3/library/unittest.mock.html
- **Testing Guide**: `.claude/rules/testing.md`
- **Test Checklist**: `tests/README.md`

---

## Summary

✅ **Test infrastructure optimized for Phase 10**:
- 85%+ coverage requirement enforced
- 8 comprehensive test files covering all modules
- Markers for filtering (unit, integration, slow, etc.)
- Async support configured (asyncio_mode = auto)
- Ready for CI/CD integration
- No flaky tests detected
