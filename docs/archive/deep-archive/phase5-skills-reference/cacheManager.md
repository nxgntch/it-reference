# Cache Manager Skill

High-performance distributed caching with <1ms latency and automatic TTL management.

**Status**: ✅ Production Ready | **Coverage**: >85%

## Description

Distributed caching layer for nxgntch with in-memory LRU and optional Redis backend. Stores agent results, cost estimates, and configurations to eliminate redundant computation.

**Use Case**: Cache frequently accessed data (agent results, computations, configurations)  
**Benefit**: <1ms lookups reduce latency and costs for repeated operations

## Features

- **Sub-Millisecond Latency**: <1ms average Get operation
- **In-Memory LRU Cache**: Up to 10K items with automatic eviction
- **TTL Support**: Automatic expiration (5-minute default)
- **Redis Integration**: Optional distributed backend for horizontal scaling
- **Hit/Miss Tracking**: Monitor cache effectiveness
- **Batch Operations**: Set/Get multiple keys efficiently
- **Thread-Safe**: Concurrent access without data corruption

## Quick Start

```python
from skills.cacheManager import CacheManager

cache = CacheManager(config={"max_size": 10000, "default_ttl": 300})
await cache.initialize()

# Set value
await cache.execute({
    "operation": "set",
    "key": "agent:result:123",
    "value": {"status": "success"},
    "ttl": 3600
})

# Get value
result = await cache.execute({
    "operation": "get",
    "key": "agent:result:123"
})
```

## API Reference

### Operations

| Operation | Description | Parameters |
|-----------|-------------|------------|
| `set` | Store value with TTL | key, value, ttl (optional), distributed (optional) |
| `get` | Retrieve value | key, distributed (optional) |
| `batch_set` | Store multiple values | data (dict), ttl (optional) |
| `batch_get` | Retrieve multiple values | keys (list) |
| `delete` | Remove value | key |
| `clear` | Clear all values | none |
| `stats` | Get cache statistics | none |

### Response Format

All operations return:
```python
{
    "status": "success" | "error",
    "output": {
        "value": ...,           # For get operations
        "source": "cache" | "not_found",
        "hits": int,            # For stats
        "misses": int,
        "hitRatePercent": float,
        "itemCount": int
    }
}
```

## Configuration

Via `CacheManager` constructor:
- `max_size`: Maximum cached items (default: 10000)
- `default_ttl`: Default TTL in seconds (default: 300)
- `redis_url`: Redis connection string (optional)

## Performance Characteristics

- **Get Latency**: <1ms (in-memory), 1-5ms (Redis)
- **Set Latency**: <1ms (in-memory), 2-10ms (Redis)
- **Memory**: ~1KB per cached item (average)
- **Max Items**: 10K (in-memory), unlimited (Redis)

## Usage

### Basic Example

```python
from skills.cacheManager import CacheManager

# Initialize cache
cache = CacheManager(config={"max_size": 10000})
await cache.initialize()

# Cache agent results
result = await cache.execute({
    "operation": "set",
    "key": f"agent:{agentId}:result:{taskId}",
    "value": agentOutput,
    "ttl": 3600
})

# Retrieve cached result
cached = await cache.execute({
    "operation": "get",
    "key": f"agent:{agentId}:result:{taskId}"
})

if cached["output"]["source"] == "cache":
    print("Cache hit!")  # Use cached result
```

### Common Patterns

**Batch caching results**:
```python
results = {"task1": data1, "task2": data2}
await cache.execute({
    "operation": "batch_set",
    "data": {f"result:{k}": v for k, v in results.items()},
    "ttl": 1800
})
```

**Invalidate on state change**:
```python
await cache.execute({
    "operation": "delete",
    "key": f"agent:{agentId}:config"
})
```

## See Also

- [`cache.py`](./cache.py) — Implementation
- [`SKILL.md`](./SKILL.md) — This file
- [`tests/`](./tests/) — Test suite
