# Code Generation Skill

**Generate production-ready code from specifications, designs, and requirements.**

Version: 1.0.0 | Status: ✅ Production Ready | Phase: 18+ | Coverage: >85%

---

## Description

**Generate production-ready code from specifications, designs, and requirements.**

## Overview

The Code Generation skill is the **code synthesis engine** in nxgntch. It transforms specifications, API schemas, and design documents into production-ready code with comprehensive testing and documentation.

**When to use**: When you need to generate code from specifications, designs, or requirements.  
**What it solves**: Eliminates manual coding effort for well-defined tasks, ensures consistent code quality and patterns, generates tests alongside implementation.  
**Key benefit**: Reduce development time by generating correct, tested code from specifications.

---

## Key Features

- **Multi-Source Input**: Generate from specifications, APIs, requirements, designs
- **Multi-Language Output**: Support Python, JavaScript, TypeScript, Go, Java
- **Test Generation**: Automatically create unit tests alongside code
- **Type Safety**: Full type hints and schema validation
- **Documentation**: Generate docstrings and inline comments
- **Pattern Consistency**: Enforce project coding standards
- **Component Extraction**: Identify reusable components and modules

---

## Quick Start

Minimal example to generate code from specification:

```python
from skills.codeGeneration import CodeGeneration

# Initialize the skill
skill = CodeGeneration()

# Execute on a specification
result = await skill.execute({
    "specification": {
        "name": "calculateDiscount",
        "description": "Calculate percentage discount on purchase price",
        "inputs": [{"name": "price", "type": "float"}, {"name": "discountPercent", "type": "float"}],
        "outputs": {"type": "float"}
    },
    "targetLanguage": "python",
    "includeTests": True
})

# Result contains generated code
print(result["output"])
# {
#     "code": "def calculateDiscount(price: float, discountPercent: float) -> float:\n    ...",
#     "tests": "def testCalculateDiscount(): ...",
#     "components": ["calculateDiscount"],
#     "coverage": "100%"
# }
```

---

## Usage

### Basic Usage: Generate Function from Spec

```python
# Example 1: Simple function generation
result = await skill.execute({
    "specification": {
        "name": "formatCurrency",
        "description": "Format number as currency with 2 decimals",
        "inputs": [{"name": "amount", "type": "float"}],
        "outputs": {"type": "string"}
    },
    "targetLanguage": "python"
})

code = result["output"]["code"]
print(code)
```

### With Tests: Generate Tests Alongside Code

```python
# Example 2: Generate with comprehensive tests
result = await skill.execute({
    "specification": {
        "name": "validateEmail",
        "description": "Validate email address format",
        "inputs": [{"name": "email", "type": "string"}],
        "outputs": {"type": "bool"}
    },
    "targetLanguage": "python",
    "includeTests": True,
    "testCases": [
        {"input": "user@example.com", "expectedOutput": True},
        {"input": "invalid-email", "expectedOutput": False},
        {"input": "", "expectedOutput": False}
    ]
})

code = result["output"]["code"]
tests = result["output"]["tests"]
print(f"Code:\n{code}\n\nTests:\n{tests}")
```

### Advanced: Multi-Language with Patterns

```python
# Example 3: Generate across multiple languages
result = await skill.execute({
    "specification": {
        "name": "PaymentProcessor",
        "description": "Process payment transactions",
        "inputs": [{"name": "amount", "type": "float"}, {"name": "cardToken", "type": "string"}],
        "outputs": {"type": "dict"}
    },
    "targetLanguages": ["python", "typescript", "go"],
    "patterns": ["error_handling", "logging", "retry"],
    "documentation": "comprehensive"
})

for lang, code in result["output"]["code"].items():
    print(f"=== {lang.upper()} ===\n{code}\n")
```

### Error Handling: Invalid Specification

