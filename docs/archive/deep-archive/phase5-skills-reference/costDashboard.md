# Cost Dashboard Skill

**Real-time cost monitoring and visualization.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: Post-19

---

## Description

Real-time dashboard for cost visibility across teams, agents, and tasks. Tracks spending trends, budget status, anomalies, and optimization opportunities.

---

## Key Features

- **Team Dashboards**: Per-team spending overview
- **Budget Status**: Real-time budget utilization
- **Cost Trends**: Historical spending patterns
- **Anomaly Alerts**: Detect unusual spending
- **Agent Efficiency**: Cost per agent
- **Optimization Recommendations**: Top savings opportunities
- **Spending Breakdown**: By agent, model, task type

---

## Quick Start

```python
from skills.costDashboard.dashboard import CostDashboard

dashboard = CostDashboard()

# Get team dashboard
team_view = await dashboard.get_team_dashboard("engineering")
# {
#   "team_id": "engineering",
#   "monthly_cap": 1000.00,
#   "monthly_spent": 450.23,
#   "monthly_remaining": 549.77,
#   "budget_percentage": 45.0,
#   "daily_average": 15.01,
#   "trends": [...],
#   "alerts": [...]
# }

# Get cost anomalies
anomalies = await dashboard.get_anomalies("engineering")

# Get optimization opportunities
optimizations = await dashboard.get_top_optimizations()
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team_id` | string | Yes | Team identifier |
| `time_period` | string | No | Period (daily, weekly, monthly) |
| `include_forecast` | bool | No | Include spending forecast |
| `include_anomalies` | bool | No | Include anomaly detection |

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `team_id` | string | Team identifier |
| `monthly_cap` | float | Monthly budget cap |
| `monthly_spent` | float | Amount spent this month |
| `monthly_remaining` | float | Remaining budget |
| `budget_percentage` | float | Percentage of budget used |
| `daily_average` | float | Average daily spending |
| `trends` | array | Historical spending trends |
| `alerts` | array | Active alerts |
| `top_agents` | array | Most expensive agents |
| `optimizations` | array | Recommended optimizations |

---

## Features

### Real-time Updates
- Live spending tracking
- Instant budget status
- Alert notifications
- Trend visualization

### Analytics
- Spending by agent
- Spending by model
- Spending by task type
- Daily/weekly/monthly trends

### Alerts
- Budget threshold warnings
- Anomaly detection
- Cost spike alerts
- Forecast overages

### Optimization
- Model alternatives
- Batching opportunities
- Resource utilization
- Cost efficiency scores

---

## Testing

```bash
pytest tests/test_costDashboard.py -v
```

---

## Performance

- Latency: <100ms for dashboard load
- Updates: Real-time (1-second refresh)
- Scalability: 1000+ teams
- Data retention: 90 days

