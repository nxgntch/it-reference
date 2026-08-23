# Phase 11: Skill Extensions - Detailed Design

**Focus**: Enhance codeGeneration skill to accept multiple input types  
**Target**: Production-ready multi-modal code generation  
**Timeline**: Week 1 (3-4 days)

---

## Overview

Currently, `codeGeneration` accepts text-based requirements and specifications. Phase 11 extends it to accept design images, API specifications, and architectural decisions as inputs, creating a true multi-modal skill.

### Current vs. Enhanced

| Aspect | v1.0 (Current) | v2.0 (Phase 11) |
|--------|----------------|-----------------|
| **Input Types** | Text (requirements/specs) | Design images, API specs, architecture, requirements |
| **Processing** | Direct prompt engineering | Mode detection → specialized pipeline |
| **Output Quality** | Good (text-based constraints) | Excellent (visual + structural constraints) |
| **Use Cases** | From requirements → code | From design/API → production code |
| **Complexity** | Standard | High (multi-modal) |

---

## Architecture

### Input Processing Pipeline

```
User Input
    ↓
[Mode Detection]
    ├─ requirements-spec → Text mode
    ├─ design-image → Vision mode
    ├─ api-spec → Structured mode
    └─ architecture-decision → Context mode
    ↓
[Input Validation]
    └─ Type checks, format validation
    ↓
[Context Extraction]
    ├─ Parse design constraints
    ├─ Extract API schemas
    ├─ Load architectural context
    └─ Load existing requirements
    ↓
[Code Generation]
    ├─ Generate implementation
    ├─ Add integration points
    └─ Create test suite
    ↓
Output: Code + Tests + Integration Guide
```

---

## Input Modes Specification

### Mode 1: Design Image Input

**Purpose**: Generate code from UI/UX design images

**Input**:
```python
class DesignImageInput:
    image: bytes  # PNG/JPG design mockup
    designTool: str  # "figma" | "sketch" | "adobe"
    designSystem: Optional[str]  # Link to design tokens
    requirements: Optional[str]  # Text requirements
```

**Processing**:
1. Upload image to Claude's vision API
2. Extract layout, components, interactions
3. Identify design patterns (buttons, cards, modals, etc.)
4. Map to component library if available
5. Generate responsive code

**Output**:
```python
class GeneratedCode:
    component: str  # React/Vue/HTML
    styles: str  # CSS with responsive breakpoints
    interactions: str  # Event handlers, state management
    tests: str  # Component tests
    integrationPoints: List[str]  # How to integrate
```

**Example**:
```python
# Input: Design image of a login form
input = DesignImageInput(
    image=read_image("login_design.png"),
    designTool="figma",
    designSystem="https://design.company.com/tokens",
    requirements="Login form with email/password, remember me, 2FA"
)

output = codeGeneration(input, mode="design-image")
# Output: Full login component with tests
```

**Testing**:
- [ ] Test with Figma design export
- [ ] Test with Sketch mockup
- [ ] Test responsive design generation
- [ ] Test component library mapping
- [ ] Test accessibility compliance (WCAG)

---

### Mode 2: API Specification Input

**Purpose**: Generate server code from API schema

**Input**:
```python
class APISpecInput:
    spec: dict  # OpenAPI/Swagger spec (JSON)
    technology: str  # "fastapi" | "express" | "django"
    database: str  # "postgresql" | "mongodb" | "dynamodb"
    requirements: Optional[str]  # Additional requirements
    existingCode: Optional[str]  # Existing implementation
```

**Processing**:
1. Parse OpenAPI/Swagger specification
2. Extract endpoints, methods, parameters, responses
3. Identify data models and relationships
4. Generate database schema
5. Implement CRUD operations
6. Add authentication/authorization hooks

**Output**:
```python
class GeneratedAPI:
    routes: str  # Endpoint implementations
    models: str  # Data models/schemas
    migrations: str  # Database migrations
    tests: str  # API tests (integration + unit)
    documentation: str  # API docs with examples
```

**Example**:
```python
# Input: OpenAPI spec for user management API
input = APISpecInput(
    spec=load_openapi("users_api.yaml"),
    technology="fastapi",
    database="postgresql",
    requirements="Add audit logging, soft deletes, team isolation"
)

output = codeGeneration(input, mode="api-spec")
# Output: Full API implementation with tests
```

