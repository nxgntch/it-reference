# Phase 16: Parametrization

**Overview**: Applied parametrization pattern to integration/E2E tests. 160+ tests parametrized across 8 files. Reduced duplication through validation error patterns, cross-reference testing, boundary value testing, configuration variations, and error case variations. Foundation: Phase 15.2 unit test consolidation.

**Status**: 🚀 In Progress | **Target**: 160+ tests parametrized | **Duration**: ~1 week | **Date Started**: 2026-08-26

---

## Scope & Metrics

### Test Files (Batch Breakdown)

| Batch | File | Lines | Tests | Parametrization Target | Priority |
|-------|------|-------|-------|------------------------|----------|
| 1 | test_documentation_and_sync_pipeline.py | 2,413 | 82 | 60+ | HIGH |
| 1 | test_performance_optimization_and_batching.py | 2,723 | 87 | 65+ | HIGH |
| 2 | test_configuration_and_cost_management.py | 2,770 | 95 | 70+ | HIGH |
| 2 | test_metrics_performance_and_optimization.py | 2,227 | 78 | 60+ | MEDIUM |
| 3 | test_operations_and_monitoring.py | 1,475 | 52 | 40+ | MEDIUM |
| 3 | test_system_resilience_and_optimization.py | 1,843 | 65 | 50+ | MEDIUM |
| 4 | test_validation_and_property_testing.py | 1,446 | 51 | 40+ | MEDIUM |
| 4 | test_llm_processing_and_agent_routing.py | 1,374 | 48 | 35+ | LOW |

**Total Target**: 160+ tests parametrized across 8 files

### Parametrization Patterns to Apply

1. **Validation Errors** (Multiple constructor params)
   - Error with minimal fields → Error with file → Error with line → Error with suggestion
   - **Pattern**: @pytest.mark.parametrize("category,message,file,line,suggestion", [...])

2. **Cross-Reference Testing** (Multiple link types)
   - No links → Broken links → External links → Anchor links
   - **Pattern**: Parametrize with (linkType, content, expectedValid)

3. **Boundary Value Testing** (Min/max/edge cases)
   - Single item → Exact fit → Overflow → Multiple → Empty
   - **Pattern**: Parametrize task counts, batch sizes, resource limits

4. **Configuration Variations** (Different configs)
   - Budget configs (low/medium/high)
   - Model configs (haiku/sonnet/opus)
   - Agent configs (different roles/teams)
   - **Pattern**: Parametrize config parameters

5. **Error Case Variations** (Different failure modes)
   - Missing field → Invalid format → Out of range → Timeout
   - **Pattern**: Parametrize error conditions

---

## Examples: Before → After

### Example 1: ValidationError Tests

**BEFORE** (4 separate functions, ~50 LOC):
```python
@pytest.mark.unit
def testValidationErrorSimple():
    error = ValidationError("TestCategory", "Test message")
    assert error.category == "TestCategory"
    assert error.message == "Test message"
    assert error.file is None

@pytest.mark.unit
def testValidationErrorWithFile():
    error = ValidationError("TestCategory", "Test message", file="test.md")
    result = str(error)
    assert "test.md" in result

@pytest.mark.unit
def testValidationErrorWithLine():
    error = ValidationError("TestCategory", "Test message", file="test.md", line=42)
    result = str(error)
    assert "test.md:42" in result

@pytest.mark.unit
def testValidationErrorWithSuggestion():
    error = ValidationError("TestCategory", "Test message", suggestion="Do this")
    result = str(error)
    assert "Suggestion: Do this" in result
```

**AFTER** (1 parametrized function, ~20 LOC):
```python
@pytest.mark.unit
@pytest.mark.parametrize(
    "category,message,file,line,suggestion,checkHas",
    [
        ("TestCategory", "Test message", None, None, None, ["TestCategory", "Test message"]),
        ("TestCategory", "Test message", "test.md", None, None, ["test.md"]),
        ("TestCategory", "Test message", "test.md", 42, None, ["test.md:42"]),
        ("TestCategory", "Test message", None, None, "Do this", ["Suggestion: Do this"]),
    ],
    ids=["simple", "withFile", "withLine", "withSuggestion"],
)
def testValidationError(category, message, file, line, suggestion, checkHas):
    error = ValidationError(category, message, file=file, line=line, suggestion=suggestion)
    result = str(error)
    for check in checkHas:
        assert check in result
```

**Benefits**:
- ✅ 1 function instead of 4 (75% less code)
- ✅ Single test logic, multiple cases
- ✅ Easy to add new cases (one line)
- ✅ Clear test IDs for debugging

### Example 2: Cross-References Tests

**BEFORE** (4+ separate functions):
```python
def testValidateCrossReferencesNoLinks(pluginStructure):
    validator = DocumentationValidator(str(pluginStructure))
    valid, _errors = validator.validateCrossReferences()
    assert valid is True

def testValidateCrossReferencesBrokenLink(tmpDocDir):
    docsDir = tmpDocDir / "docs"
    docsDir.mkdir()
    docFile = docsDir / "test.md"
    docFile.write_text("[Link](nonexistent.md)")
    validator = DocumentationValidator(str(tmpDocDir))
    valid, errors = validator.validateCrossReferences()
    assert valid is False
    assert any("BrokenLink" in e.category for e in errors)

def testValidateCrossReferencesExternalLinks(tmpDocDir):
    # ...similar pattern
    docFile.write_text("[External](https://example.com)")
    assert valid is True

def testValidateCrossReferencesAnchorLinks(tmpDocDir):
    # ...similar pattern
    docFile.write_text("[Section](#section)")
    assert valid is True
```

