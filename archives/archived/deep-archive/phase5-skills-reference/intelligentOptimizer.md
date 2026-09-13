# Intelligent Optimizer Skill

**Phase**: 19  
**Week**: 2  
**Category**: ML Optimization  
**Status**: ✅ Complete

---

## Description

**Phase**: 19  

## Overview

ML-driven resource optimization with reinforcement learning feedback loops. Recommends parameter adjustments for performance, cost, efficiency, and reliability objectives. Learns from feedback to improve recommendations over time.

---

## Features

- **Multi-Objective Optimization**: Performance, cost, efficiency, reliability, balanced
- **Reinforcement Learning**: Parameter weights learned from feedback rewards
- **Improvement Prediction**: Estimate impact of parameter changes
- **Parameter Adaptation**: Learn optimal values for key parameters
- **History Tracking**: Complete optimization action history
- **Feedback Integration**: Reward signals drive learning

---

## Optimization Objectives

- `performance` - Maximize throughput/minimize latency
- `cost` - Minimize spending
- `efficiency` - Maximize output per resource
- `reliability` - Maximize availability/minimize errors
- `balanced` - Multi-objective balance

---

## Parameters

Learnable parameters:
- `cache_size` - Application cache size (KB)
- `connection_pool` - Database connection pool size
- `timeout` - Request timeout (ms)
- `batch_size` - Batch processing size
- `worker_threads` - Async worker count
- `cache_ttl` - Cache time-to-live (seconds)

---

## Operations

### optimize
Run optimization pass for current metrics.

**Parameters**:
- `metrics` (dict): Current system metrics
- `objective` (str): Optimization objective

**Returns**:
```json
{
  "success": true,
  "action_id": "opt_1",
  "parameter": "cache_size",
  "old_value": 512.0,
  "new_value": 768.0,
  "estimated_improvement_percent": 15.5,
  "objective": "performance",
  "optimization_time_ms": 2.3
}
```

### recommend_action
Get optimization recommendation for objective.

**Parameters**:
- `current_state` (dict): Current system state
- `objective` (str): Optimization objective

**Returns**:
```json
{
  "success": true,
  "parameter": "cache_size",
  "recommendation": "Increase cache size for better hit ratio",
  "confidence_percent": 95.0,
  "objective": "performance"
}
```

### provide_feedback
Provide feedback on optimization outcome.

**Parameters**:
- `action_id` (str): Optimization action ID
- `reward` (float): Reward value (>0 = good, <0 = bad)
- `outcome_metrics` (dict): Metrics after applying optimization

**Returns**:
```json
{
  "success": true,
  "action_id": "opt_1",
  "reward": 8.5,
  "parameter_weight_updated": 1.085,
  "learning_status": "learning"
}
```

### predict_improvement
Predict improvement for parameter change.

**Parameters**:
- `parameter` (str): Parameter name
- `change_magnitude` (float): Percent change

**Returns**:
```json
{
  "success": true,
  "parameter": "cache_size",
  "change_magnitude": 20.0,
  "predicted_improvement_percent": 17.2,
  "confidence": "high"
}
```

### set_objective
Set optimization objective.

**Parameters**:
- `objective` (str): Target objective

**Returns**:
```json
{
  "success": true,
  "objective": "reliability",
  "active": true
}
```

### get_learned_weights
Get learned parameter weights.

**Returns**:
```json
{
  "success": true,
  "parameter_weights": {
    "cache_size": 1.15,
    "connection_pool": 1.08,
    "timeout": 0.92
  },
  "learning_iterations": 42
}
```

### get_optimization_history
Get optimization action history.

**Parameters**:
- `limit` (int): Number of recent actions (default: 50)

**Returns**:
```json
{
  "success": true,
  "history": [
    {
      "action_id": "opt_1",
      "parameter": "cache_size",
      "improvement_percent": 15.5,
      "feedback_received": true,
      "reward": 8.5
    }
  ],
  "count": 1,
  "total_actions": 42
}
```

---

## Configuration

Via `config/skills.yaml`:

```yaml
- id: intelligentOptimizer
  phase: 19
  week: 2
  costTier: quick
```

Via constructor:

```python
optimizer = IntelligentOptimizer(config={
    "max_history": 1000  # Max optimization actions to retain
})
```

---

## Example Usage

```python
optimizer = IntelligentOptimizer()
await optimizer.initialize()

# Set optimization objective
await optimizer.execute(
    operation="set_objective",
    objective="performance"
)

# Get recommendation
recommendation = await optimizer.execute(
    operation="recommend_action",
    current_state={"cpu": 75, "memory": 60},
    objective="performance"
)

# Apply optimization
opt_result = await optimizer.execute(
    operation="optimize",
    metrics={"latency": 100, "throughput": 500},
    objective="performance"
)

# Provide feedback on outcome
await optimizer.execute(
    operation="provide_feedback",
    action_id=opt_result["action_id"],
    reward=12.5,  # Positive: optimization was beneficial
    outcome_metrics={"latency": 85, "throughput": 580}
)

# Predict impact of future changes
prediction = await optimizer.execute(
    operation="predict_improvement",
    parameter="cache_size",
    change_magnitude=25.0
)

# View learned weights
weights = await optimizer.execute(
    operation="get_learned_weights"
)
```

---

## Learning Loop

1. **Optimize**: Recommend parameter change for objective
2. **Apply**: User applies recommended changes in production
3. **Monitor**: Measure outcome metrics
4. **Feedback**: Provide reward signal to optimizer
5. **Learn**: Weights updated: `new_weight = old_weight * (1 + reward/100)`
6. **Repeat**: Next optimization uses updated weights

---

## Performance

- **Optimization Decision**: <30ms
- **Recommendation**: <10ms
- **Prediction**: <5ms per parameter
- **Feedback Processing**: <5ms
- **Total Latency**: <100ms per operation

---

## Integration

Works with:
- **forecastingEngine**: Predict optimization impact on forecast accuracy
- **rootCauseAnalyzer**: Use root causes to inform optimization direction

---

## Testing

20 tests covering:
- Optimization pass (7 tests)
- Recommendation generation (1 test)
- Feedback processing (1 test)
- Weight management (1 test)
- Prediction (1 test)
- Statistics (1 test)

Run: `pytest tests/test_phase19_week2_ml.py::TestIntelligentOptimizer -v`

## Usage
### Example
```python
result = skill.optimize(objectives, constraints)
print(f'Solution: {result}')
```

## API

### Class: IntelligentOptimizer

```python
class IntelligentOptimizer:
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
from intelligentOptimizer.skill import IntelligentOptimizer

skill = IntelligentOptimizer()
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

skill = IntelligentOptimizer(config=config)
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
| ValueError | Invalid input | Check parameters |

## Related Skills
- See CONSOLIDATION_OPPORTUNITIES_2026-08-30.md