```python
# Example 4: Handle malformed specifications
result = await skill.execute({
    "specification": {
        "name": "incomplete_spec"
        # Missing description, inputs, outputs
    }
})

output = result["output"]
if output.get("incomplete"):
    print("Specification incomplete:")
    for field in output.get("missingFields", []):
        print(f"  - Missing: {field}")
    print(f"Suggestions: {output.get('clarifyingQuestions')}")
```

---

## API Reference

### Input Schema

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `specification` | dict | Yes | Code specification (name, description, inputs, outputs) |
| `targetLanguage` | string | Yes | Output language (python/typescript/go/java) |
| `targetLanguages` | list | No | Multiple languages (overrides targetLanguage) |
| `includeTests` | bool | No | Generate tests alongside code (default: false) |
| `testCases` | list | No | Test cases to validate generated code |
| `patterns` | list | No | Code patterns to apply (error_handling, logging, retry) |
| `documentation` | string | No | Documentation level (minimal/standard/comprehensive) |
| `codeStyle` | dict | No | Coding style preferences (naming, formatting) |

**Input Example**:
```python
{
    "specification": {
        "name": "calculateTotalCost",
        "description": "Calculate total cost including tax",
        "inputs": [
            {"name": "subtotal", "type": "float"},
            {"name": "taxRate", "type": "float"}
        ],
        "outputs": {"type": "float"}
    },
    "targetLanguage": "python",
    "includeTests": True,
    "patterns": ["error_handling", "logging"],
    "documentation": "comprehensive"
}
```

### Output Schema

| Field | Type | Description |
|-------|------|-------------|
| `success` | bool | Whether code generation succeeded |
| `data.code` | string/dict | Generated code (string for single lang, dict for multiple) |
| `data.tests` | string | Generated test code |
| `data.components` | list | Identified components/modules |
| `data.documentation` | string | Generated documentation/docstrings |
| `data.coverage` | string | Test coverage estimate |
| `data.incomplete` | bool | Specification missing required fields |
| `data.missingFields` | list | Which fields are incomplete |
| `metadata.latency_ms` | float | Processing time |

**Output Example**:
```python
{
    "success": True,
    "data": {
        "code": "def calculateTotalCost(subtotal: float, taxRate: float) -> float:\n    ...",
        "tests": "def testCalculateTotalCost(): ...",
        "components": ["calculateTotalCost"],
        "documentation": "Calculate total cost including tax...",
        "coverage": "100%"
    },
    "metadata": {
        "latency_ms": 125.3,
        "lines_generated": 42,
        "complexity": "simple"
    }
}
```

---

## Configuration

Environment variables and configuration:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `CODEGEN_DEFAULT_LANGUAGE` | str | "python" | Default target language |
| `CODEGEN_INCLUDE_TESTS` | bool | true | Generate tests by default |
| `CODEGEN_DOCUMENTATION_LEVEL` | str | "standard" | Default doc level (minimal/standard/comprehensive) |
| `CODEGEN_TIMEOUT_SECONDS` | int | 30 | Code generation timeout |
| `CODEGEN_MAX_COMPLEXITY` | str | "moderate" | Complexity threshold (simple/moderate/complex) |

**Setting Configuration**:
```python
# Option 1: Via config dict
skill = CodeGeneration(config={
    "default_language": "typescript",
    "include_tests": True,
    "documentation_level": "comprehensive",
    "timeout_seconds": 60
})

# Option 2: Via environment variables
import os
os.environ["CODEGEN_DEFAULT_LANGUAGE"] = "typescript"
os.environ["CODEGEN_INCLUDE_TESTS"] = "true"
```

---

## Error Handling

### Incomplete Specification

**Cause**: Required fields missing from specification  
**Indicator**: `incomplete: True` in response  
**Solution**: Provide name, description, inputs, and outputs  
```python
result = await skill.execute({"specification": {...}})
if result["data"].get("incomplete"):
    print(f"Missing: {result['data']['missingFields']}")
```

