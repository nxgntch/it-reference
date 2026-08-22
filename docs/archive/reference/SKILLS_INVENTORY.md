# Skills Inventory

**Central registry of all skills in nxgntch** for discovery, documentation, and team assignment.

All skills are discoverable from this single table. For detailed documentation on each skill, follow the links in the "Documentation" column.

---

## Quick Navigation

| Category | Count | Skills |
|----------|-------|--------|
| **Design** | 3 | gpt-taste, image-to-code, redesign |
| **Documentation** | 1 | docOptimizer |
| **Operations & Governance** | 4 | costAnalyzer, deploymentValidator, phaseVerifier, incidentRunner |
| **Security & Compliance** | 2 | securityAudit, preCommitAuditor |
| **Configuration & System** | 2 | configSync, agentCapabilityMapper |
| **TOTAL** | **12** | |

---

## All Skills (Master Registry)

| ID | Name | Team | Category | Status | Description | Documentation |
|---|---|---|---|---|---|---|
| **gpt-taste** | Elite Design Enforcement | Design | Design | Active | Build award-winning hero sections and premium components with Python-driven randomization, motion-rich layouts, and elite visual standards | [.claude/skills/gpt-taste/SKILL.md](./../.claude/skills/gpt-taste/SKILL.md) |
| **image-to-code** | Design-First Workflow | Design | Design | Active | Design-first approach: generate section-by-section images, analyze deeply, implement faithful frontend code with high visual fidelity | [.claude/skills/image-to-code/SKILL.md](./../.claude/skills/image-to-code/SKILL.md) |
| **redesign** | Upgrade Existing Projects | Design | Design | Active | Audit existing websites and apply targeted design improvements: typography, colors, layout, interactivity without complete rewrites | [.claude/skills/redesign/SKILL.md](./../.claude/skills/redesign/SKILL.md) |
| **docOptimizer** | Documentation Optimization | Documentation | Documentation | Active | Audit, analyze, and optimize repository documentation systems; eliminate duplication, reduce cognitive load, establish single source of truth | [.claude/skills/docOptimizer/SKILL.md](./../.claude/skills/docOptimizer/SKILL.md) |
| **costAnalyzer** | Cost Analysis & Optimization | Operations | Operations & Governance | Active | Analyze spending patterns, provide cost optimization recommendations, track budgets by team and agent, forecast monthly spending | [.claude/skills/costAnalyzer.py](./../.claude/skills/costAnalyzer.py) |
| **deploymentValidator** | Deployment Validator | Operations | Operations & Governance | Active | Validate deployment readiness: security checks, configuration validation, dependency verification, smoke tests | [.claude/skills/deploymentValidator.py](./../.claude/skills/deploymentValidator.py) |
| **phaseVerifier** | Phase Completion Verifier | Operations | Operations & Governance | Active | Verify phase completion criteria, validate deliverables, generate phase completion reports, assess Go/No-Go status | [.claude/skills/phaseVerifier.py](./../.claude/skills/phaseVerifier.py) |
| **incidentRunner** | Incident Response Runner | Operations | Operations & Governance | Active | Execute incident response procedures, coordinate response actions, document incidents, track post-mortems | [.claude/skills/incidentRunner.py](./../.claude/skills/incidentRunner.py) |
| **securityAudit** | Security Audit & OWASP Compliance | Security | Security & Compliance | Active | Audit codebase for OWASP Top 10 vulnerabilities, check secure coding practices, validate security controls | [.claude/skills/securityAudit.py](./../.claude/skills/securityAudit.py) |
| **preCommitAuditor** | Pre-Commit Security Auditor | Security | Security & Compliance | Active | Run pre-commit security checks: secret scanning, dependency audit, code analysis before commits | [.claude/skills/preCommitAuditor.py](./../.claude/skills/preCommitAuditor.py) |
| **configSync** | Configuration Synchronization | Infrastructure | Configuration & System | Active | Synchronize configuration across environments, validate YAML configs, manage configuration drift | [.claude/skills/configSync.py](./../.claude/skills/configSync.py) |
| **agentCapabilityMapper** | Agent Capability Mapper | Infrastructure | Configuration & System | Active | Map agent capabilities to teams, verify agent hierarchy, validate capability assignments, generate capability reports | [.claude/skills/agentCapabilityMapper.py](./../.claude/skills/agentCapabilityMapper.py) |

