# Routing Skill

**Match tasks to optimal agents based on capabilities, cost, and constraints.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 18+ | Coverage: >85%

---

## Description

**Match tasks to optimal agents based on capabilities, cost, and constraints.**

## Overview

The Routing skill is the **agent matcher and task dispatcher** in nxgntch. It analyzes task requirements and available agents to recommend the best-fit agent for execution based on capabilities, cost, speed, and reliability constraints.

**When to use**: Every task that needs assignment to an optimal agent or team.  
**What it solves**: Eliminates guessing about which agent can best handle a task, ensures cost-effective assignment, respects capacity constraints.  
**Key benefit**: Tasks reach optimal agents quickly, reducing delays and ensuring cost-efficient execution.

---

## Key Features

- **Multi-Criteria Scoring**: Evaluate agents across capabilities, cost, speed, and reliability
- **Constraint Satisfaction**: Enforce hard requirements (budget, deadline, team availability)
- **Alternative Routing**: Generate ranked alternatives if primary route unavailable
- **Cost Awareness**: Consider team cost tiers and budget constraints in routing
- **Confidence Scoring**: Express confidence in routing recommendation (0-100%)
- **Capability Matching**: Match task requirements to agent specializations
- **Preference Weighting**: Balance cost vs. speed vs. reliability based on task priorities

---

## Quick Start

Minimal example to route a task to an optimal agent:

```python
from skills.routing import Routing

# Initialize the skill
skill = Routing()

# Execute on a task
result = await skill.execute({
    "taskGoal": "Implement user authentication",
    "requiredCapabilities": ["backend", "security"],
    "availableAgents": ["team_engineering", "team_research", "team_data"],
    "preferenceWeights": {"cost": 0.3, "speed": 0.5, "reliability": 0.2}
})

# Result contains routing recommendation
print(result["output"])
# {
#     "recommendedAgent": "team_engineering",
#     "confidence": 0.94,
#     "estimatedCost": 250.0,
#     "alternatives": ["team_research", "team_data"],
#     "reasoning": "team_engineering best matches backend+security requirements"
# }
```

---

## Usage

### Basic Usage: Route Task to Best Team

```python
# Example 1: Route with basic parameters
result = await skill.execute({
    "taskGoal": "Build REST API for user management",
    "requiredCapabilities": ["backend"],
    "availableAgents": ["team_engineering", "team_data"],
})

selectedAgent = result["output"]["recommendedAgent"]
cost = result["output"]["estimatedCost"]
print(f"Route to: {selectedAgent} (est. cost: ${cost:.2f})")
```

### With Constraints: Hard Requirements

```python
# Example 2: Route with budget and deadline constraints
result = await skill.execute({
    "taskGoal": "Optimize database queries",
    "requiredCapabilities": ["database", "performance"],
    "availableAgents": ["team_engineering", "team_infrastructure"],
    "constraints": {
        "maxCost": 500.0,
        "maxDays": 3,
        "mustHaveTeam": "team_engineering"
    }
})

route = result["output"]
print(f"Recommendation: {route['recommendedAgent']}")
if route.get("constraintViolation"):
    print(f"Warning: Violates {route['constraintViolation']}")
```

### Advanced: Preference Weighting and Alternatives

```python
# Example 3: Route with weighted preferences and alternatives
result = await skill.execute({
    "taskGoal": "Deploy to production",
    "requiredCapabilities": ["devops", "deployment"],
    "availableAgents": ["team_infrastructure", "team_engineering", "team_research"],
    "preferenceWeights": {
        "cost": 0.2,
        "speed": 0.5,
        "reliability": 0.3
    },
    "context": {
        "urgency": "high",
        "riskTolerance": "low"
    }
})

route = result["output"]
print(f"Primary: {route['recommendedAgent']} (confidence: {route['confidence']:.0%})")
print("Alternatives:")
for alt in route.get("alternatives", []):
    print(f"  - {alt['agent']} (cost: ${alt['cost']:.2f})")
```

### Error Handling: No Suitable Agent

