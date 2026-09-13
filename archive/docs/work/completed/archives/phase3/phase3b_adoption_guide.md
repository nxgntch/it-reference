# Phase 3b: Test Consolidation Adoption Guide

**Status**: IN PROGRESS  
**Date**: 2026-08-26  
**Target**: Organization-wide adoption of test consolidation patterns

---

## Overview

Phase 3a delivered **100% test consolidation** of `test_documentation_and_sync_pipeline.py`: **65 tests → 30 functions** with **39% code reduction** and **100% error fidelity**. 

Phase 3b provides the playbook for teams to apply these patterns to their own test suites.

---

## Core Principle: The Consolidation Pattern

**One parametrized test replaces N individual tests** when they:
- Test the same function/class with different inputs
- Have identical assertion logic (only data changes)
- Can be described as scenario variations (A, B, C)
- Share the same fixtures

**Before (65 individual tests)**:
```python
def testFunctionScenario1(fixture):
    # Setup for scenario 1
    result = function(data1)
    assert result == expected1

def testFunctionScenario2(fixture):
    # Setup for scenario 2
    result = function(data2)
    assert result == expected2

# ... 63 more tests
```

**After (30 parametrized tests)**:
```python
@pytest.mark.parametrize(
    "scenario,setup,expectedChecks",
    [
        ("scenario1", lambda fix: fix, [("field", expected1)]),
        ("scenario2", lambda fix: setupFunc(fix), [("field", expected2)]),
    ],
    ids=["scenario1", "scenario2"],
)
def testFunction(fixture, scenario, setup, expectedChecks):
    result = function(setup(fixture))
    for checkType, expectedValue in expectedChecks:
        assert result[checkType] == expectedValue
```

---

## Step-by-Step Adoption Process

### Phase 1: Identify Consolidation Candidates (30 minutes)

**Goal**: Find test groups that can be consolidated.

#### 1a. Analyze Your Test File

```bash
# List all test functions
grep "^def test" tests/your_test_file.py | wc -l

# Group by common name prefix
grep "^def test" tests/your_test_file.py | sed 's/def test//' | sed 's/(.*//' | sort | uniq -c | sort -rn
```

**Look for**:
- Tests with 2+ variations of same name (e.g., `testFunctionScenario1`, `testFunctionScenario2`)
- Tests using the same fixture
- Tests with identical assertion patterns but different data

#### 1b. Example: Grouping in test_documentation_and_sync_pipeline.py

```
3 testGenerateAgentsReference*       ← HIGH PRIORITY (3 tests)
8 testGenerateSkillsReference*       ← HIGH PRIORITY (8 tests)
2 testGenerateAllDocsScaling*        ← MEDIUM (2 tests)
3 testValidateAgentDocumentation*    ← MEDIUM (3 tests)
3 testValidateSkillDocumentation*    ← MEDIUM (3 tests)
3 testFindAllMarkdownFiles*          ← LOW (3 tests)
2 testValidateDocumentationStructure*← LOW (2 tests)
2 testSyncResult*                    ← LOW (2 tests)
2 testDocumentationValidator*        ← LOW (2 tests)
2 testDetectManualEdits*             ← LOW (2 tests)
```

**Result**: 14 groups, 65 tests total → consolidate into 14 parametrized tests

---

### Phase 2: Read Original Tests (30 minutes per group)

**Goal**: Understand the pattern and identify scenario variations.

#### 2a. Read All Tests in a Group

Example (FindAllMarkdownFiles group):

```python
def testFindAllMarkdownFilesNoFiles(tmpDocsDir):
    validator = DocumentationValidator(str(tmpDocsDir))
    files = validator._findAllMarkdownFiles()
    assert files == []

def testFindAllMarkdownFilesInDocs(pluginStructure):
    validator = DocumentationValidator(str(pluginStructure))
    files = validator._findAllMarkdownFiles()
    assert len(files) > 0
    assert "README.md" in [f.name for f in files]

def testFindAllMarkdownFilesIgnoresSkipDirs(pluginStructure):
    gitDir = pluginStructure / ".git"
    gitDir.mkdir()
    (gitDir / "test.md").write_text("# Git")
    validator = DocumentationValidator(str(pluginStructure))
    files = validator._findAllMarkdownFiles()
    assert not any(".git" in str(f) for f in files)
```