**Testing**:
- [ ] Test with OpenAPI 3.0 spec
- [ ] Test with Swagger 2.0 spec
- [ ] Test code matches spec exactly
- [ ] Test authentication generation
- [ ] Test database migrations correct

---

### Mode 3: Architecture Decision Input

**Purpose**: Generate implementation code from architectural decisions

**Input**:
```python
class ArchitectureInput:
    decisions: List[str]  # Architectural decisions
    pattern: str  # "microservices" | "monolith" | "serverless"
    technology: str  # Stack (e.g., "python-fastapi-postgresql")
    constraints: dict  # Performance, security, scaling
    existingCode: Optional[str]  # What to extend
```

**Processing**:
1. Parse architectural decisions
2. Load technology stack patterns
3. Identify code generation needs for each decision
4. Map to existing code structure
5. Generate bridging code and interfaces

**Output**:
```python
class GeneratedArchitecture:
    serviceDefinitions: str  # Service boundaries
    interfaces: str  # Inter-service communication
    configuration: str  # Infrastructure config
    monitoring: str  # Observability hooks
    tests: str  # Architecture tests
```

**Example**:
```python
# Input: Architectural decisions for event-driven system
input = ArchitectureInput(
    decisions=[
        "Use event-driven architecture for real-time updates",
        "Queue messages in Redis for durability",
        "Implement circuit breaker for external APIs",
        "Use saga pattern for distributed transactions"
    ],
    pattern="microservices",
    technology="python-fastapi-postgresql-redis",
    constraints={
        "maxLatency": 100,  # ms
        "minThroughput": 1000,  # requests/sec
        "availability": 0.999  # 99.9% uptime
    }
)

output = codeGeneration(input, mode="architecture-decision")
# Output: Event-driven system implementation
```

**Testing**:
- [ ] Test architectural pattern generation
- [ ] Test interface correctness
- [ ] Test configuration generation
- [ ] Test monitoring hooks
- [ ] Test latency/throughput compliance

---

### Mode 4: Requirements Specification Input (Existing)

**Purpose**: Generate code from text requirements

**Input**:
```python
class RequirementsInput:
    text: str  # Detailed requirements
    context: Optional[str]  # Project context
    examples: Optional[List[str]]  # Example use cases
```

**Processing**:
1. Parse requirements using LLM
2. Identify scope and constraints
3. Generate code addressing all requirements
4. Create comprehensive tests
5. Document integration points

**Output**:
```python
class GeneratedCode:
    code: str
    tests: str
    documentation: str
    integrationPoints: List[str]
```

---

## Implementation Detail

### Mode Detection Algorithm

```python
def detectInputMode(input_data) -> str:
    """Detect which mode to use based on input type"""
    
    if isinstance(input_data, DesignImageInput):
        return "design-image"
    elif isinstance(input_data, APISpecInput):
        return "api-spec"
    elif isinstance(input_data, ArchitectureInput):
        return "architecture-decision"
    elif isinstance(input_data, RequirementsInput):
        return "requirements-spec"
    else:
        # Default: treat as text requirements
        return "requirements-spec"
```

### Enhanced Skill Definition

**File**: `config/skills.yaml`

```yaml
codeGeneration:
  version: "2.0"
  description: "Generate production-ready code from multiple input types"
  
  capabilities:
    - design-image: "Convert UI designs to code"
    - api-spec: "Implement APIs from OpenAPI/Swagger specs"
    - architecture-decision: "Generate architecture-driven code"
    - requirements-spec: "Generate code from text requirements"
  
  inputModes:
    - name: "design-image"
      description: "Accept design images (PNG/JPG)"
      tool: "claude-vision"
      examples:
        - Figma exports
        - Sketch mockups
        - Adobe XD designs
      
    - name: "api-spec"
      description: "Accept API specifications"
      tool: "openapi-parser"
      formats:
        - OpenAPI 3.0
        - Swagger 2.0
      
    - name: "architecture-decision"
      description: "Accept architectural decisions"
      tool: "decision-parser"
      patterns:
        - microservices
        - monolith
        - serverless
        - event-driven
      
    - name: "requirements-spec"
      description: "Accept text requirements (existing)"
      tool: "text-prompt"
  
  model: "claude-3.5-sonnet"
  costTier: "high"
  latency: "< 30 seconds"
  qualityTarget: "production-ready"
```

