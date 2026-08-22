# Development Rules & Standards Reference

Complete development guidance, coding patterns, and project standards.

---

## Quick Reference by Need

| Need | File | Purpose |
|------|------|---------|
| **Naming & structure** | [.claude/rules/coding-style.md](../.claude/rules/coding-style.md) | Code organization, naming conventions |
| **Python rules** | [.claude/rules/python-conventions.md](../.claude/rules/python-conventions.md) | Python-specific standards |
| **FastAPI patterns** | [.claude/rules/fastapi-patterns.md](../.claude/rules/fastapi-patterns.md) | API design & routing patterns |
| **Testing** | [.claude/rules/testing.md](../.claude/rules/testing.md) | Test structure, TDD, coverage |
| **Git workflow** | [.claude/rules/git-workflow.md](../.claude/rules/git-workflow.md) | Commits, branches, PRs |
| **Communication** | [.claude/rules/communication-and-style.md](../.claude/rules/communication-and-style.md) | Writing, comments, error messages |

---

## Core Development Standards

**All developers must read these:**

- **[.claude/rules/README.md](../.claude/rules/README.md)** — Development rules index & quick start
- **[.claude/rules/token-efficiency.md](../.claude/rules/token-efficiency.md)** — Message context efficiency (CRITICAL)
- **[.claude/rules/coding-style.md](../.claude/rules/coding-style.md)** — Naming, structure, imports, formatting
- **[.claude/rules/communication-and-style.md](../.claude/rules/communication-and-style.md)** — Writing, comments, commits, errors

---

## Security & Compliance

**Security reviews and standards:**

- **[.claude/rules/security.md](../.claude/rules/security.md)** — General security best practices
- **[.claude/rules/owasp-integration.md](../.claude/rules/owasp-integration.md)** — OWASP Top 10 mapped to nxgntch
- **[.claude/rules/code-review-checklist.md](../.claude/rules/code-review-checklist.md)** — Security code review process
- **[.claude/rules/agent-memory-guard.md](../.claude/rules/agent-memory-guard.md)** — Memory poisoning defense
- **[.claude/rules/security-config.md](../.claude/rules/security-config.md)** — Deployment security checklist

---

## Language-Specific Rules

**Python and FastAPI:**

- **[.claude/rules/python-conventions.md](../.claude/rules/python-conventions.md)** — Python-specific standards
- **[.claude/rules/fastapi-patterns.md](../.claude/rules/fastapi-patterns.md)** — FastAPI routing, DI, error handling
- **[.claude/rules/python-extensions.md](../.claude/rules/python-extensions.md)** — Extended Python rules

---

## Testing & Quality

**Test standards and coverage requirements:**

- **[.claude/rules/testing.md](../.claude/rules/testing.md)** — Test structure, coverage, TDD
- **Minimum coverage**: 85% across all modules (see [AUDIT.md](../AUDIT.md))
- **Test types**: Unit, integration, E2E (full guidance in testing.md)

---

## Version Control & Git

**Commit conventions and workflow:**

- **[.claude/rules/git-workflow.md](../.claude/rules/git-workflow.md)** — Conventional commits, branches, PR process
- **Format**: `type(scope): subject` (e.g., `feat(auth): add token validation`)
- **Types**: `feat`, `fix`, `test`, `docs`, `refactor`, `chore`, `perf`, `ci`, `style`

---

## Cost Management & Governance

**Financial controls and approval workflows:**

- **[.claude/rules/cost-management.md](../.claude/rules/cost-management.md)** — Cost tracking, budgets, enforcement
- **[.claude/rules/governance-extensions.md](../.claude/rules/governance-extensions.md)** — Spending approvals, phase gates
- **[.claude/rules/models.md](../.claude/rules/models.md)** — Claude model policy and pricing

---

## Advanced Topics

**Extended and domain-specific guidance:**

- **[.claude/rules/phase-gates.md](../.claude/rules/phase-gates.md)** — Phase completion criteria
- **[.claude/rules/mcp-chat-maintenance.md](../.claude/rules/mcp-chat-maintenance.md)** — Standalone MCP chat service

---

## Configuration Management

**IDE vs. Runtime configuration:**

- **IDE Guidance** (why we made decisions): [.claude/rules/](../.claude/rules/) MARKDOWN files
- **Runtime Configuration** (authoritative values): [config/](../config/) YAML files
  - `config/agents.yaml` — Agent definitions
  - `config/models.yaml` — Model pricing
  - `config/governance.yaml` — Budget caps

**Principle**: Never duplicate numbers between `.claude/rules/` and `config/` YAML. Always reference YAML from rules.

---

## File Checklist

**Before committing, verify:**

- [ ] Code follows [coding-style.md](../.claude/rules/coding-style.md)
- [ ] Python code follows [python-conventions.md](../.claude/rules/python-conventions.md)
- [ ] Tests pass (coverage ≥85%)
- [ ] Security review passed ([code-review-checklist.md](../.claude/rules/code-review-checklist.md))
- [ ] Commit message follows [git-workflow.md](../.claude/rules/git-workflow.md)
- [ ] No hardcoded secrets ([security.md](../.claude/rules/security.md))
- [ ] Input validated ([coding-style.md](../.claude/rules/coding-style.md))

---

## See Also

- **Navigation hubs** — [LINKS_NAVIGATION.md](LINKS_NAVIGATION.md)
- **Core documentation** — [LINKS_CORE_DOCS.md](LINKS_CORE_DOCS.md)
- **Skills & agents** — [LINKS_SKILLS_AGENTS.md](LINKS_SKILLS_AGENTS.md)
- **All development rules** — [.claude/rules/README.md](../.claude/rules/README.md)
