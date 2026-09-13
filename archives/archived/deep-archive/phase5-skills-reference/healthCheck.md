# Health Check Skill

**Kubernetes-compatible readiness and liveness probes for orchestration health monitoring.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 18+ | Coverage: >85%

---

## Description

**Kubernetes-compatible readiness and liveness probes for orchestration health monitoring.**

## Overview

The Health Check skill is the **system observability engine** in nxgntch. It provides Kubernetes-compatible health probes (readiness and liveness) that determine whether the orchestration system is healthy enough to serve traffic, and whether individual components are functioning correctly.

**When to use**: When deploying to Kubernetes, setting up monitoring, or detecting system degradation.  
**What it solves**: Eliminates guessing about system health, enables automated recovery (restarts), provides early warning of issues.  
**Key benefit**: Know instantly whether your orchestration system is ready and healthy.

---

## Key Features

- **Readiness Probe**: All components healthy → ready to handle requests
- **Liveness Probe**: Critical components healthy → service should stay alive
- **Component Monitoring**: Track 5+ core components (cache, database, API, LLM, queue)
- **Latency Tracking**: Monitor response times per component
- **Error Rate Monitoring**: Track error rates and failure modes
- **Status Inference**: Automatic health status based on thresholds
- **Detailed Reporting**: Component-level health breakdown

---

## Quick Start

Minimal example to check orchestration health:

```python
from skills.healthCheck import HealthCheck

# Initialize the skill
skill = HealthCheck()

# Check readiness for Kubernetes
result = await skill.execute({
    "operation": "readiness"
})

if result["output"]["status"] == "healthy":
    print("Ready to serve traffic")
else:
    print(f"Not ready: {result['output']['failingComponents']}")

# Check liveness to detect if restart needed
result = await skill.execute({
    "operation": "liveness"
})

if result["output"]["status"] == "unhealthy":
    print("Critical components failed - restart recommended")
```

---

## Usage

### Basic Usage: Readiness Probe

```python
# Example 1: Check if system ready for Kubernetes
result = await skill.execute({
    "operation": "readiness"
})

health = result["output"]
if health["status"] == "healthy":
    return 200, {"ready": True}  # Kubernetes will route traffic
else:
    return 503, {"ready": False}  # Kubernetes removes from load balancer
```

### With Component Details: Detailed Health

```python
# Example 2: Get detailed component status
result = await skill.execute({
    "operation": "detailed"
})

health = result["output"]
for component in health["components"]:
    print(f"{component['name']}: {component['status']} "
          f"(latency: {component['latency']}ms, "
          f"error rate: {component['errorRate']:.1%})")
```

### Liveness Probe: Monitor Critical Components

```python
# Example 3: Kubernetes liveness check
result = await skill.execute({
    "operation": "liveness"
})

health = result["output"]
if health["status"] == "unhealthy":
    # Kubernetes will restart pod
    return 503, {"alive": False, "reason": health.get("reason")}
else:
    return 200, {"alive": True}
```

### Error Handling: Component Failures

```python
# Example 4: Identify and recover from component failures
result = await skill.execute({
    "operation": "detailed"
})

health = result["output"]
failing = [c for c in health["components"] if c["status"] == "unhealthy"]

for component in failing:
    logger.error(f"Component down: {component['name']}")
    if component["name"] == "database":
        alerting.page_oncall("Database connectivity lost")
    elif component["name"] == "llm_api":
        # LLM API down - degrade to cached responses
        use_cache_fallback()
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | string | Yes | Operation: readiness/liveness/detailed/component |
| `component` | string | No | Specific component to check (if operation=component) |
| `timeout` | int | No | Max milliseconds to wait (default: 5000) |

**Input Example**:
```python
{
    "operation": "detailed",
    "timeout": 10000
}
```

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether health check succeeded |
| `data.status` | string | Overall status (healthy/degraded/unhealthy) |
| `data.components` | list | Component-level status details |
| `data.reason` | string | Description of unhealthy status |
| `data.failingComponents` | list | Names of unhealthy components |
| `metadata.latency_ms` | float | Check execution time |
| `metadata.checkTime` | string | Timestamp of check |

**Output Example**:
```python
{
    "success": True,
    "data": {
        "status": "degraded",
        "reason": "Cache component degraded (high latency)",
        "components": [
            {
                "name": "database",
                "status": "healthy",
                "latency": 12.5,
                "errorRate": 0.0
            },
            {
                "name": "cache",
                "status": "degraded",
                "latency": 850.0,
                "errorRate": 0.05
            },
            {
                "name": "llm_api",
                "status": "healthy",
                "latency": 245.0,
                "errorRate": 0.0
            },
            {
                "name": "queue",
                "status": "healthy",
                "latency": 5.0,
                "errorRate": 0.0
            }
        ],
        "failingComponents": ["cache"],
        "checkTime": "2026-08-31T15:30:00Z"
    },
    "metadata": {
        "latency_ms": 1250,
        "checkTime": "2026-08-31T15:30:00Z"
    }
}
```

---

## Configuration

Environment variables and configuration:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `HEALTH_READINESS_TIMEOUT` | int | 5000 | Readiness check timeout (ms) |
| `HEALTH_LIVENESS_TIMEOUT` | int | 10000 | Liveness check timeout (ms) |
| `HEALTH_LATENCY_THRESHOLD_WARNING` | int | 500 | Latency threshold for degraded status (ms) |
| `HEALTH_LATENCY_THRESHOLD_CRITICAL` | int | 2000 | Latency threshold for unhealthy status (ms) |
| `HEALTH_ERROR_RATE_WARNING` | float | 0.05 | Error rate for degraded (0.05 = 5%) |
| `HEALTH_ERROR_RATE_CRITICAL` | float | 0.10 | Error rate for unhealthy (0.10 = 10%) |

**Setting Configuration**:
```python
# Option 1: Via config dict
skill = HealthCheck(config={
    "readiness_timeout": 5000,
    "liveness_timeout": 10000,
    "latency_threshold_warning": 500,
    "latency_threshold_critical": 2000
})

