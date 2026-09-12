# Integration Skill

**Compose multiple services/components into cohesive workflows with dependency resolution and validation.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 18+ | Coverage: >85%

---

## Description

**Compose multiple services/components into cohesive workflows with dependency resolution and validation.**

## Overview

The Integration skill is the **service composition engine** in nxgntch. It takes independent services, components, or agents and automatically wires them together into cohesive workflows, resolving dependencies, validating connections, and identifying potential issues before execution.

**When to use**: When building complex workflows from multiple services or components that need to work together.  
**What it solves**: Eliminates manual wiring errors, ensures all dependencies are satisfied, identifies configuration gaps, enables composable architectures.  
**Key benefit**: Compose complex systems from simple components with automatic validation and error detection.

---

## Key Features

- **Dependency Resolution**: Automatically order services based on dependencies
- **Connection Validation**: Ensure inputs/outputs align between services
- **Workflow Generation**: Create executable workflows from component definitions
- **Conflict Detection**: Identify incompatibilities and constraint violations
- **Alternative Composition**: Suggest alternative arrangements if initial fails
- **Configuration Recommendation**: Propose missing configurations
- **Circular Dependency Detection**: Prevent infinite loops in service chains

---

## Quick Start

Minimal example to compose services into a workflow:

```python
from skills.integration import Integration

# Initialize the skill
skill = Integration()

# Execute on service definitions
result = await skill.execute({
    "goal": "Create user authentication workflow",
    "components": [
        {"id": "auth_service", "inputs": ["credentials"], "outputs": ["token"]},
        {"id": "validation_service", "inputs": ["token"], "outputs": ["isValid"]},
        {"id": "logging_service", "inputs": ["event"], "outputs": []}
    ],
    "constraints": ["auth_service must run first", "validation_service requires auth_service output"]
})

# Result contains composed workflow
print(result["output"])
# {
#     "workflow": {
#         "steps": [
#             {"order": 1, "component": "auth_service", "inputs": {"credentials": "external"}},
#             {"order": 2, "component": "validation_service", "inputs": {"token": "auth_service.token"}},
#             {"order": 3, "component": "logging_service", "inputs": {"event": "external"}}
#         ]
#     },
#     "isValid": True,
#     "validationErrors": [],
#     "recommendations": []
# }
```

---

## Usage

### Basic Usage: Simple Service Composition

```python
# Example 1: Compose two interdependent services
result = await skill.execute({
    "goal": "Payment processing workflow",
    "components": [
        {"id": "payment_validator", "inputs": ["amount"], "outputs": ["isValid"]},
        {"id": "payment_processor", "inputs": ["amount", "isValid"], "outputs": ["receipt"]}
    ]
})

workflow = result["output"]["workflow"]
print(f"Steps: {len(workflow['steps'])}, Valid: {result['output']['isValid']}")
```

### With Constraints: Hard Requirements

```python
# Example 2: Composition with mandatory constraints
result = await skill.execute({
    "goal": "Data pipeline with error handling",
    "components": [
        {"id": "data_source", "inputs": [], "outputs": ["data"]},
        {"id": "data_transformer", "inputs": ["data"], "outputs": ["transformed"]},
        {"id": "error_handler", "inputs": ["error"], "outputs": ["logged"]},
        {"id": "data_sink", "inputs": ["transformed"], "outputs": []}
    ],
    "constraints": [
        "data_source must run first",
        "error_handler must be available to catch errors",
        "data_sink must run last"
    ]
})

for error in result["output"]["validationErrors"]:
    print(f"Configuration issue: {error}")
```

### Advanced: Complex Multi-Service Composition

```python
# Example 3: Large workflow with multiple branches
result = await skill.execute({
    "goal": "Microservice architecture integration",
    "components": [
        {"id": "api_gateway", "inputs": ["request"], "outputs": ["routed_request"]},
        {"id": "user_service", "inputs": ["routed_request"], "outputs": ["user_data"]},
        {"id": "auth_service", "inputs": ["user_data"], "outputs": ["token"]},
        {"id": "profile_service", "inputs": ["user_data"], "outputs": ["profile"]},
        {"id": "cache_service", "inputs": ["profile", "token"], "outputs": ["cached"]},
        {"id": "response_builder", "inputs": ["cached", "profile"], "outputs": ["response"]}
    ],
    "constraints": [
        "api_gateway must execute first",
        "auth_service and profile_service can run in parallel",
        "cache_service must wait for auth_service and profile_service",
        "response_builder must run last"
    ]
})

composition = result["output"]
print(f"Parallel opportunities: {composition.get('parallelGroups', [])}")
print(f"Critical path: {composition.get('criticalPath', [])}")
```

