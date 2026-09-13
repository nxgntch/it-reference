# geoRouterExtended

**Version**: 1.0.0 | **Status**: Production | **Phase**: 19 | **Category**: Infrastructure

## Description

**Version**: 1.0.0 | **Status**: Production | **Phase**: 19 | **Category**: Infrastructure

## Overview

Multi-region routing with geographic failover. Routes requests to optimal region based on latency, health, and preferences. Supports automatic failover to healthy regions with <5ms routing decision latency.

## Quick Start

```python
from skills.geoRouterExtended import GeoRouterExtended

router = GeoRouterExtended(config={
    "primary_region": "us-east-1",
    "regions": {
        "us-east-1": {"latency_ms": 10, "error_rate": 0.0},
        "us-west-2": {"latency_ms": 50, "error_rate": 0.0},
        "eu-west-1": {"latency_ms": 80, "error_rate": 0.0},
    }
})

await router.initialize()

# Route request to optimal region
result = await router.execute(
    operation="route",
    request_id="req-001",
    tenant_id="tenant-1",
    preferences={"preferred_region": "us-east-1"}
)

# result: {
#   "success": true,
#   "target_region": "us-east-1",
#   "alternatives": ["us-west-2"],
#   "latency_estimate_ms": 10,
#   "routing_time_ms": 2.5
# }
```

## Configuration

```yaml
skills:
  geoRouterExtended:
    enabled: true
    primary_region: "us-east-1"
    health_check_interval_seconds: 30
    max_history: 1000
    regions:
      us-east-1:
        latency_ms: 10
        error_rate: 0.0
      us-west-2:
        latency_ms: 50
        error_rate: 0.0
      eu-west-1:
        latency_ms: 80
        error_rate: 0.0
```

## Operations

| Operation | Parameters | Returns | Latency |
|-----------|-----------|---------|---------|
| `route` | request_id, tenant_id, preferences | target_region, alternatives | <5ms |
| `route_with_failover` | request_id, tenant_id | primary_region, fallback_regions | <5ms |
| `check_region_health` | region_id | status, latency_ms, error_rate | <2ms |
| `get_region_metrics` | region_id | latency_ms, error_rate, is_healthy | <1ms |
| `update_metrics` | region_id, latency_ms, error_rate | success, is_healthy | <1ms |
| `failover` | from_region, to_region | new_active, failover_count | <5ms |
| `get_routing_history` | limit (optional) | routing_history, count | <10ms |
| `stats` | - | total_regions, healthy_regions, active_region | <5ms |

## Performance

- Routing decision latency: <5ms
- Region health check: <2ms
- Metrics update: <1ms
- Failover decision: <5ms

## Use Cases

1. **Multi-region deployment**: Route requests to geographically optimal region
2. **Disaster recovery**: Automatic failover when primary region fails
3. **Performance optimization**: Latency-aware routing for users
4. **Cost optimization**: Prefer cheaper regions when available
5. **Compliance**: Route data to region-specific servers

## Monitoring

```python
# Check router health
health = await router.health_check()
# {
#   "status": "ready",
#   "geo_router_stats": {
#     "total_regions": 4,
#     "healthy_regions": 4,
#     "routing_decisions": 1523
#   }
# }
```

## Testing

```bash
pytest tests/test_phase19_week1_geo.py::TestGeoRouterExtended -v
```

## Integrations

- Works with `regionFailoverManager` for coordinated failover
- Works with `dataLocalityOptimizer` for data replication
- Extends existing `TenantRouter` with geographic awareness

## Dependencies

- Python 3.9+
- asyncio
- BaseSkill (from skills.base)

## Troubleshooting

**All regions unhealthy**: Check regional health status and verify network connectivity.

**High routing latency**: Examine region metrics and consider reducing history size if memory is constrained.

**Failover not triggering**: Verify failover plans are configured and health check is running.

---

**Learn more**: See [geoRouterExtended/router.py](router.py) for implementation details.

## Usage
### Example
```python
routing = skill.routeToOptimalRegion(request, regions)
print(f'Region: {routing["region"]}')
```

## API

### Class: GeoRouterExtended

```python
class GeoRouterExtended:
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
from geoRouterExtended.skill import GeoRouterExtended

skill = GeoRouterExtended()
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

skill = GeoRouterExtended(config=config)
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
