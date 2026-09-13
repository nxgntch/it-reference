# Cost Forecasting Skill

**Predict future spending and identify cost optimization opportunities.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 18+ | Coverage: >85%

---

## Description

**Predict future spending and identify cost optimization opportunities.**

## Overview

The Cost Forecasting skill is the **spending prediction engine** in nxgntch. It analyzes historical spending patterns to forecast future costs, identify budget risks, and recommend cost optimization strategies.

**When to use**: Before executing large tasks, to understand cost implications and budget impact.  
**What it solves**: Eliminates surprises about spending, enables proactive budget management, identifies cost optimization opportunities.  
**Key benefit**: Make informed decisions with clear cost visibility and risk awareness.

---

## Key Features

- **Time-Series Forecasting**: Predict future spending based on historical patterns
- **Trend Detection**: Identify upward/downward spending trends
- **Budget Risk Assessment**: Calculate probability of budget overrun
- **Anomaly Detection**: Identify unusual spending spikes or dips
- **Optimization Recommendations**: Suggest cost-saving actions with savings estimates
- **Scenario Analysis**: "What-if" modeling for budget planning
- **Confidence Metrics**: Express confidence in forecasts

---

## Quick Start

Minimal example to forecast spending:

```python
from skills.costForecasting import CostForecasting

# Initialize the skill
skill = CostForecasting()

# Execute forecast
result = await skill.execute({
    "historicalSpend": [100.0, 105.0, 110.0, 115.0, 120.0],
    "currentSpend": 120.0,
    "budget": 1000.0,
    "forecastPeriods": 7,
    "daysElapsed": 5
})

# Result contains forecast and risk analysis
print(result["output"])
# {
#     "forecast7Day": 875.0,
#     "forecastMonthly": 3500.0,
#     "riskLevel": "low",
#     "projectedOverage": 0.0,
#     "recommendations": [
#         {"action": "Optimize batch sizes", "savings": 150.0}
#     ]
# }
```

---

## Usage

### Basic Usage: Forecast Next Period

```python
# Example 1: Simple spending forecast
result = await skill.execute({
    "historicalSpend": [100.0, 105.0, 110.0, 115.0, 120.0],
    "forecastPeriods": 7
})

forecast = result["output"]["forecast7Day"]
daily_avg = result["output"]["dailyAverage"]
print(f"7-day forecast: ${forecast:.2f} (avg: ${daily_avg:.2f}/day)")
```

### With Budget Risk: Budget Impact Analysis

```python
# Example 2: Assess budget safety
result = await skill.execute({
    "historicalSpend": [100.0, 105.0, 110.0, 115.0, 120.0],
    "currentSpend": 450.0,
    "budget": 1000.0,
    "daysElapsed": 15,
    "projectedTotalDays": 30
})

risk = result["output"]
print(f"Risk level: {risk['riskLevel']}")
if risk['riskLevel'] == 'high':
    print(f"Projected overage: ${risk['projectedOverage']:.2f}")
```

### With Optimization: Identify Cost-Saving Opportunities

```python
# Example 3: Get optimization recommendations
result = await skill.execute({
    "historicalSpend": [100.0, 105.0, 110.0, 115.0, 120.0],
    "costPattern": {
        "avgDailyCost": 110.0,
        "peakDailyCost": 150.0,
        "anomalies": [
            {"date": "2026-08-25", "cost": 150.0, "cause": "unexpected spike"}
        ]
    },
    "includeRecommendations": True
})

for rec in result["output"]["recommendations"]:
    print(f"- {rec['action']}: Save ${rec['estimatedSavings']:.2f}")
```

### Error Handling: Insufficient Data

