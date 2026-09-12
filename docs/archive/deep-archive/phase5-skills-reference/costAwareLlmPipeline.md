# Cost Aware Llm Pipeline Skill

## Description

LLM invocation pipeline optimized for cost with model selection and caching.

## Inputs

```python
task: str, budget: float, quality: str
```

## Outputs

```python
result: str, costUsed: float, model: str, cacheHits: int
```

## Configuration

- **ID**: cost-aware-llm-pipeline
- **Name**: Cost Aware Llm Pipeline
- **Phase**: Phase 4 optimization

## Status

[PENDING] Interface defined. Ready for implementation.

## Usage
### Example 1: Select Model by Budget

```python
from skills.costAwareLlmPipeline.skill import CostAwareLlmPipeline

skill = CostAwareLlmPipeline()

task = {
    "description": "Analyze customer feedback",
    "maxCost": 5.0,
    "priority": "accuracy"
}

selection = skill.selectModel(task)
print(f"Selected: {selection['model']} (Est. cost: ${selection['cost']:.2f})")
```

### Example 2: Route Request Through Pipeline

```python
request = {
    "task": "Generate report",
    "model": "claude-opus",
    "useCache": True
}

result = skill.routeRequest(request)
print(f"Status: {result['status']}, Cost: ${result['cost']:.2f}")
```

## API

### Class: CostAwareLlmPipeline

```python
class CostAwareLlmPipeline:
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
from costAwareLlmPipeline.skill import CostAwareLlmPipeline

skill = CostAwareLlmPipeline()
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

skill = CostAwareLlmPipeline(config=config)
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
| `ValueError` | Negative cost budget | Ensure maxCost > 0 |
| `ValueError` | Unknown model name | Use registered model names |
| `TimeoutError` | Pipeline timeout | Reduce task complexity or increase timeout |
| `RuntimeError` | No model meets budget | Increase budget or use simpler task |

## Related Skills

- **Upstream**: [To be documented]
- **Downstream**: [To be documented]
- **Alternative**: None