```python
# Example 4: Handle edge cases
result = await skill.execute({
    "taskGoal": "Requires uncommon specialty skill",
    "requiredCapabilities": ["obscure_skill"],
    "availableAgents": ["team_a", "team_b"],
})

output = result["output"]
if output.get("confidence", 0) < 0.7:
    print("Low confidence routing:")
    print(f"  Reason: {output.get('reasoning')}")
    print(f"  Alternatives available: {len(output.get('alternatives', []))}")
elif output.get("noSuitableAgent"):
    print("No agent can satisfy requirements")
    print(f"  Gap: {output.get('missingCapabilities')}")
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskGoal` | string | Yes | Description of task objective |
| `requiredCapabilities` | list[string] | Yes | Agent specializations needed (e.g., ["backend", "security"]) |
| `availableAgents` | list[string] | Yes | Team or agent IDs to consider |
| `preferenceWeights` | dict | No | Weight preferences {"cost": 0.3, "speed": 0.5, "reliability": 0.2} |
| `constraints` | dict | No | Hard requirements (maxCost, maxDays, mustHaveTeam) |
| `context` | dict | No | Additional context (urgency, risk tolerance, etc.) |

**Input Example**:
```python
{
    "taskGoal": "Build REST API",
    "requiredCapabilities": ["backend", "api_design"],
    "availableAgents": ["team_engineering", "team_research"],
    "preferenceWeights": {
        "cost": 0.3,
        "speed": 0.4,
        "reliability": 0.3
    },
    "constraints": {
        "maxCost": 1000.0,
        "maxDays": 7
    },
    "context": {
        "urgency": "medium",
        "riskTolerance": "moderate"
    }
}
```

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether routing succeeded |
| `data.recommendedAgent` | string | Best-fit agent ID |
| `data.confidence` | float | Confidence in recommendation (0-1) |
| `data.estimatedCost` | float | Estimated cost for task |
| `data.scores` | dict | Score per agent (for comparison) |
| `data.alternatives` | list | Alternative agents ranked |
| `data.reasoning` | string | Explanation of routing choice |
| `data.noSuitableAgent` | bool | No agent met requirements |
| `data.missingCapabilities` | list | Capabilities no agent has |
| `data.constraintViolation` | string | Which constraint was violated |
| `metadata.latency_ms` | float | Processing time |

**Output Example**:
```python
{
    "success": True,
    "data": {
        "recommendedAgent": "team_engineering",
        "confidence": 0.93,
        "estimatedCost": 350.0,
        "scores": {
            "team_engineering": 9.3,
            "team_research": 7.1,
            "team_data": 6.8
        },
        "alternatives": [
            {"agent": "team_research", "cost": 400.0, "score": 7.1},
            {"agent": "team_data", "cost": 420.0, "score": 6.8}
        ],
        "reasoning": "team_engineering has best backend+API expertise match and acceptable cost"
    },
    "metadata": {
        "latency_ms": 35.2,
        "agents_evaluated": 3
    }
}
```

---

## Configuration

Environment variables and configuration:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `ROUTING_SCORING_METHOD` | str | "weighted" | Scoring algorithm (weighted/ranking/ml) |
| `ROUTING_CONFIDENCE_THRESHOLD` | float | 0.7 | Minimum confidence for recommendation |
| `ROUTING_TIMEOUT_SECONDS` | int | 5 | Routing evaluation timeout |
| `ROUTING_COST_WEIGHT` | float | 0.3 | Default weight for cost factor |
| `ROUTING_SPEED_WEIGHT` | float | 0.4 | Default weight for speed factor |
| `ROUTING_RELIABILITY_WEIGHT` | float | 0.3 | Default weight for reliability factor |

**Setting Configuration**:
```python
# Option 1: Via config dict
skill = Routing(config={
    "scoring_method": "weighted",
    "confidence_threshold": 0.8,
    "timeout_seconds": 10,
    "cost_weight": 0.2,
    "speed_weight": 0.5,
    "reliability_weight": 0.3
})

# Option 2: Via environment variables
import os
os.environ["ROUTING_CONFIDENCE_THRESHOLD"] = "0.8"
os.environ["ROUTING_TIMEOUT_SECONDS"] = "10"
```

---

## Error Handling

### No Suitable Agent

**Cause**: No agent meets required capabilities  
**Indicator**: `noSuitableAgent: True` in response  
**Solution**: Add agents with required capabilities or relax requirements  
```python
result = await skill.execute({"requiredCapabilities": ["rare_skill"], ...})
if result["data"].get("noSuitableAgent"):
    print(f"Missing: {result['data']['missingCapabilities']}")
```