### Error Handling: Invalid Composition

```python
# Example 4: Handle composition failures
result = await skill.execute({
    "goal": "Workflow with unresolved dependencies",
    "components": [
        {"id": "service_a", "inputs": ["data"], "outputs": ["result"]},
        {"id": "service_b", "inputs": ["missing_input"], "outputs": ["output"]}
    ]
})

output = result["output"]
if not output["isValid"]:
    print("Composition invalid:")
    for error in output["validationErrors"]:
        print(f"  - {error}")
    for rec in output["recommendations"]:
        print(f"  Suggestion: {rec}")
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `goal` | string | Yes | Workflow objective (e.g., "Authentication workflow") |
| `components` | list | Yes | Service/component definitions (id, inputs, outputs, type) |
| `constraints` | list | No | Ordering or dependency constraints |
| `allowParallel` | bool | No | Allow parallel execution of independent services (default: true) |
| `strictValidation` | bool | No | Enforce strict input/output matching (default: true) |

**Input Example**:
```python
{
    "goal": "Email notification workflow",
    "components": [
        {
            "id": "email_service",
            "inputs": ["recipient", "subject", "body"],
            "outputs": ["emailId"],
            "type": "service"
        },
        {
            "id": "audit_logger",
            "inputs": ["emailId", "recipient"],
            "outputs": [],
            "type": "logging"
        }
    ],
    "constraints": [
        "email_service must complete before audit_logger starts"
    ],
    "allowParallel": True,
    "strictValidation": True
}
```

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether composition succeeded |
| `data.workflow` | dict | Composed workflow with ordered steps |
| `data.isValid` | bool | Whether workflow is valid and executable |
| `data.validationErrors` | list | Issues preventing execution |
| `data.recommendations` | list | Suggested fixes or improvements |
| `data.parallelGroups` | list | Groups of services that can run in parallel |
| `data.criticalPath` | list | Critical path for execution ordering |
| `metadata.latency_ms` | float | Processing time |

**Output Example**:
```python
{
    "success": True,
    "data": {
        "workflow": {
            "steps": [
                {
                    "order": 1,
                    "component": "email_service",
                    "inputs": {"recipient": "external", "subject": "external", "body": "external"},
                    "outputs": {"emailId": "to_audit_logger"}
                },
                {
                    "order": 2,
                    "component": "audit_logger",
                    "inputs": {"emailId": "email_service.emailId", "recipient": "external"}
                }
            ]
        },
        "isValid": True,
        "validationErrors": [],
        "recommendations": ["Consider adding error handler for email failures"],
        "parallelGroups": [],
        "criticalPath": ["email_service", "audit_logger"]
    },
    "metadata": {
        "latency_ms": 35.2,
        "component_count": 2,
        "step_count": 2
    }
}
```

---

## Configuration

Environment variables and configuration:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `INTEGRATION_ALLOW_PARALLEL` | bool | true | Allow parallel service execution |
| `INTEGRATION_STRICT_VALIDATION` | bool | true | Require strict input/output matching |
| `INTEGRATION_TIMEOUT_SECONDS` | int | 10 | Composition timeout |
| `INTEGRATION_MAX_COMPONENTS` | int | 100 | Maximum services per workflow |
| `INTEGRATION_ALLOW_CYCLES` | bool | false | Allow circular dependencies (dangerous) |

**Setting Configuration**:
```python
# Option 1: Via config dict
skill = Integration(config={
    "allow_parallel": True,
    "strict_validation": True,
    "timeout_seconds": 15,
    "max_components": 50
})

# Option 2: Via environment variables
import os
os.environ["INTEGRATION_ALLOW_PARALLEL"] = "true"
os.environ["INTEGRATION_STRICT_VALIDATION"] = "true"
```

---

## Error Handling

### Unresolved Dependencies

**Cause**: Component requires input that no other component provides  
**Error**: Returns with flag `hasUnresolvedDependencies: True`  
**Solution**: Add component that provides missing output or mark as external input  
```python
result = await skill.execute({...})
if result["data"].get("hasUnresolvedDependencies"):
    print("Missing inputs:")
    for dep in result["data"].get("unmetDependencies", []):
        print(f"  - {dep['component']} needs {dep['input']}")
