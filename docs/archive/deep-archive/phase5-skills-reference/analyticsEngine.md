# Analytics Engine Skill

## Description

Data aggregation and trend analysis for orchestration insights.

## Inputs

```python
metrics: List[Dict], timeWindow: str, aggregationType: str
```

## Outputs

```python
aggregated: Dict, trends: List[Dict], statistics: Dict
```

## Configuration

- **ID**: analyticsEngine
- **Name**: Analytics Engine
- **Phase**: Phase 18 observability

## Status

[IMPLEMENTED] Core aggregation and trend analysis.

## Usage

### Example 1: Aggregate Metrics

```python
from skills.analyticsEngine.skill import AnalyticsEngine

skill = AnalyticsEngine()

metrics = [
    {'timestamp': '2026-08-30T00:00Z', 'latency': 100, 'throughput': 1000},
    {'timestamp': '2026-08-30T01:00Z', 'latency': 105, 'throughput': 1050},
    {'timestamp': '2026-08-30T02:00Z', 'latency': 110, 'throughput': 1100},
]

aggregated = skill.aggregate(metrics, timeWindow='1h', aggregationType='avg')
print(f"Average latency: {aggregated['avgLatency']}ms")
```

### Example 2: Analyze Trends

```python
trends = skill.identifyTrends(metrics, window=3)

for trend in trends:
    direction = 'increasing' if trend['slope'] > 0 else 'decreasing'
    print(f"{trend['metric']}: {direction} ({trend['slope']:.2f}/hour)")
```

### Example 3: Generate Report

```python
report = skill.generateReport(
    metrics=metrics,
    metrics_to_analyze=['latency', 'throughput', 'errorRate']
)

print(f"Metrics analyzed: {report['metricsCount']}")
print(f"Time span: {report['startTime']} to {report['endTime']}")
```

## API

### Class: AnalyticsEngine

```python
class AnalyticsEngine:
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
from analyticsEngine.skill import AnalyticsEngine

skill = AnalyticsEngine()
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

skill = AnalyticsEngine(config=config)
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
| `ValueError` | Empty metrics list | Provide at least one metric |
| `KeyError` | Missing timestamp in metric | Ensure all metrics have 'timestamp' field |
| `ValueError` | Invalid time window format | Use format: '1h', '30m', '1d' |
| `TypeError` | Non-numeric metric values | Validate metric values are floats/ints |

## Related Skills

- **Upstream**: metricsCollector (provides raw metrics)
- **Downstream**: anomalyDetector, rootCauseAnalyzer (consume aggregated data)
- **Alternative**: None (primary aggregation skill)