```python
# Example 4: Handle edge cases
result = await skill.execute({
    "historicalSpend": [100.0]  # Only 1 day of data
})

output = result["output"]
if output.get("insufficientData"):
    print("Need at least 3 days of data")
    print(f"Days provided: {output.get('daysProvided')}")
    print(f"Days required: {output.get('daysRequired')}")
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `historicalSpend` | list[float] | Yes | Daily spending history (minimum 3 days) |
| `currentSpend` | float | No | Current period spend so far |
| `budget` | float | No | Budget cap for period |
| `forecastPeriods` | int | No | Days to forecast ahead (default: 7) |
| `daysElapsed` | int | No | Days elapsed in current period |
| `projectedTotalDays` | int | No | Total days in current period |
| `costPattern` | dict | No | Detailed cost pattern analysis |
| `includeRecommendations` | bool | No | Include optimization suggestions (default: true) |

**Input Example**:
```python
{
    "historicalSpend": [100.0, 105.0, 110.0, 115.0, 120.0],
    "currentSpend": 450.0,
    "budget": 1000.0,
    "forecastPeriods": 7,
    "daysElapsed": 15,
    "projectedTotalDays": 30,
    "includeRecommendations": True
}
```

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether forecast succeeded |
| `data.forecast7Day` | float | 7-day spending forecast |
| `data.forecastMonthly` | float | 30-day spending forecast |
| `data.dailyAverage` | float | Average daily spend |
| `data.trendDirection` | string | Trend (increasing/stable/decreasing) |
| `data.riskLevel` | string | Budget risk (low/medium/high) |
| `data.projectedOverage` | float | Projected budget overage (0 if safe) |
| `data.recommendations` | list | Cost optimization suggestions |
| `data.insufficientData` | bool | Not enough history for forecast |
| `metadata.latency_ms` | float | Processing time |
| `metadata.confidence` | float | Forecast confidence (0-1) |

**Output Example**:
```python
{
    "success": True,
    "data": {
        "forecast7Day": 875.0,
        "forecastMonthly": 3500.0,
        "dailyAverage": 125.0,
        "trendDirection": "increasing",
        "riskLevel": "low",
        "projectedOverage": 0.0,
        "recommendations": [
            {"action": "Optimize batch sizes", "estimatedSavings": 150.0},
            {"action": "Cache query results", "estimatedSavings": 100.0}
        ]
    },
    "metadata": {
        "latency_ms": 45.2,
        "confidence": 0.87,
        "data_points": 5
    }
}
```

---

## Configuration

Environment variables and configuration:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `FORECAST_MIN_HISTORY_DAYS` | int | 3 | Minimum days needed for forecast |
| `FORECAST_MODEL` | str | "exponential_smoothing" | Forecasting algorithm |
| `FORECAST_CONFIDENCE_THRESHOLD` | float | 0.7 | Minimum confidence for recommendation |
| `FORECAST_TIMEOUT_SECONDS` | int | 10 | Forecast computation timeout |
| `FORECAST_ANOMALY_THRESHOLD` | float | 2.0 | Std dev threshold for anomalies |

**Setting Configuration**:
```python
# Option 1: Via config dict
skill = CostForecasting(config={
    "min_history_days": 5,
    "model": "arima",
    "confidence_threshold": 0.8,
    "timeout_seconds": 15
})

# Option 2: Via environment variables
import os
os.environ["FORECAST_MIN_HISTORY_DAYS"] = "5"
os.environ["FORECAST_MODEL"] = "arima"
```

---

## Error Handling

### Insufficient Historical Data

**Cause**: Fewer than 3 days of spending history  
**Indicator**: `insufficientData: True` in response  
**Solution**: Provide at least 3 days of spending data  
```python
result = await skill.execute({"historicalSpend": [100.0]})
if result["data"].get("insufficientData"):
    print(f"Need {result['data']['daysRequired']} days, got {result['data']['daysProvided']}")
```

### Invalid Spend Data

**Cause**: Negative values or non-numeric data  
**Error**: ValueError raised  
**Solution**: Ensure all spending values are non-negative numbers  
```python
# Valid: [100.0, 105.0, 110.0]
# Invalid: [-50.0, 100.0, 150.0] (negative value)
```

### Budget Less Than Current Spend

**Cause**: Budget cap is below already-spent amount  
**Error**: Returns with flag `budgetAlreadyExceeded: True`  
**Solution**: Adjust budget or investigate overspend  
```python
if result["data"].get("budgetAlreadyExceeded"):
    print(f"Already spent: ${result['data']['currentSpend']:.2f}")
