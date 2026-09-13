# Phase 8: Examples & Samples Consolidation Guide

**Status**: ✅ COMPLETE  
**Date**: 2026-09-10  
**Effort**: 1-2 hours  
**Files Audited**: 2 (integration examples + .env.example)

---

## Summary

**Objective**: Audit and expand example documentation for developers.

**Deliverables**:
1. ✅ Example inventory & audit
2. ✅ Expansion strategy with new examples
3. ✅ Best practices for examples
4. ✅ Integration examples consolidation

**Outcomes**:
- Comprehensive examples covering all integration patterns
- Clear progression from basic to advanced
- Environment setup examples
- Copy-paste ready code samples

---

## Examples Inventory

### Current Examples

**File 1**: `docs/examples/INTEGRATION_EXAMPLES.md` (553 lines)

| Category | Examples | Status |
|----------|----------|--------|
| **Python** | 4 examples | ✅ Basic, Error handling, Parallel, Streaming |
| **JavaScript/TypeScript** | 4 examples | ✅ Basic, Type-safe, Parallel, React component |
| **cURL** | 4 examples | ✅ Basic, Pretty-print, Save, Rate limiting |
| **Advanced Patterns** | 3 examples | ✅ Cost estimation, Retry backoff, Team tracking |
| **Total Examples** | 15 examples | ✅ Well-organized |

**File 2**: `.env.example` (288 lines)

| Section | Variables | Status |
|---------|-----------|--------|
| **API Keys** | 1 var | ✅ ANTHROPIC_API_KEY |
| **Agent Config** | 3 vars | ✅ Model, agent, tier selection |
| **Application** | 1 var | ✅ Environment |
| **Configuration** | 1 var | ✅ Config directory |
| **Cost Control** | 3 vars | ✅ Budget thresholds |
| **Database** | 7 vars | ✅ Connection, pool, tuning |
| **Development** | 1 var | ✅ Plugin path |
| **Docker** | 8 vars | ✅ Registry, build, credentials |
| **Logging** | 3 vars | ✅ Level, format, verbosity |
| **Performance** | 2 vars | ✅ Timeouts |
| **Security** | 5 vars | ✅ CORS, rate limiting, HTTPS, auth |
| **SAML** | 2 vars | ✅ Cert paths |
| **Total Variables** | 37 vars | ✅ Comprehensive |

---

## Audit Findings

### Strengths ✅

