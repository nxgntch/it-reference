# Forecasting Engine Skill

**Phase**: 19  
**Week**: 2  
**Category**: ML Optimization  
**Status**: ✅ Complete

---

## Description

**Phase**: 19  

## Overview

Advanced time-series forecasting engine supporting multiple algorithms (ARIMA, exponential smoothing, linear regression, seasonal) with confidence intervals and trend analysis. Designed for enterprise-scale metric predictions with <100ms latency.

---

## Features

- **Multiple Forecasting Methods**: Linear, exponential, ARIMA, seasonal
- **Confidence Intervals**: 95% confidence bands via std_dev * 1.96
- **Trend Detection**: Linear regression-based trend calculation
- **Model Training**: Fast in-process model training
- **Accuracy Tracking**: Per-model accuracy metrics
- **Method Comparison**: Automatic algorithm comparison and selection

---

## Operations

### add_data_point
Add historical metric data point.

**Parameters**:
- `metric_name` (str): Metric identifier
- `value` (float): Data point value

**Returns**:
```json
{
  "success": true,
  "metric_name": "cpu_usage",
  "data_points": 42,
  "latest_value": 65.5
}
```

### train_model
Train forecasting model for metric.

**Parameters**:
- `metric_name` (str): Metric identifier
- `method` (str): "linear" | "exponential" | "arima" | "seasonal"

**Returns**:
```json
{
  "success": true,
  "metric_name": "cpu_usage",
  "method": "linear",
  "data_points": 42,
  "mean": 58.3,
  "std_dev": 12.5,
  "trend": 0.25,
  "training_time_ms": 12.4
}
```

### forecast
Generate forecast for specified steps.

**Parameters**:
- `metric_name` (str): Metric identifier
- `steps` (int): Number of steps to forecast (default: 1)

**Returns**:
```json
{
  "success": true,
  "metric_name": "cpu_usage",
  "method": "linear",
  "forecasts": [
    {
      "step": 1,
      "predicted_value": 58.8,
      "lower_bound": 34.1,
      "upper_bound": 83.5
    }
  ],
  "forecast_time_ms": 8.3
}
```

### compare_methods
Compare all forecasting methods for metric.

**Parameters**:
- `metric_name` (str): Metric identifier

**Returns**:
```json
{
  "success": true,
  "metric_name": "cpu_usage",
  "comparisons": [
    {
      "method": "linear",
      "accuracy": 0.87,
      "recommended": true
    }
  ],
  "best_method": "linear"
}
```

### get_model
Get trained model details.

**Parameters**:
- `metric_name` (str): Metric identifier

**Returns**:
```json
{
  "success": true,
  "metric_name": "cpu_usage",
  "method": "linear",
  "data_points": 42,
  "mean": 58.3,
  "std_dev": 12.5,
  "trend": 0.25,
  "accuracy": 0.87
}
```

### evaluate_accuracy
Evaluate model accuracy.

**Parameters**:
- `metric_name` (str): Metric identifier

**Returns**:
```json
{
  "success": true,
  "metric_name": "cpu_usage",
  "accuracy": 0.87,
  "mape": 13.2,
  "evaluation_status": "good"
}
```

---

## Configuration

Via `config/skills.yaml`:

```yaml
- id: forecastingEngine
  phase: 19
  week: 2
  costTier: quick
```

Via constructor:

```python
engine = ForecastingEngine(config={
    "max_history": 5000,      # Max data points per metric
    "confidence_level": 0.95   # Confidence interval level
})
```

---

## Example Usage

```python
engine = ForecastingEngine()
await engine.initialize()

# Add historical data
for i in range(30):
    await engine.execute(
        operation="add_data_point",
        metric_name="response_time",
        value=100 + (i * 2)
    )

# Train model
await engine.execute(
    operation="train_model",
    metric_name="response_time",
    method="linear"
)

# Generate forecast
forecast = await engine.execute(
    operation="forecast",
    metric_name="response_time",
    steps=10
)

# Compare methods
best = await engine.execute(
    operation="compare_methods",
    metric_name="response_time"
)
```

---

## Performance

- **Training**: <50ms for 500+ data points
- **Forecasting**: <10ms per forecast
- **Method Comparison**: <100ms for all methods
- **Total Latency**: <100ms per operation

---

## Integration

Works with:
- **rootCauseAnalyzer**: Feed forecasts as baseline for anomaly detection
- **intelligentOptimizer**: Use forecasts to predict optimization impact

---

## Testing

20 tests covering:
- Data point addition (6 tests)
- Model training (6 tests)
- Forecasting (6 tests)
- Method comparison (1 test)
- Statistics (1 test)

Run: `pytest tests/test_phase19_week2_ml.py::TestForecastingEngine -v`

## Usage
### Example 1: Forecast Time Series

```python
from skills.forecastingEngine.skill import ForecastingEngine

skill = ForecastingEngine()

historical = [100, 105, 110, 115, 120, 125, 130]

forecast = skill.forecast(
    timeSeries=historical,
    periods=7,
    method="exponential_smoothing"
)

print(f"Forecasted values: {forecast['predictions']}")
print(f"Confidence interval: [{forecast['lower']}, {forecast['upper']}]")
```

## API

### Class: ForecastingEngine

```python
class ForecastingEngine:
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
from forecastingEngine.skill import ForecastingEngine

skill = ForecastingEngine()
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

skill = ForecastingEngine(config=config)
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
| `ValueError` | Insufficient historical data | Provide at least 10 data points |
| `ValueError` | Unknown forecast method | Use: 'arima', 'exponential_smoothing', 'linear' |

## Related Skills

- **Upstream**: [To be documented]
- **Downstream**: [To be documented]
- **Alternative**: None