```

### Circular Dependencies

**Cause**: Services form a cycle (A → B → A)  
**Error**: Returns with flag `hasCircularDependencies: True`  
**Solution**: Break cycle by removing or reordering services  
```python
result = await skill.execute({...})
if result["data"].get("hasCircularDependencies"):
    print(f"Circular dependency detected: {result['data']['cycle']}")
```

### Type Mismatch

**Cause**: Service output type doesn't match expected input type  
**Indicator**: `validationErrors` includes type mismatch messages  
**Solution**: Add adapter/transformer between services or adjust types  
```python
# Add transformer service
components.append({
    "id": "type_adapter",
    "inputs": ["incompatible_output"],
    "outputs": ["compatible_output"]
})
```

### Too Many Components

**Cause**: Workflow exceeds maximum component limit  
**Error**: Returns with flag `exceedsMaxComponents: True`  
**Solution**: Split into multiple workflows or increase `INTEGRATION_MAX_COMPONENTS`  
```python
if result["data"].get("exceedsMaxComponents"):
    print(f"Workflow too large: {result['data']['componentCount']} components")
```

---

## Testing

- **Unit Tests**: `tests/test_integration.py` (6+ comprehensive tests)
- **Coverage**: >85% of composition logic
- **Test Patterns**: Dependency resolution, constraint satisfaction, validation

### Running Tests

```bash
# Run integration tests
pytest tests/test_integration.py -v

# Run with coverage
pytest tests/test_integration.py --cov=skills.integration --cov-report=term-missing

# Run specific test
pytest tests/test_integration.py::TestIntegration::testComposesServicesInCorrectOrder -v
```

### Test Coverage

- ✅ Simple two-service composition
- ✅ Complex multi-service workflows
- ✅ Dependency resolution and ordering
- ✅ Parallel execution identification
- ✅ Circular dependency detection
- ✅ Input/output validation
- ✅ Constraint satisfaction checking
- ✅ Error handling and recovery

---

## Dependencies

### Skills That Use This Skill

- **orchestrator** — Composes agent workflows for complex tasks
- **routing** — Determines service order and parallel groups

### Skills Used By This Skill

- **decomposition** — May decompose complex services into simpler components
- **decisionMaking** — Evaluates alternative compositions

### Related Skills

- **decomposition**: Can break services into components before integration
- **costForecasting**: Can estimate cost of composed workflows

---

## Performance Characteristics

- **Latency (p50)**: ~25-35 ms
- **Latency (p95)**: <100 ms
- **Throughput**: 200+ compositions/second (single instance)
- **Scalability**: Horizontal (stateless)
- **Complexity**: O(n² log n) where n = component count

---

## Troubleshooting

### Issue: Composition Too Slow

**Diagnosis**: Composition evaluation exceeds timeout  
**Solutions**:
1. Reduce component count (consider multi-stage workflows)
2. Increase `INTEGRATION_TIMEOUT_SECONDS`
3. Disable strict validation if not needed
4. Pre-compute static compositions

### Issue: False Validation Errors

**Diagnosis**: Valid compositions rejected as invalid  
**Solutions**:
1. Set `strictValidation: False` if types are compatible
2. Add type adapters between services
3. Review constraint definitions for incorrectness
4. Enable debug logging for detailed error messages

### Issue: Missed Parallelization

**Diagnosis**: Sequential execution when parallel possible  
**Solutions**:
1. Verify `allowParallel: True`
2. Check constraints aren't overly restrictive
3. Ensure independent services don't have false dependencies
4. Review suggested parallel groups in output

### Issue: Cycles Not Detected

**Diagnosis**: Circular dependencies not caught  
**Solutions**:
1. Enable strict cycle checking (default)
2. Verify service definitions include all connections
3. Review constraints manually for logical cycles
4. Consider using acyclic-only mode if cycles not needed

---

## Changelog

### Version 1.0.0 (Phase 18+)
- ✅ Core service composition engine
- ✅ Dependency resolution and topological ordering
- ✅ Circular dependency detection
- ✅ Constraint satisfaction checking
- ✅ Parallel execution identification
- ✅ Input/output validation
- ✅ Workflow generation
- ✅ >85% test coverage

---

## Related Documentation

- **Skill Dependencies**: See `skills/DEPENDENCIES.md` for full skill graph
- **Configuration**: See `config/skills.yaml` for skill registry
- **Unified Template**: See `skills/SKILL_TEMPLATE_UNIFIED.md` for documentation format
- **Orchestration**: See `skills/orchestrator/SKILL.md` (downstream consumer)