**AFTER** (1 parametrized function with fixtures):
```python
@pytest.mark.parametrize(
    "linkContent,expectedValid,shouldHaveErrors",
    [
        ("", True, False),  # No links
        ("[Link](nonexistent.md)", False, True),  # Broken link
        ("[External](https://example.com)", True, False),  # External link
        ("[Section](#section)", True, False),  # Anchor link
    ],
    ids=["noLinks", "brokenLink", "externalLink", "anchorLink"],
)
def testValidateCrossReferences(tmpDocDir, linkContent, expectedValid, shouldHaveErrors):
    if linkContent:
        docsDir = tmpDocDir / "docs"
        docsDir.mkdir()
        docFile = docsDir / "test.md"
        docFile.write_text(linkContent)
    
    validator = DocumentationValidator(str(tmpDocDir))
    valid, errors = validator.validateCrossReferences()
    
    assert valid is expectedValid
    if shouldHaveErrors:
        assert any("BrokenLink" in e.category for e in errors)
    else:
        assert len(errors) == 0
```

**Benefits**:
- ✅ 4 functions → 1 parametrized function
- ✅ Shared setup, varied test data
- ✅ Easier to add new link types

---

## Execution Plan

### Phase 16.5.1: Audit & Baseline (Day 1, 2 hours)
- [x] Identify test files (8 files, 186 tests total)
- [x] Analyze patterns (validation, cross-references, boundary values, configs, errors)
- [x] Create examples (before/after)
- [x] Document approach (this file)

### Phase 16.5.2: Batch 1 (Day 1-2, 8 hours)
- **Files**: test_documentation_and_sync_pipeline.py, test_performance_optimization_and_batching.py
- **Focus**: Validation errors, cross-references, boundary value tests
- **Target**: 120+ tests → 60+ parametrized functions
- **Expected LOC Reduction**: 1,500+ → 1,000 (33% reduction)

### Phase 16.5.3: Batch 2 (Day 2-3, 8 hours)
- **Files**: test_configuration_and_cost_management.py, test_metrics_performance_and_optimization.py
- **Focus**: Configuration variations, cost/performance parametrization
- **Target**: 173+ tests → 85+ parametrized functions
- **Expected LOC Reduction**: 1,200+ → 800 (33% reduction)

### Phase 16.5.4: Batch 3 (Day 3-4, 8 hours)
- **Files**: test_operations_and_monitoring.py, test_system_resilience_and_optimization.py
- **Focus**: Error case variations, monitoring scenarios
- **Target**: 117+ tests → 60+ parametrized functions
- **Expected LOC Reduction**: 900+ → 600 (33% reduction)

### Phase 16.5.5: Batch 4 (Day 4-5, 6 hours)
- **Files**: test_validation_and_property_testing.py, test_llm_processing_and_agent_routing.py
- **Focus**: Validation rules, routing scenarios
- **Target**: 99+ tests → 50+ parametrized functions
- **Expected LOC Reduction**: 800+ → 550 (31% reduction)

### Phase 16.5.6: Verification & Commit (Day 5-6, 4 hours)
- Run full test suite
- Verify coverage maintained (≥85%)
- Check all tests passing
- Commit with "phase 16.5:" prefix

---

## Success Criteria

- ✅ 160+ tests parametrized
- ✅ All 402+ tests passing (100%)
- ✅ Coverage maintained (≥85%)
- ✅ No regression (test count same or higher)
- ✅ LOC reduction: 20-30% in parametrized sections
- ✅ Documentation updated
- ✅ Clean git history (5-8 focused commits)

---

## Status Tracking

### Batch 1: test_documentation_and_sync_pipeline.py
- Status: ⏳ In Progress
- Tests parametrized: 0/82
- Target: 60+
- Start date: 2026-08-26

### Batch 1: test_performance_optimization_and_batching.py
- Status: ⏳ In Progress
- Tests parametrized: 0/87
- Target: 65+
- Start date: 2026-08-26

### Batch 2: test_configuration_and_cost_management.py
- Status: ⏹️ Not Started
- Tests parametrized: 0/95
- Target: 70+

### Batch 2: test_metrics_performance_and_optimization.py
- Status: ⏹️ Not Started
- Tests parametrized: 0/78
- Target: 60+

### Batch 3: test_operations_and_monitoring.py
- Status: ⏹️ Not Started
- Tests parametrized: 0/52
- Target: 40+

### Batch 3: test_system_resilience_and_optimization.py
- Status: ⏹️ Not Started
- Tests parametrized: 0/65
- Target: 50+

### Batch 4: test_validation_and_property_testing.py
- Status: ⏹️ Not Started
- Tests parametrized: 0/51
- Target: 40+

### Batch 4: test_llm_processing_and_agent_routing.py
- Status: ⏹️ Not Started
- Tests parametrized: 0/48
- Target: 35+

---

## Reference

- **Parametrization Template**: [`docs/guides/development/PARAMETRIZATION_TEMPLATE.md`](PARAMETRIZATION_TEMPLATE.md)
- **Parametrization Examples**: [`docs/guides/development/PARAMETRIZATION_EXAMPLES.md`](PARAMETRIZATION_EXAMPLES.md)
- **Phase 15.2 Ref**: Applied parametrization to unit tests (100% adoption)
- **Testing Standards**: [`.claude/rules/testing.md`](./../rules/testing.md)