### Invalid Type Specification

**Cause**: Type references unknown or invalid types  
**Error**: ValueError raised  
**Solution**: Use standard language types (string, number, bool, list, dict)  
```python
# Valid types: str, int, float, bool, list, dict
# Invalid: custom types without definition
```

### Too Complex

**Cause**: Specification too complex for code generation  
**Error**: Returns with flag `tooComplex: True`  
**Solution**: Break into smaller functions or lower complexity threshold  
```python
if result["data"].get("tooComplex"):
    print("Specification too complex, consider breaking down")
```

### Timeout

**Cause**: Code generation exceeded timeout  
**Error**: TimeoutError raised  
**Solution**: Increase CODEGEN_TIMEOUT_SECONDS or simplify specification  
```python
try:
    result = await skill.execute({...}, timeout=60)
except TimeoutError:
    print("Code generation timed out")
```

---

## Testing

- **Unit Tests**: `tests/test_codeGeneration.py` (12+ comprehensive tests)
- **Coverage**: >85% of code generation logic
- **Test Patterns**: Spec validation, code generation accuracy, test generation

### Running Tests

```bash
# Run code generation tests
pytest tests/test_codeGeneration.py -v

# Run with coverage
pytest tests/test_codeGeneration.py --cov=skills.codeGeneration --cov-report=term-missing

# Run specific test
pytest tests/test_codeGeneration.py::TestCodeGeneration::testGeneratesFunctionCorrectly -v
```

### Test Coverage

- ✅ Function generation from specifications
- ✅ Multi-language output
- ✅ Test case generation
- ✅ Type validation and inference
- ✅ Code pattern application
- ✅ Documentation generation
- ✅ Edge cases (empty specs, complex types)

---

## Dependencies

### Skills That Use This Skill

- **developer workflow** — Uses code generation for rapid prototyping
- **automation** — Generates code for repetitive tasks

### Skills Used By This Skill

- None (standalone generation)

### Related Skills

- **codeReview**: Validates generated code quality
- **testing**: Complements test generation

---

## Performance Characteristics

- **Latency (p50)**: ~100-150 ms
- **Latency (p95)**: <500 ms
- **Throughput**: 30+ generations/second (single instance)
- **Scalability**: Horizontal (stateless)
- **Complexity**: O(n) where n = specification complexity

---

## Troubleshooting

### Issue: Generated Code Doesn't Match Requirements

**Diagnosis**: Output code missing expected functionality  
**Solutions**:
1. Provide more detailed specification
2. Add examples or patterns to clarify intent
3. Break complex specs into smaller functions
4. Review type specifications for ambiguity

### Issue: Tests Not Generated

**Diagnosis**: Generated code has no test coverage  
**Solutions**:
1. Set `includeTests: true` in input
2. Verify specification is complete
3. Provide test cases in `testCases` field
4. Check CODEGEN_INCLUDE_TESTS config

### Issue: Type Errors in Generated Code

**Diagnosis**: Generated code has type mismatches  
**Solutions**:
1. Use standard types only (str, int, float, bool, list, dict)
2. Provide type definitions for custom types
3. Review outputs for correctness
4. Enable strict type checking in target language

---

## Changelog

### Version 1.0.0 (Phase 18+)
- ✅ Core code generation engine
- ✅ Multi-language support (Python, TypeScript, Go, Java)
- ✅ Test generation
- ✅ Type inference and validation
- ✅ Documentation generation
- ✅ Pattern application
- ✅ >85% test coverage

---

## Related Documentation

- **Skill Dependencies**: See `skills/DEPENDENCIES.md` for full skill graph
- **Configuration**: See `config/skills.yaml` for skill registry
- **Unified Template**: See `skills/SKILL_TEMPLATE_UNIFIED.md` for documentation format
- **Code Standards**: See `../../docs/rules/coding-style.md` for output patterns
