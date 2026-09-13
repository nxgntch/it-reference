# Decision Making Skill

**Evaluate options and recommend the best choice based on criteria, constraints, and context.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 18+ | Coverage: >85%

---

## Description

**Evaluate options and recommend the best choice based on criteria, constraints, and context.**

## Overview

The Decision Making skill is the **agent's judgment layer**. When facing multiple options (routes, strategies, priorities), this skill evaluates them against criteria, weights, and constraints, then recommends the best choice with transparent reasoning.

**When to use**: Every agent decision point where multiple valid paths exist (team selection, strategy choice, resource allocation, priority ranking).  
**What it solves**: Eliminates arbitrary choice-making, ensures consistent decision logic, provides explainable recommendations.  
**Key benefit**: Transparent, defensible decisions that can be audited and improved.

---

## Key Features

- **Multi-Option Evaluation**: Compare 2+ options against weighted criteria
- **Transparent Scoring**: Detailed scoring breakdown showing how each criterion contributed
- **Tradeoff Analysis**: Explicit documentation of pros/cons of each option
- **Constraint Checking**: Validate options against hard constraints (budget, latency, etc.)
- **Confidence Scoring**: Express confidence in recommendation (0-100%)
- **Explainability**: All recommendations include reasoning and weights used

---

## Quick Start

Minimal example to make a decision:

```python
from skills.decisionMaking import DecisionMaking

# Initialize the skill
skill = DecisionMaking()

# Execute on decision scenario
result = await skill.execute({
    "options": ["team_a", "team_b", "team_c"],
    "criteria": {"expertise": 0.4, "availability": 0.3, "cost": 0.3},
    "constraints": {"max_cost": 1000, "min_expertise": 8},
    "context": "Need to assign complex ML optimization task"
})

# Result contains recommendation with reasoning
print(result["output"])
# {
#     "recommendation": "team_b",
#     "confidence": 0.92,
#     "scores": {"team_a": 7.8, "team_b": 8.6, "team_c": 7.2},
#     "tradeoffs": ["team_b slightly more expensive", "best expertise match"],
#     "reasoning": "Team B has highest expertise score (8.5/10) and fits budget constraint"
# }
```

---

## Usage

### Basic Usage: Simple Option Evaluation

```python
# Example 1: Choose routing strategy
result = await skill.execute({
    "options": ["direct_route", "parallel_route", "queued_route"],
    "criteria": {"latency": 0.5, "throughput": 0.3, "cost": 0.2},
})

recommendation = result["output"]["recommendation"]
confidence = result["output"]["confidence"]
print(f"Recommended: {recommendation} (confidence: {confidence:.0%})")
```

### With Constraints: Hard Requirements

```python
# Example 2: Team selection with hard constraints
result = await skill.execute({
    "options": ["team_engineering", "team_research", "team_data"],
    "criteria": {
        "domain_expertise": 0.4,
        "availability": 0.3,
        "team_cost": 0.3
    },
    "constraints": {
        "max_daily_cost": 500,
        "min_expertise_score": 7,
        "must_available_by": "2026-09-01"
    },
    "context": "Complex database optimization task"
})

choice = result["output"]["recommendation"]
tradeoffs = result["output"]["tradeoffs"]
```

### Advanced: Weighted Scoring with Context

```python
# Example 3: Complex decision with full context
result = await skill.execute({
    "options": ["option_aggressive", "option_balanced", "option_conservative"],
    "criteria": {
        "risk_tolerance": 0.3,
        "time_to_implement": 0.4,
        "team_readiness": 0.3
    },
    "weights_override": {
        "option_aggressive": 0.8,  # Boost this option
        "option_conservative": 0.6  # Reduce this option
    },
    "context": {
        "deadline_days": 3,
        "team_skills": ["ML", "distributed_systems"],
        "budget_remaining": 10000,
        "risk_appetite": "moderate"
    }
})

recommendation = result["output"]["recommendation"]
confidence = result["output"]["confidence"]
reasoning = result["output"]["reasoning"]
```

### Error Handling: Invalid Scenarios

```python
# Example 4: Handle edge cases gracefully
try:
    result = await skill.execute({
        "options": ["only_option"],  # Single option
        "criteria": {"relevance": 1.0}
    })
    
    if result["output"].get("all_options_equal"):
        print("All options equivalent, choosing first")
    else:
        print(f"Recommendation: {result['output']['recommendation']}")
        
except ValueError as e:
    print(f"Invalid input: {e}")
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `options` | list[str] | Yes | 2+ option names/IDs to evaluate |
| `criteria` | dict | Yes | Weighted criteria {"name": weight, ...} |
| `constraints` | dict | No | Hard requirements (must satisfy all) |
| `context` | str/dict | No | Additional context for decision |
| `weights_override` | dict | No | Per-option weight multipliers |

**Input Example**:
```python
{
    "options": ["team_a", "team_b", "team_c"],
    "criteria": {
        "expertise": 0.4,
        "availability": 0.3,
        "cost": 0.3
    },
    "constraints": {
        "max_cost": 1000,
        "min_expertise": 7
    },
    "context": "Complex ML task, tight deadline"
}
```

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether decision succeeded |
| `data.recommendation` | string | Recommended option |
| `data.confidence` | float | Confidence score (0-1) |
| `data.scores` | dict | Score per option |
| `data.tradeoffs` | list | Pros/cons of recommendation |
| `data.reasoning` | string | Explanation of choice |
| `data.all_options_equal` | bool | All scored equally (edge case) |
| `metadata.latency_ms` | float | Processing time |

**Output Example**:
```python
{
    "success": True,
    "data": {
        "recommendation": "team_b",
        "confidence": 0.92,
        "scores": {
            "team_a": 7.8,
            "team_b": 8.6,
            "team_c": 7.2
        },
        "tradeoffs": [
            "Team B slightly more expensive but best expertise",
            "Team C is cheaper but less experienced"
        ],
        "reasoning": "Team B scores highest (8.6/10) on weighted criteria while meeting all constraints"
    },
    "metadata": {
        "latency_ms": 25.3,
        "criteria_weights": {"expertise": 0.4, "availability": 0.3, "cost": 0.3}
    }
}
```

---

## Configuration

Environment variables and configuration:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `DECISION_CONFIDENCE_THRESHOLD` | float | 0.7 | Minimum confidence for recommendation |
| `DECISION_SCORING_METHOD` | str | "weighted" | Scoring algorithm (weighted/voting/ml) |
| `DECISION_TIMEOUT_SECONDS` | int | 5 | Decision evaluation timeout |
| `DECISION_EXPLAIN_THRESHOLD` | float | 0.05 | Min score diff to note in tradeoffs |

**Setting Configuration**:
```python
# Via config dict
skill = DecisionMaking(config={
    "confidence_threshold": 0.8,
    "scoring_method": "weighted",
    "timeout_seconds": 10
})

