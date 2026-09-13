# Dashboard Consumer

Consult executive, operations, and metrics dashboards for context-aware decision making. Provides quick operational snapshots.

## Agent
- **Primary Agent**: director
- **Cost Tier**: quick

## Capabilities
- Dashboard querying
- Metrics retrieval
- Operational context
- Decision support

## Description
Operational intelligence skill that enables the Director agent to rapidly access executive, operations, and metrics dashboards for real-time context. Provides quick operational snapshots to inform routing and task allocation decisions.

## Input
- No specific input required (queries current dashboard state)
- Optional: Specific metrics or dashboard sections to query

## Output
- Dashboard snapshot with current metrics
- Key metrics summary (health, performance, cost)
- Alert summaries
- Operational context for decision making

## Usage

### Basic Usage

```python
from app.skills.dashboardConsumer import DashboardConsumer

skill = DashboardConsumer()
result = await skill.execute({
    "dashboard_type": "operations"
})

print(result)
# Output: {"metrics": {...}, "alerts": [...], "status": "healthy"}
```

### Query Specific Metrics

```python
# Get metrics dashboard with specific sections
result = await skill.execute({
    "dashboard_type": "metrics",
    "sections": ["system_health", "api_performance", "cost_summary"]
})

# Returns dashboard snapshot with requested sections
```

### Executive Dashboard

```python
# Get executive summary dashboard
result = await skill.execute({
    "dashboard_type": "executive",
    "include_alerts": True,
    "include_forecasts": True
})

# Returns executive dashboard with key metrics, alerts, and projections
```

---

## Configuration

Dashboard Consumer is configured through `config/skills.yaml`:

```yaml
dashboardConsumer:
  enabled: true
  dashboard_urls:
    executive: "http://dashboards/executive"
    operations: "http://dashboards/operations"
    metrics: "http://dashboards/metrics"
  update_frequency_seconds: 30
  cache_duration_seconds: 60
  include_alerts: true
  include_forecasts: false
  default_time_range: "24h"
```

**Configuration Parameters**:
- `dashboard_urls`: Base URLs for each dashboard type
- `update_frequency_seconds`: How often to refresh dashboard data
- `cache_duration_seconds`: Cache duration for dashboard snapshots
- `include_alerts`: Include alert summaries in output
- `include_forecasts`: Include trend forecasts in output
- `default_time_range`: Default time range for metrics (1h, 24h, 7d, 30d)

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dashboard_type` | str | Yes | Dashboard to query: executive, operations, metrics |
| `sections` | list | No | Specific sections to include (if not all) |
| `include_alerts` | bool | No | Include alert summary (default: true) |
| `include_forecasts` | bool | No | Include trend forecasts (default: false) |
| `time_range` | str | No | Time range for metrics: 1h, 24h, 7d, 30d |

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `dashboard_type` | str | Type of dashboard queried |
| `metrics` | dict | Key metrics by section |
| `alerts` | list | Active alerts and notifications |
| `status` | str | Overall system status: healthy, degraded, critical |
| `updated_at` | str | Timestamp of dashboard update |
| `forecasts` | dict | Optional trend forecasts |

Example output:
```python
{
    "dashboard_type": "operations",
    "metrics": {
        "system_health": {"uptime": 99.95, "services_healthy": 24, "services_down": 0},
        "api_performance": {"latency_p95": 125, "error_rate": 0.02},
        "cost_summary": {"used_today": 150, "projected_monthly": 4500}
    },
    "alerts": [
        {"level": "warning", "message": "API latency elevated (p95=150ms)"},
        {"level": "info", "message": "Daily cost on track"}
    ],
    "status": "healthy",
    "updated_at": "2026-08-31T14:23:45Z"
}
```

---

## Usage
Used by the Director agent to maintain situational awareness across system operations. Complements healthMonitoring (system availability) and costIntelligence (budget status) by providing holistic operational context.