# Option 2: Via environment variables
import os
os.environ["HEALTH_LATENCY_THRESHOLD_WARNING"] = "500"
os.environ["HEALTH_ERROR_RATE_WARNING"] = "0.05"
```

---

## Error Handling

### Check Timeout

**Cause**: Health check exceeded timeout  
**Error**: TimeoutError raised  
**Solution**: Increase timeout or investigate slow components  
```python
try:
    result = await skill.execute({"operation": "readiness", "timeout": 5000})
except TimeoutError:
    logger.error("Health check timeout - some components may be slow")
```

### Component Unreachable

**Cause**: Cannot connect to component for health check  
**Indicator**: Component status = "unreachable"  
**Solution**: Verify component is running, check connectivity  
```python
result = await skill.execute({"operation": "detailed"})
for component in result["output"]["components"]:
    if component["status"] == "unreachable":
        print(f"Cannot reach {component['name']} - investigate connectivity")
```

### Degraded Service

**Cause**: Components responding but with latency or errors  
**Indicator**: Overall status = "degraded"  
**Solution**: Investigate specific components, consider load reduction  
```python
if result["output"]["status"] == "degraded":
    failing = result["output"]["failingComponents"]
    logger.warning(f"Service degraded: {failing}")
```

### Critical Failure

**Cause**: Critical components (database, queue) unhealthy  
**Indicator**: Overall status = "unhealthy"  
**Solution**: Page on-call, investigate immediately  
```python
if result["output"]["status"] == "unhealthy":
    alerting.page_oncall(f"Critical failure: {result['output']['reason']}")
```

---

## Testing

- **Unit Tests**: `tests/test_healthCheck.py` (9+ comprehensive tests)
- **Coverage**: >85% of health check logic
- **Test Patterns**: Readiness/liveness probes, component monitoring, status inference

### Running Tests

```bash
# Run health check tests
pytest tests/test_healthCheck.py -v

# Run with coverage
pytest tests/test_healthCheck.py --cov=skills.healthCheck --cov-report=term-missing

# Run specific test
pytest tests/test_healthCheck.py::TestHealthCheck::testReadinessFailsWhenComponentUnhealthy -v
```

### Test Coverage

- ✅ Readiness probe (all components required)
- ✅ Liveness probe (critical components required)
- ✅ Detailed component checks
- ✅ Latency-based status inference
- ✅ Error rate-based status inference
- ✅ Timeout handling
- ✅ Component unreachability detection
- ✅ Kubernetes probe format compliance

---

## Dependencies

### Skills That Use This Skill

- **orchestrator** — Checks health before accepting new tasks
- **monitoring** — Uses health status for alerting

### Skills Used By This Skill

- **metricsCollector** — Reads component metrics for health status

### Related Skills

- **metricsCollector**: Provides component latency and error metrics

---

## Performance Characteristics

- **Latency (p50)**: ~50-100 ms (readiness), ~200-300 ms (detailed)
- **Latency (p95)**: <500 ms (readiness), <1000 ms (detailed)
- **Throughput**: 100+ checks/second (single instance)
- **Scalability**: Horizontal (independent checks)
- **Memory**: ~1 KB per check

---

## Troubleshooting

### Issue: False Positives (Healthy Shows as Degraded)

**Diagnosis**: Components responding but marked degraded  
**Solutions**:
1. Increase `HEALTH_LATENCY_THRESHOLD_WARNING` if thresholds too strict
2. Verify component is actually slow or has errors
3. Check for temporary network latency causing false warnings
4. Increase error rate thresholds if spikes expected

### Issue: False Negatives (Unhealthy Marked as Healthy)

**Diagnosis**: Component not responding but marked healthy  
**Solutions**:
1. Verify component check is implemented
2. Check component is actually reachable
3. Review component status inference logic
4. Manually test component connectivity

### Issue: Readiness Probe Never Succeeds

**Diagnosis**: Stuck in degraded or unhealthy state  
**Solutions**:
1. Check which components are failing: Use detailed probe
2. Restart failing components individually
3. Verify database and queue (critical components) are healthy
4. Review recent logs for errors in specific components

### Issue: Liveness Probe Too Sensitive

**Diagnosis**: Kubernetes keeps restarting pods  
**Solutions**:
1. Increase `HEALTH_LIVENESS_TIMEOUT` for slower components
2. Relax error rate thresholds for queue (temporary queue slowness)
3. Don't make liveness check as strict as readiness
4. Consider increasing pod restart backoff in Kubernetes

---

## Changelog

### Version 1.0.0 (Phase 18+)
- ✅ Readiness probe (all components required)
- ✅ Liveness probe (critical components required)
- ✅ Detailed component health reporting
- ✅ Latency and error rate monitoring
- ✅ Kubernetes probe format compliance
- ✅ Component-level status inference
- ✅ >85% test coverage

---

## Related Documentation

- **Skill Dependencies**: See `skills/DEPENDENCIES.md` for full skill graph
- **Configuration**: See `config/skills.yaml` for skill registry
- **Unified Template**: See `skills/SKILL_TEMPLATE_UNIFIED.md` for documentation format
- **Kubernetes Probes**: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
