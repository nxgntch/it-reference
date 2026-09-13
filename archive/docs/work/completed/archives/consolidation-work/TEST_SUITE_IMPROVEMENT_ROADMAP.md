# Test Suite Improvement Roadmap

**Current State**: 14 test files, 91 tests (mostly stubs)  
**Lines of test code**: 438 total (~31 lines per file)  
**Coverage**: 54% of skills have tests (14/26)  

---

## Current Test Audit

### Test Breakdown

- **Unit tests**: 78 (85%)
- **Integration tests**: 10 (11%)
- **Async tests**: 3 (3%)
- **Performance tests**: 0 (0%)
- **Property-based tests**: 0 (0%)

### Test File Status

| Skill | Lines | Tests | Status |
|-------|-------|-------|--------|
| costForecasting | 45 | 5 | Stub + error cases |
| costAwareLlmPipeline | 38 | 6 | Stub + edge cases |
| analyticsEngine | 55 | 7 | Stub + validation |
| intelligentOptimizer | 40 | 6 | Stub |
| geoRouterExtended | 57 | 7 | Stub + constraints |
| codeReview | 40 | 7 | Stub |
| decomposition | 50 | 7 | Stub |
| routing | 50 | 7 | Stub |
| metricsCollector | 45 | 8 | Stub |
| healthCheck | 42 | 8 | Stub |
| cacheManager | 60 | 8 | Stub + state |
| performanceTracing | 25 | 5 | Minimal |
| tenantRouter | 30 | 5 | Minimal |
| tenantAudit | 25 | 4 | Minimal |

---

## Improvement Areas (Priority Order)

### 1. **Flesh Out Existing Stubs** (HIGH IMPACT)

**Current**: Most tests are templates with `pass` or minimal assertions  
**Goal**: Add real test logic and assertions

**Action items per skill**:

```python
# BEFORE (current stub)
@pytest.mark.unit
def testReviewsCodeForQuality(skillInstance, sampleCode):
    review = skillInstance.reviewCode(sampleCode)
    assert review is not None

# AFTER (improved)
@pytest.mark.unit
def testReviewsCodeForQuality(skillInstance, sampleCode):
    review = skillInstance.reviewCode(sampleCode)
    
    assert review is not None
    assert "issues" in review or "score" in review
    assert isinstance(review.get("issues", []), list)
    
    # Verify format
    for issue in review.get("issues", []):
        assert "type" in issue
        assert "line" in issue or "severity" in issue
```

**Effort**: 2-3 hours (fill in test logic for 14 files)  
**Impact**: HIGH (actual assertions instead of `pass`)

---

### 2. **Add Property-Based Tests** (MEDIUM IMPACT)

**Current**: Only explicit test cases  
**Goal**: Use Hypothesis for property-based testing

**Example**:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.floats(min_value=0, max_value=10000)))
@pytest.mark.property
def testCostForecastAlwaysPositive(historical):
    if len(historical) >= 3:
        forecast = skillInstance.forecast(historical, periods=7)
        assert all(v >= 0 for v in forecast['predictions'])
```

**Benefit**: Catch edge cases and boundary conditions  
**Effort**: 1-2 hours  
**Impact**: MEDIUM (finds bugs in edge cases)

---

### 3. **Add Performance/Benchmark Tests** (MEDIUM IMPACT)

**Current**: No performance baselines  
**Goal**: Use pytest-benchmark for latency tracking

**Example**:

```python
@pytest.mark.perf
def testCostForecastingPerformance(benchmark, skillInstance):
    historical = list(range(1000))  # Large dataset
    
    result = benchmark(skillInstance.forecast, historical, periods=7)
    
    # Assert performance
    assert result is not None
    # benchmark automatically reports timing
```

**Benefits**:
- Detect performance regressions
- Track improvements over time
- Establish baselines

**Effort**: 1-2 hours  
**Impact**: MEDIUM (prevents performance regressions)

---

### 4. **Add Integration Test Chains** (MEDIUM IMPACT)

**Current**: Tests are isolated  
**Goal**: Test real workflow chains

**Example**:

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def testCostForecastingIntegration(
    costForecasting, costAwareLlmPipeline
):
    # Real workflow: forecast → cost-aware selection
    historical = [100, 105, 110, 115]
    
    forecast = await costForecasting.forecast(historical)
    selection = await costAwareLlmPipeline.selectModel(
        {"budget": forecast["avgDailyCost"] * 1.1}
    )
    
    assert selection['cost'] <= forecast['avgDailyCost'] * 1.1
```

**Benefit**: Test real scenarios, not isolated functions  
**Effort**: 2-3 hours  
**Impact**: MEDIUM-HIGH (catches integration bugs)

---

### 5. **Add Test Data Factories** (LOW-MEDIUM IMPACT)

**Current**: Test data hardcoded in fixtures  
**Goal**: Use factories for realistic test data generation

**Example**:

```python
# conftest.py
class MetricFactory:
    @staticmethod
    def create_metric(timestamp=None, latency=None, throughput=None):
        return {
            "timestamp": timestamp or "2026-08-30T00:00:00Z",
            "latency": latency or random.randint(50, 500),
            "throughput": throughput or random.randint(100, 10000)
        }

# test_analyticsEngine.py
@pytest.mark.unit
def testAggregatesVariableMetrics(skillInstance):
    metrics = [
        MetricFactory.create_metric(latency=100),
        MetricFactory.create_metric(latency=200),
        MetricFactory.create_metric(latency=150),
    ]
    
    result = skillInstance.aggregate(metrics)
    assert result['avgLatency'] == 150
```

**Benefit**: Easier to create realistic test data  
**Effort**: 1-2 hours  
**Impact**: LOW-MEDIUM (improves test maintainability)

