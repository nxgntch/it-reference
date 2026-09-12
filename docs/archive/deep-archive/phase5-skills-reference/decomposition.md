# Decomposition Skill

**Break down complex tasks into independently executable subtasks with dependencies.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 18+ | Coverage: >85%

---

## Description

**Break down complex tasks into independently executable subtasks with dependencies.**

## Overview

The Decomposition skill is the **task planning engine** in nxgntch. It transforms large, complex goals into manageable subtasks with clear dependencies, effort estimates, and parallel execution opportunities.

**When to use**: Every complex task that needs to be broken into executable work units.  
**What it solves**: Eliminates paralysis from overwhelming tasks, identifies execution order, enables concurrent work on independent subtasks.  
**Key benefit**: Large goals become achievable through structured decomposition and dependency management.

---

## Key Features

- **Granularity Control**: Fine (detailed steps), moderate (balanced), or coarse (high-level phases)
- **Dependency Mapping**: Identify which subtasks must complete before others
- **Effort Estimation**: Per-subtask time/complexity estimates
- **Parallelization Identification**: Find independent subtasks for concurrent execution
- **Domain-Aware**: API/feature/infrastructure-specific decomposition patterns
- **Constraint Awareness**: Respect scope, deadline, and resource constraints
- **Decomposition Analysis**: Detailed breakdown of strategy and rationale

---

## Quick Start

Minimal example to decompose a complex task:

```python
from skills.decomposition import Decomposition

# Initialize the skill
skill = Decomposition()

# Execute on a task
result = await skill.execute({
    "goal": "Build and deploy user authentication system",
    "context": "Mobile app backend, OAuth2 integration",
    "preferredGranularity": "moderate",
    "constraints": {"maxDays": 10, "maxTeamSize": 2}
})

# Result contains subtask breakdown
print(result["output"])
# {
#     "subtasks": [
#         {"id": 1, "title": "Design auth schema", "effort": "4h", "dependencies": []},
#         {"id": 2, "title": "Implement OAuth2 provider", "effort": "8h", "dependencies": []},
#         {"id": 3, "title": "Integrate with app", "effort": "6h", "dependencies": [1, 2]},
#         {"id": 4, "title": "Write tests", "effort": "5h", "dependencies": [3]},
#         {"id": 5, "title": "Deploy to staging", "effort": "2h", "dependencies": [4]}
#     ],
#     "estimatedTotalEffort": "25h",
#     "parallelWorkAvailable": ["tasks 1&2 can run concurrently"],
#     "criticalPath": ["1 or 2", "3", "4", "5"]
# }
```

---

## Usage

### Basic Usage: Decompose Complex Goal

```python
# Example 1: Simple task decomposition
result = await skill.execute({
    "goal": "Add user registration feature",
    "context": "Web application, basic CRUD",
    "preferredGranularity": "moderate"
})

subtasks = result["output"]["subtasks"]
for task in subtasks:
    print(f"{task['id']}: {task['title']} ({task['effort']})")
```

### With Granularity Control: Fine-Grained Breakdown

```python
# Example 2: Detailed breakdown for complex feature
result = await skill.execute({
    "goal": "Optimize database query performance",
    "context": "Production database with 100M+ rows, high query latency",
    "preferredGranularity": "fine",  # More detailed steps
    "constraints": {
        "maxDays": 5,
        "scope": "read-only queries only"
    }
})

for task in result["output"]["subtasks"]:
    deps = f" (depends on: {task['dependencies']})" if task['dependencies'] else ""
    print(f"- {task['title']}: {task['effort']}{deps}")
```

### With Constraint Awareness: Deadline & Resource Limits

```python
# Example 3: Decompose with resource constraints
result = await skill.execute({
    "goal": "Migrate to new architecture",
    "context": "Major refactoring, high risk, critical system",
    "preferredGranularity": "coarse",  # High-level phases
    "constraints": {
        "maxDays": 14,
        "maxTeamSize": 3,
        "riskTolerance": "low",
        "downtime_allowed": False
    }
})

analysis = result["output"]
print(f"Total effort: {analysis['estimatedTotalEffort']}")
print(f"Parallel work: {analysis['parallelWorkAvailable']}")
print(f"Critical path: {' → '.join(analysis['criticalPath'])}")
```

### Error Handling: Impossible Constraints

