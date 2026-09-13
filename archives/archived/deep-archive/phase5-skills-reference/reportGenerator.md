# Report Generator Skill

## Description

Generate formatted reports (HTML, PDF, Markdown) from analytics data.

## Inputs

```python
data: dict, format: str (html|pdf|markdown), template: str
```

## Outputs

```python
report: bytes, format: str, filesize: int, renderTime: float
```

## Configuration

- **ID**: reportGenerator
- **Name**: Report Generator
- **Phase**: Phase 18 observability

## Status

[IMPLEMENTED] Report generation for analytics and monitoring data.

## Usage

### Example 1: Generate HTML Report

```python
from skills.reportGenerator.skill import ReportGenerator

skill = ReportGenerator()

data = {
    "title": "Monthly Analytics",
    "metrics": {"uptime": 99.9, "latency": 150},
    "charts": [{"type": "line", "data": [1, 2, 3]}]
}

report = skill.generateReport(
    data=data,
    format="html",
    template="standard"
)

with open("report.html", "wb") as f:
    f.write(report["content"])
```

### Example 2: Generate PDF with Custom Styling

```python
report = skill.generateReport(
    data=data,
    format="pdf",
    template="executive",
    styling={"color": "blue", "fontSize": 12}
)
```

## API

### Class: ReportGenerator

```python
class ReportGenerator:
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
from reportGenerator.skill import ReportGenerator

skill = ReportGenerator()
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

skill = ReportGenerator(config=config)
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
| ValueError | Invalid data format | Provide dict with required fields |
| ValueError | Unsupported format | Use: html, pdf, markdown |
| ValueError | Missing template | Use valid template name |
| TimeoutError | Report too complex | Reduce data size or simplify template |

## Related Skills

- **Upstream**: analyticsEngine, metricsCollector (provide data)
- **Downstream**: docUpdater (incorporates reports)
- **Alternative**: None (primary reporting skill)
