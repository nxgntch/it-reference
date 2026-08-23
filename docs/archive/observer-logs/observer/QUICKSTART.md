# Task Observer Quick Start

Get task-observer running in 5 minutes.

---

## What You Just Got

A complete system to track, review, and apply skill improvements based on your development sessions.

---

## In 5 Minutes

### 1. Read the Overview (2 min)

```bash
cat .claude/observer/README.md
```

**Key idea**: Observer captures corrections, gaps, and patterns → you review weekly → skills improve.

### 2. Check Configuration (1 min)

```bash
cat .claude/observer/config.yaml
```

Default settings are solid. Customize if needed:
- `monitored_skills`: Your custom skills to track
- `review.schedule`: When to review (default: daily scan, weekly batch)

### 3. During Your Next Work Session (2 min)

When you catch yourself correcting AI output or doing repetitive work:

Follow: [`.claude/observer/workflows/capture-session.md`](.claude/observer/workflows/capture-session.md)

Add observations to: `.claude/observer/logs/observations.jsonl`

**Template**:
```json
{"observation_id":"obs_YYYY-MM-DD_001","timestamp":"2026-08-22T14:35:42Z","type":"correction|gap|blind_spot","priority":"high|medium|low","affected_skill":"skill_name","context":{"description":"What happened?","why_corrected":"Why did you change it?"},"suggestion":{"suggested_skill":"skill_name","suggested_action":"What needs fixing?"},"status":"new"}
```

---

## Weekly Ritual (30 min)

**Every Friday, 9am**:

```bash
# View new observations
jq 'select(.status=="new")' .claude/observer/logs/observations.jsonl

# Approve good ones
# (Move to .claude/observer/approved/skill-updates.yaml)

# Implement approved changes
# Update skills, test, mark as applied
```

Follow: [`.claude/observer/workflows/review-recommendations.md`](workflows/review-recommendations.md)

---

## Example Session

### Step 1: Spot a Gap (during work)

```
You: "I'm manually checking for CORS misconfiguration every time"
Observer: "That's a gap. Should security-review catch this?"
You: "Yeah, let me add it to observations"
```

### Step 2: Log It (end of session)

Add to `.claude/observer/logs/observations.jsonl`:
```json
{"observation_id":"obs_2026-08-22_001","timestamp":"2026-08-22T14:30:00Z","type":"gap","priority":"high","affected_skill":"security-review","context":{"description":"Manually checking CORS allow_origins=['*'] pattern every review"},"suggestion":{"suggested_skill":"security-review","suggested_action":"Add automatic CORS validation","automation_level":"High"},"status":"new"}
```

### Step 3: Review (Friday)

```bash
jq 'select(.observation_id=="obs_2026-08-22_001")' logs/observations.jsonl
```

**Decision**: This is a real pattern (CORS checked 3 times this week). **APPROVE IT.**

Add to `.claude/observer/approved/skill-updates.yaml`:
```yaml
- observation_id: "obs_2026-08-22_001"
  status: "approved"
  skill: "security-review"
  change:
    description: "Add CORS validation check"
    estimated_effort: "30 minutes"
```

### Step 4: Implement (next sprint)

1. Update security-review skill to detect CORS misconfigs
2. Test it works
3. Commit: `feat(security-review): add CORS validation (obs_2026-08-22_001)`
4. Update `skill-updates.yaml`: set `status: "applied"`

✅ **Skill improved.**

---

## Navigation

| I want to... | Go to... |
|---|---|
| Understand how it works | [`README.md`](README.md) |
| See the complete index | [`INDEX.md`](INDEX.md) |
| Capture observations | [`workflows/capture-session.md`](workflows/capture-session.md) |
| Review & approve changes | [`workflows/review-recommendations.md`](workflows/review-recommendations.md) |
| See observation format | [`logs/observations-schema.md`](logs/observations-schema.md) |
| View approved changes | [`approved/skill-updates.yaml`](approved/skill-updates.yaml) |
| Check project principles | [`approved/cross-cutting-principles.yaml`](approved/cross-cutting-principles.yaml) |
| Customize behavior | [`config.yaml`](config.yaml) |

---

## Key Folders

```
.claude/observer/
├── README.md                          ← Start here
├── INDEX.md                           ← Full navigation
├── config.yaml                        ← Customize settings
├── logs/
│   ├── observations.jsonl             ← Your observation log (auto-created)
│   ├── observations-schema.md         ← Data format reference
│   └── monthly/                       ← Archived old observations
├── approved/
│   ├── skill-updates.yaml             ← Approved changes waiting implementation
│   └── cross-cutting-principles.yaml  ← Project-wide patterns
└── workflows/
    ├── capture-session.md             ← How to log observations
    └── review-recommendations.md      ← How to approve changes
```

---

## First Week

### Day 1-5 (During work)
- Use your skills normally
- When you spot corrections or gaps, note them
- End of day: add to `logs/observations.jsonl`

### Friday (30 min)
- Review all week's observations
- Approve good ones → add to `approved/skill-updates.yaml`
- Archive low-priority ones

### Following Week
- Implement approved changes
- Continue capturing observations
- Repeat next Friday

---

## Common Patterns

### Correction (AI suggested something suboptimal)

```json
{
  "type": "correction",
  "context": {
    "original_ai_output": "What AI suggested",
    "user_modification": "What you changed",
    "why_corrected": "Why it needed changing"
  },
  "suggestion": {
    "suggested_skill": "Which skill could catch this?",
    "suggested_action": "Add this check to skill"
  }
}
```

### Gap (Manual work that could be automated)

```json
{
  "type": "gap",
  "context": {
    "description": "Manual workflow: step1 > step2 > step3"
  },
  "suggestion": {
    "suggested_skill": "new-skill-name",
    "suggested_action": "Create skill to automate workflow",
    "automation_level": "High"
  }
}
```

### Blind Spot (Observer missed something)

```json
{
  "type": "blind_spot",
  "context": {
    "description": "Observer didn't detect change I made"
  },
  "suggestion": {
    "suggested_action": "Improve observer to detect this pattern"
  }
}
```

---

## Tips

- **Be specific**: "Add CORS validation" not "Fix security"
- **Include why**: Explain the reasoning, not just what changed
- **Note frequency**: Is this recurring?
- **Link to docs**: Reference `.claude/rules/` when applicable
- **Use tags**: `["security", "cors", "api"]` for filtering

---

## Questions?

- **How does it work?** → [`README.md`](README.md)
- **Full guide?** → [`INDEX.md`](INDEX.md)
- **During work?** → [`workflows/capture-session.md`](workflows/capture-session.md)
- **During review?** → [`workflows/review-recommendations.md`](workflows/review-recommendations.md)
- **Format questions?** → [`logs/observations-schema.md`](logs/observations-schema.md)

---

**Ready to start?** Go capture your first observation during your next work session! 🚀
