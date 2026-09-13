# regionFailoverManager

**Version**: 1.0.0 | **Status**: Production | **Phase**: 19 | **Category**: Operations

## Description

Automatic region failover management with health monitoring for multi-region deployments. Continuously monitors regional health, detects failures, and coordinates automatic failover to healthy regions. Supports multiple failover plans with priority-based execution.

## Overview

Automatic region failover management with health monitoring. Continuously monitors regional health, detects failures, and coordinates automatic failover to healthy regions. Supports multiple failover plans with priority-based execution. <100ms failover detection.

## Quick Start

```python
from skills.regionFailoverManager import RegionFailoverManager

manager = RegionFailoverManager(config={
    "health_check_interval_seconds": 30,
    "failover_threshold_errors": 10,
})

await manager.initialize()

# Monitor region
status = await manager.execute(
    operation="monitor_region",
    region_id="us-east-1"
)

# Detect failures
detected = await manager.execute(
    operation="detect_failure",
    region_id="us-east-1",
    error_count=15  # >= threshold triggers failover
)

# Initiate failover
failover = await manager.execute(
    operation="initiate_failover",
    from_region="us-east-1",
    to_region="us-west-2"
)
```

## Configuration

```yaml
skills:
  regionFailoverManager:
    enabled: true
    health_check_interval_seconds: 30
    failover_threshold_errors: 10
    max_events: 1000
    failover_plans:
      - from: "us-east-1"
        to: "us-west-2"
        priority: 1
        duration: 60
      - from: "us-west-2"
        to: "eu-west-1"
        priority: 2
        duration: 120
```

## Operations

| Operation | Parameters | Returns | Latency |
|-----------|-----------|---------|---------|
| `monitor_region` | region_id | state, monitoring_active | <5ms |
| `detect_failure` | region_id, error_count | is_failed, state | <10ms |
| `initiate_failover` | from_region, to_region | failover_id, status | <20ms |
| `cancel_failover` | failover_id | status | <5ms |
| `get_failover_status` | region_id | state, is_failed, is_recovering | <2ms |
| `get_failover_plans` | from_region | plans, count | <5ms |
| `get_failover_history` | limit (optional) | failover_history, count | <10ms |
| `stats` | - | total_regions, failed_regions, failover_events | <5ms |

## Performance

- Failure detection: <100ms (configurable threshold)
- Failover initiation: <20ms
- Status check: <5ms
- History retrieval: <10ms

## Use Cases

1. **High availability**: Automatic failover when region fails
2. **Disaster recovery**: Coordinated multi-region recovery
3. **Maintenance**: Graceful failover during updates
4. **SLA compliance**: Minimize downtime with rapid failover
5. **Cost optimization**: Failover to cheaper regions

## Monitoring

```python
# Get failover statistics
stats = await manager.execute(operation="stats")
# {
#   "total_regions_monitored": 4,
#   "failed_regions": 1,
#   "failover_plans_available": 3,
#   "total_failover_events": 5,
# }
```

## Testing

```bash
pytest tests/test_phase19_week1_geo.py::TestRegionFailoverManager -v
```

## Integrations

- Works with `geoRouterExtended` for coordinated routing
- Works with `dataLocalityOptimizer` for replication during failover
- Extends existing `TenantRouter` with failover awareness

## State Machine

```
HEALTHY → DEGRADED → FAILED → RECOVERING → HEALTHY
    ↓
monitor_region() checks continuously
detect_failure() triggers state transitions
initiate_failover() moves traffic
```

## Dependencies

- Python 3.9+
- asyncio
- BaseSkill (from skills.base)

## Troubleshooting

**Failover not executing**: Verify failover plans configured for the region pair.

**False failure detection**: Increase error threshold if temporary errors trigger failover.

**Slow recovery**: Check target region health and replication lag.

---

**Learn more**: See [regionFailoverManager/failover.py](failover.py) for implementation details.

## Usage
### Example 1: Detect and Handle Failover

```python
from skills.regionFailoverManager.skill import RegionFailoverManager

skill = RegionFailoverManager()

request = {
    "primaryRegion": "us-east",
    "secondaryRegions": ["us-west", "eu-west"],
    "failureConditions": ["latency > 1000", "errorRate > 0.1"]
}

failoverDecision = skill.handleFailover(request)

if failoverDecision['requiresFailover']:
    print(f"Failover to: {failoverDecision['targetRegion']}")
```

## API

### Class: RegionFailoverManager

```python
class RegionFailoverManager:
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
from regionFailoverManager.skill import RegionFailoverManager

skill = RegionFailoverManager()
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

skill = RegionFailoverManager(config=config)
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
| `ValueError` | No secondary regions defined | Provide at least one fallback region |
| `RuntimeError` | All regions unavailable | Implement circuit breaker |

## Related Skills

- **Upstream**: [To be documented]
- **Downstream**: [To be documented]
- **Alternative**: None
