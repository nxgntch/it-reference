# Metrics Collector Skill

**Collect, aggregate, and export Prometheus-compatible operational metrics with dimensional filtering.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 18+ | Coverage: >85%

---

## Description

**Collect, aggregate, and export Prometheus-compatible operational metrics with dimensional filtering.**

## Overview

The Metrics Collector skill is the **operational metrics engine** in nxgntch. It collects performance data (latency, throughput, errors) from agents and services, aggregates metrics across dimensions (team, agent, operation), and exports summaries for monitoring and alerting.

**When to use**: When you need to track performance, identify bottlenecks, or generate operational dashboards.  
**What it solves**: Eliminates manual metric tracking, enables data-driven optimization, provides visibility into system behavior.  
**Key benefit**: Understand what's happening in your orchestration system with dimensional metrics and aggregations.

---

## Key Features

- **Emit Metrics**: Record performance measurements with labels
- **Query Metrics**: Retrieve metrics by name with dimensional filtering
- **Aggregate Metrics**: Calculate p50, p95, p99, min, max, sum, avg
- **Export Metrics**: Generate Prometheus-format summaries
- **TTL Management**: Automatic metric retention and cleanup
- **Dimensional Analysis**: Filter/group by team, agent, operation, status
- **Time Series Storage**: Ordered history with efficient retrieval

---

## Quick Start

Minimal example to collect and aggregate metrics:

```python
from skills.metricsCollector import MetricsCollector

# Initialize the skill
skill = MetricsCollector()

# Emit a metric
result = await skill.execute({
    "operation": "emit",
    "metric": {
        "name": "agent_latency",
        "value": 145.2,
        "timestamp": "2026-08-31T15:30:00Z",
        "labels": {"agent": "director", "team": "engineering", "status": "success"}
    }
})

# Query aggregated metrics
result = await skill.execute({
    "operation": "aggregate",
    "metricName": "agent_latency",
    "filters": {"team": "engineering"},
    "aggregations": ["p50", "p95", "p99", "avg"]
})

print(result["output"])
# {
#     "metricName": "agent_latency",
#     "p50": 142.0,
#     "p95": 256.3,
#     "p99": 512.7,
#     "avg": 148.5,
#     "count": 1250,
#     "pointCount": 1250
# }
```

---

## Usage

### Basic Usage: Emit and Query Metrics

```python
# Example 1: Record task execution metric
result = await skill.execute({
    "operation": "emit",
    "metric": {
        "name": "task_execution_time",
        "value": 2345.0,
        "labels": {"task_type": "data_processing", "result": "success"}
    }
})

# Query the metric back
result = await skill.execute({
    "operation": "query",
    "metricName": "task_execution_time",
    "filters": {"task_type": "data_processing"}
})

for point in result["output"]["points"]:
    print(f"{point['timestamp']}: {point['value']}ms")
```

### With Aggregation: Statistical Analysis

```python
# Example 2: Get performance percentiles
result = await skill.execute({
    "operation": "aggregate",
    "metricName": "request_latency",
    "filters": {"service": "api", "region": "us-east"},
    "aggregations": ["p50", "p95", "p99", "min", "max", "avg"],
    "timeWindow": "1h"
})

stats = result["output"]
print(f"Median latency: {stats['p50']}ms")
print(f"P95 latency: {stats['p95']}ms (99th percentile: {stats['p99']}ms)")
print(f"Slowest request: {stats['max']}ms, Fastest: {stats['min']}ms")
```

### Advanced: Multi-Dimensional Analysis

```python
# Example 3: Analyze by team and agent
result = await skill.execute({
    "operation": "aggregate",
    "metricName": "agent_cost",
    "groupBy": ["team", "agent"],
    "filters": {"status": "completed"},
    "aggregations": ["sum", "avg", "count"]
})

for group in result["output"]["groups"]:
    team, agent = group["dimensions"]["team"], group["dimensions"]["agent"]
    print(f"{team}/{agent}: Total cost ${group['sum']:.2f} ({group['count']} calls)")
```

### Error Handling: Invalid Queries

