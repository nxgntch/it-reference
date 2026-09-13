# Performance Tracing Skill (IMPLEMENTED)

## Description

OpenTelemetry-compatible tracing for latency breakdown and performance analysis.

## Features

- **Start Trace**: Begin a new distributed trace with auto-generated or custom ID
- **End Trace**: Complete a trace and calculate total duration
- **Query Trace**: Retrieve stored trace with all spans
- **Export Traces**: Export summary statistics for all traces
- **Span Management**: Store and organize spans within traces

## Inputs

```python
operation: str (start, end, query, export)
traceId: Optional[str]
span: Optional[TraceSpan]
```

## Outputs

```python
trace: Trace
  traceId: str
  spans: List[TraceSpan]
  totalDuration: float (ms)
  spanCount: int
```

## Implementation Details

- In-memory trace storage with automatic lifecycle management
- Active trace tracking (start/end times)
- Span organization within traces
- Summary export with total traces, spans, and active counts
- Comprehensive logging at all trace events

## Status

✅ (IMPLEMENTED) 11 tests passing. Full trace lifecycle management with span tracking.

## Usage
### Example: Trace Request Performance
```python
skill.startTrace('req-1')
skill.startSpan('operation')
skill.endSpan('operation')
report = skill.getTraceReport('req-1')```

## Configuration

Performance Tracing is configured through `config/skills.yaml`:

```yaml
performanceTracing:
  enabled: true
  trace_storage_enabled: true
  max_spans_per_trace: 1000
  trace_retention_seconds: 3600
  export_summary_enabled: true
```

**Configuration Parameters**:
- `enabled`: Enable performance tracing (default: true)
- `trace_storage_enabled`: Store traces in memory (default: true)
- `max_spans_per_trace`: Maximum spans per trace (default: 1000)
- `trace_retention_seconds`: How long to retain traces (default: 3600)
- `export_summary_enabled`: Enable trace summary export (default: true)

## API

### Class: PerformanceTracing

```python
class PerformanceTracing:
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
from performanceTracing.skill import PerformanceTracing

skill = PerformanceTracing()
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

skill = PerformanceTracing(config=config)
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
| `ValueError` | Invalid trace ID | Use unique identifiers |

## Related Skills
- **Upstream**: [To be documented]
- **Downstream**: [To be documented]