```

### Low Forecast Confidence

**Cause**: Historical data too volatile or insufficient pattern  
**Indicator**: `confidence < 0.7` in metadata  
**Solution**: Provide more historical data or reduce forecast horizon  
```python
if result["metadata"]["confidence"] < 0.7:
    print("Low forecast confidence - consider extending history")
```

---

## Testing

- **Unit Tests**: `tests/test_costForecasting.py` (10+ comprehensive tests)
- **Coverage**: >85% of forecasting logic
- **Test Patterns**: Trend detection, risk calculation, recommendation generation

### Running Tests

```bash
# Run cost forecasting tests
pytest tests/test_costForecasting.py -v

# Run with coverage
pytest tests/test_costForecasting.py --cov=skills.costForecasting --cov-report=term-missing

# Run specific test
pytest tests/test_costForecasting.py::TestCostForecasting::testForecastsSpendingAccurately -v
```

### Test Coverage

- ✅ Spending forecast accuracy
- ✅ Trend detection (increasing/stable/decreasing)
- ✅ Budget risk calculation
- ✅ Anomaly detection in spending patterns
- ✅ Optimization recommendation generation
- ✅ Edge cases (minimal data, flat spending, spikes)

---

## Dependencies

### Skills That Use This Skill

- **routing** — Uses forecasts to evaluate cost impact of routing decisions
- **decisionMaking** — Incorporates cost forecasts into decision logic
- **orchestrator** — Checks forecasts before executing expensive tasks

### Skills Used By This Skill

- None (standalone forecasting)

### Related Skills

- **costAwareLlmPipeline**: Consumes forecasts for cost-aware decisions

---

## Performance Characteristics

- **Latency (p50)**: ~25-35 ms
- **Latency (p95)**: <100 ms
- **Throughput**: 200+ forecasts/second (single instance)
- **Scalability**: Horizontal (stateless)
- **Complexity**: O(n) where n = days of history

---

## Troubleshooting

### Issue: Forecast Seems Inaccurate

**Diagnosis**: Predicted spending doesn't match actual  
**Solutions**:
1. Verify historical data is complete and accurate
2. Check for seasonal patterns (forecasting may miss them)
3. Review anomalies (spikes may skew trend)
4. Increase minimum history for more accurate baseline

### Issue: Budget Risk Always Low

**Diagnosis**: Risk assessment shows low risk despite tight budget  
**Solutions**:
1. Verify budget and current spend values are correct
2. Check if trend is actually increasing (not detected)
3. Review historical volatility (may be too stable)
4. Lower confidence threshold to be more conservative

### Issue: Recommendations Too Generic

**Diagnosis**: Optimization suggestions not specific to your use case  
**Solutions**:
1. Provide detailed cost pattern analysis
2. Include specific anomalies and their causes
3. Set constraints on recommendations (e.g., "don't reduce quality")
4. Combine with domain-specific knowledge for better suggestions

---

## Changelog

### Version 1.0.0 (Phase 18+)
- ✅ Time-series spending forecasting
- ✅ Trend detection (increasing/stable/decreasing)
- ✅ Budget risk assessment
- ✅ Anomaly detection
- ✅ Cost optimization recommendations
- ✅ Scenario analysis
- ✅ >85% test coverage

---

## Related Documentation

- **Skill Dependencies**: See `skills/DEPENDENCIES.md` for full skill graph
- **Configuration**: See `config/skills.yaml` for skill registry
- **Unified Template**: See `skills/SKILL_TEMPLATE_UNIFIED.md` for documentation format
- **Cost Management**: See `docs/guides/operations/COST_MANAGEMENT.md` for cost strategies