---

## Skills by Team

### Design Team (3 skills)
Focus: Frontend excellence, design enforcement, visual quality, user experience.

- **gpt-taste**: Award-winning design enforcement for hero sections and premium components
- **image-to-code**: Design-first workflow with section-by-section image generation and code implementation
- **redesign**: Targeted design audits and improvements for existing projects

**Related**: [CLAUDE.md § Design Skills](../CLAUDE.md#design-skills)

### Documentation Team (1 skill)
Focus: Documentation optimization, knowledge management, cognitive load reduction.

- **docOptimizer**: Systematic documentation audit and optimization (4-phase: preparation, restructuring, deduplication, consolidation)

**Related**: [docs/PHASE_2_COMPLETION_REPORT.md](PHASE_2_COMPLETION_REPORT.md), [docs/PHASE_3_COMPLETION_REPORT.md](PHASE_3_COMPLETION_REPORT.md)

### Operations & Governance (4 skills)
Focus: Cost control, deployment management, phase tracking, incident response.

- **costAnalyzer**: Cost analysis, budget forecasting, team spending reports
- **deploymentValidator**: Pre-deployment verification, smoke tests, configuration validation
- **phaseVerifier**: Phase completion verification, deliverable validation, Go/No-Go assessment
- **incidentRunner**: Incident coordination, response execution, post-mortem tracking

**Related**: [docs/MIGRATION_PLAN.md](MIGRATION_PLAN.md), [AUDIT.md](../AUDIT.md)

### Security & Compliance (2 skills)
Focus: Vulnerability detection, secure coding, OWASP compliance, pre-commit checks.

- **securityAudit**: OWASP Top 10 vulnerability assessment, secure coding practice verification
- **preCommitAuditor**: Automated secret scanning, dependency security checks, code security analysis

**Related**: [.claude/rules/security.md](../.claude/rules/security.md), [.claude/rules/owasp-integration.md](../.claude/rules/owasp-integration.md)

### Configuration & System (2 skills)
Focus: Configuration management, system integration, capability mapping.

- **configSync**: Configuration synchronization, environment parity, YAML validation
- **agentCapabilityMapper**: Agent capability mapping, hierarchy validation, team assignments

**Related**: [config/agents.yaml](../config/agents.yaml), [config/governance.yaml](../config/governance.yaml)

---

## Skill Discovery & Usage

### Finding the Right Skill

**For design questions** → See [CLAUDE.md § Design Skills](../CLAUDE.md#design-skills) or use **gpt-taste**, **image-to-code**, **redesign**

**For documentation optimization** → Use **docOptimizer** with `--plan` and `--execute` commands

**For cost & budget queries** → Use **costAnalyzer** to analyze spending, forecast budgets, identify optimization opportunities

**For security reviews** → Use **securityAudit** for vulnerability assessment or **preCommitAuditor** for pre-commit checks

**For deployment** → Use **deploymentValidator** to verify readiness before production release

**For phase tracking** → Use **phaseVerifier** to validate completion criteria and Go/No-Go status

**For incident response** → Use **incidentRunner** to coordinate response and track resolution

### Common Workflows

**Design a new feature:**
1. Use **gpt-taste** for hero/landing page sections
2. Use **image-to-code** for full design-to-code workflow
3. Use **redesign** if upgrading existing components

**Optimize documentation:**
1. Use **docOptimizer --audit** to scan current state
2. Use **docOptimizer --plan** to design strategy
3. Use **docOptimizer --execute phase-N** to implement changes
4. Use **docOptimizer --verify** to validate completion

**Release to production:**
1. Use **preCommitAuditor** for pre-commit security checks
2. Use **securityAudit** for comprehensive vulnerability assessment
3. Use **costAnalyzer** to review budget status
4. Use **deploymentValidator** to verify deployment readiness

**Monitor ongoing operations:**
1. Use **costAnalyzer** for weekly cost reports
2. Use **phaseVerifier** for phase progress tracking
3. Use **incidentRunner** if critical issues arise

---

## Skill Command Reference

| Skill | Primary Commands | Invocation |
|-------|-----------------|-----------|
| **gpt-taste** | Design hero/components | `/gpt-taste` with design prompt |
| **image-to-code** | Design-first workflow | `/image-to-code` with design requirements |
| **redesign** | Upgrade existing design | `/redesign` with project details |
| **docOptimizer** | --audit, --plan, --execute phase-N, --verify | `/docOptimizer --audit` |
| **costAnalyzer** | analyze, forecast, report | Via API or agent invocation |
| **deploymentValidator** | validate | Via deployment pipeline |
| **phaseVerifier** | verify, report | Via CI/CD or manual trigger |
| **incidentRunner** | execute, coordinate | Via incident management system |
| **securityAudit** | scan, report | Via CI/CD or manual trigger |
| **preCommitAuditor** | check | Via pre-commit hook |
| **configSync** | sync, validate | Via autosync pipeline |
| **agentCapabilityMapper** | map, validate | Via system initialization |

---

## Integration & Dependencies

### Skills in Agent Configuration

**Director Agent** (routing, orchestration):
- docOptimizer (cost_tier: quick)

**Engineering Manager Agent** (technical execution):
- docOptimizer (cost_tier: standard)

**Design Agent** (frontend excellence):
- gpt-taste
- image-to-code
- redesign

See [`config/agents.yaml`](../config/agents.yaml) for current agent-skill assignments.

### Skills in CI/CD Pipeline

- **preCommitAuditor**: Runs before every commit (secret scanning, dependencies)
- **securityAudit**: Runs in CI pipeline (OWASP compliance, vulnerability scan)
- **deploymentValidator**: Runs before production deployment (smoke tests, readiness checks)
- **costAnalyzer**: Runs on schedule (daily cost reports, budget alerts)
- **phaseVerifier**: Runs at phase completion (deliverable validation, Go/No-Go)

### Skills in Autosync Pipeline

- **configSync**: Validates configuration across environment/workspace/mpc-chat
- **agentCapabilityMapper**: Verifies agent assignments and team capability matrix

---

## Maintenance & Updates

### Adding a New Skill

1. Create skill in `.claude/skills/<skill-id>/SKILL.md` or `.claude/skills/<skill-id>.py`
2. Add entry to this SKILLS_INVENTORY.md table
3. Update [.claude/rules/README.md](../.claude/rules/README.md) if applicable
4. Update [CLAUDE.md](../CLAUDE.md) navigation if new category
5. Wire into agent config ([config/agents.yaml](../config/agents.yaml)) if agent-based
6. Update [docs/INDEX.md](INDEX.md) with new skill reference

### Updating Skill Metadata

When a skill's status, team, or description changes:
1. Update this SKILLS_INVENTORY.md table entry
2. Update referenced skill documentation (SKILL.md or .py file)
3. Commit changes together (inventory + skill doc)
4. Update related phase completion reports if applicable

### Deprecating a Skill

1. Change "Status" to "Deprecated" in this table
2. Add migration path (recommend replacement skill)
3. Remove from agent config if wired in
4. Keep documentation for reference (archive in LINKS_ARCHIVE.md later)

---

## See Also

- **Quick Start**: [CLAUDE.md](../CLAUDE.md) § Quick Navigation by Role
- **Design Guidance**: [.claude/skills/README.md](../.claude/skills/README.md)
- **Agent Configuration**: [config/agents.yaml](../config/agents.yaml)
- **Documentation Index**: [docs/INDEX.md](INDEX.md)
- **All Documentation**: [docs/LINKS_NAVIGATION.md](LINKS_NAVIGATION.md)

---

**Last updated**: 2026-08-20  
**Total skills**: 12 (4 directory-based, 8 Python utility)  
**Status**: Complete for Phase 4 Skill Inventory Consolidation