---

## Quality Standards

### Code Generation Quality

- ✅ **Syntactically correct** - Code must compile/run without errors
- ✅ **Follows project style** - Matches existing code conventions
- ✅ **Well-tested** - Includes comprehensive test suite
- ✅ **Documented** - Has docstrings and integration guide
- ✅ **Performant** - Meets latency/throughput targets
- ✅ **Secure** - Follows security best practices (OWASP)
- ✅ **Accessible** - Meets WCAG standards (for UI code)

### Testing Strategy

#### Unit Tests
```python
def test_design_image_mode():
    """Test design image input mode"""
    input = DesignImageInput(image=test_image)
    output = codeGeneration(input, mode="design-image")
    assert output.component is not None
    assert output.styles is not None
    assert len(output.tests) > 0

def test_api_spec_mode():
    """Test API spec input mode"""
    input = APISpecInput(spec=test_spec)
    output = codeGeneration(input, mode="api-spec")
    assert spec_matches_code(test_spec, output.routes)

def test_architecture_mode():
    """Test architecture decision input mode"""
    input = ArchitectureInput(decisions=test_decisions)
    output = codeGeneration(input, mode="architecture-decision")
    assert all_patterns_implemented(test_decisions, output)
```

#### Integration Tests
```python
def test_design_to_code_integration():
    """Test design image → code → test → verified"""
    # 1. Generate from design
    code = codeGeneration_from_design(test_design)
    
    # 2. Compile code
    assert compiles(code)
    
    # 3. Run generated tests
    test_results = run_tests(code.tests)
    assert test_results.passed == test_results.total
    
    # 4. Verify design compliance
    assert design_compliance_check(code.component, test_design)
```

#### Acceptance Tests
```python
def test_example_use_cases():
    """Test real-world use cases"""
    # Use case 1: Convert Figma design to React component
    # Use case 2: Generate FastAPI from OpenAPI spec
    # Use case 3: Implement event-driven architecture
    # Use case 4: Generate from requirements
```

---

## Examples & Documentation

### Example 1: Design Image → React Component

**Input**: Figma design export (login form)

**Generated Output**:
```jsx
// components/LoginForm.jsx
import React, { useState } from 'react';
import styles from './LoginForm.module.css';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    // Integration point: call login API
  };
  
  return (
    <div className={styles.container}>
      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={styles.input}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={styles.input}
          required
        />
        <label className={styles.checkbox}>
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
          />
          Remember me
        </label>
        <button type="submit" className={styles.button}>
          Login
        </button>
      </form>
    </div>
  );
}
```

**Generated Tests**:
```jsx
// components/LoginForm.test.jsx
import { render, screen, fireEvent } from '@testing-library/react';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('should render email and password inputs', () => {
    render(<LoginForm />);
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
  });
  
  it('should call submit handler on form submission', () => {
    // Test implementation
  });
  
  it('should meet WCAG 2.1 AA standards', () => {
    // Accessibility tests
  });
});
```

---

### Example 2: OpenAPI Spec → FastAPI

**Input**: User management API spec

**Generated Output**:
```python
# routers/users.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# ... more endpoints matching spec
```

---

## Phase 11 → Phase 12 Handoff

After Phase 11, codeGeneration will be the foundation for Phase 12's new design skills:

1. **Design Optimization** - Uses codeGeneration's design-image mode to enhance existing designs
2. **Design & UX Enforcement** - Uses codeGeneration to generate code ensuring WCAG compliance

---

## Success Criteria

- [ ] All 4 input modes working
- [ ] 100% of generated code is syntactically correct
- [ ] All generated tests pass
- [ ] Code matches input specs exactly
- [ ] Design compliance validated
- [ ] API routes match OpenAPI spec
- [ ] Architecture implementation correct
- [ ] Documentation complete with examples
- [ ] No regressions in requirements-spec mode

---

**Status**: Ready for Phase 11 Week 1 implementation  
**Last Updated**: 2026-08-22
