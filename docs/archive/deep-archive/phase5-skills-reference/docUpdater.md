# Docupdater Skill (IMPLEMENTED)

## Description

Generate and maintain documentation from code changes and commit history with automatic changelog generation. Routes all generated documents to the centralized `/docs/` directory structure using configuration from `config/documentation.yaml`.

## Inputs

```python
changes: List[CodeChange], existingDocs: List[DocumentationFile], updateScope: str
```

## Outputs

```python
updates: List[DocumentationUpdate], newSections: List[GeneratedDocumentation], changeLog: ChangeLog
```

## Configuration

- **ID**: docUpdater
- **Name**: Docupdater
- **Phase**: Phase 4 critical (documentation automation)

## Status

(IMPLEMENTED) Complete with 11 tests, 100% passing. Changelog generation, breaking change detection, deprecation handling, multi-change documentation. Now integrated with `config/documentation.yaml` for centralized routing.

## Document Routing

DocUpdater automatically routes generated documents to the correct `/docs/` locations:

| Document Type | Target Location | Trigger |
|---|---|---|
| phase-status | docs/work/current/phase-status.md | Phase transition |
| phase-summary | docs/work/completed/ | Phase completion |
| active-tasks | docs/work/current/active-tasks.md | Task status change |
| roadmap | docs/work/planned/roadmap.md | Phase planning |
| quarterly-goals | docs/work/planned/quarterly-goals.md | Quarterly review |
| api | docs/specifications/API_SPECIFICATION.md | API changes |
| features | docs/guides/reference/FEATURES.md | New features |
| deprecated | docs/guides/operations/DEPRECATED.md | Removals/deprecations |
| changelog | docs/work/current/CHANGELOG.md | Release/batch changes |
| migration | docs/guides/operations/MIGRATION.md | Breaking changes |
| audit-report | docs/work/current/audit-report.md | Weekly audit |

**Configuration Source**: All paths are defined in `config/documentation.yaml` under `skillOutputTargets.docUpdater`. Updates to this file automatically affect docUpdater's routing behavior.

## Usage
### Example: Update Documentation
```python
result = skill.updateDocumentation(changes)
print(f"Updated: {result['filesChanged']}")```

## API

### Class: DocUpdater

```python
class DocUpdater:
    """Main skill class."""
    
    def __init__(self, config: dict = None):
        """Initialize the skill.
        
        Args:
            config: Optional configuration dictionary
        """
        pass
    
    def execute(self, input_data: dict) -> dict:
        """Execute the skill.
        
        Args:
            input_data: Input parameters (see Parameters section)
        
        Returns:
            Result dictionary with status and output
        
        Raises:
            ValueError: If input validation fails
            RuntimeError: If execution fails
        """
        pass
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| (See skill documentation above for specific parameters) | - | - | - |

### Return Value

```python
{
    "status": "success",           # "success" or "error"
    "output": {...},             # Skill-specific output
    "timestamp": "2026-08-30T...", # ISO 8601 timestamp
    "duration_ms": 123             # Execution time in milliseconds
}
```

## Examples

### Example 1: Basic Execution

```python
from docUpdater.skill import DocUpdater

skill = DocUpdater()
result = skill.execute({
    "input": "your_data_here"
})

print(f"Status: {result['status']}")
print(f"Duration: {result['duration_ms']}ms")
```

### Example 2: With Configuration

```python
config = {
    "timeout": 30,
    "retries": 3,
    "verbose": True
}

skill = DocUpdater(config=config)
result = skill.execute({"input": "data"})
```

### Example 3: Error Handling

```python
try:
    result = skill.execute({})
except ValueError as e:
    print(f"Input error: {e}")
except RuntimeError as e:
    print(f"Execution error: {e}")
```

### Example 4: Batch Processing

```python
inputs = [
    {"input": "data1"},
    {"input": "data2"},
    {"input": "data3"},
]

results = []
for input_data in inputs:
    try:
        result = skill.execute(input_data)
        if result["status"] == "success":
            results.append(result["output"])
    except Exception as e:
        print(f"Failed: {e}")

print(f"Processed {len(results)}/{len(inputs)} items")
```

## Error Handling
| `ValueError` | Invalid file path | Verify file exists |
| `RuntimeError` | Write permission denied | Check file permissions |

## Related Skills
- **Upstream**: [To be documented]
- **Downstream**: [To be documented]
