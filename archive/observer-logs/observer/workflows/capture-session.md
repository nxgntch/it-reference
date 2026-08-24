# Session Capture Workflow

How to capture and log observations during Claude Code sessions.

---

## Overview

Task Observer captures three types of observations:
1. **Corrections**: When you modify AI output
2. **Gaps**: When you discover manual work that could be automated
3. **Blind Spots**: When observer misses something or could improve

---

## During Your Session

### Tracking Corrections

When you modify AI output:
1. **Note the change**: What did you correct? Why?
2. **Identify the skill**: Which skill could prevent this?
3. **Assess the pattern**: Is this recurring?

**Example**:
```
AI suggested:
  app.add_middleware(CORSMiddleware, allow_origins=["*"])

You changed to:
  app.add_middleware(CORSMiddleware, allow_origins=["https://app.example.com"])

Observation:
  - Affected skill: security-review
  - Type: correction
  - Priority: high (security issue)
  - Suggestion: Add CORS validation to skill
```

### Spotting Gaps

When you do something manually that feels repetitive:
1. **Describe the task**: What are you doing?
2. **Identify the pattern**: Is this automatable?
3. **Name the potential skill**: What should this be called?

**Example**:
```
Manual work:
  Running: pip audit
  Reading: requirements.txt
  Updating: requirements.txt with new versions
  Running: pytest to verify

Observation:
  - Type: gap
  - Gap description: "Dependency management is manual"
  - Suggested skill: "dependency-updater"
  - Automation level: High (fully automatable)
  - Priority: high (recurring, time-consuming)
```

### Catching Blind Spots

When observer misses something:
1. **Note what you did**: What wasn't observed?
2. **Explain why it matters**: What pattern does this reveal?
3. **Suggest improvement**: How should observer improve?

**Example**:
```
Observation:
  - Type: blind_spot
  - What observer missed: User changed error message format
  - Why it matters: Signal of consistency improvement
  - Suggestion: Add pattern detection for error message rewrites
  - Priority: medium
```

---

## After Your Session

### Manual Log Entry (Until Automation Ready)

Add entries to `logs/observations.jsonl`:

```bash
# Open the log file
vim .claude/observer/logs/observations.jsonl

# Add new observation (one JSON object per line)
# Use the schema from logs/observations-schema.md
```

**Template** (copy-paste this):
```json
{"observation_id":"obs_YYYY-MM-DD_NNN","timestamp":"2026-08-22T14:35:42Z","session_id":"session_id_here","session_duration_minutes":45,"type":"correction|gap|blind_spot","priority":"high","affected_skill":"skill_name","context":{"description":"What happened?","original_ai_output":"What did AI suggest?","user_modification":"What did you change?","why_corrected":"Why was this needed?"},"observation_details":{"is_pattern":true,"frequency_in_session":1,"recurring_issue":true,"severity_to_workflow":"high"},"suggestion":{"suggested_skill":"skill_name","suggested_action":"What needs to change?","automation_level":"High","estimated_effort":"30 minutes"},"status":"new","metadata":{"user":"christian.salvador210@gmail.com","model_used":"claude-opus-5","tags":["security","cors"]},"review_notes":"","approval_date":null}
```

---

## Example Workflow

### Session 1: Security Review Work (20 min)

**Time: 14:00-14:20**

1. Use security-review skill → it misses CORS misconfiguration
2. You manually add CORS check to code
3. Skill doesn't mention error message consistency
4. You manually review error messages for consistency

**Observations captured**:
- Correction #1: CORS wildcard not flagged
- Correction #2: Error message format inconsistency not noted
- Gap: Error message style guide missing