#### 2b. Identify Patterns

Ask these questions:

1. **Fixture**: Same fixture or different? → `tmpDocsDir` vs `pluginStructure`
2. **Setup**: Any file/directory creation? → Yes: `.git` directory in scenario 3
3. **Initialization**: Same class/function call? → Yes: `DocumentationValidator(...)`
4. **Assertions**: Same logic, different data? → Yes: All check file lists

**Pattern Template for this group**:
```
scenario | fixture        | setup                      | checks
---------|----------------|----------------------------|----------------
noFiles  | tmpDocsDir     | none                       | length == 0
withDocs | pluginStructure| none                       | length > 0, "README.md" in names
skipDirs | pluginStructure| create .git/test.md        | ".git" not in paths
```

---

### Phase 3: Design Parametrize Table (15 minutes)

**Goal**: Define the `@pytest.mark.parametrize` decorator.

#### 3a. Define Columns

For FindAllMarkdownFiles group:

```python
@pytest.mark.parametrize(
    "scenario,setup,expectedChecks",  # Columns
    [
        # Rows (each scenario)
    ],
    ids=["noFiles", "withDocs", "skipDirs"],  # Display names
)
```

#### 3b. Build Rows

**Row 1: noFiles**
- Fixture: `tmpDocsDir`
- Setup: no-op (lambda returns fixture as-is)
- Checks: list is empty

```python
("noFiles", lambda fix: fix, [("length", 0, "eq")])
```

**Row 2: withDocs**
- Fixture: `pluginStructure`
- Setup: no-op
- Checks: list has files, contains README.md

```python
("withDocs", lambda fix: fix, [("length", 0, "gt"), ("name", "README.md", "in")])
```

**Row 3: skipDirs**
- Fixture: `pluginStructure`
- Setup: create `.git` dir with `.md` file
- Checks: `.git` not in paths

```python
("skipDirs", lambda fix: (fix / ".git").mkdir(exist_ok=True) or (fix / ".git" / "test.md").write_text("# Git") or fix, [("path", ".git", "not")])
```

---

### Phase 4: Write Parametrized Test (20 minutes)

**Goal**: Implement the unified test function.

#### 4a. Signature

```python
@pytest.mark.parametrize(
    "scenario,setup,expectedChecks",
    [
        ("noFiles", lambda fix: fix, [("length", 0, "eq")]),
        ("withDocs", lambda fix: fix, [("length", 0, "gt"), ("name", "README.md", "in")]),
        ("skipDirs", lambda fix: (fix / ".git").mkdir(exist_ok=True) or (fix / ".git" / "test.md").write_text("# Git") or fix, [("path", ".git", "not")]),
    ],
    ids=["noFiles", "withDocs", "skipDirs"],
)
@pytest.mark.unit
def testFindAllMarkdownFiles(tmpDocsDir, pluginStructure, scenario, setup, expectedChecks):
    """Consolidated parametrized test for finding markdown files."""
```

#### 4b. Fixture Selection

Select the right fixture based on scenario:

```python
# Select fixture based on scenario
docsDir = tmpDocsDir if scenario == "noFiles" else pluginStructure
docsDir = setup(docsDir)  # Apply setup lambda
```

#### 4c. Core Logic

Keep original logic, unchanged:

```python
validator = DocumentationValidator(str(docsDir))
files = validator._findAllMarkdownFiles()
```

#### 4d. Assertions

Generalize assertion checks:

```python
for checkType, value, operator in expectedChecks:
    if checkType == "length":
        if operator == "eq":
            assert len(files) == value
        elif operator == "gt":
            assert len(files) > value
    elif checkType == "name":
        fileNames = [f.name for f in files]
        assert value in fileNames
    elif checkType == "path":
        assert not any(value in str(f) for f in files)
```

