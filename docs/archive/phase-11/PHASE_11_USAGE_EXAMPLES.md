# Phase 11: Code Generation v2.0 - Usage Examples

Multi-modal code generation with design images, API specifications, architecture decisions, and text requirements.

## Quick Start

```python
from skills.codeGeneration.pipeline import ProcessingPipeline
from skills.codeGeneration.inputs import (
    DesignImageInput,
    APISpecInput,
    ArchitectureInput,
    RequirementsInput
)

pipeline = ProcessingPipeline()
result = await pipeline.process(input_data)
```

## Example 1: Design Image → React Component

Convert a Figma design to React components with accessibility validation.

```python
# Load design image
with open("design.png", "rb") as f:
    image_bytes = f.read()

# Process design
input_data = DesignImageInput(
    image=image_bytes,
    designTool="figma",
    designSystem="Material Design 3",
    requirements="Accessible, responsive card component"
)

result = await pipeline.process(input_data)

# Output includes:
# - Extracted components: result["analysis"]["componentCount"]
# - Component hierarchy: result["hierarchy"]
# - React code skeletons: result["componentSkeletons"]
# - Design patterns detected: result["patterns"]
# - Accessibility report: result["accessibilityValidation"]
```

**Output Structure:**
```python
{
    "mode": "design-image",
    "designTool": "figma",
    "designSystem": "Material Design 3",
    "analysis": {
        "layout": "flex",
        "componentCount": 5,
        "colors": ["#1F2937", "#FFFFFF", "#3B82F6"],
        "typography": {
            "heading": {"font": "Inter", "size": 24, "weight": 700},
            "body": {"font": "Inter", "size": 16, "weight": 400}
        },
        "spacing": {"padding": 16, "margin": 8},
        "responsiveBreakpoints": [768, 1024, 1280],
        "accessibility": {
            "labels": ["aria-label present"],
            "contrast": "AAA compliant"
        },
        "interactiveElements": ["hover", "focus", "active"]
    },
    "patterns": ["card-based-layout"],
    "accessibilityValidation": {
        "issues": [],
        "recommendations": [],
        "isAccessible": True
    },
    "hierarchy": {
        "structure": [
            {
                "name": "Card",
                "type": "div",
                "children": [
                    {"name": "Header", "type": "h2"},
                    {"name": "Content", "type": "div"}
                ]
            }
        ],
        "constraints": {
            "layout": "flex",
            "spacing": {"padding": 16}
        }
    },
    "componentSkeletons": [
        "export function Card() { ... }",
        "export function CardHeader() { ... }"
    ],
    "processingSteps": [
        "extract_layout",
        "identify_components",
        "detect_patterns",
        "validate_accessibility",
        "map_component_library",
        "generate_responsive_constraints",
        "generate_component_code"
    ]
}
```

## Example 2: OpenAPI Spec → FastAPI App

Generate a complete FastAPI application from an OpenAPI specification.

```python
# OpenAPI specification
spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "User Management API",
        "version": "1.0.0"
    },
    "paths": {
        "/users": {
            "get": {
                "summary": "List all users",
                "responses": {"200": {"description": "List of users"}}
            },
            "post": {
                "summary": "Create new user",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    }
                }
            }
        },
        "/users/{id}": {
            "get": {"summary": "Get user by ID"},
            "put": {"summary": "Update user"},
            "delete": {"summary": "Delete user"}
        }
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "minLength": 1, "maxLength": 100},
                    "email": {"type": "string"},
                    "active": {"type": "boolean"}
                },
                "required": ["id", "name", "email"]
            }
        }
    }
}

# Process specification
input_data = APISpecInput(
    spec=spec,
    technology="fastapi",
    database="postgresql",
    requirements="Add JWT authentication middleware"
)

result = await pipeline.process(input_data)

# Generated code includes:
# - Database models: result["generatedCode"]["databaseModels"]
# - API routes: result["generatedCode"]["routes"]
```

**Generated Pydantic Model:**
```python
class User(BaseModel):
    """User data model"""
    id: int
    name: str  # min=1, max=100
    email: str
    active: Optional[bool]

    model_config = ConfigDict(from_attributes=True)
```

**Generated FastAPI Route:**
```python
@router.get("/users", tags=["User Management API"])
async def list_users():
    """
    List all users
    
    Responses: 200
    """
    try:
        # TODO: Implement endpoint logic
        return {"status": "success", "data": None}
    except Exception as e:
        logger.error(f"Error in list_users: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Example 3: Architecture Decisions → Implementation

Generate service definitions from architectural decisions.

```python
input_data = ArchitectureInput(
    decisions=[
        "Use event-driven architecture with RabbitMQ for messaging",
        "Implement saga pattern for distributed transactions",
        "Add circuit-breaker pattern for external service resilience",
        "Implement caching layer with Redis",
        "Deploy microservices independently"
    ],
    pattern="microservices",
    technology="python-fastapi-rabbitmq-redis",
    constraints={
        "maxLatency": "500ms",
        "availability": "99.9%",
        "scalability": "horizontal",
        "dataConsistency": "eventual"
    }
)

