# Observation Log Schema

Structured format for observations captured during work sessions.

---

## File Format

**Format**: JSONL (JSON Lines) — one observation per line  
**Location**: `logs/observations.jsonl` (append-only)  
**Rotation**: Monthly archives in `logs/monthly/YYYY-MM-observations.json`

---

## Observation Object

Each line is a JSON object with this structure:

```json
{
  "observation_id": "obs_2026-08-22_001",
  "timestamp": "2026-08-22T14:35:42Z",
  "session_id": "session_01RZJDtm6ryNFQqMVbwRcsoZ",
  "session_duration_minutes": 45,
  
  "type": "correction|gap|blind_spot",
  "priority": "critical|high|medium|low",
  
  "affected_skill": "security-review",
  "affected_components": ["cors_validation", "error_messages"],
  
  "context": {
    "description": "User corrected CORS configuration check",
    "original_ai_output": "CORS check using allow_origins=['*']",
    "user_modification": "Changed to explicit list of approved origins",
    "why_corrected": "Security best practice: explicit > wildcard"
  },
  
  "observation_details": {
    "is_pattern": false,
    "frequency_in_session": 1,
    "recurring_issue": true,
    "severity_to_workflow": "high",
    "affects_code_quality": true
  },
  
  "suggestion": {
    "suggested_skill": "security-review",
    "suggested_action": "Add CORS validation check to skill",
    "automation_level": "High (can be fully automated)",
    "estimated_effort": "30 minutes",
    "success_criteria": "Skill catches CORS misconfigurations automatically"
  },
  
  "cross_cutting": {
    "is_cross_cutting": false,
    "affects_multiple_skills": false,
    "principle_category": null
  },
  
  "metadata": {
    "user": "christian.salvador210@gmail.com",
    "model_used": "claude-opus-5",
    "repository": "illestninja/it",
    "branch": "main",
    "related_skills": ["code-review", "owasp-integration"],
    "related_files": [".claude/rules/security-config.md"],
    "tags": ["security", "cors", "api_security"]
  },
  
  "status": "new|reviewed|approved|archived|applied",
  "review_notes": "",
  "approval_date": null
}
```

---

## Field Definitions

### Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `observation_id` | string | Unique ID (format: `obs_YYYY-MM-DD_NNN`) |
| `timestamp` | ISO 8601 | When observation was captured |
| `session_id` | string | Claude Code session ID |
| `session_duration_minutes` | number | Length of session |

### Classification

| Field | Type | Options | Description |
|-------|------|---------|-------------|
| `type` | enum | `correction`, `gap`, `blind_spot` | What kind of observation |
| `priority` | enum | `critical`, `high`, `medium`, `low` | How urgent |
| `status` | enum | `new`, `reviewed`, `approved`, `archived`, `applied` | Review state |

### Scope

| Field | Type | Description |
|-------|------|-------------|
| `affected_skill` | string | Primary skill this touches |
| `affected_components` | array | Specific parts of skill (e.g., ["cors_validation"]) |

### Context & Details

| Field | Type | Description |
|-------|------|-------------|
| `context.description` | string | What happened (narrative) |
| `context.original_ai_output` | string | What AI suggested |
| `context.user_modification` | string | What you changed |
| `context.why_corrected` | string | Why the change was needed |

### Observation Attributes

| Field | Type | Description |
|-------|------|-------------|
| `observation_details.is_pattern` | boolean | Is this a recurring pattern? |
| `observation_details.frequency_in_session` | number | Times this happened in this session |
| `observation_details.recurring_issue` | boolean | Have you seen this before? |
| `observation_details.severity_to_workflow` | string | How much does this slow you down? |
| `observation_details.affects_code_quality` | boolean | Does this impact code quality? |

### Suggestion

| Field | Type | Description |
|-------|------|-------------|
| `suggestion.suggested_skill` | string | Which skill to improve |
| `suggestion.suggested_action` | string | Specific improvement needed |
| `suggestion.automation_level` | string | Can this be automated? (High/Medium/Low) |
| `suggestion.estimated_effort` | string | Time to implement |
| `suggestion.success_criteria` | string | How to know it worked |

### Cross-Cutting

| Field | Type | Description |
|-------|------|-------------|
| `cross_cutting.is_cross_cutting` | boolean | Does this affect multiple skills? |
| `cross_cutting.affects_multiple_skills` | boolean | Affects >1 skill? |
| `cross_cutting.principle_category` | string | Category if it's a principle (e.g., "security") |

### Metadata

| Field | Type | Description |
|-------|------|-------------|
| `metadata.user` | string | Who made the correction |
| `metadata.model_used` | string | Which Claude model was used |
| `metadata.repository` | string | Which repo (e.g., "illestninja/it") |
| `metadata.branch` | string | Git branch worked on |
| `metadata.related_skills` | array | Other skills this touches |
| `metadata.related_files` | array | Documentation/rules this relates to |
| `metadata.tags` | array | Labels (e.g., ["security", "api"]) |