```python
# Example 4: Handle infeasible decompositions
result = await skill.execute({
    "goal": "Complex feature",
    "constraints": {
        "maxDays": 1,  # Very tight deadline
        "maxTeamSize": 1  # Very small team
    }
})

output = result["output"]
if output.get("infeasible"):
    print("Constraints make task infeasible:")
    print(f"  Gap: {output.get('reason')}")
    print(f"  Realistic estimate: {output.get('realisticEffort')}")
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `goal` | string | Yes | Task objective to decompose (e.g., "Build payment integration") |
| `context` | string | No | Additional context (domain, constraints, history) |
| `preferredGranularity` | string | No | Level of detail: fine/moderate/coarse (default: moderate) |
| `constraints` | dict | No | Hard requirements (maxDays, maxTeamSize, riskTolerance, etc.) |
| `domainHint` | string | No | Domain category (api/feature/infrastructure/migration) |

**Input Example**:
```python
{
    "goal": "Implement real-time notifications system",
    "context": "Mobile app backend, 100k+ concurrent users, WebSocket support",
    "preferredGranularity": "moderate",
    "constraints": {
        "maxDays": 14,
        "maxTeamSize": 2,
        "riskTolerance": "low",
        "scope": "backend only"
    },
    "domainHint": "infrastructure"
}
```

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether decomposition succeeded |
| `data.subtasks` | list | Array of subtasks (id, title, effort, dependencies) |
| `data.estimatedTotalEffort` | string | Total time estimate (e.g., "25h") |
| `data.dependencies` | list | Task dependency pairs [dependent, dependency] |
| `data.criticalPath` | list | Ordered list of tasks on critical path |
| `data.parallelWorkAvailable` | list | Groups of independent tasks |
| `data.infeasible` | bool | True if constraints make goal impossible |
| `data.reason` | string | Why decomposition is infeasible (if applicable) |
| `metadata.latency_ms` | float | Processing time |

**Output Example**:
```python
{
    "success": True,
    "data": {
        "subtasks": [
            {"id": 1, "title": "Design WebSocket protocol", "effort": "6h", "complexity": "high", "dependencies": []},
            {"id": 2, "title": "Implement server-side logic", "effort": "12h", "complexity": "high", "dependencies": [1]},
            {"id": 3, "title": "Build client SDK", "effort": "8h", "complexity": "medium", "dependencies": [1]},
            {"id": 4, "title": "Write integration tests", "effort": "4h", "complexity": "medium", "dependencies": [2, 3]},
            {"id": 5, "title": "Load testing", "effort": "5h", "complexity": "medium", "dependencies": [4]},
            {"id": 6, "title": "Deploy to staging", "effort": "2h", "complexity": "low", "dependencies": [5]}
        ],
        "estimatedTotalEffort": "37h",
        "criticalPath": [1, 2, 4, 5, 6],
        "parallelWorkAvailable": ["tasks 2 and 3 can run concurrently after task 1"],
        "dependencies": [[2, 1], [3, 1], [4, 2], [4, 3], [5, 4], [6, 5]]
    },
    "metadata": {
        "latency_ms": 45.1,
        "granularity": "moderate",
        "subtask_count": 6
    }
}
```

---

## Configuration

Environment variables and configuration:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DECOMPOSITION_GRANULARITY_DEFAULT` | str | "moderate" | Default granularity (fine/moderate/coarse) |
| `DECOMPOSITION_TIMEOUT_SECONDS` | int | 10 | Decomposition evaluation timeout |
| `DECOMPOSITION_MIN_EFFORT` | str | "1h" | Minimum subtask effort before stopping |
| `DECOMPOSITION_COMPLEXITY_WEIGHTS` | dict | ... | Weights for complexity scoring |
| `DECOMPOSITION_CONSTRAINT_STRICTNESS` | str | "moderate" | How strictly to enforce constraints |

**Setting Configuration**:
```python
# Option 1: Via config dict
skill = Decomposition(config={
    "granularity_default": "fine",
    "timeout_seconds": 15,
    "min_effort": "30m",
    "constraint_strictness": "strict"
})

# Option 2: Via environment variables
import os
os.environ["DECOMPOSITION_GRANULARITY_DEFAULT"] = "fine"
os.environ["DECOMPOSITION_TIMEOUT_SECONDS"] = "15"
```

---

## Error Handling

### Infeasible Constraints

**Cause**: Deadline/resource constraints make task impossible  
**Indicator**: `infeasible: True` in response  
**Solution**: Relax constraints or extend deadline  
```python
result = await skill.execute({...})
if result["data"].get("infeasible"):
    print(f"Not feasible: {result['data']['reason']}")
    print(f"Realistic effort: {result['data']['realisticEffort']}")
```

### Ambiguous Goal