result = await pipeline.process(input_data)

# Output includes detected patterns and implementation strategy
# result["detectedPatterns"] → ["event-driven", "saga", "circuit-breaker", "caching", "resilience"]
# result["decisions"] → List of architectural decisions
# result["constraints"] → Deployment and performance constraints
```

**Output:**
```python
{
    "mode": "architecture-decision",
    "pattern": "microservices",
    "technology": "python-fastapi-rabbitmq-redis",
    "decisions": [
        "Use event-driven architecture with RabbitMQ...",
        "Implement saga pattern...",
        "Add circuit-breaker pattern...",
        "Implement caching layer...",
        "Deploy microservices independently"
    ],
    "detectedPatterns": [
        "Event-Driven Architecture",
        "Saga Pattern",
        "Fault Tolerance",
        "Performance Optimization",
        "Service Boundaries"
    ],
    "constraints": {
        "maxLatency": "500ms",
        "availability": "99.9%",
        "scalability": "horizontal",
        "dataConsistency": "eventual"
    },
    "processingSteps": [
        "parse_decisions",
        "load_technology_patterns",
        "identify_generation_needs",
        "map_existing_code",
        "generate_bridges",
        "create_monitoring"
    ]
}
```

## Example 4: Text Requirements → Code

Generate code from text-based requirements (backward compatible mode).

```python
input_data = RequirementsInput(
    text="Create a login form component with email validation, password strength indicator, and remember-me checkbox",
    context="React application using Material-UI",
    examples=[
        "User enters email",
        "Real-time validation feedback",
        "Password strength meter",
        "Remember me option"
    ]
)

result = await pipeline.process(input_data)

# Output: {"requirements": "Create a login form..."}
```

## Integration Example: Full Workflow

Process multiple input types in sequence to build a complete application:

```python
pipeline = ProcessingPipeline()

# Step 1: Design image → Components
design_result = await pipeline.process(
    DesignImageInput(image=design_bytes, designTool="figma")
)
print(f"Generated {design_result['analysis']['componentCount']} components")

# Step 2: OpenAPI → Database models & routes
api_result = await pipeline.process(
    APISpecInput(spec=openapi_spec, technology="fastapi", database="postgresql")
)
print(f"Generated {api_result['endpoints']['count']} API endpoints")

# Step 3: Architecture → Implementation
arch_result = await pipeline.process(
    ArchitectureInput(decisions=["event-driven"], pattern="microservices", ...)
)
print(f"Detected patterns: {', '.join(arch_result['detectedPatterns'])}")

# Step 4: Combine outputs
app_structure = {
    "components": design_result["componentSkeletons"],
    "models": api_result["generatedCode"]["databaseModels"],
    "routes": api_result["generatedCode"]["routes"],
    "patterns": arch_result["detectedPatterns"],
    "accessibility": design_result["accessibilityValidation"]
}

# Write generated code to files
```

## Concurrent Processing Example

Process multiple inputs in parallel:

```python
import asyncio

pipeline = ProcessingPipeline()

inputs = [
    DesignImageInput(image=img1, designTool="figma"),
    DesignImageInput(image=img2, designTool="sketch"),
    APISpecInput(spec=spec1, technology="fastapi", database="postgresql"),
    ArchitectureInput(decisions=decisions, pattern="microservices", ...)
]

# Process all concurrently
results = await asyncio.gather(
    *[pipeline.process(inp) for inp in inputs]
)

print(f"Processed {len(results)} inputs successfully")
```

## Error Handling

The generated FastAPI routes include comprehensive error handling:

```python
# All generated routes follow this pattern:
@router.get("/endpoint")
async def endpoint_handler():
    """Endpoint description"""
    try:
        # Implementation
        return {"status": "success", "data": result}
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail="Invalid input")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Performance Characteristics

- **Design image analysis**: ~2-5 seconds (depends on image complexity)
- **OpenAPI parsing**: ~100-500ms (scales with endpoint count)
- **Architecture pattern detection**: ~10-50ms
- **Concurrent processing**: Linear scaling with CPU cores

## Accessibility Validation

Design-to-React processing includes automatic accessibility checking:

```python
accessibility_report = result["accessibilityValidation"]
# {
#     "issues": ["submit button missing aria-label"],
#     "recommendations": ["Verify color contrast for buttons"],
#     "isAccessible": False
# }

if not accessibility_report["isAccessible"]:
    print(f"Accessibility issues found: {accessibility_report['issues']}")
```

## Next Steps

1. Review generated code for your specific needs
2. Integrate with your build system
3. Add business logic implementation
4. Run generated tests
5. Deploy to your environment

For more details, see:
- [Vision Processor API](../specifications/VISION_PROCESSOR_API.md)
- [OpenAPI Parser API](../specifications/OPENAPI_PARSER_API.md)
- [Pipeline Architecture](../guides/architecture/PHASE_11_ARCHITECTURE.md)
