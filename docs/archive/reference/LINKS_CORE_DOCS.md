# Core Documentation & Reference

Architecture, planning, API reference, and core project understanding.

---

## Architecture & System Design

**Understanding how nxgntch works:**

- **[docs/AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md)** — System architecture overview (components, flows, design)
- **[docs/AGENT_INVENTORY.md](AGENT_INVENTORY.md)** — Agent inventory (definitions, capabilities, hierarchy)
- **[docs/AGENTS_FULL_REFERENCE.md](AGENTS_FULL_REFERENCE.md)** — Complete agent reference (capabilities, models, usage)

---

## API Reference & Endpoints

**Runtime API documentation:**

- **[docs/API_REFERENCE.md](API_REFERENCE.md)** — All runtime endpoints, methods, schemas
- **[config/agents.yaml](../config/agents.yaml)** — Agent configuration definitions
- **[config/models.yaml](../config/models.yaml)** — Model pricing and configuration
- **[config/governance.yaml](../config/governance.yaml)** — Budget caps, cost policies

---

## Planning & Roadmap

**Current development status and next steps:**

- **[docs/MIGRATION_PLAN.md](MIGRATION_PLAN.md)** — Development roadmap and current phase
- **[AUDIT.md](../AUDIT.md)** — Living audit trail (metrics, progress, status)

---

## Index & Navigation

**Finding what you need:**

- **[docs/INDEX.md](INDEX.md)** — Master documentation index (all docs with purposes)
- **[CLAUDE.md](../CLAUDE.md)** — Project guidance & navigation hub

---

## Configuration Files

**YAML configuration reference:**

| Config | Purpose |
|--------|---------|
| **[config/agents.yaml](../config/agents.yaml)** | Agent definitions, capabilities, hierarchy |
| **[config/models.yaml](../config/models.yaml)** | LLM model pricing, costs, availability |
| **[config/governance.yaml](../config/governance.yaml)** | Budget caps, cost policies, alerts |

---

## Code Structure & Examples

**Key implementation files:**

| File | Purpose |
|------|---------|
| **[app/main.py](../app/main.py)** | FastAPI app factory, routes, lifespan |
| **[app/api/tasks.py](../app/api/tasks.py)** | Task invocation endpoints |
| **[app/api/schemas.py](../app/api/schemas.py)** | Request/response schemas (Pydantic) |
| **[app/db/models.py](../app/db/models.py)** | Database models (SQLAlchemy) |
| **[app/core/agents.py](../app/core/agents.py)** | Agent logic and definitions |
| **[app/core/orchestrator.py](../app/core/orchestrator.py)** | Orchestration engine |
| **[app/core/cost.py](../app/core/cost.py)** | Cost tracking & calculation |
| **[app/core/security.py](../app/core/security.py)** | Authentication & authorization |
| **[app/core/memoryGuard.py](../app/core/memory_guard.py)** | Agent memory poisoning protection |
| **[app/db/](../app/db/)** | Database layer (ORM, session management) |
| **[app/providers/](../app/providers/)** | LLM provider integrations |

---

## Testing

**Test structure and examples:**

- **[tests/test_orchestrator.py](../tests/)** — Orchestrator tests
- **[.claude/rules/testing.md](../.claude/rules/testing.md)** — Testing standards & TDD guide

---

## See Also

- **Development rules** — [LINKS_REFERENCE.md](LINKS_REFERENCE.md)
- **Skills & agents** — [LINKS_SKILLS_AGENTS.md](LINKS_SKILLS_AGENTS.md)
- **All navigation** — [LINKS_NAVIGATION.md](LINKS_NAVIGATION.md)
