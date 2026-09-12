# Root Cause Analyzer Skill

**Phase**: 19  
**Week**: 2  
**Category**: ML Optimization  
**Status**: ✅ Complete

---

## Description

**Phase**: 19  

## Overview

Advanced anomaly root-cause analysis with correlation detection and hypothesis generation. Identifies likely causes for metric anomalies by analyzing metric relationships, historical patterns, and context, with confidence scoring and evidence tracking.

---

## Features

- **Root Cause Hypothesis Generation**: Automatic generation of multiple hypotheses
- **Multi-Dimensional Correlation Analysis**: Detect metric relationships
- **Evidence Tracking**: Collect supporting evidence for each hypothesis
- **Confidence Scoring**: Rank causes by likelihood percentage
- **Historical Pattern Matching**: Correlate with past anomalies
- **Context-Aware Analysis**: Incorporate deployment info and other context

---

## Cause Types

Supported root causes:
- `resource_exhaustion` - CPU/memory/disk saturation
- `network_degradation` - Network latency/packet loss
- `configuration_change` - Configuration modification effects
- `deployment` - New code deployment impact
- `external_dependency` - Third-party service issues
- `load_spike` - Concurrent request surge
- `software_bug` - Code defect introduced
- `hardware_failure` - Infrastructure failure
- `unknown` - Insufficient data for diagnosis

---

## Operations

### analyze_anomaly
Analyze anomaly and generate root cause hypotheses.

**Parameters**:
- `anomaly_id` (str): Unique anomaly identifier
- `metric_name` (str): Affected metric
- `anomaly_value` (float): Anomalous value
- `context` (dict): Additional context (deployment time, config changes, etc.)

**Returns**:
```json
{
  "success": true,
  "anomaly_id": "anom-001",
  "metric_name": "error_rate",
  "most_likely_cause": "resource_exhaustion",
  "confidence": 40,
  "hypotheses": 3,
  "analysis_time_ms": 8.5
}
```

### rank_causes
Rank potential causes by likelihood.

**Parameters**:
- `anomaly_id` (str): Anomaly identifier

**Returns**:
```json
{
  "success": true,
  "anomaly_id": "anom-001",
  "ranked_causes": [
    {
      "cause": "resource_exhaustion",
      "likelihood_percent": 40,
      "evidence_count": 2
    }
  ],
  "top_cause": "resource_exhaustion"
}
```

### find_correlations
Find correlated metrics for root cause.

**Parameters**:
- `metric_name` (str): Primary metric
- `metrics_to_check` (list): List of metric names to check correlation

**Returns**:
```json
{
  "success": true,
  "metric_name": "error_rate",
  "correlations": {
    "cpu_usage": 0.78,
    "memory_usage": 0.65
  },
  "strong_correlations": {
    "cpu_usage": 0.78
  },
  "correlation_count": 1
}
```

### get_root_cause
Get detailed root cause for anomaly.

**Parameters**:
- `anomaly_id` (str): Anomaly identifier

**Returns**:
```json
{
  "success": true,
  "anomaly_id": "anom-001",
  "cause": "resource_exhaustion",
  "likelihood_percent": 40,
  "supporting_evidence": [
    "High metric value",
    "Potential capacity issue"
  ],
  "correlated_metrics": ["cpu_usage", "memory_usage"]
}
```

### pattern_match
Match anomaly against historical patterns.

**Parameters**:
- `anomaly_pattern` (str): Pattern to search for
- `historical_limit` (int): Number of recent analyses to check

**Returns**:
```json
{
  "success": true,
  "pattern": "cpu",
  "matches": 3,
  "matched_analyses": [...]
}
```

### validate_hypothesis
Validate root cause hypothesis.

**Parameters**:
- `anomaly_id` (str): Anomaly identifier
- `hypothesis_cause` (str): Cause to validate

**Returns**:
```json
{
  "success": true,
  "anomaly_id": "anom-001",
  "hypothesis": "resource_exhaustion",
  "is_valid": true,
  "validation_status": "confirmed"
}
```

---

## Configuration

Via `config/skills.yaml`:

```yaml
- id: rootCauseAnalyzer
  phase: 19
  week: 2
  costTier: quick
```

Via constructor:

```python
analyzer = RootCauseAnalyzer(config={
    "max_history": 1000  # Max analysis records to retain
})
```

---

## Example Usage

```python
analyzer = RootCauseAnalyzer()
await analyzer.initialize()

# Detect and analyze anomaly
result = await analyzer.execute(
    operation="analyze_anomaly",
    anomaly_id="anom-prod-001",
    metric_name="error_rate",
    anomaly_value=15.2,
    context={
        "deployment_time": "2024-01-15T10:30:00Z"
    }
)

# Get detailed analysis
root_cause = await analyzer.execute(
    operation="get_root_cause",
    anomaly_id="anom-prod-001"
)

# Find correlated metrics
correlations = await analyzer.execute(
    operation="find_correlations",
    metric_name="error_rate",
    metrics_to_check=["cpu_usage", "memory_usage", "latency"]
)

# Pattern matching against similar past anomalies
patterns = await analyzer.execute(
    operation="pattern_match",
    anomaly_pattern="error_rate",
    historical_limit=50
)
```

---

## Performance

- **Analysis**: <50ms per anomaly
- **Correlation Detection**: <30ms for 10 metrics
- **Pattern Matching**: <40ms over 100 historical analyses
- **Total Latency**: <100ms per operation

---

## Integration

Works with:
- **forecastingEngine**: Use forecasts as expected baseline; deviation = anomaly
- **intelligentOptimizer**: Root causes inform optimization recommendations

---

## Testing

20 tests covering:
- Anomaly analysis (6 tests)
- Cause ranking (6 tests)
- Correlation detection (1 test)
- Root cause retrieval (1 test)
- Pattern matching (1 test)
- Statistics (1 test)

Run: `pytest tests/test_phase19_week2_ml.py::TestRootCauseAnalyzer -v`

## Usage
### Example 1: Analyze Anomaly Root Cause

```python
from skills.rootCauseAnalyzer.skill import RootCauseAnalyzer

skill = RootCauseAnalyzer()

anomaly = {
    "metric": "latency",
    "value": 5000,  # 5000ms (anomaly)
    "timestamp": "2026-08-30T14:30:00Z",
    "baselineValue": 100,
}

analysis = skill.analyzeRootCause(anomaly)
print(f"Likely causes: {analysis['potentialCauses']}")
print(f"Confidence: {analysis['confidence']:.2%}")
```

### Example 2: Generate Remediation Steps

```python
remediation = skill.getRemediationSteps(analysis)

for step in remediation['steps']:
    print(f"- {step['action']} (Impact: {step['estimatedImpact']})")
```

## API

### Class: RootCauseAnalyzer

```python
class RootCauseAnalyzer:
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
from rootCauseAnalyzer.skill import RootCauseAnalyzer

skill = RootCauseAnalyzer()
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

skill = RootCauseAnalyzer(config=config)
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
| `ValueError` | Missing anomaly data | Provide metric, value, timestamp, baseline |
| `ValueError` | Baseline equals anomaly value | No anomaly to analyze |
| `TimeoutError` | Analysis took too long | Try simpler metric or fewer dimensions |

## Related Skills

- **Upstream**: [To be documented]
- **Downstream**: [To be documented]
- **Alternative**: None
