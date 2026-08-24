# Review & Approval Workflow

How to review task-observer recommendations and approve changes.

---

## Overview

Each week, review observations and decide which to apply. Three outcomes:
1. **Approve** → Add to `approved/skill-updates.yaml`
2. **Archive** → Low priority or already handled
3. **Clarify** → Need more info before deciding

---

## Weekly Review Schedule

### Monday Morning: Critical Scan (5 min)

**Check for urgent issues:**

```bash
# See critical observations
jq 'select(.priority=="critical" and .status=="new")' \
  .claude/observer/logs/observations.jsonl
```

**Action**: Address critical items immediately (same day if possible)

### Friday: Full Week Review (30 min)

**Batch review all week's observations:**

```bash
# Count observations by priority
jq -s 'group_by(.priority) | map({priority: .[0].priority, count: length})' \
  .claude/observer/logs/observations.jsonl

# Get summary
jq -s 'group_by(.type) | map({type: .[0].type, count: length})' \
  .claude/observer/logs/observations.jsonl
```

---

## Review Checklist

For each observation, ask:

### 1. Is This a Real Pattern?

- [ ] Have I seen this before (or multiple times this week)?
- [ ] Would fixing this save me time/effort?
- [ ] Is the suggestion actionable?

**If NO**: Archive observation

**If YES**: Continue to step 2

### 2. Is This High Priority?

- [ ] Affects security or stability?
- [ ] Blocks workflow repeatedly?
- [ ] Affects code quality significantly?
- [ ] Used by multiple skills?

**If YES (critical/high)**: Prioritize for this sprint

**If NO (medium/low)**: Queue for next sprint or backlog

### 3. Can I Act on This?

- [ ] Is the suggestion clear enough to implement?
- [ ] Do I have the expertise to make this change?
- [ ] Can I test it before applying?
- [ ] Will it break existing functionality?

**If NO**: Add review notes and revisit later

**If YES**: Approve and add to skill-updates.yaml

### 4. What's the Risk?

- [ ] Could this change break existing workflows?
- [ ] Will it affect other skills?
- [ ] Are there edge cases to handle?
- [ ] Do I need tests?

**Risk assessment**: Low/Medium/High

---

## Step-by-Step Approval Process

### Step 1: View New Observations

```bash
cd /home/user/it

# See all new observations awaiting review
jq 'select(.status=="new")' .claude/observer/logs/observations.jsonl | \
  jq -s 'sort_by(.priority) | reverse' | \
  jq '.[] | {id: .observation_id, type: .type, skill: .affected_skill, priority: .priority, description: .context.description}'
```

### Step 2: Evaluate Each Observation

```bash
# Review specific observation
OBSID="obs_2026-08-22_001"
jq "select(.observation_id==\"$OBSID\")" .claude/observer/logs/observations.jsonl
```

**Think through**:
- Is this a real pattern?
- Is this actionable?
- What's the priority?
- Should I approve, archive, or clarify?

### Step 3: Approve the Change

Open `.claude/observer/approved/skill-updates.yaml` and add entry:

```yaml
- observation_id: "obs_2026-08-22_001"
  status: "approved"
  skill: "security-review"
  
  change:
    description: "Add CORS validation to security checks"
    affected_sections: ["cors_validation"]
    estimated_effort: "30 minutes"
  
  implementation:
    approach: "Detect allow_origins=['*'] pattern"
    success_criteria: "Skill flags CORS misconfigs automatically"
  
  applied_date: null
  notes: "Pattern observed 3 times this week. High priority."
```

### Step 4: Commit Approval

```bash
git add .claude/observer/approved/skill-updates.yaml
git commit -m "chore(observer): approve skill updates for security-review"
```

### Step 5: Update Observation Status

Once in the file, the observation is marked "approved". When implementing:

1. Make the skill change
2. Test the change
3. Update `skill-updates.yaml`:
   - Set `status: "applied"`
   - Set `applied_date: "2026-08-22"`
   - Set `applied_by: "christian.salvador210@gmail.com"`
   - Set `applied_in_commit: "abc123..."`
4. Commit: `feat(security-review): add CORS validation (obs_2026-08-22_001)`

---

## Decision Matrix

Use this to decide quickly:

| Type | Priority | Pattern? | Approval |
|------|----------|----------|----------|
| Correction | Critical | Yes | APPROVE (today) |
| Correction | High | Yes | APPROVE (this sprint) |
| Correction | Medium | Yes | QUEUE (next sprint) |
| Gap | High | Yes | APPROVE (new skill) |
| Gap | Medium | Yes | QUEUE (backlog) |
| Blind Spot | High | Yes | APPROVE (improve observer) |
| Blind Spot | Medium | - | ARCHIVE (revisit later) |

