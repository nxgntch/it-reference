# Task Observer System

Automated observation of your development sessions to identify skill gaps, corrections, and methodology improvements.

---

## Overview

Task Observer monitors your work sessions and produces three types of observations:

1. **Corrections & Adjustments** — When you steer AI output, it signals skill gaps
2. **Manual Work Patterns** — Repetitive tasks that could be systematized as skills
3. **Observer Blind Spots** — Improvements to the observer's own methodology

---

## How It Works

### Session Capture

During each Claude Code session:
- Track corrections made to AI output
- Capture manual workarounds applied
- Note gaps in existing skills
- Identify cross-cutting patterns

### Observation Log

Each session produces a structured log with:
- **Timestamp**: When observations occurred
- **Skill affected**: Which skill could be improved
- **Observation type**: Correction, Gap, or Blind Spot
- **Details**: Specific context and suggestion
- **Priority**: Critical, High, Medium, Low

### Review & Approval

1. **Generate**: Observer produces recommendation
2. **Review**: You evaluate the suggestion
3. **Approve**: Mark for skill update or archive
4. **Update**: Skill is enhanced based on approval

---

## Observation Types

### Type 1: Corrections & Adjustments

**Trigger**: You modify AI output

**Example**:
```yaml
type: correction
affected_skill: security-review
context: "AI suggested using allow_origins=['*'], you changed to explicit list"
suggestion: "Add CORS misconfiguration detection to security-review skill"
priority: High
```

### Type 2: Skill Gaps

**Trigger**: You do something manually that a skill could automate

**Example**:
```yaml
type: skill_gap
gap_description: "Manually running pip audit, pip freeze, updating requirements.txt"
suggested_skill: "dependency-updater"
automation_level: "High (fully automatable)"
priority: High
```

### Type 3: Blind Spots

**Trigger**: Observer's own methodology improvements

**Example**:
```yaml
type: blind_spot
affected_observer_component: "pattern_detection"
observation: "Observer missed correction where user changed error message format"
improvement: "Add pattern matching for error message rewrites"
priority: Medium
```

---

## File Structure

```
.claude/observer/
├── README.md (this file)
├── config.yaml (observer configuration)
├── logs/
│   ├── observations.jsonl (streaming observation log)
│   └── monthly/ (archived observations by month)
│       ├── 2026-08-observations.json
│       └── 2026-09-observations.json
├── approved/
│   ├── skill-updates.yaml (approved skill improvements)
│   └── cross-cutting-principles.yaml
└── workflows/
    ├── capture-session.md (how to log observations)
    ├── review-recommendations.md (approval process)
    └── skill-update-template.md (template for skill changes)
```

---

## Integration Points

### Claude Code Session Hook

Add to `~/.claude/settings.json`:
```json
{
  "hooks": {
    "after_turn": "python .claude/observer/capture_session.py"
  }
}
```

### Review Schedule

- **Daily**: Scan observations for critical items
- **Weekly**: Batch review all observations
- **Monthly**: Update skills based on approved recommendations

### Skill Auto-Check

New/updated skills are automatically checked against:
- Cross-cutting principles (from `approved/cross-cutting-principles.yaml`)
- Existing observation patterns
- Blind spot improvements

---

## Getting Started

1. **Review this README** — Understand observation types
2. **Configure observer** — Edit `config.yaml` with your preferences
3. **Set up capture** — Enable session hook in Claude Code settings
4. **First review** — Check `logs/observations.jsonl` after next session
5. **Approve changes** — Move observations to `approved/` as you accept them

---

## Key Files

| File | Purpose |
|------|---------|
| `config.yaml` | Observer settings (skills to monitor, thresholds) |
| `logs/observations.jsonl` | Real-time observation stream (append-only) |
| `approved/skill-updates.yaml` | Approved changes waiting to be applied |
| `approved/cross-cutting-principles.yaml` | Project-wide principles from observations |
| `workflows/capture-session.md` | How to log observations during work |
| `workflows/review-recommendations.md` | Step-by-step review process |

---

## Example Workflow

### Session 1: Work on security review skill

You use the security-review skill, manually correct three items:
1. Add CORS check
2. Add rate limiting check  
3. Add error message validation

**Observer captures**:
```yaml
corrections:
  - skill: security-review
    correction: "Added CORS validation"
    suggestion: "Enhance CORS section in skill"
    priority: High
  - skill: security-review
    correction: "Added rate limiting check"
    suggestion: "Add rate limiting to baseline checks"
    priority: High
  - skill: security-review
    correction: "Added error message validation"
    suggestion: "Add error handling section"
    priority: Medium
```

### Session 2: Review observations

You review the captured observations:
```bash
# Check observations
cat .claude/observer/logs/observations.jsonl | tail -5

# Approve the changes
# Move to .claude/observer/approved/skill-updates.yaml
```

### Session 3: Update skill

Based on approved observations, enhance security-review:
```bash
# Review approved changes
cat .claude/observer/approved/skill-updates.yaml

# Update the skill
vim .claude/skills/securityAudit.py

# Mark as applied
# Move observation from approved to applied/
```

---

## Best Practices

### Observation Quality
- **Be specific**: "Add X to skill Y" not "Improve skill"
- **Include context**: Why was this correction needed?
- **Link to rules**: Reference `.claude/rules/` when applicable
- **Note frequency**: Is this a one-off or recurring pattern?

### Review Frequency
- **Daily**: Check for critical observations (security, deployment)
- **Weekly**: Batch review all observations
- **Monthly**: Apply approved changes to skills

### Skill Updates
- **Small changes**: Apply immediately
- **Major changes**: Test with next session before finalizing
- **Cross-skill impact**: Check for unintended side effects

---

## Configuration

See `config.yaml` for:
- Which skills to monitor
- Observation thresholds
- Review frequency
- Notification preferences
- Cross-cutting principle rules

---

## Questions & Troubleshooting

**Q: How often should I review observations?**  
A: Daily for critical items (security, deployments), weekly for everything else.

**Q: What if I disagree with an observation?**  
A: Archive it (it's not a mandate). Observer learns from your choices.

**Q: Can I track cross-skill patterns?**  
A: Yes, see `approved/cross-cutting-principles.yaml`.

**Q: How does this affect my current skills?**  
A: It doesn't—observer only makes recommendations. You decide what to apply.

---

## See Also

- Observation logs: `logs/observations.jsonl`
- Approved changes: `approved/skill-updates.yaml`
- Cross-cutting principles: `approved/cross-cutting-principles.yaml`
- Capture workflow: `workflows/capture-session.md`
- Review workflow: `workflows/review-recommendations.md`
- Main rules: `../.claude/rules/`
