# Phase 11 Code Generation API Reference

Complete API documentation for codeGeneration v2.0 multi-modal input processors.

## Table of Contents

1. [Input Types](#input-types)
2. [ProcessingPipeline](#processingpipeline)
3. [VisionProcessor](#visionprocessor)
4. [OpenAPIParser](#openapiparsser)
5. [Data Models](#data-models)

---

## Input Types

### DesignImageInput

Convert design images to component code.

```python
@dataclass
class DesignImageInput:
    image: bytes                    # PNG/JPG image bytes
    designTool: str                 # "figma" | "sketch" | "adobe"
    designSystem: Optional[str] = None  # e.g., "Material Design 3"
    requirements: Optional[str] = None  # Additional requirements
```

**Usage:**
```python
input_data = DesignImageInput(
    image=image_bytes,
    designTool="figma",
    designSystem="Material Design 3",
    requirements="Accessible card component"
)
```

### APISpecInput

Convert API specifications to code.

```python
@dataclass
class APISpecInput:
    spec: Dict[str, Any]          # OpenAPI 3.0 or Swagger 2.0 dict
    technology: str                # "fastapi" | "express" | "django"
    database: str                  # "postgresql" | "mongodb"
    requirements: Optional[str] = None  # Custom requirements
    existingCode: Optional[str] = None  # Existing code to reference
```

**Usage:**
```python
input_data = APISpecInput(
    spec=openapi_spec_dict,
    technology="fastapi",
    database="postgresql",
    requirements="Add JWT auth"
)
```

### ArchitectureInput

Convert architecture decisions to implementation guides.

```python
@dataclass
class ArchitectureInput:
    decisions: List[str]           # Architecture decisions
    pattern: str                   # "microservices" | "monolith" | "serverless"
    technology: str                # Technology stack
    constraints: Dict[str, Any]    # Performance/availability constraints
    existingCode: Optional[str] = None  # Reference code
```

**Usage:**
```python
input_data = ArchitectureInput(
    decisions=["Use event-driven", "Implement circuit-breaker"],
    pattern="microservices",
    technology="python-fastapi-rabbitmq",
    constraints={"maxLatency": "500ms", "availability": "99.9%"}
)
```

### RequirementsInput

Text-based requirements (backward compatible).

```python
@dataclass
class RequirementsInput:
    text: str                      # Requirements description
    context: Optional[str] = None  # Project context
    examples: Optional[List[str]] = None  # Usage examples
```

---

## ProcessingPipeline

Main entry point for multi-modal code generation.

### Constructor

```python
class ProcessingPipeline:
    def __init__(self, vision_client=None):
        """
        Initialize pipeline
        
        Args:
            vision_client: Optional Anthropic client for Vision API
                If None, uses mock implementation (for testing)
        """
```

### Methods

#### `async process(input_data) -> Dict[str, Any]`

Process any input type through appropriate pipeline.

```python
pipeline = ProcessingPipeline()
result = await pipeline.process(input_data)
```

**Returns:** Processed context dictionary with generated code

**Response Structure:** Varies by input mode (see examples)

---

## VisionProcessor

Design image analysis using Claude Vision API.

### Constructor

```python
class VisionProcessor:
    def __init__(self, client=None):
        """
        Initialize vision processor
        
        Args:
            client: Optional Anthropic API client
        """
```

### Methods

#### `async analyze_design(image_data: bytes, design_tool: str) -> DesignAnalysis`

Analyze design image and extract UI structure.

```python
analysis = await processor.analyze_design(
    image_data=image_bytes,
    design_tool="figma"
)
```

**Parameters:**
- `image_data` (bytes): PNG/JPG image bytes
- `design_tool` (str): "figma" | "sketch" | "adobe"

**Returns:** `DesignAnalysis` with components and constraints

**DesignAnalysis Fields:**
```python
@dataclass
class DesignAnalysis:
    layout: str                             # "flex", "grid", "absolute"
    components: List[Component]             # Extracted UI components
    colors: List[str]                       # Color palette
    typography: Dict[str, Any]              # Font definitions
    spacing: Dict[str, float]               # Padding/margin patterns
    responsiveBreakpoints: List[Dict]       # Mobile/tablet/desktop
    accessibility: Dict[str, Any]           # A11y constraints
    interactiveElements: List[Dict]         # Hover, click, states
```

#### `extract_component_hierarchy(analysis: DesignAnalysis) -> Dict[str, Any]`

Build component tree structure for code generation.

```python
hierarchy = processor.extract_component_hierarchy(analysis)
```

**Returns:** Hierarchy dict with structure and constraints

#### `generate_component_skeleton(component: Component, framework: str) -> str`

Generate code skeleton for a component.

```python
code = processor.generate_component_skeleton(
    component=component,
    framework="react"  # "react" | "vue" | "html"
)
```

**Returns:** Component code skeleton as string

#### `detect_design_patterns(components: List[Component]) -> List[str]`

Identify common design patterns in component hierarchy.

```python
patterns = processor.detect_design_patterns(components)
# Returns: ["card-based-layout", "modal-driven-interactions", ...]
```

**Detected Patterns:**
- `card-based-layout` - 3+ card components
- `modal-driven-interactions` - 2+ modals
- `form-heavy` - 2+ form components
- `navigation-header` - Top navigation present
- `list-based-content` - 2+ list components

#### `validate_accessibility(components: List[Component]) -> Dict[str, Any]`

Validate accessibility constraints.

```python
report = processor.validate_accessibility(components)
# {
#     "issues": ["button missing aria-label"],
#     "recommendations": ["Verify color contrast"],
#     "isAccessible": True
# }
```

---

## OpenAPIParser

OpenAPI/Swagger specification parser.

### Constructor

```python
class OpenAPIParser:
    def __init__(self):
        """Initialize parser"""
```

### Methods

#### `parse(spec: Dict[str, Any]) -> APISpecification`

Parse OpenAPI or Swagger specification (auto-detects version).

```python
parser = OpenAPIParser()
api_spec = parser.parse(openapi_dict)
```

**Parameters:**
- `spec` (Dict): OpenAPI 3.0 or Swagger 2.0 spec dict

**Returns:** `APISpecification` with parsed structure

**APISpecification Fields:**
```python
@dataclass
class APISpecification:
    title: str                          # API title
    version: str                        # API version
    basePath: str                       # Base URL path
    endpoints: List[Endpoint]           # All endpoints
    schemas: Dict[str, Schema]          # Data models
    securitySchemes: Dict[str, Any]     # Auth methods
```

#### `generate_database_models(api_spec: APISpecification, database: str) -> str`

Generate database models from API schemas.

```python
models_code = parser.generate_database_models(
    api_spec=api_spec,
    database="postgresql"  # "postgresql" | "mongodb"
)
```

**Supports:**
- **PostgreSQL**: SQLAlchemy ORM models
- **MongoDB**: Pydantic models

**Returns:** Generated model code as string

#### `generate_routes(api_spec: APISpecification, framework: str) -> str`

Generate API routes with error handling.

```python
routes_code = parser.generate_routes(
    api_spec=api_spec,
    framework="fastapi"  # "fastapi" | "generic"
)
```

**Supports:**
- **FastAPI**: Async routes with type hints
- **Generic**: Route stubs for any framework

**Returns:** Generated route code as string

---

## Data Models

### Component

UI component extracted from design.

```python
@dataclass
class Component:
    name: str                           # Component name
    type: str                           # "button", "input", "card", etc.
    position: Dict[str, float]          # x, y, width, height
    properties: Dict[str, Any]          # color, size, text, etc.
    children: List['Component'] = None  # Nested components
```

### Parameter

API endpoint parameter.

```python
@dataclass
class Parameter:
    name: str                           # Parameter name
    type: str                           # JSON schema type
    location: str                       # "query", "path", "header", "body"
    required: bool                      # Is required
    description: str = ""               # Description
```

### Endpoint

API endpoint definition.

```python
@dataclass
class Endpoint:
    path: str                           # URL path
    method: HTTPMethod                  # HTTP method
    summary: str                        # Short description
    description: str = ""               # Full description
    parameters: List[Parameter] = None  # Query/path/header params
    requestBody: Optional[Schema] = None  # Request body schema
    responses: Dict[int, Dict] = None   # Response codes/schemas
    security: List[str] = None          # Security schemes
```

### Schema

Data model definition.

```python
@dataclass
class Schema:
    name: str                           # Schema name
    type: str                           # "object", "string", etc.
    properties: Dict[str, Any]          # Field definitions
    required: List[str]                 # Required fields
    description: str = ""               # Description
```

---

## Type Mapping

### JSON Schema → Python Type

| JSON Schema | Python |
|------------|--------|
| `string` | `str` |
| `integer` | `int` |
| `number` | `float` |
| `boolean` | `bool` |
| `array` | `List` |
| `object` | `Dict` |

---

## Error Handling

### Vision Processor Errors

```python
try:
    analysis = await processor.analyze_design(image_data, design_tool)
except RuntimeError as e:
    # Vision API call failed
    print(f"API error: {e}")
```

### Parser Errors

```python
try:
    api_spec = parser.parse(spec)
except ValueError as e:
    # Unknown spec format
    print(f"Parse error: {e}")
```

### Pipeline Errors

All errors are caught and logged by pipeline; check output for error details.

```python
result = await pipeline.process(input_data)
if "error" in result:
    print(f"Processing error: {result['error']}")
```

---

## Performance

| Operation | Latency | Notes |
|-----------|---------|-------|
| Design analysis | 2-5s | Depends on image complexity |
| OpenAPI parsing | 100-500ms | Scales with endpoint count |
| Pattern detection | 10-50ms | Single pass analysis |
| Concurrent processing | Linear | Scales with CPU cores |

---

## Examples

See [PHASE_11_USAGE_EXAMPLES.md](../guides/PHASE_11_USAGE_EXAMPLES.md) for complete examples.

---

## API Stability

- ✅ Stable: Input/Output data structures (v2.0)
- ✅ Stable: Pipeline interface
- ⚠️ Beta: Vision API integration (depends on Claude Vision API)
- ✅ Stable: OpenAPI parser (v3.0 and Swagger 2.0)

All APIs follow semantic versioning: MAJOR.MINOR.PATCH