---

## Rejection Guide

If you decide NOT to approve:

1. Add review notes to observation:
   ```bash
   # Edit observation entry (manual edit for now)
   jq ".review_notes = \"Not approved: Already handled by X skill\"" observation.json
   ```

2. Set status to "archived":
   ```json
   {"status": "archived", "review_notes": "Why you're not approving"}
   ```

3. Document in `.claude/observer/approved/skill-updates.yaml` under "Rejected Changes"

**Reasons to archive**:
- Already handled by existing skill
- Too vague or unclear
- Not actually a pattern (one-off issue)
- Not worth the effort
- Outside scope of project

---

## Monthly Review (1st of month)

### Generate Monthly Report

```bash
# Analyze observations from past month
python .claude/observer/generate_report.py --month 2026-08

# Shows:
# - Observations by type
# - Skills most affected
# - Cross-cutting patterns
# - Recommended priorities
# - Trends
```

### Archive Old Observations

```bash
# Move observations older than 30 days to monthly archive
python .claude/observer/archive_monthly.py --month 2026-08
```

### Review Trends

- Which skills need the most improvement?
- Are corrections decreasing (indicator of skill improvement)?
- New patterns emerging?
- Observer effectiveness improving?

---

## Cross-Cutting Principles

When approving observations, check if they reveal principles:

**Question**: Does this pattern apply across multiple skills?

**Example**:
```
Observation: CORS validation needed in security-review
Observation: Rate limiting needed in deployment-validator
Observation: URL whitelist needed in code-review

Pattern: "Explicit allow > implicit deny" (cross-cutting principle)

Action: Add to cross-cutting-principles.yaml
```

When added as a principle, new skills are automatically checked against it.

---

## Integration with Skill Updates

### Approved Changes Flow

```
observations.jsonl (new)
    ↓
review-recommendations.md (you read & decide)
    ↓
skill-updates.yaml (you add approved items)
    ↓
.claude/skills/{skill}/ (you implement)
    ↓
skill-updates.yaml (you mark as applied)
    ↓
observations.jsonl (observer records completion)
```

---

## Review Templates

### Quick Approve (High Priority, Clear Suggestion)

```
Observation: CORS validation
Priority: High
Frequency: 3× this week
Decision: APPROVE
Effort: 30 min
Timeline: This sprint
```

### Request Clarification

```
Observation: {ID}
Why clarifying: Not clear which skill should handle this
Need from observer: Which skill is primary owner?
Decision: HOLD for next review
```

### Archive (Already Handled)

```
Observation: {ID}
Why archiving: Similar check already in code-review skill
Note: Code-review should catch this already
Decision: ARCHIVE
Follow-up: Check if code-review is actually catching this
```

---

## Approval SLA

Based on priority (from `config.yaml`):

| Priority | Review SLA | Target Date |
|----------|------------|-------------|
| Critical | Same day | Next business day |
| High | 3 days | This sprint |
| Medium | Weekly | Next sprint |
| Low | Monthly | Backlog |

---

## Metrics to Track

Track over time to assess observer effectiveness:

```
metrics:
  observation_rate: "observations per session"
  approval_rate: "% approved vs rejected"
  implementation_rate: "% approved that get applied"
  time_to_approval: "days from observation to approval"
  skill_improvement_velocity: "skills improved per month"
  correction_reduction: "are corrections decreasing?"
```

---

## Common Questions

**Q: Should I approve every observation?**  
A: No—only ones that represent real patterns you'd change. Others can be archived.

**Q: What if I disagree with observer's suggestion?**  
A: Archive with note explaining why. Observer learns from your decisions.

**Q: How long should skill updates take to implement?**  
A: Estimate in observation. Aim for 30-60 min for small improvements, queue larger ones.

**Q: Can I batch approve similar observations?**  
A: Yes—group by skill, approve together, implement as batch.

**Q: What if a skill is already doing what observer suggests?**  
A: Archive observation with note. Consider if skill should be more prominent in guidelines.

---

## Next Steps

1. **Monday**: Quick critical scan (5 min)
2. **Friday**: Full week review (30 min)
3. **Approve**: Add to skill-updates.yaml
4. **Implement**: Make changes to skills
5. **Close loop**: Mark observations as applied
6. **1st of month**: Generate monthly report

---

## See Also

- Observation schema: `logs/observations-schema.md`
- Approved changes: `approved/skill-updates.yaml`
- Cross-cutting principles: `approved/cross-cutting-principles.yaml`
- Session capture: `workflows/capture-session.md`
- Configuration: `config.yaml`
