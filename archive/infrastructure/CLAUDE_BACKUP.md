# nxgntch: Navigation Hub

**Multi-agent orchestration system** with cost tracking, team isolation, and OWASP security integration.

---

## Where To Start

**New to nxgntch?** → [`docs/INDEX.md`](docs/INDEX.md)  
**Infrastructure & IDE setup** → [`.claude/INFRASTRUCTURE.md`](.claude/INFRASTRUCTURE.md)  
**Complete documentation map** → [`docs/NAVIGATION.md`](docs/NAVIGATION.md)  
**Development guidance** → [`docs/guides/development/rules/README.md`](docs/guides/development/rules/README.md)  
**Project overview** → [`README.md`](README.md)  

**📚 Reference Repository** → [`nxgntch/it-reference`](https://github.com/nxgntch/it-reference)  
Historical documentation, archived phases, planning materials (not loaded at startup)  

---

## Current Status

**Phase**: Phase 13 (Quality Hardening & Agent Integration) ✅ COMPLETE & MERGED  
**Last Update**: 2026-08-23  
**Progress**: ✅ Phase 13 Complete (199 tests, 8,399 lines) + Agent Skills Extension

**Latest Completion**:
- ✅ Phase 11: Error Recovery System (110 tests, merged to main)
- ✅ Phase 12: Optimization & Performance (193 tests, 10,068 lines, merged to main)
- ✅ Phase 13: Monitoring & Observability (199 tests, 8,399 lines, merged to main)
  - Week 1: Core Monitoring (141 tests)
  - Week 2: Dashboard & Aggregation (58 tests)
- ✅ **Phase 13 Extension**: Agent Skills Integration (3 skills, config updated)

**Test Status**: 500+ tests passing (Phase 11-13), 100% pass rate ✅

See [`AUDIT.md`](AUDIT.md) for comprehensive audit trail and Phase 13 metrics.  
See [`.claude/SKILLS_INVENTORY.md`](.claude/SKILLS_INVENTORY.md) for skill reference.  

**Phase 13 Deliverables** 🚀

**Monitoring & Observability**:
- ✅ Health monitoring system with 4-level status hierarchy
- ✅ Dashboard registry with pre-aggregated metrics
- ✅ Log aggregation with structured query interface
- ✅ Cost tracking integrated with monitoring
- ✅ Alert system with severity-based routing

**Agent Skills Integration** (Extension):
- ✅ `healthMonitoring` skill for Director routing decisions
- ✅ `dashboardConsumer` skill for all agents (context-aware decisions)
- ✅ `logTracing` skill for audit trail and compliance
- ✅ Updated `config/agents.yaml` with 9 new skill assignments
- ✅ Integration guide with patterns and examples

---

## Quick Links by Role

| Role | Start Here |
|------|-----------|
| **New developer** | [`docs/INDEX.md`](docs/INDEX.md) |
| **Writing code** | [`docs/guides/development/`](docs/guides/development/) |
| **Code review** | [`docs/guides/development/rules/code-review-checklist.md`](docs/guides/development/rules/code-review-checklist.md) |
| **Deploying** | [`docs/guides/operations/DEPLOYMENT.md`](docs/guides/operations/DEPLOYMENT.md) |
| **Security** | [`docs/guides/development/rules/security.md`](docs/guides/development/rules/security.md) |
| **API reference** | [`docs/specifications/API_SPECIFICATION.md`](docs/specifications/API_SPECIFICATION.md) |
| **Cost control** | [`docs/guides/operations/COST_CONTROL.md`](docs/guides/operations/COST_CONTROL.md) |
| **Architecture** | [`docs/guides/architecture/`](docs/guides/architecture/) |
| **IDE skills** | [`docs/guides/development/IDE_SKILLS_INVENTORY.md`](docs/guides/development/IDE_SKILLS_INVENTORY.md) |
| **Platform skills** | [`docs/PLATFORM_SKILLS_INVENTORY.md`](docs/PLATFORM_SKILLS_INVENTORY.md) |
| **Skill evolution** | [`.claude/observer/INDEX.md`](.claude/observer/INDEX.md) |

---

## Key Directories

| Directory | Purpose |
|-----------|---------|
| **`.claude/`** | IDE configuration: agents, skills, rules, hooks |
| **`.claude/observer/`** | Task Observer for skill evolution & pattern tracking |
| **`app/`** | Runtime application code (FastAPI) |
| **`config/`** | YAML configuration: models, agents, governance |
| **`docs/`** | **Complete documentation (guides, specs, examples)** |
| **`tests/`** | Test suite (pytest) |
| **`scripts/`** | Utility scripts and sync pipeline |
| **`mpc-chat/`** | Standalone MCP server for Claude Chat |

---

## Documentation Structure

```
docs/
├── guides/                  ← How-to and conceptual docs
│   ├── architecture/        ← System design
│   ├── development/         ← How to code (includes rules/)
│   ├── operations/          ← How to deploy/operate
│   └── reference/           ← Quick lookups
├── specifications/          ← Formal API & specs
├── examples/                ← Working code samples
├── roadmap/                 ← Plans & completion reports
├── NAVIGATION.md            ← Complete cross-reference
└── INDEX.md                 ← Quick-start entry point
```

**Full structure**: [`docs/NAVIGATION.md`](docs/NAVIGATION.md)

---

## Reference Documentation (Secondary Repo)

**Archive & Planning Docs** → [`nxgntch/it-reference`](https://github.com/nxgntch/it-reference)

Historical and planning documentation is stored in a separate repository to reduce startup overhead:
- **`docs/archive/`** - Completed phase documentation (historical context)
- **`skills/planning/`** - Skill design and planning documents

These are **NOT loaded during initialization** to keep startup fast. Access them for:
- Historical context on architectural decisions
- Design documents for upcoming features
- Offline reference material

**Sync reference docs locally:**
```bash
bash scripts/sync-reference-docs.sh  # Optional, caches docs locally
```

---

## Configuration Philosophy

**Runtime Config** (`config/` YAML): Authoritative numbers, agent definitions, budgets  
**Development Guidance** (`docs/guides/`): How and why to do things  

**Principle**: Don't duplicate numbers between them. Rules link to `config/` for current values.

---

## MCP Chat Maintenance

⚠️ **`mcp-chat/` is standalone** — do NOT edit directly.

All changes flow through the autosync pipeline:
```bash
python scripts/sync/autosync.py
```

See [`docs/guides/development/rules/mcp-chat-maintenance.md`](docs/guides/development/rules/mcp-chat-maintenance.md)

---

## Pre-Commit Checklist

```bash
black app/ tests/
ruff check app/ tests/
mypy app/
pytest tests/ --cov=app
```

See [`docs/guides/development/rules/README.md`](docs/guides/development/rules/README.md) for details.

---

## Claude Code IDE Setup & Workflows

**Setting up Claude Code?** → [`.claude/IDE_SETUP.md`](.claude/IDE_SETUP.md)  
**Common development workflows** → [`.claude/WORKFLOWS.md`](.claude/WORKFLOWS.md)  
**IDE configuration** → [`.claude/settings.json`](.claude/settings.json)  
**Custom keybindings** → [`.claude/keybindings.json`](.claude/keybindings.json)

### Quick IDE Tips

| Task | Method |
|------|--------|
| **Run full test suite** | Ctrl+Shift+T (or Cmd+Shift+T on macOS) |
| **Format & lint code** | Ctrl+Shift+L (runs black, ruff, mypy) |
| **Code review** | Ctrl+Shift+R (with auto-fix) |
| **Security audit** | Ctrl+Shift+S (OWASP review) |
| **Check docs** | Ctrl+Shift+D (audit documentation) |
| **Git status** | Ctrl+Shift+C |
| **Recent commits** | Ctrl+Shift+G |

### SessionStart Automation

When you start a Claude Code session, nxgntch automatically:
1. ✅ Checks black formatting
2. ✅ Runs ruff linting
3. ✅ Validates mypy type checking
4. ✅ Executes pytest with coverage
5. 💡 Reports any issues with remediation steps

See `.claude/hooks/sessionStart.sh` for details.

---

## Need Help?

- **Questions about development?** → [`docs/guides/development/rules/`](docs/guides/development/rules/)
- **Can't find something?** → [`docs/NAVIGATION.md`](docs/NAVIGATION.md)
- **API reference?** → [`docs/specifications/API_SPECIFICATION.md`](docs/specifications/API_SPECIFICATION.md)
- **Troubleshooting?** → [`docs/guides/operations/TROUBLESHOOTING.md`](docs/guides/operations/TROUBLESHOOTING.md)

---

**Last updated**: 2026-08-23 · **IDE setup automated with hooks, keybindings & workflows** · **Phase 13 Complete**