**At end of session**, add to `logs/observations.jsonl`:
```json
{"observation_id":"obs_2026-08-22_001","timestamp":"2026-08-22T14:20:00Z","type":"correction","priority":"high","affected_skill":"security-review","context":{"description":"Security-review missed CORS misconfiguration","original_ai_output":"allow_origins=['*']","user_modification":"Changed to explicit list","why_corrected":"Wildcard CORS is security vulnerability"},"suggestion":{"suggested_skill":"security-review","suggested_action":"Add CORS validation check"},"status":"new"}
{"observation_id":"obs_2026-08-22_002","timestamp":"2026-08-22T14:25:00Z","type":"correction","priority":"medium","affected_skill":"security-review","context":{"description":"Error messages inconsistently formatted","why_corrected":"Consistency in error messages improves user experience"},"suggestion":{"suggested_skill":"security-review","suggested_action":"Add error message format validation"},"status":"new"}
```

### Session 2: Dependency Update Work (30 min)

**Time: 15:00-15:30**

1. Manual `pip audit` → identifies CVEs
2. Manual `grep` and `sed` → update requirements.txt
3. Manual `pytest` → verify no breakage
4. Manual commit → push changes

**Observation captured**:
- Gap: This entire workflow could be a skill

**At end of session**, add to `logs/observations.jsonl`:
```json
{"observation_id":"obs_2026-08-22_003","timestamp":"2026-08-22T15:30:00Z","type":"gap","priority":"high","context":{"description":"Manual dependency management workflow: audit > update > test > commit"},"observation_details":{"is_pattern":true,"frequency_in_session":1,"recurring_issue":true},"suggestion":{"suggested_skill":"dependency-updater (NEW)","suggested_action":"Automate: audit > identify CVEs > update requirements.txt > run tests > commit","automation_level":"High"},"status":"new"}
```

---

## Automated Capture (Future)

When Claude Code hook is enabled:

```bash
# Edit ~/.claude/settings.json
{
  "hooks": {
    "after_turn": "python .claude/observer/capture_session.py"
  }
}
```

This will automatically:
- Detect corrections in git diff
- Compare output to prior sessions (gap detection)
- Log observations to `logs/observations.jsonl`
- Alert you to critical observations

---

## Tips for Better Observations

### Be Specific
- ✅ "CORS configuration using allow_origins=['*']"
- ❌ "Security issue"

### Include Context
- ✅ "User corrected AI's CORS config because wildcard is OWASP #5 vulnerability"
- ❌ "User changed CORS"

### Note Patterns
- ✅ "This is the 3rd time security-review missed CORS checks"
- ❌ "CORS issue"

### Link to Rules
- ✅ "Relates to `.claude/rules/owasp-integration.md` § CORS Misconfiguration"
- ❌ "Security thing"

### Estimate Effort
- ✅ "30 minutes to add regex pattern detection"
- ❌ "Fix the skill"

---

## What Makes an Observation Worth Capturing

**Capture if**:
- Recurring pattern (happened before or multiple times this session)
- Affects workflow significantly (takes time, blocks progress)
- Could be automated (skill would prevent manual work)
- Affects code quality or security

**Skip if**:
- One-off typo or minor issue
- Already covered by existing skill
- Too vague to actionable

---

## Submission Checklist

Before finishing your session:

- [ ] All corrections logged (with why-corrected)
- [ ] All gaps noted (with automation_level)
- [ ] All blind spots captured (with improvement suggestion)
- [ ] Observations added to `logs/observations.jsonl`
- [ ] Entries are in valid JSON format
- [ ] All required fields filled in
- [ ] Tags are helpful (can search later)
- [ ] Priorities seem reasonable

---

## Next Steps

After capturing observations:

1. **Next day**: Review observations in daily scan
2. **This week**: Batch review all observations
3. **Approve**: Move good suggestions to `approved/skill-updates.yaml`
4. **Apply**: Implement approved skill improvements
5. **Close loop**: Mark observations as "applied" when done

---

## Questions?

- **Schema**: See `logs/observations-schema.md` for full field definitions
- **Status transitions**: See `logs/observations-schema.md` § Status Transitions
- **Review process**: See `workflows/review-recommendations.md`
- **Examples**: See `logs/observations-schema.md` § Example Observations