# Via environment variables
import os
os.environ["DECISION_CONFIDENCE_THRESHOLD"] = "0.8"
os.environ["DECISION_TIMEOUT_SECONDS"] = "10"
```

---

## Error Handling

### Ambiguous Decision (Multiple Top Scorers)

**Cause**: Multiple options score equally  
**Indicator**: `confidence < 0.7` in response  
**Solution**: Add more criteria or provide more context  
```python
result = await skill.execute({"options": [...], "criteria": {...}})
if result["data"]["confidence"] < 0.7:
    print(f"Low confidence, consider additional criteria")
```

### Constraint Violation

**Cause**: All options violate at least one constraint  
**Error**: Returns recommendation with flag `violates_constraints=True`  
**Solution**: Relax constraints or add more options  
```python
if result["data"].get("violates_constraints"):
    print("All options violate constraints. Relax constraints or add options.")
```

### Missing Required Input

**Cause**: `options` or `criteria` not provided  
**Error**: ValueError raised  
**Solution**: Ensure both options list and criteria dict are provided  
```python
try:
    result = await skill.execute({"criteria": {...}})  # Missing options
except ValueError as e:
    print(f"Invalid input: {e}")
```

### Timeout

**Cause**: Decision evaluation exceeded timeout  
**Error**: TimeoutError raised  
**Solution**: Increase DECISION_TIMEOUT_SECONDS or reduce options/criteria  
```python
try:
    result = await skill.execute({...}, timeout=30)
except TimeoutError:
    print("Decision evaluation timed out, try simpler scenario")
```

---

## Testing

- **Unit Tests**: `tests/test_decisionMaking.py` (8+ comprehensive tests)
- **Coverage**: >85% of skill logic
- **Test Patterns**: Option evaluation, constraint checking, scoring accuracy

### Running Tests

```bash
# Run decision making tests
pytest tests/test_decisionMaking.py -v

# Run with coverage
pytest tests/test_decisionMaking.py --cov=skills.decisionMaking --cov-report=term-missing

# Run specific test
pytest tests/test_decisionMaking.py::TestDecisionMakingScoring::testScoresOptionsCorrectly -v
```

### Test Coverage

- ✅ Basic option evaluation and scoring
- ✅ Weighted criteria application
- ✅ Constraint checking and enforcement
- ✅ Confidence calculation
- ✅ Tradeoff identification
- ✅ Edge cases (equal scores, constraint violations)

---

## Dependencies

### Skills That Use This Skill

- **routing** — Uses decisions for path selection
- **decisionMaking** (itself) — Core agent decision capability

### Skills Used By This Skill

- None (standalone evaluation)

### Related Skills

- **routing**: Downstream consumer of decisions
- **taskIntake**: Provides context for decisions

---

## Performance Characteristics

- **Latency (p50)**: ~15-25 ms
- **Latency (p95)**: <100 ms
- **Throughput**: 200+ decisions/second (single instance)
- **Scalability**: Horizontal (stateless)
- **Complexity**: O(n) where n = number of options × number of criteria

---

## Troubleshooting

### Issue: Low Confidence in Recommendations

**Diagnosis**: Confidence score < 0.7  
**Solutions**:
1. Add more distinguishing criteria
2. Provide better context to differentiate options
3. Review weights (may be too balanced)
4. Check if options are truly different

### Issue: Wrong Option Recommended

**Diagnosis**: Recommendation doesn't match expected choice  
**Solutions**:
1. Review criteria weights (adjust relative importance)
2. Add constraints to eliminate bad options
3. Check option scoring logic (may need tuning)
4. Provide more detailed context

### Issue: Constraint Violations

**Diagnosis**: Recommended option violates constraints  
**Solutions**:
1. Verify constraints are correct
2. Relax overly strict constraints
3. Add more options that meet constraints
4. Re-evaluate constraint priorities

---

## Changelog

### Version 1.0.0 (Phase 18+)
- ✅ Core decision evaluation engine
- ✅ Multi-option scoring
- ✅ Constraint checking
- ✅ Confidence calculation
- ✅ Transparent reasoning
- ✅ >85% test coverage

---

## Related Documentation

- **Skill Dependencies**: See `skills/DEPENDENCIES.md` for full skill graph
- **Configuration**: See `config/skills.yaml` for skill registry
- **Unified Template**: See `skills/SKILL_TEMPLATE_UNIFIED.md` for documentation format
- **Integration**: See `skills/routing/SKILL.md` (downstream consumer)