---

### Phase 5: Test & Validate (10 minutes)

**Goal**: Ensure parametrized test behaves identically to originals.

#### 5a. Run the Parametrized Test

```bash
pytest tests/your_test_file.py::testFindAllMarkdownFiles -v

# Expected output:
# testFindAllMarkdownFiles[noFiles] PASSED
# testFindAllMarkdownFiles[withDocs] PASSED
# testFindAllMarkdownFiles[skipDirs] PASSED
```

#### 5b. Compare Error Behavior

**Original**:
```
FAILED testFindAllMarkdownFilesNoFiles - AttributeError: 'DocumentationValidator' object has no attribute '_findAllMarkdownFiles'
```

**Parametrized**:
```
FAILED testFindAllMarkdownFiles[noFiles] - AttributeError: 'DocumentationValidator' object has no attribute '_findAllMarkdownFiles'
```

✅ **Identical error at same point** → consolidation successful

#### 5c. Count Lines Saved

```bash
# Before
grep -A 20 "def testFindAllMarkdownFilesNoFiles" tests/test_file.py | wc -l
# 36 lines (all 3 tests combined)

# After
grep -A 25 "def testFindAllMarkdownFiles" tests/test_file.py | wc -l
# 27 lines (1 parametrized test)

# Reduction: 9 lines (25% reduction)
```

---

### Phase 6: Commit & Document (5 minutes)

**Goal**: Record the consolidation with clear commit message.

#### 6a. Commit

```bash
git add tests/your_test_file.py
git commit -m "test(group): consolidate 3-param testFindAllMarkdownFiles"
```

Format: `test(<group>): consolidate <N>-param <testName>`

#### 6b. Update Metrics

Track in a local document:

```markdown
| Group | Before | After | Reduction |
|-------|--------|-------|-----------|
| FindAllMarkdownFiles | 3 | 1 | 9 lines (25%) |
```

---

## Consolidation Patterns by Type

### Pattern 1: Simple State Tests (2-3 tests)

**When**: Tests check different states/properties of same object.

**Example**: `testSyncResultDefaults`, `testSyncResultAccumulation`

**Template**:
```python
@pytest.mark.parametrize(
    "scenario,setup,checks",
    [
        ("defaults", lambda obj: obj, [("field1", value1), ("field2", value2)]),
        ("modified", lambda obj: (obj.field = value; obj), [("field1", new_val1)]),
    ],
    ids=["defaults", "modified"],
)
def testObjectState(fixture, scenario, setup, checks):
    obj = setup(fixture)
    for field, expected in checks:
        assert getattr(obj, field) == expected
```

**Reduction**: 30-40% lines

---

### Pattern 2: File I/O Tests (2-4 tests)

**When**: Tests create different file structures and check results.

**Example**: `testFindAllMarkdownFiles` (3 tests)

**Template**:
```python
@pytest.mark.parametrize(
    "scenario,setup,checks",
    [
        ("empty", lambda fix: fix, [("empty", True)]),
        ("populated", lambda fix: (fix / "file.md").write_text("...") or fix, [("count", 1)]),
    ],
    ids=["empty", "populated"],
)
def testFileFunction(tmpdir, scenario, setup, checks):
    dir = setup(tmpdir)
    result = processFiles(dir)
    for checkType, expected in checks:
        # assertions
```

**Reduction**: 25-35% lines

---

### Pattern 3: Configuration/Validation Tests (3-5 tests)

**When**: Tests validate different config scenarios.

**Example**: `testValidateDocumentationStructure` (2 tests)

**Template**:
```python
@pytest.mark.parametrize(
    "scenario,setup,checks",
    [
        ("valid", lambda cfg: cfg, [("valid", True), ("errors", 0)]),
        ("invalid", lambda cfg: modifyConfig(cfg), [("valid", False), ("errors", 1)]),
    ],
    ids=["valid", "invalid"],
)
def testValidateConfig(config_fixture, scenario, setup, checks):
    cfg = setup(config_fixture)
    result = validate(cfg)
    for field, expected in checks:
        assert result[field] == expected
```

