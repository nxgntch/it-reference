# Anomaly Detector Skill

## Description

Statistical anomaly detection with configurable sensitivity.

## Inputs

```python
timeSeries: List[float], sensitivity: float (0.0-1.0), method: str
```

## Outputs

```python
anomalies: List[Dict], threshold: float, statistics: Dict
```

## Configuration

- **ID**: anomalyDetector
- **Name**: Anomaly Detector
- **Phase**: Phase 18 observability

## Status

[IMPLEMENTED] Statistical anomaly detection with configurable algorithms.

## Usage

### Example 1: Detect Anomalies

```python
from skills.anomalyDetector.skill import AnomalyDetector

skill = AnomalyDetector()

timeSeries = [100, 102, 101, 103, 100, 102, 500, 101, 102]  # 500 is anomaly

anomalies = skill.detectAnomalies(
    timeSeries=timeSeries,
    sensitivity=0.8,
    method='zscore'
)

for anomaly in anomalies:
    print(f"Anomaly at index {anomaly['index']}: value={anomaly['value']}")
```

### Example 2: Use Custom Sensitivity

```python
# High sensitivity = more anomalies detected
strictDetection = skill.detectAnomalies(
    timeSeries=timeSeries,
    sensitivity=0.95,  # Very strict
    method='iqr'
)

# Low sensitivity = fewer false positives
lenientDetection = skill.detectAnomalies(
    timeSeries=timeSeries,
    sensitivity=0.5,  # More lenient
    method='isolation_forest'
)
```

### Example 3: Analyze Anomaly Statistics

```python
analysis = skill.analyzeAnomalies(timeSeries, sensitivity=0.85)

print(f"Baseline mean: {analysis['baselineMean']:.2f}")
print(f"Baseline std: {analysis['baselineStd']:.2f}")
print(f"Detection threshold: {analysis['threshold']:.2f}")
print(f"Anomalies found: {len(analysis['anomalies'])}")
```

## API

### Class: AnomalyDetector

```python
class AnomalyDetector:
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
from anomalyDetector.skill import AnomalyDetector

skill = AnomalyDetector()
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

skill = AnomalyDetector(config=config)
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
| `ValueError` | Empty time series | Provide at least 5 data points |
| `ValueError` | Sensitivity outside 0-1 range | Use sensitivity between 0.0 and 1.0 |
| `ValueError` | Unknown detection method | Use: 'zscore', 'iqr', 'isolation_forest' |
| `TypeError` | Non-numeric values in series | Ensure all values are int or float |

## Related Skills

- **Upstream**: analyticsEngine (provides aggregated metrics)
- **Downstream**: rootCauseAnalyzer (analyzes why anomalies occurred)
- **Alternative**: None (primary anomaly detection skill)