```python
# Example 4: Handle missing or invalid metrics
result = await skill.execute({
    "operation": "query",
    "metricName": "nonexistent_metric",
    "filters": {"team": "engineering"}
})

output = result["output"]
if output.get("noData"):
    print("No metrics found for query")
    print(f"Suggestion: Available metrics are {output.get('availableMetrics', [])}")
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `operation` | string | Yes | Operation: emit/query/aggregate/export/purge |
| `metric` | dict | No | Metric to emit (required for emit operation) |
| `metricName` | string | No | Metric name (required for query/aggregate) |
| `filters` | dict | No | Dimensional filters (label key/value pairs) |
| `aggregations` | list | No | Aggregation types: p50, p95, p99, min, max, avg, sum |
| `groupBy` | list | No | Dimensions to group by |
| `timeWindow` | string | No | Time window (e.g., "1h", "30m", "1d") |

**Input Example**:
```python
{
    "operation": "aggregate",
    "metricName": "orchestrator_invocation_time",
    "filters": {
        "team": "engineering",
        "status": "success"
    },
    "aggregations": ["p50", "p95", "avg", "count"],
    "groupBy": ["agent_type"],
    "timeWindow": "24h"
}
```

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether operation succeeded |
| `data.points` | list | Metric points (for query) |
| `data.p50/p95/p99` | float | Percentile values (for aggregate) |
| `data.min/max/avg/sum` | float | Statistical values |
| `data.count` | int | Number of data points |
| `data.groups` | list | Grouped results (if groupBy specified) |
| `metadata.latency_ms` | float | Operation latency |

**Output Example**:
```python
{
    "success": True,
    "data": {
        "metricName": "orchestrator_invocation_time",
        "p50": 185.0,
        "p95": 512.3,
        "p99": 1024.7,
        "min": 45.2,
        "max": 2048.1,
        "avg": 210.5,
        "count": 5430,
        "timeWindow": "24h"
    },
    "metadata": {
        "latency_ms": 52.3
    }
}
```

---

## Configuration

Environment variables and configuration:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `METRICS_MAX_RETENTION` | int | 2592000 | Max metric age in seconds (30 days) |
| `METRICS_AGGREGATION_WINDOW` | int | 60 | Window for aggregations in seconds |
| `METRICS_EXPORT_FORMAT` | str | "prometheus" | Export format (prometheus/json) |
| `METRICS_EMIT_BATCH_SIZE` | int | 100 | Batch size for metric writes |
| `METRICS_QUERY_TIMEOUT` | int | 30 | Query timeout in seconds |

**Setting Configuration**:
```python
# Option 1: Via config dict
skill = MetricsCollector(config={
    "max_retention": 2592000,
    "aggregation_window": 60,
    "export_format": "prometheus",
    "query_timeout": 30
})

# Option 2: Via environment variables
import os
os.environ["METRICS_MAX_RETENTION"] = "2592000"
os.environ["METRICS_EXPORT_FORMAT"] = "prometheus"
```

---

## Error Handling

### Invalid Metric Name

**Cause**: Requested metric doesn't exist  
**Indicator**: `noData: True` in response  
**Solution**: Use valid metric name or check available metrics  
```python
result = await skill.execute({"operation": "query", "metricName": "invalid"})
if result["data"].get("noData"):
    print(f"Available: {result['data']['availableMetrics']}")
```

### Invalid Time Window

**Cause**: Time window format incorrect  
**Error**: ValueError raised  
**Solution**: Use formats like "1h", "30m", "1d"  
```python
# Valid formats
result = await skill.execute({
    "operation": "query",
    "timeWindow": "1h"  # or "30m", "1d", "7d"
})
```

### Query Timeout

**Cause**: Metric query exceeded timeout  
**Error**: TimeoutError raised  
**Solution**: Reduce time window or increase `METRICS_QUERY_TIMEOUT`  
```python
try:
    result = await skill.execute({
        "operation": "aggregate",
        "timeWindow": "7d"  # May timeout for large windows
    })
except TimeoutError:
    # Retry with shorter window
    result = await skill.execute({"operation": "aggregate", "timeWindow": "1d"})