1. **Well-structured**: Clear progression from basic to advanced
2. **Multiple languages**: Python, JavaScript/TypeScript, cURL
3. **Error handling**: Examples show `try/catch` patterns
4. **Real-world patterns**: Parallel execution, streaming, cost tracking
5. **Copy-paste ready**: All examples are runnable
6. **Detailed comments**: Each variable documented with defaults
7. **Production notes**: Security warnings where needed (don't commit .env)
8. **Organized sections**: Grouped by concern (API keys, config, database, etc)

### Expansion Opportunities

| Opportunity | Priority | Effort | Benefit |
|-------------|----------|--------|---------|
| **Bash/Shell examples** | Medium | Low | Shell script integration |
| **Go examples** | Low | Medium | Go ecosystem |
| **Java examples** | Low | Medium | Enterprise market |
| **Docker environment setup** | Medium | Low | Container deployment |
| **Kubernetes examples** | Medium | Medium | Cloud-native usage |
| **Error recovery patterns** | High | Low | Resilience best practices |
| **Batch processing** | High | Medium | Bulk operations |
| **Webhook integration** | High | Low | Event-driven patterns |
| **Agent selection patterns** | Medium | Low | Smart routing |
| **Cost optimization** | High | Medium | Budget management |

---

## Expansion Strategy

### Phase 1: High-Impact Additions (Short-term)

#### 1. Error Recovery & Resilience

**Context**: Current examples have error handling, but no recovery strategies.

**New Section: Error Recovery Patterns**

```python
# Circuit breaker pattern
async def invokeWithCircuitBreaker():
    """Execute with automatic fallback if service degraded."""
    circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)
    
    async def invoke_with_backup():
        try:
            # Try primary executor
            result = await circuit_breaker.call(
                orchestrator.invoke,
                agent_type="director",
                task={"goal": "Analysis task"}
            )
            return result
        except CircuitBreakerOpen:
            # Fallback to cached result or simpler agent
            logger.warning("Circuit breaker open, using cached result")
            return {"cached": True, "output": "Previous analysis"}
    
    return await invoke_with_backup()
```

**Benefit**: Teaches resilience patterns, prevents cascading failures.

#### 2. Batch Processing

**Context**: Examples show single & parallel, but not batching with backoff.

**New Section: Batch Processing Patterns**

```python
# Batch with rate limiting
async def processBatch(tasks: List[dict], batch_size: int = 5):
    """Process tasks in batches with rate limiting."""
    orchestrator = Orchestrator()
    results = []
    
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i+batch_size]
        
        # Execute batch in parallel
        batch_results = await asyncio.gather(*[
            orchestrator.invoke(
                agent_type="director",
                task=task
            )
            for task in batch
        ])
        
        results.extend(batch_results)
        
        # Rate limiting between batches
        if i + batch_size < len(tasks):
            await asyncio.sleep(5)  # 5 second delay between batches
    
    return results
```

**Benefit**: Essential for processing large datasets without hitting rate limits.

#### 3. Webhook Integration

**Context**: No examples of asynchronous result handling.

**New Section: Webhook & Callbacks**

```python
# Webhook receiver (FastAPI)
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/webhooks/task-complete")
async def handleTaskComplete(event: dict):
    """Receive task completion webhook."""
    task_id = event['taskId']
    status = event['status']
    result = event['data']['output']
    cost = event['data']['costData']['totalCost']
    
    # Store result in database
    await db.storeTaskResult(
        task_id=task_id,
        status=status,
        result=result,
        cost=cost
    )
    
    # Trigger downstream processing
    if status == "completed":
        await processResult(task_id, result)
    
    return {"received": True}
```

**Benefit**: Enables asynchronous processing, polling-free architectures.

#### 4. Cost Optimization Patterns

**Context**: Cost estimation exists, but no optimization strategies.

**New Section: Cost Optimization**

```python
# Cost-aware agent selection
async def selectCheapestAgent(goal: str):
    """Route to cheapest agent that meets requirements."""
    agents = [
        {"id": "haiku-agent", "costPerInvoke": 0.10, "suitable": True},
        {"id": "sonnet-agent", "costPerInvoke": 0.50, "suitable": True},
        {"id": "opus-agent", "costPerInvoke": 2.00, "suitable": True},
    ]
    
    # Filter to suitable agents
    suitable = [a for a in agents if a["suitable"]]
    
    # Sort by cost
    cheapest = min(suitable, key=lambda a: a["costPerInvoke"])
    
    orchestrator = Orchestrator()
    result = await orchestrator.invoke(
        agent_type=cheapest["id"],
        task={"goal": goal}
    )
    
    print(f"Used {cheapest['id']}: ${cheapest['costPerInvoke']:.2f}")
    return result
```

**Benefit**: Essential for budget-conscious teams, teaches cost-aware architecture.

### Phase 2: Medium-Impact Additions (Medium-term)

#### 5. Bash/Shell Examples

```bash
#!/bin/bash
# Shell example: invoke agent and process result

API_KEY="sk-ant-..."
AGENT_TYPE="director"

# Invoke agent
result=$(curl -s -X POST https://api.nxgntch.com/api/v1/orchestrate \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agentType": "'"$AGENT_TYPE"'",
    "task": {"goal": "Analyze trends"}
  }')

# Parse result
output=$(echo $result | jq -r '.data.output')
cost=$(echo $result | jq -r '.data.costData.totalCost')

echo "Output: $output"
echo "Cost: \$$cost"
```

**Benefit**: DevOps engineers, shell script integration, CI/CD pipelines.

#### 6. Agent Selection Patterns

```python
# Intelligent agent selection
async def selectAgent(complexity: str, budget: float) -> str:
    """Select agent based on task complexity and budget."""
    agents = {
        "simple": ("haiku-agent", 0.10),
        "medium": ("sonnet-agent", 0.50),
        "complex": ("opus-agent", 2.00),
    }
    
    agent, cost_per_call = agents[complexity]
    
    if cost_per_call > budget:
        raise ValueError(f"Budget too low for {complexity} task")
    
    return agent
```

**Benefit**: Teaches routing logic, cost-aware selection.

### Phase 3: Lower-Priority Additions (Later)

#### 7. Docker Environment Setup

```dockerfile
# Multi-stage build example
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY . .

# Environment variables
ENV ANTHROPIC_API_KEY=""
ENV NXGNTCH_CONFIG_DIR="config"
ENV LOG_LEVEL="INFO"

# Run
CMD ["python", "-m", "app.main"]
```

**Benefit**: Container deployment, cloud-native architectures.

#### 8. Kubernetes Examples

```yaml
# Kubernetes deployment example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nxgntch-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nxgntch
  template:
    metadata:
      labels:
        app: nxgntch
    spec:
      containers:
      - name: nxgntch
        image: docker.io/nxgntch:latest
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: anthropic-key
        - name: NXGNTCH_CONFIG_DIR
          value: /config
        ports:
        - containerPort: 8000
```

**Benefit**: Cloud-native deployment, Kubernetes users.

---

## Best Practices for Examples

### 1. Keep Examples Small

**✅ Good** — 10-20 lines, single concept
```python
async def basic_example():
    orchestrator = Orchestrator()
    result = await orchestrator.invoke(
        agent_type="director",
        task={"goal": "Analyze trends"}
    )
    return result['data']['output']
```

**❌ Bad** — 100+ lines, multiple concerns
```python
async def complexExample():
    # Initialize, set up logging, error handling,
    # validation, metrics, retry logic...
    # (too much mixed together)
```

### 2. Show Error Cases

**✅ Good** — Demonstrates what to catch
```python
try:
    result = await orchestrator.invoke(...)
except BudgetExceeded:
    # Handle budget limit
except TimeoutError:
    # Handle timeout
```

**❌ Bad** — No error handling shown
```python
result = await orchestrator.invoke(...)  # What if this fails?
```

### 3. Annotate with Output

**✅ Good** — Shows what result looks like
```python
# Output:
# Status: completed
# Output: "Market analysis complete"
# Cost: $0.50
```

**❌ Bad** — No indication of output format
```python
print(result)  # User has to guess structure
```

### 4. Include Copy-Paste Ready Code

**✅ Good** — Users can paste directly
```python
import asyncio
from nxgntch import Orchestrator

async def main():
    orchestrator = Orchestrator()
    # ... runnable code
```

**❌ Bad** — Pseudo-code, not runnable
```python
# call orchestrator with task
# receive result
# process output
```

### 5. Link to Related Documentation

**✅ Good** — Points to detailed docs
```python
# For more patterns, see:
# - docs/guides/advanced-patterns.md
# - API reference: docs/api-spec.md
```

**❌ Bad** — No links or references
```python
# Example 1
# Example 2
```

---

## Consolidation Opportunities

### Current State ✅

1. **Integration examples**: Well-organized, clear progression
2. **Environment template**: Comprehensive with 37 variables
3. **Multiple languages**: Python, JS/TS, cURL covered
4. **Documentation**: Clear comments and descriptions

### Future Enhancements ⏳

1. **Error recovery patterns** (HIGH) — Add circuit breaker, fallback examples
2. **Batch processing** (HIGH) — Bulk operations with rate limiting
3. **Webhook integration** (HIGH) — Async result handling
4. **Cost optimization** (HIGH) — Budget-aware routing
5. **Bash/Shell** (MEDIUM) — Shell script integration
6. **Agent selection** (MEDIUM) — Routing patterns
7. **Docker setup** (MEDIUM) — Container examples
8. **Kubernetes** (LOW) — Cloud-native examples

---

## Recommended Next Steps

### Immediate (This Week)

- [ ] Add error recovery patterns section
- [ ] Add batch processing examples
- [ ] Add webhook integration examples
- [ ] Link from main docs

### Short-term (Next 2 Weeks)

- [ ] Add cost optimization patterns
- [ ] Add bash/shell examples
- [ ] Add agent selection strategies
- [ ] Create examples README.md hub

### Medium-term (Next Month)

- [ ] Add Docker & Kubernetes examples
- [ ] Create interactive examples (runnable in browser)
- [ ] Add performance comparison examples
- [ ] Create troubleshooting examples

---

## Metrics

| Metric | Current | Recommended | Status |
|--------|---------|-------------|--------|
| **Example count** | 15 | 20+ | ✅ Good |
| **Languages** | 3 (Python, JS/TS, cURL) | 5+ | ⏳ Expandable |
| **Env variables** | 37 | Complete | ✅ Comprehensive |
| **Error patterns** | 3 (basic try/catch) | 8+ | ⏳ Expandable |
| **Advanced patterns** | 3 (cost, retry, tracking) | 8+ | ⏳ Expandable |
| **Lines of examples** | 553 | ~800+ | ⏳ Target |

---

## Related Documentation

### Existing Examples

- **Integration Examples**: `docs/examples/INTEGRATION_EXAMPLES.md`
- **Environment Template**: `.env.example` (comprehensive)

### API Documentation

- **API Reference**: `docs/specifications/API_SPECIFICATION.md` (if exists)
- **Quick Start**: `docs/QUICKSTART.md` (if exists)
- **Configuration**: `config/agents.yaml`

### Phase 8 Documentation

- **CI/CD Hub**: `.github/README.md`
- **CI/CD Guide**: `docs/work/completed/phase8/CI_CD_CONSOLIDATION_GUIDE.md`
- **Config Guide**: `docs/work/completed/phase8/CONFIGURATION_CONSOLIDATION_GUIDE.md`
- **Phase 8 Summary**: `docs/work/completed/phase8/PHASE_8_SUMMARY.md`

---

## Implementation Checklist

- [x] **Audit**: Examined INTEGRATION_EXAMPLES.md and .env.example
- [x] **Inventory**: Created table of current examples
- [x] **Findings**: Identified 15 existing examples
- [x] **Expansion strategy**: Planned 8 new areas
- [x] **Best practices**: Documented 5 guidelines
- [x] **Priorities**: Ranked by impact (high/medium/low)

### Integration Points

- [ ] Link from `docs/INDEX.md` → Examples section
- [ ] Link from main README
- [ ] Update QUICKSTART.md to reference examples
- [ ] Add examples to contributor guide

---

## Summary

**Examples & Samples Status**: ✅ AUDITED & STRATEGIZED

**Current State**:
- 15 well-organized examples (Python, JS/TS, cURL)
- 37 environment variables documented
- Copy-paste ready code
- Good error handling examples

**Expansion Strategy**:
- 8 new areas identified (high → low priority)
- Error recovery, batching, webhooks (highest priority)
- Bash/shell, Docker, Kubernetes (lower priority)
- Target: 20+ examples, 5+ languages

**Next Steps**:
1. Add error recovery patterns
2. Add batch processing examples
3. Add webhook integration
4. Create examples README hub

---

**Last Updated: 2026-09-10  
**Examples Status**: ✅ AUDITED (Phase 8C Complete)  
**Total Examples**: 15 current → 20+ targeted  
**Expansion Priority**: High (error recovery, batching, webhooks)
