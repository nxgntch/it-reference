# NXGNTCH Agent Configuration

**Agent definitions and orchestration configuration for nxgntch multi-agent system.**

## ⚠️ Important: Agent Configuration Has Changed

As of Phase 15, all agent definitions have been consolidated into a **single source of truth**:
- **Runtime Agents**: See [`../../config/agents.yaml`](../../config/agents.yaml)
- **Reference Documentation**: See [`../../docs/guides/reference/ARCHITECTURE_REFERENCE.md`](../../docs/guides/reference/ARCHITECTURE_REFERENCE.md)

Individual agent markdown files (`../../agents/*.md`) no longer exist. All agent specifications (model, capabilities, budget) are now maintained in config files for consistency and easier updates.

## Overview

Agents are orchestrated via:
- FastAPI runtime endpoints
- Skill integration (runtime task execution)
- Cost tracking and budget enforcement
- Multi-team isolation

All agents use **Anthropic models exclusively** (no external LLMs).

## Current Agent System

The nxgntch agent system operates at **runtime** via FastAPI and cost-tracking orchestration.

### Single Source of Truth
All agent definitions are now in `../../config/agents.yaml`:
- Agent IDs and display names
- Model assignments (Opus 5 for complex, Sonnet 5 for standard, Haiku 4.5 for simple)
- Team membership and hierarchy
- Skill assignments and capabilities
- Budget allocation and cost limits

### Agent Hierarchy
```
Director (Orchestration)
├── Engineering Manager (Team Lead)
│   └── Specialists (Architect, DevOps, etc.)
├── Research Manager (Team Lead)
│   └── Researchers
└── Operations Manager (Team Lead)
    └── Coordinators
```

### Configuration Files
- **Agent definitions**: `../../config/agents.yaml` (SSOT)
- **Model pricing**: `../../config/models.yaml`
- **Skills registry**: `../../config/skills.yaml`
- **Budget allocation**: `../../config/governance.yaml`
- **Orchestration settings**: `../../config/orchestration.yaml`

## Documentation

For detailed information about the agent system, see:
- **Full Reference**: [`../../docs/guides/reference/ARCHITECTURE_REFERENCE.md`](../../docs/guides/reference/ARCHITECTURE_REFERENCE.md)
- **Orchestrator Integration**: [`../../docs/guides/agents/ORCHESTRATOR_INTEGRATION.md`](../../docs/guides/agents/ORCHESTRATOR_INTEGRATION.md)
- **Agent Skills**: [`../../docs/guides/agents/AGENT_SKILLS_GUIDE.md`](../../docs/guides/agents/AGENT_SKILLS_GUIDE.md)

## References

- **Agent Registry** (SSOT): [`../../config/agents.yaml`](../../config/agents.yaml)
- **Configuration Index**: [`../../CLAUDE.md`](../../CLAUDE.md) § Configuration
- **Development Rules**: [`../../../docs/rules/INDEX.md`](../../../docs/rules/INDEX.md)
