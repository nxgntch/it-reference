# Skills Reference

Complete reference for all 7 integrated skills in NXGNTCH.

---

## Quick Index

| Skill | Workflow | Cost | Duration | Best For |
|-------|----------|------|----------|----------|
| [codeReview](#codeReview) | Code → Review → Security → Perf | ~$0.10 | 60-90s | Comprehensive review |
| [securityReview](#securityReview) | Code → Security → Audit → Verify | ~$0.08 | 45-60s | Security audit |
| [performanceOptimization](#performanceOptimization) | Code → Analysis → Optimization | ~$0.08 | 45-60s | Performance tuning |
| [costAnalysis](#costAnalysis) | Analyze costs → Optimize | ~$0.04 | 30-45s | Cost reduction |
| [docReview](#docReview) | Docs → Quality audit → Improve | ~$0.06 | 30-45s | Documentation quality |
| [agentRouter](#agentRouter) | Task → Analyze → Route | ~$0.03 | 15-30s | Find right agent |
| [costOptimizer](#costOptimizer) | Analyze → Recommend → Plan | ~$0.05 | 30-45s | Cost optimization |

---

## Skill Definitions

### codeReview

**Workflow:** Code Analysis → Code Review → Security Review → Performance Analysis

**What it does:**
Comprehensive code review combining multiple perspectives for complete analysis.

**Steps:**
1. **Code Review** (via `codeReviewer` agent) — General quality, style, best practices
2. **Security Review** (via `securityReviewer` agent) — Vulnerabilities, OWASP compliance
3. **Performance Analysis** (via `performanceOptimizer` agent) — Speed, efficiency
4. **Synthesis** — Combined report with priorities

**Use When:**
- Critical code that needs complete review
- Pull request with security implications
- Code that impacts performance
- Time-sensitive review needed

**Example:**
```
/codeReview
"Review this payment API endpoint:

[code snippet]

Requirements:
- Must be PCI compliant
- Must handle 1000 TPS
- Must have <100ms latency"
```

**Typical Results:**
- Code quality score
- Security findings (with severity)
- Performance recommendations
- Action items prioritized by impact

**Cost:** ~$0.08-0.15 per invocation  
**Duration:** 60-120 seconds  
**Best For:** Critical code, PR reviews, security-sensitive work

---

### securityReview

**Workflow:** Code Analysis → Security Assessment → OWASP Audit → Threat Modeling

**What it does:**
Dedicated security audit checking for vulnerabilities and compliance.

**Steps:**
1. **Security Scan** (via `securityReviewer`) — Vulnerability detection, OWASP Top 10
2. **Threat Model** — Identify attack vectors
3. **Compliance Check** — Standards and regulations
4. **Remediation** — Fix recommendations

**Use When:**
- Security audit needed
- Handling sensitive data
- Public-facing API
- Authentication/authorization code
- Compliance required

**Example:**
```
/securityReview
"Security audit of user authentication flow:
- Login endpoint
- Password reset
- 2FA implementation
- Token handling"
```

**Typical Results:**
- Vulnerability list (by severity)
- Attack vectors identified
- Compliance gaps
- Remediation steps
- Code changes needed

**Cost:** ~$0.06-0.12 per invocation  
**Duration:** 45-90 seconds  
**Best For:** Security-critical code, compliance audits, sensitive data handling

---

### performanceOptimization

**Workflow:** Code Analysis → Bottleneck ID → Optimization Strategies → Benchmarking

**What it does:**
Identifies performance issues and recommends optimizations.

**Steps:**
1. **Performance Analysis** — Identify bottlenecks, measure current performance
2. **Optimization Strategies** — Recommend changes with impact estimates
3. **Implementation Guide** — Step-by-step changes
4. **Benchmarking Plan** — How to verify improvements

**Use When:**
- Code is slow
- Need performance improvement
- Have profiling data
- Scalability concerns
- Latency requirements

**Example:**
```
/performanceOptimization
"Optimize this query:

[database query]

Current: 500ms per request
Need: <50ms per request
Volume: 10k RPS

Database size: 1M rows"
```

**Typical Results:**
- Performance issues identified
- Root cause analysis
- Optimization recommendations
- Expected impact
- Implementation steps

**Cost:** ~$0.06-0.12 per invocation  
**Duration:** 45-90 seconds  
**Best For:** Performance-critical code, scaling issues, latency optimization

---

### costAnalysis

**Workflow:** Cost Data Analysis → Breakdown → Optimization Opportunities → Recommendations

**What it does:**
Analyzes LLM/cloud costs and identifies optimization opportunities.

**Steps:**
1. **Cost Breakdown** — Analyze spending by model, agent, workflow
2. **Trend Analysis** — Identify cost drivers
3. **Opportunity ID** — Where can we save?
4. **ROI Analysis** — What changes are worth it?

**Use When:**
- Monitor monthly spending
- Identify cost overruns
- Budget planning
- Resource optimization
- Cost awareness

**Example:**
```
/costAnalysis
"Analyze last month's costs:

Total: $1,500
- CEO agent: $600
- Architect: $400
- Code reviewer: $300
- Other: $200"
```

**Typical Results:**
- Cost breakdown by agent/model/workflow
- Top cost drivers
- Optimization opportunities
- Potential savings (with effort)
- Budget recommendations

**Cost:** ~$0.03-0.06 per invocation  
**Duration:** 30-45 seconds  
**Best For:** Budget planning, cost monitoring, optimization

---

### docReview

**Workflow:** Documentation Assessment → Quality Audit → Improvement Recommendations

**What it does:**
Reviews documentation quality and suggests improvements.

**Steps:**
1. **Documentation Audit** — Completeness, accuracy, clarity
2. **Quality Check** — Is it helpful to users?
3. **Gap Analysis** — What's missing?
4. **Improvement Plan** — How to improve

**Use When:**
- Documentation needs review
- Updating docs
- New feature documentation
- API documentation
- User guide improvements

**Example:**
```
/docReview
"Review our API documentation:

Current docs:
[documentation text]

Recent changes:
[list of API changes]"
```

**Typical Results:**
- Quality score (clarity, completeness, accuracy)
- Issues found (with severity)
- Missing documentation
- Improvement recommendations
- Update plan

**Cost:** ~$0.04-0.08 per invocation  
**Duration:** 30-60 seconds  
**Best For:** Documentation quality, keeping docs in sync

---

### agentRouter

**Workflow:** Task Analysis → Agent Evaluation → Recommendation

**What it does:**
Analyzes a task and recommends the best agent to handle it.

**Steps:**
1. **Task Analysis** — What is being asked?
2. **Agent Evaluation** — Which agents could help?
3. **Recommendation** — Best agent + reasoning
4. **Alternative Routes** — Backup options

**Use When:**
- Not sure which agent to use
- Complex task needing multiple agents
- Want optimal cost/quality
- Learning what agents do

**Example:**
```
/agentRouter
"What's the best agent for this?

Task: Refactor our authentication module
- Improve code clarity
- Add type hints
- Check security
- Write tests"
```

**Typical Results:**
- Recommended agent (with confidence)
- Why it's the best choice
- Alternative agents (if needed)
- Suggested workflow
- Estimated cost/time

**Cost:** ~$0.01-0.03 per invocation  
**Duration:** 15-30 seconds  
**Best For:** Learning, complex tasks, optimal routing

---

### costOptimizer

**Workflow:** Cost Structure Analysis → Optimization Strategy → Implementation Plan

**What it does:**
Provides strategic cost optimization recommendations and implementation plan.

**Steps:**
1. **Cost Structure Review** — Current spending, drivers, trends
2. **Optimization Strategy** — What should we change?
3. **Implementation Plan** — Steps to implement
4. **ROI Analysis** — Cost/benefit of changes

**Use When:**
- Need to reduce costs
- Budget pressure
- Scaling concerns
- Efficiency improvement
- Strategic cost planning

**Example:**
```
/costOptimizer
"How can we reduce our Claude usage costs?

Current: $10k/month
Target: $5k/month

Current usage:
- 50% architect agent
- 30% code review
- 20% other"
```

**Typical Results:**
- Cost reduction opportunities (with % savings)
- Implementation effort
- Timeline to implement
- Risk assessment
- Expected results

**Cost:** ~$0.03-0.06 per invocation  
**Duration:** 30-45 seconds  
**Best For:** Cost reduction, budget planning, efficiency

---

## Workflow Patterns

### Pattern 1: Comprehensive Code Review

```
/codeReview "My API endpoint"
    ↓
[Code Review + Security + Performance Analysis]
    ↓
Read full report
    ↓
Ask follow-up questions to specific agents if needed
```

**Time:** 60-120s  
**Cost:** ~$0.10  
**When:** Critical code, PRs, complex features

### Pattern 2: Security-First Review

```
/securityReview "Sensitive feature"
    ↓
[Dedicated security audit]
    ↓
Identify vulnerabilities
    ↓
/codeReviewer "Implement security fixes"
```

**Time:** 90-120s + fix time  
**Cost:** ~$0.15  
**When:** Security-critical, handling PII, compliance

### Pattern 3: Performance Optimization Loop

```
/performanceOptimization "Slow code"
    ↓
Get recommendations
    ↓
Implement changes
    ↓
/codeReview "Review the optimization"
    ↓
Profile to verify improvements
```

**Time:** 120-180s  
**Cost:** ~$0.15  
**When:** Performance issues, scaling

### Pattern 4: Cost Monitoring

```
Monthly: /costAnalysis [last month's data]
    ↓
Identify trends
    ↓
If over budget: /costOptimizer [current costs]
    ↓
Implement recommendations
    ↓
Recheck next month
```

**Time:** 60s/month  
**Cost:** ~$0.05  
**When:** Continuous cost management

### Pattern 5: Documentation Sync

```
New feature implemented
    ↓
/docReview [docs + implementation]
    ↓
Identify gaps
    ↓
/doc-updater "Update these sections"
    ↓
/docReview again to verify
```

**Time:** 90-120s  
**Cost:** ~$0.10  
**When:** Feature complete, before release

---

## Skill Composition

### codeReview
- **Primary:** `/codeReviewer` (code quality)
- **Secondary:** `/securityReviewer` (vulnerabilities)
- **Tertiary:** `/performanceOptimizer` (speed)
- **Synthesis:** Combined analysis

### securityReview
- **Primary:** `/securityReviewer` (vulnerabilities)
- **Secondary:** `/codeReviewer` (code quality)
- **Depth:** Threat modeling, OWASP audit

### performanceOptimization
- **Primary:** `/performanceOptimizer` (performance)
- **Secondary:** `/codeExplorer` (understanding code)
- **Depth:** Benchmarking, profiling

### costAnalysis
- **Primary:** Cost data analysis
- **Secondary:** Trend identification
- **Depth:** Driver analysis, ROI

### docReview
- **Primary:** `/docUpdater` (documentation)
- **Secondary:** `/codeExplorer` (understanding changes)
- **Depth:** Completeness, accuracy check

### agentRouter
- **Primary:** Task understanding
- **Secondary:** Agent capability matching
- **Depth:** Workflow recommendation

### costOptimizer
- **Primary:** Strategic cost analysis
- **Secondary:** Implementation planning
- **Depth:** ROI analysis, roadmap

---

## Cost Comparison: Agents vs. Skills

### Scenario: Review a Function

**Option 1: Direct Agent**
```
/codeReviewer "Review this"
Cost: ~$0.02
Time: 15s
Result: Code quality only
```

**Option 2: Skill (comprehensive)**
```
/codeReview "Review this"
Cost: ~$0.10
Time: 60s
Result: Code + security + performance
```

**Option 3: Multiple Agents (sequential)**
```
/codeReviewer → /securityReviewer → /performanceOptimizer
Cost: ~$0.08
Time: 45s
Result: Full analysis
```

**Best for:**
- Quick check → Direct agent
- Comprehensive → Skill
- Custom workflow → Multiple agents

---

## Tips for Success

1. **Use skills for critical code** — Get comprehensive analysis
2. **Use agents for quick checks** — Fast, cheap, focused
3. **Chain agents for custom workflows** — Maximum control
4. **Monitor costs** — Use `/costAnalysis` monthly
5. **Route intelligently** — Use `/agentRouter` for complex tasks
6. **Document improvements** — Use `/docReview` to keep docs in sync

---

## See Also

- **[AGENTS_REFERENCE.md](AGENTS_REFERENCE.md)** — Individual agent details
- **[GETTING_STARTED.md](GETTING_STARTED.md)** — Quick start guide
- **[PLUGIN_STRUCTURE.md](PLUGIN_STRUCTURE.md)** — How plugin is organized

