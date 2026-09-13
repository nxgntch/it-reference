# Planning Skill

**Create structured execution plans with phases, dependencies, risk assessment, and cost estimation.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 4+ | Coverage: >85%

---

## Description

**Create structured execution plans with phases, dependencies, risk assessment, and cost estimation.**

## Overview

The Planning skill transforms high-level goals into detailed, executable plans. It breaks work into phases, identifies dependencies, assesses risks, and estimates costs—enabling teams to execute complex projects with clarity and confidence.

**When to use**: When starting a new project, defining quarterly goals, or tackling complex technical initiatives.  
**What it solves**: Eliminates ambiguity about how to execute goals, identifies risks proactively, allocates resources realistically.  
**Key benefit**: Teams can execute complex plans with clear phases, known risks, and realistic timelines.

---

## Key Features

- **Phase Breakdown**: Decompose goals into executable phases with clear milestones
- **Dependency Tracking**: Identify task dependencies and critical paths
- **Risk Assessment**: Detect risks, assess probability/impact, recommend mitigations
- **Cost Estimation**: Calculate resource requirements and budget needs
- **Success Probability**: Model likelihood of on-time, on-budget delivery
- **Timeline Planning**: Estimate duration based on team size and complexity
- **Constraint Handling**: Respect budget, timeline, and resource constraints

---

## Quick Start

Minimal example to create a project plan:

```python
from skills.planning import Planning

# Initialize the skill
skill = Planning()

# Execute planning
result = await skill.execute({
    "goal": "Build multi-region deployment system",
    "timeline": "8 weeks",
    "teamSize": 5,
    "constraints": [
        {"type": "budget", "value": 50000},
        {"type": "timeline", "value": "8 weeks"}
    ],
    "riskTolerance": "moderate"
})

# Result contains phases, dependencies, risks, and cost estimates
print(result["plan"])  # ExecutionPlan object
print(result["phases"])  # List of phases with milestones
print(result["risks"])  # Identified risks with probabilities
```

---

## API Reference

### Input Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `goal` | str | Yes | High-level goal or objective |
| `timeline` | str | Yes | Desired timeline (e.g., "8 weeks") |
| `teamSize` | int | Yes | Number of people available |
| `constraints` | List[Constraint] | No | Budget, timeline, resource limits |
| `riskTolerance` | str | No | Risk appetite: "low", "moderate", "high" |

### Output Structure

```python
{
    "plan": ExecutionPlan,  # Overall plan structure
    "phases": List[Phase],  # Breakdown by phase
    "risks": List[Risk],    # Identified risks
    "recommendations": List[str],  # Action items
    "estimatedCost": float,  # Total cost estimate
    "successProbability": float,  # 0.0-1.0 confidence
    "criticalPath": List[str]  # Critical dependencies
}
```

---

## Usage

### Example 1: Simple Goal Planning

```python
result = await skill.execute({
    "goal": "Launch customer analytics dashboard",
    "timeline": "4 weeks",
    "teamSize": 3
})

# Access plan structure
for phase in result["phases"]:
    print(f"Phase: {phase.name}")
    print(f"  Duration: {phase.duration}")
    print(f"  Deliverables: {phase.deliverables}")
```

### Example 2: Constrained Project Planning

```python
result = await skill.execute({
    "goal": "Migrate database to cloud",
    "timeline": "12 weeks",
    "teamSize": 6,
    "constraints": [
        {"type": "budget", "value": 100000},
        {"type": "downtime", "value": "2 hours max"}
    ],
    "riskTolerance": "low"
})

# Analyze identified risks
for risk in result["risks"]:
    print(f"{risk.name}: {risk.probability*100:.0f}% chance")
    print(f"  Mitigation: {risk.mitigation}")
```

### Example 3: Multi-Team Coordination

```python
result = await skill.execute({
    "goal": "Build distributed tracing platform",
    "timeline": "16 weeks",
    "teamSize": 12,
    "constraints": [
        {"type": "budget", "value": 200000}
    ]
})

# Use critical path for team coordination
print(f"Critical path: {result['criticalPath']}")
print(f"Success probability: {result['successProbability']*100:.1f}%")
```

---

## Error Handling

### Common Errors

| Error | Cause | Recovery |
|-------|-------|----------|
| InvalidGoalError | Goal is too vague | Provide specific, measurable objective |
| InsufficientTeamError | Team too small for timeline | Increase team size or extend timeline |
| InfeasibleConstraintsError | Constraints contradict | Loosen constraints or simplify goal |
| MissingDependencyError | Required input missing | Provide goal, timeline, teamSize |

### Example Error Handling

```python
try:
    result = await skill.execute({"goal": "do something"})  # Missing timeline
except MissingDependencyError as e:
    print(f"Planning requires: {e.required}")
    
try:
    result = await skill.execute({
        "goal": goal,
        "timeline": "1 week",
        "teamSize": 2,
        "constraints": [{"type": "budget", "value": 5000}]
    })
except InfeasibleConstraintsError as e:
    print(f"Constraints conflict: {e.details}")
    print("Try increasing budget or timeline")
```

---

## Related Skills

### Upstream (Input to Planning)

- **decisionMaking** — Identifies goals and objectives that planning structures
- **decomposition** — Can assist with breaking goals into components

### Downstream (Output from Planning)

- **taskIntake** — Accepts planning output to schedule individual tasks
- **integration** — Coordinates execution of planned phases across teams
- **docUpdater** — Documents plan for team visibility

### Alternative Skills

- **decomposition** — For simpler goal breakdown (no risk/cost)
- **routing** — For task-level scheduling (not high-level planning)

---

## Configuration

```yaml
skills:
  planning:
    enabled: true
    timeout_seconds: 30
    max_phases: 10
    risk_detection: true
    cost_estimation: true
```

---

## Performance Notes

- **Planning Time**: 2-5s depending on complexity
- **Team Size Limit**: Effective up to 20-person teams
- **Timeline Range**: 1 week to 2 years
- **Concurrent Calls**: Safe for parallel planning sessions

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04 | Initial release with 4-phase generation |

---

## Status

✅ **IMPLEMENTED** — 20 tests, 100% passing. Full 4-phase generation, risk detection, cost estimation, success probability calculation.
