# Phase 3a-2.1: ExtractAgentMetadata Consolidation

**Date**: 2026-08-26  
**Group**: 9 (HIGH Priority)  
**Tests**: 12 → 1 parametrized  
**Estimated Reduction**: 60-70% lines  
**Status**: IN PROGRESS

---

## Consolidation Plan

### Original Tests (12 functions)

1. `testExtractAgentMetadataValid` - Valid metadata extraction
2. `testExtractAgentMetadataExtractsContentDescription` - ContentDescription field
3. `testExtractAgentMetadataNoFrontmatter` - Missing frontmatter
4. `testExtractAgentMetadataIncompleteFrontmatter` - Incomplete frontmatter
5. `testExtractAgentMetadataInvalidYAML` - Invalid YAML syntax
6. `testExtractAgentMetadataFileNotFound` - Nonexistent file
7. `testExtractAgentMetadataPreservesExtraFields` - Extra fields preservation
8. `testExtractAgentMetadataEmptyFrontmatter` - Empty frontmatter
9. `testExtractAgentMetadataMinimalContent` - Minimal valid content
10. `testExtractAgentMetadataSkipsCommentLines` - Comment line handling
11. `testExtractAgentMetadataHandlesSpecialCharacters` - Special character handling
12. `testExtractAgentMetadataWithBinaryFile` - Binary file handling

### Consolidated Test (1 function)

```python
@pytest.mark.parametrize("scenario,fileContent,expectMetadata,checkField,checkValue,expectNone,expectException", [
    # Scenario 1: Valid metadata extraction
    (
        "valid",
        "---\nname: testAgent\nmodel: claude-sonnet-5\ndescription: A test agent\neffort: high\n---\nContent",
        True, "name", "testAgent", False, False
    ),
    # Scenario 2: ContentDescription extraction
    (
        "description",
        "---\nname: test\n---\ntest agent content",
        True, "contentDescription", "test agent", False, False
    ),
    # Scenario 3: No frontmatter
    (
        "noFrontmatter",
        "No frontmatter here\nname: test",
        False, None, None, True, False
    ),
    # Scenario 4: Incomplete frontmatter
    (
        "incompleteFrontmatter",
        "---\nname: test\nNo closing delimiter",
        False, None, None, True, False
    ),
    # Scenario 5: Invalid YAML
    (
        "invalidYAML",
        "---\nname: test\ninvalid: [unclosed\n---\nContent",
        False, None, None, True, False
    ),
    # Scenario 6: Empty frontmatter
    (
        "emptyFrontmatter",
        "---\n---\nContent",
        False, None, None, True, False
    ),
    # Scenario 7: Minimal valid content
    (
        "minimal",
        "---\nname: minimal\n---\nSingle line",
        True, "name", "minimal", False, False
    ),
    # Scenario 8: Extra fields preservation
    (
        "extraFields",
        "---\nname: test\ncustomField: value\ntemperature: 0.7\n---\nContent",
        True, "customField", "value", False, False
    ),
    # Scenario 9: Comment handling
    (
        "comments",
        "---\nname: test\n---\n# Comment\nReal content",
        True, "contentDescription", "Real content", False, False
    ),
    # Scenario 10: Special characters
    (
        "special",
        "---\nname: special\ndescription: Test @#$%\n---\nContent",
        True, "description", "@#$%", False, False
    ),
    # Scenario 11: Binary file (no setup needed - handled separately)
    # Scenario 12: File not found (no file setup needed - handled separately)
])
def testExtractAgentMetadata(tmpDocsDir, validAgentFile, scenario, fileContent, expectMetadata, checkField, checkValue, expectNone, expectException):
```

### Implementation Strategy

1. **Create helper functions** to reduce parametrization complexity:
   - `_createAgentFile(tmpDir, content)` - Create file with content
   - `_checkMetadata(metadata, checkField, checkValue)` - Verify field values

2. **Handle special cases** (file not found, binary file):
   - Use `request.getfixturevalue()` or separate test logic
   - OR create test data with marker-based logic

3. **Verify all scenarios**:
   - Valid extraction (name, model, description, effort, contentDescription, extra fields)
   - Invalid inputs (no frontmatter, incomplete, invalid YAML, empty)
   - Edge cases (special chars, comments, minimal content)
   - Error cases (file not found, binary file)

---

## Implementation Status

- [ ] Read full test file section
- [ ] Extract parametrization data
- [ ] Create consolidated test function
- [ ] Handle edge cases (file not found, binary)
- [ ] Verify all 12 test cases pass
- [ ] Measure metrics
- [ ] Commit

---

## Metrics Tracking

**Before Consolidation:**
- Lines of code: ~160 lines
- Number of functions: 12
- Code duplication: High (setup patterns repeated)

**Expected After:**
- Lines of code: ~50-60 lines
- Number of functions: 1
- Code reduction: 60-70%

---

## Next Steps

1. Implement consolidated test
2. Verify all test cases pass
3. Compare line counts
4. Commit as `test(phase3a-1): consolidate 12-param testExtractAgentMetadata`
5. Move to Phase 3a-2.2 (ExtractSkillMetadata consolidation)

