# Health Monitoring

Check system health status before routing high-priority tasks. Provides health context and routing safety recommendations.

## Agent
- **Primary Agent**: director
- **Cost Tier**: quick

## Capabilities
- System health checking
- Service status monitoring
- Routing impact assessment
- Health-aware recommendations

## Description
Proactive health monitoring skill that enables the Director agent to assess system health before making critical routing decisions. Provides health context and recommendations for safe task routing based on current service availability.

## Input
- No specific input required (queries current system health)
- Optional: Routing parameters or task requirements for health-aware assessment

## Output
- System health status
- Service status summary
- Recommendations for task routing
- Impact assessment (health status vs task requirements)

## Usage

### Basic Usage

```python
from app.skills.healthMonitoring import HealthMonitoring

skill = HealthMonitoring()
result = await skill.execute({})

print(result)
# Output: {"status": "healthy", "services": [...], "recommendations": [...]}
```

### Check Health Before Routing

```python
# Check system health for a specific task
result = await skill.execute({
    "task_type": "analytics_processing",
    "required_services": ["database", "cache", "api_gateway"],
    "priority": "high"
})

# Returns health assessment and routing recommendations
```

### Detailed Health Check

```python
# Get detailed health status with service-level info
result = await skill.execute({
    "include_service_details": True,
    "include_metrics": True,
    "check_dependencies": True
})

# Returns comprehensive health status for all services
```

## Configuration

Health Monitoring is configured through `config/skills.yaml`:

```yaml
healthMonitoring:
  enabled: true
  health_check_interval: 30
  cache_enabled: true
  cache_ttl_seconds: 300
  include_service_details: false
  include_metrics: false
```

**Configuration Parameters**:
- `enabled`: Enable health monitoring (default: true)
- `health_check_interval`: Health check frequency in seconds (default: 30)
- `cache_enabled`: Cache health check results (default: true)
- `cache_ttl_seconds`: Cache time-to-live in seconds (default: 300)
- `include_service_details`: Include per-service details by default (default: false)
- `include_metrics`: Include health metrics by default (default: false)

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task_type` | str | No | Type of task to assess health for |
| `required_services` | list | No | List of services required for the task |
| `priority` | str | No | Task priority: low, medium, high, critical |
| `include_service_details` | bool | No | Include per-service health details (default: false) |
| `include_metrics` | bool | No | Include health metrics (default: false) |
| `check_dependencies` | bool | No | Check service dependencies (default: false) |

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `status` | str | Overall system health: healthy, degraded, critical |
| `services` | list | Service health status details |
| `recommendations` | list | Routing recommendations based on health |
| `safe_to_route` | bool | Whether system is safe for task routing |
| `unhealth_services` | list | Services currently experiencing issues |
| `estimated_recovery_time` | str | ETA for unhealthy services to recover |

Example output:
```python
{
    "status": "degraded",
    "services": [
        {"name": "database", "status": "healthy", "latency_ms": 45},
        {"name": "cache", "status": "healthy", "latency_ms": 2},
        {"name": "api_gateway", "status": "degraded", "error_rate": 0.05},
        {"name": "ml_inference", "status": "healthy", "load": 0.75}
    ],
    "recommendations": [
        "System degraded - route only critical tasks",
        "Avoid ML-intensive tasks until API gateway recovers",
        "Database performing well - safe for data operations"
    ],
    "safe_to_route": True,
    "unhealthy_services": ["api_gateway"],
    "estimated_recovery_time": "5 minutes"
}
```

---

## Usage
Used by the Director agent during task intake and routing decisions to ensure tasks are routed only when system health permits.
