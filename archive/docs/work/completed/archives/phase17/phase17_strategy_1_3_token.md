# Phase 17 Initiative 1.3: Token Optimization for Cost Reduction

**Goal**: Reduce token usage by 15-20%  
**Baseline**: TestTokenOptimizerIntegrationParametrized passing (6/6 tests)  
**Target**: ≥15% token reduction, measured cost savings  
**Week**: 3 (9/8-9/14)  
**Effort**: 18-22 hours

---

## Current Baseline Status

**Test Results**: 6/6 PASSING ✅
- Architect short prompt: PASS
- Researcher medium prompt: PASS
- Coordinator long prompt: PASS
- Verbose style compression: PASS
- Concise style compression: PASS
- Moderate style compression: PASS

**Baseline Metrics to Capture**:
- Current tokens/task for each agent: ___ tokens
- Current tokens/task by prompt length: ___ tokens
- Compression ratio by style: ___ %

**Cost Calculation** (example):
- Current: 150 tokens/task × $0.00125 (haiku) = $0.1875/task
- Target: 128 tokens/task × $0.00125 = $0.16/task
- Savings: $0.0275/task (14.7% cost reduction)

---

## Token Usage Analysis

### Current Patterns

**By Agent Type**:
- Architect (complex design): 200-300 tokens
- Researcher (data analysis): 150-250 tokens
- Coordinator (task management): 80-150 tokens

**By Prompt Style**:
- Verbose (extensive context): 300+ tokens
- Moderate (balanced): 150-200 tokens
- Concise (minimal): 80-120 tokens

**Opportunities**:
1. Verbose prompts have 3-4x overhead
2. Redundant instructions in prompts
3. Unused context sections
4. Repetitive examples in few-shot

---

## Optimization Strategy

### Phase 1.3.1: Token Usage Analysis

**Identify High-Token Patterns**:
```python
# Analyze TestTokenOptimizerIntegrationParametrized results
from collections import defaultdict

token_usage = defaultdict(list)
for test_result in test_results:
    agent = test_result['agent_type']
    tokens = test_result['token_count']
    style = test_result['prompt_style']
    
    token_usage[f"{agent}_{style}"].append(tokens)

# Find top contributors
for pattern, tokens in sorted(token_usage.items(), key=lambda x: sum(x[1]), reverse=True):
    avg = sum(tokens) / len(tokens)
    print(f"{pattern}: {avg:.0f} tokens avg")
```

**Target Reduction Areas** (in order):
1. Verbose architect prompts (-30% target)
2. Redundant coordinator instructions (-25% target)
3. Researcher context bloat (-20% target)

---

### Phase 1.3.2: Prompt Compression & Refinement

**Optimization 1: Remove Redundant Instructions**

*Current* (example):
```
You are an architect. Your role is to design systems.
Design a system according to the following requirements.
Consider performance, scalability, and maintainability.
[30+ line prompt with repeated guidance]
```

*Target*:
```
Architect: Design a system for:
[Requirements]

Focus: performance, scalability, maintainability
```

**Token Reduction**: 40-50% (60-80 tokens saved)

---

**Optimization 2: Consolidate Few-Shot Examples**

*Current* (likely):
```
Example 1: [20 tokens]
Example 2: [20 tokens]
Example 3: [20 tokens]
(3-5 examples = 60-100 tokens)
```

*Target*:
```
Example: [15 tokens]
(1-2 examples = 15-30 tokens)
```

**Token Reduction**: 50-70% (30-70 tokens saved)

---

**Optimization 3: Use Prompt Templates**

*Current*:
```
Full prompt for each task = 150-300 tokens each
```

*Target*:
```
Template: [80 tokens]
+ Task-specific data: [20-40 tokens]
= Total: 100-120 tokens per task
```

**Token Reduction**: 25-33% (30-50 tokens saved per task)

---

**Optimization 4: Context Window Management**

*Current* (likely):
- Include full conversation history (500+ tokens)
- All available examples (200+ tokens)
- All context sections (200+ tokens)

*Target*:
- Last 2 messages only (100 tokens)
- 1-2 relevant examples (30 tokens)
- Required context only (100 tokens)

**Token Reduction**: 40-50% (400+ tokens saved)

---

### Phase 1.3.3: Cost Impact Measurement

**Re-run Token Optimizer Tests**:
```bash
pytest tests/test_performance_optimization_and_batching.py::TestTokenOptimizerIntegrationParametrized -v
```

**Measure Results**:
- Architect tokens (target: 140-180 tokens)
- Researcher tokens (target: 120-160 tokens)
- Coordinator tokens (target: 60-100 tokens)
- All 3 styles (verbose, concise, moderate)

**Calculate Cost Savings**:
```python
# Before optimization
before_tokens = 150_000  # tokens/month across all tasks
before_cost = (150_000 / 1000) * 0.00125  # haiku pricing
# before_cost ≈ $187.50/month

# After optimization
after_tokens = 127_500  # 15% reduction
after_cost = (127_500 / 1000) * 0.00125
# after_cost ≈ $159.38/month

savings = before_cost - after_cost  # $28.12/month
savings_pct = (1 - after_tokens/before_tokens) * 100  # 15%
```

**Success Criteria**:
- [ ] All 6 tests still passing (no regressions)
- [ ] Token usage reduced by ≥15%
- [ ] Output quality maintained (no degradation)
- [ ] Cost savings calculated and documented
- [ ] AUDIT.md updated with savings amount

---

## Implementation Checklist

**Week 3 Monday-Wednesday (9/8-9/10)**: Implementation
- [ ] Analyze current token usage patterns
- [ ] Remove redundant instructions (-30%)
- [ ] Consolidate few-shot examples (-50%)
- [ ] Create prompt templates
- [ ] Optimize context window usage

**Week 3 Thursday-Friday (9/11-9/12)**: Validation
- [ ] Run TestTokenOptimizerIntegrationParametrized
- [ ] Measure token reduction
- [ ] Verify output quality unchanged
- [ ] Calculate cost savings
- [ ] Commit optimized prompts

---

## Code Quality Requirements

- [ ] Prompts well-documented with inline comments
- [ ] Template variables clearly named
- [ ] No hardcoded context windows
- [ ] Test coverage maintained (≥85%)
- [ ] Follows `.claude/rules/communication-and-style.md`

---

## Metrics to Track

After implementation, update AUDIT.md:

```
Initiative 1.3 Results:
- Architect token reduction: [before] → [after] tokens ([%]% reduction)
- Researcher token reduction: [before] → [after] tokens ([%]% reduction)
- Coordinator token reduction: [before] → [after] tokens ([%]% reduction)
- Overall reduction: [%]%
- Monthly cost savings: $[amount]
- Output quality: [maintained/degraded] (verify manually)
- Test pass rate: 6/6 (100%)
```

---

## References

- **Baseline**: `phase17_baseline.json` → token.tests_passed = 6/6
- **Test Class**: `TestTokenOptimizerIntegrationParametrized` (6 tests, 3 agents)
- **Phase 16 Archive**: `docs/work/completed/phase-16-archive/README.md`
- **Task Breakdown**: `docs/work/planned/phase-17-task-breakdown.md` § 1.3

---

**Status**: READY FOR WEEK 3 IMPLEMENTATION  
**Last Updated**: 2026-08-27