### Review State

| Field | Type | Description |
|-------|------|-------------|
| `review_notes` | string | Your notes during review |
| `approval_date` | ISO 8601 | When you approved it |

---

## Example Observations

### Example 1: Correction

```json
{
  "observation_id": "obs_2026-08-22_001",
  "timestamp": "2026-08-22T14:35:42Z",
  "session_id": "session_abc123",
  "type": "correction",
  "priority": "high",
  "affected_skill": "security-review",
  "affected_components": ["cors_validation"],
  "context": {
    "description": "AI suggested CORS with allow_origins=['*'], user corrected to explicit list",
    "original_ai_output": "Allow CORS from all origins for flexibility",
    "user_modification": "Changed to specific approved domains only",
    "why_corrected": "Security: wildcard CORS is a vulnerability per OWASP #5"
  },
  "observation_details": {
    "is_pattern": true,
    "frequency_in_session": 3,
    "recurring_issue": true,
    "severity_to_workflow": "high"
  },
  "suggestion": {
    "suggested_skill": "security-review",
    "suggested_action": "Add automatic CORS validation: catch allow_origins=['*'] and suggest explicit list",
    "automation_level": "High (can detect and fix)",
    "estimated_effort": "30 minutes"
  },
  "status": "new",
  "metadata": {
    "tags": ["security", "cors", "owasp"]
  }
}
```

### Example 2: Skill Gap

```json
{
  "observation_id": "obs_2026-08-22_002",
  "timestamp": "2026-08-22T15:10:15Z",
  "session_id": "session_abc123",
  "type": "gap",
  "priority": "high",
  "affected_skill": null,
  "context": {
    "description": "User manually ran pip audit, checked requirements, updated versions—repeatedly for 15 min",
    "why_corrected": "This is a common dependency management pattern that could be automated"
  },
  "observation_details": {
    "is_pattern": true,
    "frequency_in_session": 1,
    "recurring_issue": true,
    "severity_to_workflow": "high"
  },
  "suggestion": {
    "suggested_skill": "dependency-updater (NEW SKILL)",
    "suggested_action": "Create new skill to: run pip audit, identify CVEs, update requirements.txt, run tests",
    "automation_level": "High (fully automatable)",
    "estimated_effort": "2 hours"
  },
  "status": "new",
  "metadata": {
    "tags": ["dependencies", "automation", "security"]
  }
}
```

### Example 3: Blind Spot

```json
{
  "observation_id": "obs_2026-08-22_003",
  "timestamp": "2026-08-22T16:05:30Z",
  "session_id": "session_abc123",
  "type": "blind_spot",
  "priority": "medium",
  "context": {
    "description": "Observer didn't detect that user changed error message format from 'Invalid X' to 'Could not process X'",
    "why_corrected": "This signals a consistency improvement that observer should catch"
  },
  "observation_details": {
    "is_pattern": false,
    "severity_to_workflow": "medium"
  },
  "suggestion": {
    "suggested_action": "Add pattern detection for error message rewrites (from 'Invalid' to 'Could not')",
    "automation_level": "Medium (requires NLP understanding)"
  },
  "status": "new",
  "metadata": {
    "tags": ["observer_improvement", "error_messages"]
  }
}
```

---

## Status Transitions

```
new → reviewed → approved → applied
                ↓
              archived (if rejected/low priority)
```

- **new**: Just captured, not yet reviewed
- **reviewed**: You've looked at it, deciding whether to apply
- **approved**: You've decided to apply this improvement
- **applied**: The skill has been updated based on observation
- **archived**: Rejected or low-priority, filed away

---

## Querying Observations

### Get all corrections for a skill
```bash
jq 'select(.type=="correction" and .affected_skill=="security-review")' logs/observations.jsonl
```

### Get critical observations
```bash
jq 'select(.priority=="critical")' logs/observations.jsonl
```

### Get new observations awaiting review
```bash
jq 'select(.status=="new")' logs/observations.jsonl | tail -10
```

### Get approved changes ready to apply
```bash
jq 'select(.status=="approved")' logs/observations.jsonl
```

### Count observations by type
```bash
jq -s 'group_by(.type) | map({type: .[0].type, count: length})' logs/observations.jsonl
```

---

## Best Practices

1. **Specificity**: Include exact quotes from AI output and your changes
2. **Context**: Explain WHY the correction was needed (not just WHAT)
3. **Patterns**: Note if this is recurring or one-off
4. **Tags**: Use consistent tags for filtering/analysis
5. **Links**: Reference related files, skills, or issues
6. **Metrics**: Quantify impact when possible (frequency, time saved, etc.)

---

## Integration

Observations feed into:
- **Skill updates**: `approved/skill-updates.yaml`
- **Cross-cutting principles**: `approved/cross-cutting-principles.yaml`
- **Reports**: `observer/reports/`
- **Trends**: Analyzed for patterns in monthly reports
