# Task Observer Index

Complete navigation for the nxgntch Task Observer system.

---

## Quick Start

1. **Understand the system** → Read [`README.md`](README.md)
2. **Configure it** → Edit [`config.yaml`](config.yaml) to your preferences
3. **Capture observations** → During work, follow [`workflows/capture-session.md`](workflows/capture-session.md)
4. **Review weekly** → Follow [`workflows/review-recommendations.md`](workflows/review-recommendations.md)
5. **Apply approved changes** → Update skills and mark as done

---

## Directory Structure

```
.claude/observer/
├── INDEX.md (you are here)
├── README.md (overview & how it works)
├── config.yaml (configuration & settings)
│
├── logs/
│   ├── observations-schema.md (structured format for observations)
│   ├── observations.jsonl (append-only log—created after first session)
│   └── monthly/ (archived monthly observations)
│
├── approved/
│   ├── skill-updates.yaml (approved changes waiting implementation)
│   ├── cross-cutting-principles.yaml (project-wide patterns)
│   └── blind-spot-improvements.yaml (observer methodology fixes)
│
└── workflows/
    ├── capture-session.md (how to log observations)
    ├── review-recommendations.md (approval process)
    └── validate-principles.py (auto-validate skills—future)
```

---

## Files by Purpose

### Understanding the System

| File | Purpose | Read When |
|------|---------|-----------|
| `README.md` | System overview, how it works, examples | First time setup |
| `config.yaml` | Configuration options, thresholds | Customizing behavior |
| `logs/observations-schema.md` | Data format, fields, examples | Capturing observations |

### During Development

| File | Purpose | Use When |
|------|---------|----------|
| `workflows/capture-session.md` | How to log observations | End of work session |
| `logs/observations.jsonl` | Your observation log | Reviewing what you capture |

### Weekly Reviews

| File | Purpose | Use When |
|------|---------|----------|
| `workflows/review-recommendations.md` | How to approve changes | Weekly review session |
| `approved/skill-updates.yaml` | Approved changes to implement | Implementing improvements |
| `approved/cross-cutting-principles.yaml` | Project-wide principles | Understanding patterns |

### Monthly Analysis

| File | Purpose | Use When |
|------|---------|----------|
| `logs/monthly/YYYY-MM-observations.json` | Archived observations | Monthly review/analysis |

---

## Key Concepts

### Observation Types

1. **Correction**: You modified AI output → skill could be clearer
2. **Gap**: You did something manually → could be automated as skill
3. **Blind Spot**: Observer missed something → observer methodology improves

### Approval Flow

```
Observation captured
    ↓
Weekly review (you read & decide)
    ↓
Approved → skill-updates.yaml
    ↓
Implement change to skill
    ↓
Mark as applied
    ↓
✓ Skill improved
```

### Cross-Cutting Principles

Patterns that apply across multiple skills. Automatically validated when skills are created/updated.

Examples:
- Security-1: Explicit Allow > Implicit Deny
- Quality-1: Clarity Over Cleverness
- Ops-1: Configuration External to Code

---

## Workflows

### Session Capture (During Work)

```
┌─ You're working on a task
├─ You correct AI output OR spot a gap OR find observer weakness
├─ You take a note (or capture happens automatically)
├─ At end of session: add to logs/observations.jsonl
└─ ✓ Observation logged
```

→ See: [`workflows/capture-session.md`](workflows/capture-session.md)

### Weekly Review (Friday)

```
┌─ Read all observations from this week
├─ Decide: Approve, Archive, or Clarify each one
├─ Approve: Add to approved/skill-updates.yaml
├─ Archive: Mark as archived with reason
└─ ✓ Week reviewed
```

→ See: [`workflows/review-recommendations.md`](workflows/review-recommendations.md)

### Skill Implementation (When Ready)

```
┌─ Review approved change in skill-updates.yaml
├─ Implement change to skill
├─ Test it works
├─ Update skill-updates.yaml: status="applied", add commit hash
├─ Commit: feat({skill}): {description} (obs_{id})
└─ ✓ Skill improved
```

→ See: [`approved/skill-updates.yaml`](approved/skill-updates.yaml)

---

## Daily Checklist

### Every Day (2 min)

```bash
# Check for critical observations
jq 'select(.priority=="critical" and .status=="new")' .claude/observer/logs/observations.jsonl
```

- [ ] Any critical items that need immediate attention?

### Every Friday (30 min)

```bash
# Full week review
cd .claude/observer
jq 'select(.status=="new")' logs/observations.jsonl | less
```

- [ ] Read all new observations
- [ ] For each: Approve, Archive, or Clarify?
- [ ] Add approved items to approved/skill-updates.yaml

### Monthly (1 hour)

```bash
# Generate monthly report
python generate_report.py --month 2026-08
```

- [ ] Review trends (which skills need most improvement?)
- [ ] Archive old observations
- [ ] Update cross-cutting principles
- [ ] Plan skill improvements for next sprint

---

## Configuration

Start with defaults in `config.yaml`. Key settings:

```yaml
# What to track
capture:
  track_corrections: true
  track_gaps: true
  track_blind_spots: true

# Which skills to monitor (your custom + frequently used ones)
monitored_skills:
  - security-review
  - code-review
  - (your custom skills)

# Notification/review schedule
review:
  schedule:
    daily_scan: "09:00 UTC"
    weekly_batch: "Monday 09:00 UTC"
```

→ See: [`config.yaml`](config.yaml) for all options

---

## Observation Lifecycle

### Status: new

Just captured. Awaiting your review.

```bash
jq 'select(.status=="new")' logs/observations.jsonl | wc -l
# How many new observations are waiting?
```

### Status: reviewed

You've looked at it. Now deciding whether to approve.

### Status: approved

You've decided to apply it. Waiting in `skill-updates.yaml` for implementation.

```bash
grep -c "status: .approved." approved/skill-updates.yaml
# How many approved changes are ready to implement?
```

### Status: applied

Skill has been updated. Observation marks completion.

### Status: archived

You decided not to apply. Reason documented.

---

## Metrics to Track

Over time, monitor:

```
Monthly observations: 5-20 (healthy rate)
Approval rate: 60-80% (most observations are real patterns)
Implementation rate: 80-90% (most approvals get done)
Correction reduction: Should decrease over time (skills improving)
```

---

## Integration Points

### With Your Skills

Observer recommendations feed directly into your skill library:
- `.claude/skills/` — your custom skills
- Each skill can be improved based on observations

### With Your Rules

Observer reinforces your development rules:
- `.claude/rules/` — development standards
- Observations that violate rules are flagged as gaps
- Cross-cutting principles extend your rules

### With Your Git Workflow

When you apply changes:
- Commit message: `feat({skill}): {description} (obs_{id})`
- Links observation to the code change
- Creates traceable improvement record

---

## Common Tasks

### "How do I log an observation?"

→ See: [`workflows/capture-session.md`](workflows/capture-session.md)

### "What should I do during weekly review?"

→ See: [`workflows/review-recommendations.md`](workflows/review-recommendations.md)

### "What format should observations be in?"

→ See: [`logs/observations-schema.md`](logs/observations-schema.md)

### "How do I approve a change?"

→ See: [`approved/skill-updates.yaml`](approved/skill-updates.yaml) (template at top)

### "What are cross-cutting principles?"

→ See: [`approved/cross-cutting-principles.yaml`](approved/cross-cutting-principles.yaml)

### "How is the system configured?"

→ See: [`config.yaml`](config.yaml) (all options documented)

---

## Examples

### Example Session: Security Review

```
Session time: 2026-08-22 14:00-14:30 (30 min)

Activity 1 (14:00-14:15):
  - Use security-review skill
  - Skill misses CORS misconfiguration
  - You manually fix: allow_origins=['*'] → explicit list
  → Observation: Correction needed in security-review

Activity 2 (14:15-14:30):
  - Review error messages manually
  - Skill doesn't check consistency
  → Observation: Gap in security-review error handling

End of session:
  - Add 2 observations to logs/observations.jsonl
  - Priority: high (both are recurring patterns)

Friday review:
  - Read both observations
  - Decide: APPROVE both for skill-updates.yaml
  - Add to approved/skill-updates.yaml

Next sprint:
  - Implement CORS validation in security-review (30 min)
  - Implement error message checks in security-review (20 min)
  - Mark both as applied
  - Security-review skill is now better
```

### Example Approval Decision

Observation: `obs_2026-08-22_001`
```json
{
  "type": "gap",
  "affected_skill": null,
  "context": {
    "description": "Manually running: pip audit, grep, sed, pytest, git push"
  },
  "suggestion": {
    "suggested_skill": "dependency-updater (NEW SKILL)",
    "automation_level": "High (fully automatable)"
  }
}
```

Your decision: **APPROVE** (this is high-value automation)

Added to `skill-updates.yaml`:
```yaml
- observation_id: "obs_2026-08-22_001"
  status: "approved"
  skill: "dependency-updater"
  change:
    description: "Create new skill to automate pip audit → requirements.txt update"
    estimated_effort: "2 hours"
  notes: "High-value skill. Recurring manual workflow."
```

Next sprint: Implement the skill.

---

## Support

### "How do I...?"

1. Check this INDEX (you're reading it!)
2. Search the relevant workflow file
3. Check config.yaml for behavior customization
4. Review examples in observations-schema.md

### "I have a question about..."

| Topic | File |
|-------|------|
| How the system works | README.md |
| Observation format | logs/observations-schema.md |
| Capturing observations | workflows/capture-session.md |
| Approving changes | workflows/review-recommendations.md |
| Configuration options | config.yaml |
| Project principles | approved/cross-cutting-principles.yaml |

---

## Next Steps

1. **Today**: Read `README.md` to understand the system
2. **Today**: Configure `config.yaml` to your preferences
3. **During work**: Follow `workflows/capture-session.md` when you spot patterns
4. **This Friday**: Do your first weekly review using `workflows/review-recommendations.md`
5. **Next sprint**: Implement approved skill improvements

---

## Version

Task Observer setup: v1.0 (2026-08-22)  
Last updated: 2026-08-22

---

**See Also**: Main project documentation at `CLAUDE.md`