### Constraint Violation

**Cause**: All suitable agents violate at least one constraint  
**Error**: Returns recommendation with flag `constraintViolation=constraint_name`  
**Solution**: Relax constraints or add budget/time/capacity  
```python
if result["data"].get("constraintViolation"):
    print(f"Violated: {result['data']['constraintViolation']}")
    print("Consider increasing deadline or budget")
```

### Low Confidence

**Cause**: Multiple agents score similarly  
**Indicator**: `confidence < 0.7` in response  
**Solution**: Provide more context or clarify requirements  
```python
if result["data"]["confidence"] < 0.7:
    print("Low confidence - consider:")
    print("1. More specific capability requirements")
    print("2. Additional context about task priority")
```

### Timeout

**Cause**: Routing evaluation exceeded timeout threshold  
**Error**: TimeoutError raised  
**Solution**: Increase ROUTING_TIMEOUT_SECONDS or reduce agent pool  
```python
try:
    result = await skill.execute({...}, timeout=30)
except TimeoutError:
    print("Routing evaluation timed out")
```

---

## Testing

- **Unit Tests**: `tests/test_routing.py` (9+ comprehensive tests)
- **Coverage**: >85% of routing logic
- **Test Patterns**: Agent scoring, constraint checking, alternative generation

### Running Tests

```bash
# Run routing tests
pytest tests/test_routing.py -v

# Run with coverage
pytest tests/test_routing.py --cov=skills.routing --cov-report=term-missing

# Run specific test
pytest tests/test_routing.py::TestRoutingScoring::testScoresAgentsCorrectly -v
```

### Test Coverage

- ✅ Multi-criteria agent scoring
- ✅ Constraint satisfaction and violation detection
- ✅ Alternative agent ranking
- ✅ Confidence calculation
- ✅ Cost estimation accuracy
- ✅ Edge cases (no agents, no capabilities match)

---

## Dependencies

### Skills That Use This Skill

- **orchestrator** — Uses routing to assign tasks to agents
- **taskIntake** — Output fed to routing for agent assignment

### Skills Used By This Skill

- None (standalone routing engine)

### Related Skills

- **decisionMaking**: Parallel evaluation of agent options
- **taskIntake**: Upstream task normalization

---

## Performance Characteristics

- **Latency (p50)**: ~20-30 ms
- **Latency (p95)**: <100 ms
- **Throughput**: 150+ routings/second (single instance)
- **Scalability**: Horizontal (stateless)
- **Complexity**: O(n*m) where n = agents, m = criteria

---

## Troubleshooting

### Issue: Wrong Agent Recommended

**Diagnosis**: Routing selects unexpected agent  
**Solutions**:
1. Review preference weights (may need rebalancing)
2. Check agent capability definitions (may be incomplete)
3. Verify constraints allow preferred agent
4. Provide more specific task context

### Issue: Low Confidence Consistently

**Diagnosis**: Confidence score < 0.7 on valid routings  
**Solutions**:
1. Increase scoring variance (agents too similar)
2. Add more distinguishing criteria
3. Clarify agent specializations
4. Adjust ROUTING_CONFIDENCE_THRESHOLD if too strict

### Issue: Always Picks Same Agent

**Diagnosis**: All tasks route to single agent regardless of needs  
**Solutions**:
1. Verify other agents are in availableAgents list
2. Check capability matching (agents may lack variety)
3. Review cost weights (may favor one agent)
4. Ensure scoring reflects true differences

---

## Changelog

### Version 1.0.0 (Phase 18+)
- ✅ Core agent routing and matching
- ✅ Multi-criteria scoring engine
- ✅ Constraint satisfaction checking
- ✅ Alternative ranking
- ✅ Confidence calculation
- ✅ Cost-aware routing
- ✅ >85% test coverage

---

## Related Documentation

- **Skill Dependencies**: See `skills/DEPENDENCIES.md` for full skill graph
- **Configuration**: See `config/skills.yaml` for skill registry
- **Unified Template**: See `skills/SKILL_TEMPLATE_UNIFIED.md` for documentation format
- **Integration**: See `skills/taskIntake/SKILL.md` (upstream consumer)
