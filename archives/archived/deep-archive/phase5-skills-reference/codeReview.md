# Codereview Skill (IMPLEMENTED)

## Description

Security-focused code review with OWASP Top 10 detection and quality metrics.

## Inputs

```python
code: str, language: str, checkTypes: List[str]
```

## Outputs

```python
issues: List[Issue], score: float, canMerge: bool
```

## Configuration

- **ID**: codeReview
- **Name**: Codereview
- **Phase**: Phase 4 release

## Status

[PENDING] Interface defined. Ready for implementation.

## Usage
### Example 1: Review Code Quality

```python
from skills.codeReview.skill import CodeReview

skill = CodeReview()

code = '''
def process(data):
    return data * 2
'''

review = skill.reviewCode(code)
print(f"Issues: {review['issues']}")
print(f"Score: {review.get('score', 'N/A')}")
```

### Example 2: Security Review

```python
review = skill.reviewCode(code, securityCheck=True)
# Flags security vulnerabilities
```

## API

### Class: CodeReview

```python
class CodeReview:
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
from codeReview.skill import CodeReview

skill = CodeReview()
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

skill = CodeReview(config=config)
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

| Error | Cause | Recovery |
|-------|-------|----------|
| `ValueError` | Code syntax invalid | Provide syntactically valid code |
| `TimeoutError` | Code review timeout | Review simpler code or increase timeout |

## Related Skills

- **Upstream**: [To be documented]
- **Downstream**: [To be documented]
- **Alternative**: None