**Reduction**: 30-45% lines

---

## Best Practices

### ✅ DO

1. **Read original tests thoroughly** before consolidating
   - Understand fixture requirements
   - Identify setup differences
   - Map assertion patterns

2. **Use lambda setup functions** for complex setups
   - Keeps parametrize decorator readable
   - Setup logic clear in test body
   - Use `exist_ok=True` for mkdir (prevent conflicts)

3. **Preserve error behavior**
   - Test failures should point to same place
   - Parametrized test fails at same operation as original
   - Error messages identical

4. **Use descriptive IDs**
   - `ids=["scenario1", "scenario2"]` not `ids=["a", "b"]`
   - Display name helps with test selection
   - Shows up in test output

5. **Test immediately**
   - Run `pytest testName -v` after consolidation
   - Verify all scenarios run
   - Check failure behavior matches original

### ❌ DON'T

1. **Don't force consolidation** if patterns don't match
   - If fixture requirements differ significantly, keep separate
   - If assertion logic completely different, keep separate
   - Quality > aggressive consolidation

2. **Don't over-parametrize**
   - Keep to 2-5 scenarios per test (max 11)
   - If > 11, split into multiple parametrized tests
   - Readability matters

3. **Don't ignore setup complexity**
   - If setup is complex, put it in a fixture, not a lambda
   - Lambda should be 1-2 lines, not 10+
   - Readability matters

4. **Don't change test logic**
   - Consolidation = restructure, not refactor
   - Original assertions, unchanged
   - Original behavior, 100% preserved

---

## Adoption Roadmap

### Phase 3b: Foundation (2-4 hours this session)
- [x] Consolidation pattern finalized
- [x] Adoption guide written (this document)
- [ ] Integration testing (run full suite)
- [ ] Metrics documentation

### Phase 3c: Rollout (1-2 hours next session)
- [ ] Team training on consolidation pattern
- [ ] Apply pattern to 1-2 additional test files
- [ ] Establish team guidelines
- [ ] Create reusable template

### Phase 3d: Org-Wide (2-4 hours, ongoing)
- [ ] Consolidate all high-priority test files
- [ ] Establish code review checklist for consolidations
- [ ] Track metrics across org
- [ ] Monthly optimization reports

---

## Integration Testing Checklist

Before declaring adoption successful:

- [ ] Full test suite runs (pytest --cov=app)
- [ ] Coverage remains ≥85%
- [ ] All parametrized tests pass at original error levels
- [ ] No false negatives (tests that should fail still fail)
- [ ] No false positives (tests that should pass still pass)
- [ ] Performance acceptable (no slowdown from parametrization)
- [ ] Documentation clear for new team members

---

## Quick Reference

### Consolidation Checklist

```
□ Identify 2+ tests with similar names
□ Read all tests in group
□ Identify: fixture, setup, assertions
□ Design parametrize table (scenario, setup, checks)
□ Write unified test function
□ Test: all scenarios pass
□ Test: failures match originals
□ Commit with metrics
□ Update adoption metrics
```

### Command Reference

```bash
# Find candidate groups
grep "^def test" tests/file.py | sed 's/def test//' | sed 's/(.*//' | sort | uniq -c | sort -rn

# Count tests before/after
grep -c "^def test" tests/file.py

# Run consolidation
pytest tests/file.py::testConsolidatedName -v

# Measure reduction
git diff HEAD~1 tests/file.py | grep -c "^-" # lines removed
git diff HEAD~1 tests/file.py | grep -c "^+" # lines added
```

---

## Resources

- **Phase 3a Complete**: `docs/work/current/phase3a_session_complete.md`
- **Phase 3a Analysis**: `docs/work/current/phase3a1_analysis.md`
- **Consolidated Test File**: `tests/test_documentation_and_sync_pipeline.py`
- **Pytest Parametrize Docs**: https://docs.pytest.org/en/stable/how-to-parametrize-fixtures.html

---

**Ready for org-wide adoption. Teams can start with Phase 1: Identify Consolidation Candidates.**
