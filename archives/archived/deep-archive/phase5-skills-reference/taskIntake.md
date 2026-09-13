# Task Intake Skill

**Normalize and structure unstructured task requests into executable work items.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 18+ | Coverage: >85%

---

## Description

**Normalize and structure unstructured task requests into executable work items.**

## Overview

The Task Intake skill is the **entry point for all work requests** in nxgntch. It transforms ambiguous, unstructured user requests (e.g., "optimize the database") into **structured, actionable tasks** with clear goals, constraints, success criteria, and team assignments.

**When to use**: Every user request that needs to become work for agents and teams.  
**What it solves**: Eliminates ambiguity, identifies constraints, determines responsible teams, and enables consistent downstream task processing.  
**Key benefit**: Structured tasks enable efficient routing, priority assignment, and execution planning.

---

## Key Features

- **Request Normalization**: Convert natural language requests into structured tasks
- **Constraint Extraction**: Identify and document latency, scope, and resource constraints
- **Team Identification**: Determine which teams (engineering, research, data, etc.) should handle the work
- **Clarity Assessment**: Rate request clarity on a scale (high/medium/low)
- **Ambiguity Detection**: Identify unclear requests and generate clarifying follow-up questions
- **Priority Inference**: Assign priority based on request characteristics and constraints
- **Success Criteria Definition**: Extract or generate success criteria for task completion

---

## Quick Start

Minimal example to normalize a task request:

```python
from skills.taskIntake import TaskIntake

# Initialize the skill
skill = TaskIntake()

# Execute on a user request
result = await skill.execute({
    "request": "Optimize the main database query performance",
    "context": {"user": "director", "team": "engineering"},
    "preferences": {"priority": "high"}
})

# Result contains structured task
print(result["output"])
# {
#     "goal": "Optimize main database query performance",
#     "constraints": {"max_latency_ms": 100, "max_lines": 50},
#     "required_teams": ["engineering"],
#     "priority": 1,
#     "success_criteria": ["Query latency < 100ms", "Maintain correctness"],
#     "clarity_level": "high",
#     "estimated_effort": "2-4 hours"
# }
```

---

## Usage

### Basic Usage: Simple Request

```python
# Example 1: Normalize a basic request
result = await skill.execute({
    "request": "Add user authentication to the API"
})

structured_task = result["output"]
print(f"Goal: {structured_task['goal']}")
print(f"Priority: {structured_task['priority']}")
print(f"Teams: {structured_task['required_teams']}")
```

### With Context: User and Team Information

```python
# Example 2: Provide context for better recommendations
result = await skill.execute({
    "request": "Reduce dashboard load time",
    "context": {
        "user": "product_manager",
        "current_team": "frontend",
        "available_teams": ["frontend", "data", "infrastructure"]
    }
})

task = result["output"]
# Response considers team capacity and specialization
```

### With Constraints: Define Boundaries

```python
# Example 3: Include known constraints
result = await skill.execute({
    "request": "Implement new reporting feature",
    "preferences": {
        "priority": "high",
        "max_effort_hours": 16,
        "deadline": "2026-09-07",
        "budget_limit": "$5000"
    }
})

task = result["output"]
print(f"Effort estimate: {task['estimated_effort']}")
print(f"Success criteria: {task['success_criteria']}")
```

### Error Handling: Ambiguous Requests

```python
# Example 4: Handle unclear requests
result = await skill.execute({
    "request": "Fix it"
})

task = result["output"]
if task["clarity_level"] == "low":
    print("Request is ambiguous!")
    print(f"Follow-up questions: {task['follow_ups']}")
    # ["What specifically needs fixing?", "Which system?", "What's the current behavior?"]
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `request` | string | Yes | The user's task request (natural language) |
| `context` | dict | No | Additional context (user, team, environment) |
| `preferences` | dict | No | Preferences (priority, deadline, budget) |

**Input Example**:
```python
{
    "request": "Optimize the database queries for the analytics dashboard",
    "context": {
        "user": "engineering_manager",
        "current_team": "backend",
        "previous_work": "performance tuning"
    },
    "preferences": {
        "priority": "high",
        "max_effort_hours": 24,
        "deadline": "2026-09-10"
    }
}
```

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether normalization succeeded |
| `data.goal` | string | Normalized task goal |
| `data.constraints` | dict | Identified constraints (latency, scope, resources) |
| `data.required_teams` | list | Teams needed for this task |
| `data.priority` | int | Priority (1=urgent, 5=low) |
| `data.success_criteria` | list | Measurable success indicators |
| `data.clarity_level` | string | Request clarity: high/medium/low |
| `data.follow_ups` | list | Clarifying questions (if clarity=low) |
| `data.estimated_effort` | string | Effort estimate (e.g., "2-4 hours") |
| `metadata.latency_ms` | float | Processing latency |

**Output Example**:
```python
{
    "success": True,
    "data": {
        "goal": "Optimize analytics dashboard database queries",
        "constraints": {
            "max_latency_ms": 500,
            "max_rows_scanned": 1000000,
            "database": "production"
        },
        "required_teams": ["backend", "data"],
        "priority": 2,
        "success_criteria": [
            "Query latency < 500ms (p95)",
            "Maintain data accuracy",
            "No concurrent query limits"
        ],
        "clarity_level": "high",
        "follow_ups": [],
        "estimated_effort": "8-16 hours"
    },
    "metadata": {
        "latency_ms": 45.2,
        "processing_version": "1.0.0"
    }
}
```

---

## Configuration

Environment variables and configuration:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `TASKINTAKE_CLARITY_THRESHOLD` | float | 0.7 | Confidence threshold for clarity assessment |
| `TASKINTAKE_MAX_FOLLOWUPS` | int | 3 | Max clarifying questions to generate |
| `TASKINTAKE_PRIORITY_BIAS` | str | "balanced" | How to weight priority (conservative/balanced/aggressive) |
| `TASKINTAKE_TIMEOUT_SECONDS` | int | 10 | Request normalization timeout |

**Setting Configuration**:
```python
# Option 1: Via config dict
skill = TaskIntake(config={
    "clarity_threshold": 0.8,
    "max_followups": 5,
    "priority_bias": "aggressive"
})