```

### Missing Labels

**Cause**: Metric emitted without required labels  
**Error**: Returns with flag `missingLabels: True`  
**Solution**: Emit with required labels (agent, team, status)  
```python
result = await skill.execute({
    "operation": "emit",
    "metric": {
        "name": "latency",
        "value": 100,
        "labels": {
            "agent": "director",      # Required
            "team": "engineering",    # Required
            "status": "success"       # Required
        }
    }
})
```

---

## Testing

- **Unit Tests**: `tests/test_metricsCollector.py` (12+ comprehensive tests)
- **Coverage**: >85% of metrics collection logic
- **Test Patterns**: Emit/query/aggregate operations, filtering, aggregation functions

### Running Tests

```bash
# Run metrics collector tests
pytest tests/test_metricsCollector.py -v

# Run with coverage
pytest tests/test_metricsCollector.py --cov=skills.metricsCollector --cov-report=term-missing

# Run specific test
pytest tests/test_metricsCollector.py::TestMetricsCollector::testAggregatesMetricsCorrectly -v
```

### Test Coverage

- ✅ Metric emission with labels
- ✅ Metric querying with filters
- ✅ Statistical aggregations (p50, p95, p99, avg, sum)
- ✅ Multi-dimensional grouping
- ✅ Time window filtering
- ✅ Metric retention and cleanup
- ✅ Export to Prometheus format
- ✅ Error handling and validation

---

## Dependencies

### Skills That Use This Skill

- **healthCheck** — Uses metrics for system health assessment
- **orchestrator** — Records metrics for invocations

### Skills Used By This Skill

- None (standalone metrics collection)

### Related Skills

- **healthCheck**: Uses metrics to assess system state
- **performanceTracing**: Records detailed operation metrics

---

## Performance Characteristics

- **Latency (p50)**: ~8-12 ms
- **Latency (p95)**: <50 ms
- **Throughput**: 1000+ metrics/second (single instance)
- **Scalability**: Horizontal (sharded by metric name)
- **Memory**: ~100 bytes overhead per metric point

---

## Troubleshooting

### Issue: No Metrics Collected

**Diagnosis**: Query returns no data  
**Solutions**:
1. Verify metrics are being emitted: Check emit calls
2. Verify filters match: Use same labels as emit
3. Check time window: Metrics may have expired
4. Enable debug logging: See verbose metric output

### Issue: Aggregation Slow

**Diagnosis**: Aggregate operation exceeds timeout  
**Solutions**:
1. Reduce time window (query 1h instead of 7d)
2. Add more specific filters (reduce data scanned)
3. Increase `METRICS_QUERY_TIMEOUT` if appropriate
4. Increase `METRICS_AGGREGATION_WINDOW` for coarser granularity

### Issue: High Memory Usage

**Diagnosis**: Metrics consuming excessive memory  
**Solutions**:
1. Reduce `METRICS_MAX_RETENTION` (keep fewer old metrics)
2. Purge old metrics: `emit purge operation`
3. Archive metrics to external storage
4. Reduce metric emission rate

### Issue: Missing Labels in Output

**Diagnosis**: Aggregated results missing expected dimensions  
**Solutions**:
1. Ensure all emitted metrics include labels
2. Verify groupBy dimensions match emitted labels
3. Check filter dimensions are correct
4. Review metric schema for required labels

---

## Changelog

### Version 1.0.0 (Phase 18+)
- ✅ Core metric collection engine
- ✅ Emit and query operations
- ✅ Statistical aggregations (p50, p95, p99, min, max, avg, sum)
- ✅ Multi-dimensional filtering and grouping
- ✅ Prometheus-format export
- ✅ TTL-based metric retention
- ✅ >85% test coverage

---

## Related Documentation

- **Skill Dependencies**: See `skills/DEPENDENCIES.md` for full skill graph
- **Configuration**: See `config/skills.yaml` for skill registry
- **Unified Template**: See `skills/SKILL_TEMPLATE_UNIFIED.md` for documentation format
- **Operations**: See `docs/guides/operations/COST_MANAGEMENT.md` for cost tracking patterns
