# dataLocalityOptimizer

**Version**: 1.0.0 | **Status**: Production | **Phase**: 19 | **Category**: Infrastructure

## Description

**Version**: 1.0.0 | **Status**: Production | **Phase**: 19 | **Category**: Infrastructure

## Overview

Data locality optimization with multi-region replication. Manages data replication policies, monitors replication lag, and optimizes data placement based on access patterns. Supports read replicas and consistency level management.

## Quick Start

```python
from skills.dataLocalityOptimizer import DataLocalityOptimizer

optimizer = DataLocalityOptimizer(config={
    "max_history": 1000,
})

await optimizer.initialize()

# Create data replica
replica = await optimizer.execute(
    operation="create_replica",
    data_id="dataset-1",
    primary_region="us-east-1",
    replica_regions=["us-west-2", "eu-west-1"]
)

# Check replication lag
lag = await optimizer.execute(
    operation="check_replica_lag",
    data_id="dataset-1"
)

# Optimize placement
optimal = await optimizer.execute(
    operation="optimize_placement",
    data_id="dataset-1",
    access_regions=["us-east-1", "us-west-2", "ap-southeast-1"]
)
```

## Configuration

```yaml
skills:
  dataLocalityOptimizer:
    enabled: true
    max_history: 1000
    replication:
      default_consistency: "eventual"
      max_lag_seconds: 30
```

## Operations

| Operation | Parameters | Returns | Latency |
|-----------|-----------|---------|---------|
| `create_replica` | data_id, primary_region, replica_regions | success, replication_lag_seconds | <5ms |
| `place_data` | data_id, size_mb, access_pattern | recommended_regions | <5ms |
| `check_replica_lag` | data_id | replication_lags_ms, max_lag_ms | <2ms |
| `sync_replica` | data_id, target_region | status, sync_time_ms | <10ms |
| `get_replicas` | data_id | primary_region, replica_regions | <2ms |
| `optimize_placement` | data_id, access_regions | primary_region, replica_regions | <10ms |
| `get_read_replicas` | data_id | read_replicas, replica_count | <2ms |
| `stats` | - | total_replicas, total_data_size_mb | <5ms |

## Performance

- Replica creation: <5ms
- Lag check: <2ms
- Sync operation: <10ms
- Placement optimization: <10ms
- Read replica retrieval: <2ms

## Use Cases

1. **Data locality**: Keep data close to users
2. **High availability**: Replicate across regions
3. **Disaster recovery**: Maintain replicas in safe locations
4. **Performance**: Reduce latency by local reads
5. **Compliance**: Regional data residency requirements

## Access Patterns

- `hot`: Frequently accessed, replicate to nearby regions (us-east-1, us-west-2)
- `warm`: Occasionally accessed, replicate globally (us-east-1, eu-west-1)
- `cold`: Rarely accessed, archive in cost-effective region (ap-southeast-1)

## Monitoring

```python
# Get replication statistics
stats = await optimizer.execute(operation="stats")
# {
#   "total_replicas": 5,
#   "total_data_size_mb": 1250.5,
#   "max_replication_lag_ms": 150,
#   "total_sync_events": 42,
# }

# Check specific replica lag
lag = await optimizer.execute(
    operation="check_replica_lag",
    data_id="dataset-1"
)
# {
#   "replication_lags_ms": {"us-west-2": 50, "eu-west-1": 120},
#   "max_lag_ms": 120,
#   "avg_lag_ms": 85
# }
```

## Testing

```bash
pytest tests/test_phase19_week1_geo.py::TestDataLocalityOptimizer -v
```

## Integrations

- Works with `geoRouterExtended` to co-locate data with routed requests
- Works with `regionFailoverManager` for replica failover coordination
- Extends existing multi-region architecture

## Consistency Models

- **Strong**: Data immediately consistent across all replicas (write-through)
- **Eventual**: Data eventually consistent, with bounded lag (async replication)

## Dependencies

- Python 3.9+
- asyncio
- BaseSkill (from skills.base)

## Troubleshooting

**High replication lag**: Check network connectivity and increase sync frequency.

**Out-of-sync replicas**: Run manual sync operation to catch up.

**Placement not optimizing**: Verify access regions are specified in optimize call.

---

**Learn more**: See [dataLocalityOptimizer/optimizer.py](optimizer.py) for implementation details.

## Usage
### Example 1: Optimize Data Locality

```python
from skills.dataLocalityOptimizer.skill import DataLocalityOptimizer

skill = DataLocalityOptimizer()

data = {
    "id": "dataset-123",
    "size": 1000,  # MB
    "accessPattern": "sequential",
    "regions": ["us-east", "eu-west"]
}

optimization = skill.optimizeLocality(data)
print(f"Replication plan: {optimization['replicationPlan']}")
```

## API

### Class: DataLocalityOptimizer

```python
class DataLocalityOptimizer:
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
from dataLocalityOptimizer.skill import DataLocalityOptimizer

skill = DataLocalityOptimizer()
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

skill = DataLocalityOptimizer(config=config)
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
| `ValueError` | Dataset not found | Verify dataset ID exists |
| `ValueError` | No regions available | Configure at least one region |

## Related Skills

- **Upstream**: [To be documented]
- **Downstream**: [To be documented]
- **Alternative**: None