# Option 2: Via environment variables
import os
os.environ["TASKINTAKE_CLARITY_THRESHOLD"] = "0.8"
os.environ["TASKINTAKE_MAX_FOLLOWUPS"] = "5"
```

---

## Error Handling

### Ambiguous Request

**Cause**: Request lacks sufficient detail for structured output  
**Indicator**: `clarity_level == "low"` in response  
**Solution**: Review `follow_ups` field and ask user for clarification  
```python
result = await skill.execute({"request": "Fix the bug"})
if result["data"]["clarity_level"] == "low":
    print(f"Please clarify: {result['data']['follow_ups']}")
```

### Invalid Input Format

**Cause**: Request parameter missing or malformed  
**Error**: ValueError raised  
**Solution**: Ensure `request` is a non-empty string  
```python
try:
    result = await skill.execute({"request": ""})
except ValueError as e:
    print(f"Invalid input: {e}")
```

### Timeout

**Cause**: Normalization exceeded timeout threshold  
**Error**: TimeoutError raised  
**Solution**: Increase TASKINTAKE_TIMEOUT_SECONDS or simplify request  
```python
try:
    result = await skill.execute({"request": "..."}, timeout=30)
except TimeoutError:
    print("Request normalization timed out, try a simpler request")
```

---

## Testing

- **Unit Tests**: `tests/test_taskIntake.py` (6 comprehensive tests)
- **Coverage**: >85% of skill logic
- **Test Patterns**: Normalization, constraint extraction, team identification, edge cases

### Running Tests

```bash
# Run taskIntake tests
pytest tests/test_taskIntake.py -v

# Run with coverage
pytest tests/test_taskIntake.py --cov=skills.taskIntake --cov-report=term-missing

# Run specific test
pytest tests/test_taskIntake.py::TestTaskIntakeNormalization::testNormalizesSimpleRequest -v
```

### Test Coverage

- ✅ Simple request normalization
- ✅ Constraint extraction from context
- ✅ Team identification and assignment
- ✅ Empty/minimal input handling
- ✅ Ambiguous request detection
- ✅ Output structure validation

---

## Dependencies

### Skills That Use This Skill

- **decomposition** — Takes structured tasks and breaks them into subtasks
- **routing** — Uses task goals to determine which agent/team should execute
- **decisionMaking** — Considers task context when making agent routing decisions

### Related Skills

- **decomposition**: Downstream skill for task breakdown
- **routing**: Downstream skill for task assignment
- **decisionMaking**: Parallel analysis of task context

### External Dependencies

- No external dependencies (self-contained skill)
- Optional: LLM for ambiguity detection and clarification (future enhancement)

---

## Performance Characteristics

- **Latency (p50)**: ~20-30 ms
- **Latency (p95)**: <100 ms
- **Throughput**: 100+ requests/second (single instance)
- **Scalability**: Horizontal (stateless)

---

## Troubleshooting

### Issue: Requests Are Over-Classified

**Diagnosis**: Simple requests are assigned too many teams or high priorities  
**Solutions**:
1. Reduce TASKINTAKE_PRIORITY_BIAS (set to "conservative")
2. Adjust clarity threshold lower (more permissive)
3. Review request wording (be more specific)

### Issue: Ambiguity Detection Not Triggered

**Diagnosis**: Unclear requests not flagged as low clarity  
**Solutions**:
1. Increase TASKINTAKE_CLARITY_THRESHOLD (higher bar for "high" clarity)
2. Check log level (set to DEBUG for detailed scoring)
3. Review input context (may override clarity detection)

### Issue: Wrong Teams Identified

**Diagnosis**: Task assigned to wrong teams  
**Solutions**:
1. Provide team information in context (lists available teams)
2. Be explicit in request ("for the backend team...")
3. Check team specialization mappings in config

---

## Changelog

### Version 1.0.0 (Phase 18+)
- ✅ Core task normalization
- ✅ Constraint extraction
- ✅ Team identification
- ✅ Clarity assessment
- ✅ >85% test coverage

### Version 0.9.0 (Phase 18)
- Initial implementation
- Basic normalization patterns

---

## Related Documentation

- **Skill Dependencies**: See `skills/DEPENDENCIES.md` for full skill graph
- **Consolidation Notes**: See `skills/CONSOLIDATION_NOTES.md` for related skills
- **Configuration**: See `config/skills.yaml` for skill registry
- **Unified Template**: See `skills/SKILL_TEMPLATE_UNIFIED.md` for documentation format