---

### 6. **Add Error Path Testing** (MEDIUM IMPACT)

**Current**: Some error cases, but incomplete  
**Goal**: Comprehensive error coverage

**Action items**:

```python
# Test all error conditions for each skill
@pytest.mark.unit
def testHandlesAllErrorTypes(skillInstance):
    error_cases = [
        (None, "None input"),
        ({}, "Empty dict"),
        ([], "Empty list"),
        ("", "Empty string"),
        ({"bad": "schema"}, "Invalid schema"),
    ]
    
    for invalid_input, description in error_cases:
        with pytest.raises((ValueError, TypeError, KeyError)):
            skillInstance.someMethod(invalid_input)
```

**Benefit**: Robust error handling validation  
**Effort**: 2-3 hours  
**Impact**: HIGH (prevents silent failures)

---

### 7. **Add Concurrency Tests** (LOW IMPACT)

**Current**: No concurrent execution tests  
**Goal**: Test thread-safety and concurrent behavior

**Example**:

```python
@pytest.mark.integration
@pytest.mark.asyncio
async def testConcurrentCalls(skillInstance):
    results = await asyncio.gather(
        skillInstance.someMethod(data1),
        skillInstance.someMethod(data2),
        skillInstance.someMethod(data3),
    )
    
    assert len(results) == 3
    assert all(r is not None for r in results)
```

**Benefit**: Detect race conditions  
**Effort**: 1-2 hours  
**Impact**: LOW (only needed for async skills)

---

## Proposed Improvement Phases

### Phase A: Quick Wins (3-4 hours)

1. **Flesh out stubs** — Add real assertions (2-3 hours)
2. **Add error path testing** — Comprehensive error cases (1-2 hours)

**ROI**: HIGH (immediate test quality improvement)

### Phase B: Advanced Testing (3-4 hours)

1. **Add property-based tests** — Use Hypothesis (1-2 hours)
2. **Add performance tests** — Use pytest-benchmark (1-2 hours)

**ROI**: MEDIUM-HIGH (prevent regressions, find edge cases)

### Phase C: Integration (2-3 hours)

1. **Add workflow chains** — Real integration tests (2-3 hours)
2. **Add test factories** — Realistic data generation (1-2 hours)

**ROI**: MEDIUM (better test coverage)

---

## Tools & Dependencies to Add

```toml
# pyproject.toml additions
pytest-benchmark>=4.0.0  # Performance testing
hypothesis>=6.80.0      # Property-based testing
pytest-asyncio>=0.21.1  # Already have
factory-boy>=3.2.0      # Test data factories (optional)
pytest-cov>=4.1.0       # Coverage reporting (already have)
pytest-xdist>=3.0.0     # Parallel test execution (optional)
```

---

## Coverage Goals

### Current

```
Skills with tests: 14/26 (54%)
Lines per test file: ~31 (mostly stubs)
Test assertions per file: ~6-7
```

### Target (After Phase A)

```
Skills with tests: 14/26 (54%)
Lines per test file: ~60-80 (with real logic)
Test assertions per file: ~15-20
Coverage: 50% → 70%
```

### Target (After Phase B+C)

```
Skills with tests: 14/26 (54%)
Lines per test file: ~100-150 (comprehensive)
Test assertions per file: ~25-35
Test types: unit + integration + perf + property
Coverage: 70% → 85%+
```

---

## Estimation

| Phase | Effort | Impact | ROI |
|-------|--------|--------|-----|
| **A: Quick wins** | 3-4h | HIGH | **10/10** |
| **B: Advanced** | 3-4h | MEDIUM-HIGH | **8/10** |
| **C: Integration** | 2-3h | MEDIUM | **7/10** |
| **TOTAL** | **8-11h** | **COMPREHENSIVE** | **8/10** |

---

## Quick Win: Sample Improved Test

**Before** (current stub):
```python
@pytest.mark.unit
def testForecasts(skill):
    result = skill.forecast([1, 2, 3])
    assert result is not None
```

**After** (Phase A):
```python
@pytest.mark.unit
def testForecastsBasicSequence(skill):
    historical = [100, 105, 110, 115, 120]
    forecast = skill.forecast(historical, periods=7)
    
    # Structure assertions
    assert forecast is not None
    assert "predictions" in forecast
    assert len(forecast["predictions"]) == 7
    
    # Value assertions
    assert all(v > 0 for v in forecast["predictions"])
    assert forecast["predictions"][0] > 120  # Upward trend
    
    # Statistical assertions
    avg = sum(forecast["predictions"]) / len(forecast["predictions"])
    assert avg > 125  # Reasonable forecast

@pytest.mark.unit
def testHandlesEmptyInput(skill):
    with pytest.raises(ValueError):
        skill.forecast([])

@pytest.mark.unit
def testHandlesInsufficientData(skill):
    with pytest.raises(ValueError):
        skill.forecast([1])  # Need at least 3 points
```

**Impact**: 3x more assertions, comprehensive error testing

---

## Recommendation

**Start with Phase A (Quick Wins)** — 3-4 hours work, HIGH impact.

- Flesh out existing stubs with real assertions
- Add comprehensive error path testing
- Result: Tests go from "mostly pass" to "actually validating"

Then decide on Phase B+C based on priorities.

---

## Files to Update

All 14 test files in:
```
skills/*/tests/test_*.py
```

Plus:
- `pytest.ini` — Add new markers for perf, property
- `pyproject.toml` — Add new test dependencies
- `.github/workflows/tests.yml` — Add benchmark/property test runs

---

**Recommendation**: Allocate 1-2 days for Phase A quick wins. High ROI, immediate impact on test quality.
