# Cost Intelligence

Analyze cost implications of tasks and routing decisions. Provides cost forecasting and optimization recommendations.

## Agent
- **Primary Agent**: director
- **Cost Tier**: quick

## Capabilities
- Cost impact analysis
- Budget forecasting
- Optimization opportunities
- Cost-aware routing

## Description
Strategic cost analysis skill that enables the Director agent to understand and optimize the cost implications of routing decisions. Provides forecasting of budget impact and identifies cost optimization opportunities before task execution.

## Input
- Task description and requirements
- Routing parameters and candidate agents/models
- Current budget status and constraints

## Output
- Cost impact analysis
- Budget implications and forecasts
- Cost optimization recommendations
- Routing suggestions for cost-optimal execution

## Usage

### Basic Usage

```python
from app.skills.costIntelligence import CostIntelligence

skill = CostIntelligence()
result = await skill.execute({
    "task_description": "Process 1000 records with Claude-3 Opus",
    "estimated_tokens": 50000,
    "current_budget_used": 2500,
    "monthly_budget": 10000
})

print(result)
# Output: {"cost_impact": {...}, "recommendations": [...]}
```

### Advanced Usage

```python
# Analyze multiple routing options
result = await skill.execute({
    "task": "Analyze customer data",
    "routing_options": [
        {"agent": "director", "model": "opus", "estimated_cost": 2.50},
        {"agent": "manager", "model": "sonnet", "estimated_cost": 0.75},
        {"agent": "specialist", "model": "haiku", "estimated_cost": 0.15}
    ],
    "budget_remaining": 7500,
    "risk_tolerance": "medium"
})

# Returns cost-optimized routing recommendation
```

## Configuration

Cost Intelligence is configured through `config/skills.yaml`:

```yaml
costIntelligence:
  enabled: true
  forecast_window_days: 30
  cache_enabled: true
  cache_ttl_seconds: 300
  risk_tolerance_default: "medium"
```

**Configuration Parameters**:
- `enabled`: Enable cost intelligence (default: true)
- `forecast_window_days`: Forecast period in days (default: 30)
- `cache_enabled`: Cache cost calculations (default: true)
- `cache_ttl_seconds`: Cache time-to-live in seconds (default: 300)
- `risk_tolerance_default`: Default risk tolerance level (default: medium)

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_description` | str | Yes | Description of the task to execute |
| `estimated_tokens` | int | Yes | Estimated token usage for the task |
| `current_budget_used` | float | Yes | Amount already spent this month |
| `monthly_budget` | float | Yes | Total monthly budget allocation |
| `routing_options` | list | No | List of routing options with costs |
| `risk_tolerance` | str | No | Budget risk tolerance: low, medium, high |

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `cost_impact` | dict | Cost impact analysis with projections |
| `recommendations` | list | Cost optimization recommendations |
| `routing_suggestion` | str | Recommended routing option |
| `budget_forecast` | dict | End-of-month budget projection |
| `risk_level` | str | Risk assessment: low, medium, high |

Example output:
```python
{
    "cost_impact": {
        "immediate_cost": 2.50,
        "monthly_projection": 7500,
        "budget_remaining": 2500
    },
    "recommendations": [
        "Consider using Sonnet model to reduce costs by 70%",
        "Current burn rate will exceed budget in 4 days"
    ],
    "routing_suggestion": "Use sonnet model for cost efficiency",
    "budget_forecast": {
        "end_of_month_projection": 12500,
        "over_budget_by": 2500,
        "recommended_action": "Optimize or hold non-critical tasks"
    },
    "risk_level": "high"
}
```

---

## Usage
Used by the Director agent during task routing to make cost-aware decisions. Complements healthMonitoring by ensuring tasks are both safe (health-aware) and economical (cost-aware).