**Cause**: Goal description too vague for meaningful decomposition  
**Error**: Returns decomposition with flag `ambiguityLevel: high`  
**Solution**: Provide more context or clarify requirements  
```python
if result["data"].get("ambiguityLevel", "low") == "high":
    print("Goal ambiguous - provide more context:")
    print(result["data"].get("clarifyingQuestions", [])
```

### Timeout

**Cause**: Decomposition evaluation exceeded timeout  
**Error**: TimeoutError raised  
**Solution**: Increase DECOMPOSITION_TIMEOUT_SECONDS or simplify goal  
```python
try:
    result = await skill.execute({...}, timeout=30)
except TimeoutError:
    print("Decomposition timed out - goal may be too complex")
```

### Invalid Granularity

**Cause**: preferredGranularity not in [fine, moderate, coarse]  
**Error**: ValueError raised  
**Solution**: Use one of the three valid values  
```python
# Valid: fine, moderate, coarse
result = await skill.execute({
    "goal": "...",
    "preferredGranularity": "moderate"
})
```

---

## Testing

- **Unit Tests**: `tests/test_decomposition.py` (20+ comprehensive tests)
- **Coverage**: >85% of decomposition logic
- **Test Patterns**: Granularity control, dependency detection, constraint satisfaction

### Running Tests

```bash
# Run decomposition tests
pytest tests/test_decomposition.py -v

# Run with coverage
pytest tests/test_decomposition.py --cov=skills.decomposition --cov-report=term-missing

# Run specific test
pytest tests/test_decomposition.py::TestDecompositionGranularity::testFineGranularityProducesMoreTasks -v
```

### Test Coverage

- ✅ Fine/moderate/coarse granularity levels
- ✅ Dependency chain detection
- ✅ Critical path identification
- ✅ Parallel work identification
- ✅ Effort estimation accuracy
- ✅ Constraint satisfaction and violation detection
- ✅ Edge cases (single task, circular dependencies, infeasible goals)

---

## Dependencies

### Skills That Use This Skill

- **orchestrator** — Uses decomposition to break large tasks into agent-executable subtasks
- **routing** — Determines which agent handles each subtask

### Skills Used By This Skill

- **taskIntake** — Normalized tasks input to decomposition

### Related Skills

- **routing**: Downstream skill for subtask assignment
- **taskIntake**: Upstream task normalization

---

## Performance Characteristics

- **Latency (p50)**: ~30-40 ms
- **Latency (p95)**: <150 ms
- **Throughput**: 100+ decompositions/second (single instance)
- **Scalability**: Horizontal (stateless)
- **Complexity**: O(n*log(n)) where n = expected subtask count

---

## Troubleshooting

### Issue: Decomposition Too Fine-Grained

**Diagnosis**: Subtasks are too small (sub-hour tasks)  
**Solutions**:
1. Switch to "moderate" granularity (coarser breakdown)
2. Increase minimum effort threshold (DECOMPOSITION_MIN_EFFORT)
3. Combine related subtasks into larger chunks
4. Verify goal complexity justified fine level

### Issue: Missing Dependencies

**Diagnosis**: Subtasks have incorrect or incomplete dependencies  
**Solutions**:
1. Increase context detail (provide more information about goal)
2. Verify goal description is unambiguous
3. Manually review critical path
4. Add domain hint if not provided

### Issue: Unrealistic Effort Estimates

**Diagnosis**: Estimated effort doesn't match actual time  
**Solutions**:
1. Provide historical data or benchmarks
2. Adjust complexity weights in config
3. Add more context about team experience
4. Break into finer granularity for more accuracy

### Issue: Constraints Infeasible

**Diagnosis**: Constraints make goal impossible  
**Solutions**:
1. Increase deadline
2. Increase team size
3. Reduce scope
4. Lower risk tolerance to allow simpler approach

---

## Changelog

### Version 1.0.0 (Phase 18+)
- ✅ Core task decomposition engine
- ✅ Multi-granularity support (fine/moderate/coarse)
- ✅ Dependency detection and critical path analysis
- ✅ Parallelization identification
- ✅ Effort estimation
- ✅ Constraint satisfaction checking
- ✅ >85% test coverage

---

## Related Documentation

- **Skill Dependencies**: See `skills/DEPENDENCIES.md` for full skill graph
- **Configuration**: See `config/skills.yaml` for skill registry
- **Unified Template**: See `skills/SKILL_TEMPLATE_UNIFIED.md` for documentation format
- **Integration**: See `skills/routing/SKILL.md` (downstream consumer)
