# Auto-Scaling Manager Skill

**Intelligent auto-scaling with cost and performance awareness.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 6

---

## Description

Manages real-time scaling decisions based on load, latency, budget, and predictions. Integrates with Phase 6 intelligent auto-scaler to maintain optimal resource utilization while respecting budget constraints.

---

## Key Features

- **Real-Time Scaling**: Make immediate up/down/maintain decisions
- **Predictive Scaling**: Forecast needs 1-24 hours ahead
- **Budget-Aware**: Respect budget constraints automatically
- **SLA Compliance**: Prioritize latency targets
- **Cost Optimization**: Right-size for constraints

---

## Quick Start

```python
from skills.autoScalingManager.skill import AutoScalingManager

manager = AutoScalingManager()

# Evaluate immediate decision
decision = await manager.evaluate_scaling_decision({
    "current_load": 0.75,
    "current_cost_rate": 100.0,
    "current_latency_ms": 450,
    "budget_remaining": 5000.0,
    "sla_target_latency_ms": 500,
})

print(f"Action: {decision['action']}")  # scale_up, scale_down, or maintain
print(f"Factor: {decision['factor']}")  # 1.3 = 30% scale up
```

---

## API Reference

### Input Schema

| Parameter | Type | Description |
|-----------|------|-------------|
| `operation` | string | Operation type (see Operations below) |
| `metrics` | object | Current metrics (load, cost, latency, budget) |
| `constraints` | object | Budget and SLA constraints |

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | Result status |
| `action` | string | `scale_up`, `scale_down`, or `maintain` |
| `factor` | float | Scale factor (1.3 = 30% up, 0.8 = 20% down) |
| `reason` | string | Human-readable reason |
| `priority` | string | `critical`, `high`, `medium`, `low` |

---

## Operations

### generate_plan

Create comprehensive scaling plan for next 24 hours.

**Input**:
```json
{
  "operation": "generate_plan",
  "metrics": {
    "current_load": 0.75,
    "current_cost_rate": 100.0,
    "current_latency_ms": 450,
    "budget_remaining": 5000.0,
    "sla_target_latency_ms": 500
  },
  "constraints": {
    "budget_cap": 10000.0,
    "max_latency_ms": 500
  }
}
```

**Output**:
```json
{
  "status": "success",
  "immediate_action": "scale_up",
  "immediate_factor": 1.2,
  "24_hour_prediction": "prepare_scale_up",
  "actions": [
    {
      "action": "scale_up",
      "timing": "within_5min",
      "reason": "High load at 75%"
    }
  ]
}
```

### evaluate_decision

Make immediate scaling decision.

**Input**:
```json
{
  "operation": "evaluate_decision",
  "metrics": { ... }
}
```

### predict_needs

Forecast scaling needs for next N hours.

**Input**:
```json
{
  "operation": "predict_needs",
  "forecast_hours": 24
}
```

### optimize_for_cost

Generate cost-optimized configuration.

**Input**:
```json
{
  "operation": "optimize_for_cost",
  "constraints": {
    "budget_cap": 10000.0,
    "current_hourly_cost": 150.0,
    "max_latency_ms": 500
  }
}
```

---

## Decision Priority

1. **SLA Compliance** (Critical): Latency >120% of SLA → Scale up
2. **Load Management** (High): Load >85% → Scale up
3. **Budget Pressure** (High): Budget <5 hours of current spend → Scale down
4. **Optimization** (Medium): Load <40% + budget healthy → Scale down
5. **Maintain** (Low): Everything nominal

---

## Scaling Factors

| Load | Action | Factor | Cost Impact |
|------|--------|--------|-------------|
| >85% | Scale up | 1.4 | +40% |
| 60-85% | Monitor | 1.0 | 0% |
| 40-60% | Monitor | 1.0 | 0% |
| <40% | Scale down | 0.8 | -20% |

---

## Budget Constraints

| Budget Status | Action | Timeline |
|---------------|--------|----------|
| Over budget | Scale down 10-25% | Immediate |
| At 80%+ | Scale down 5-15% | Next hour |
| At 60-80% | Maintain or optimize | Ongoing |
| Under 60% | Can optimize upward | Anytime |

---

## Integration Points

**Phase 5 Skills**:
- `orchestrator`: Use scaling decisions for task assignment
- `costIntelligence`: Track cost impact of scaling
- `costDashboard`: Display scaling events

**Phase 6 Components**:
- `intelligent_auto_scaler`: Underlying scaling logic
- `advanced_cost_analytics`: Cost forecasting
- `performance_profiler`: Latency data source

---

## Performance

- **Decision Time**: <50ms (real-time)
- **Prediction Time**: <100ms (up to 168 hours)
- **Update Frequency**: 1-10 seconds depending on load

---

## Tuning Parameters

| Parameter | Default | Range | Purpose |
|-----------|---------|-------|---------|
| `sla_threshold_pct` | 120 | 100-200 | Latency threshold for SLA violation |
| `high_load_pct` | 85 | 50-95 | Load % to trigger scale up |
| `budget_runway_hours` | 5 | 1-24 | Hours of budget remaining before scale |
| `low_load_pct` | 40 | 20-60 | Load % to trigger scale down |

---

## Known Limitations

- Predictions assume linear load trend (not ML-based)
- Scaling takes 1-2 seconds to apply
- Does not account for warmup/cooldown periods
- Budget constraints are hard stops (not soft limits)

---

## Monitoring & Alerts

**Alert Conditions**:
- Latency exceeds SLA: `priority: critical`
- Budget overrun: `priority: high`
- Load spike >90%: `priority: high`
- Scaling frequency >10/hour: `priority: medium` (thrashing)

---

## Related Skills

- `performanceOptimizer`: Optimize with profiler data
- `costIntelligence`: Monitor cost impact
- `costDashboard`: Visualize scaling decisions
