# IDE Skills Inventory

**Central registry of all development and engineering skills used by the nxgntch team** to build and improve nxgntch.

These are tools FOR developers working ON nxgntch. For skills offered BY nxgntch (runtime), see [`PLATFORM_SKILLS_INVENTORY.md`](PLATFORM_SKILLS_INVENTORY.md).

---

## Quick Navigation

| Category | Count | Skills |
|----------|-------|--------|
| **Code Quality & Review** | 3 | codeReview, securityReview, integration |
| **Documentation** | 2 | docReviewer, docUpdater |
| **Architecture & Design** | 6 | agentArchitectureAudit, apiDesign, architectureDecisionRecords, autonomousLoops, decomposition, routing |
| **Analysis & Research** | 5 | competitivePlatformAnalysis, contentEngine, cost-analyzer, cost-aware-llm-pipeline, researchSynthesis |
| **Planning & Coordination** | 6 | brandVoice, cross-team-synthesis, decision-making, planning, task-intake, (planning-with-files) |
| **TOTAL** | **22** | |

---

## All Skills (Master Registry)

| ID | Name | Category | Team | Status | Description | Documentation |
|---|---|---|---|---|---|---|
| **codeReview** | Code Review | Code Quality | Engineering | Active | Collaborative code review with detailed feedback on style, types, bugs, and security | [skills/codeReview/SKILL.md](../skills/codeReview/SKILL.md) |
| **securityReview** | Security Review | Code Quality | Engineering | Active | Security vulnerability detection and mitigation for auth, data handling, and APIs | [skills/securityReview/SKILL.md](../skills/securityReview/SKILL.md) |
| **integration** | Integration | Code Quality | Engineering | Active | Integration testing and multi-component validation | [skills/integration/SKILL.md](../skills/integration/SKILL.md) |
| **docReviewer** | Doc Reviewer | Documentation | Documentation | Active | Review and audit documentation for completeness, accuracy, and consistency | [skills/docReviewer/SKILL.md](../skills/docReviewer/SKILL.md) |
| **docUpdater** | Doc Updater | Documentation | Documentation | Active | Auto-generate documentation from task outputs and code changes | [skills/docUpdater/SKILL.md](../skills/docUpdater/SKILL.md) |
| **agentArchitectureAudit** | Agent Architecture Audit | Architecture | Architecture | Active | Audit agent hierarchy, capabilities, and routing logic | [skills/agentArchitectureAudit/SKILL.md](../skills/agentArchitectureAudit/SKILL.md) |
| **apiDesign** | API Design | Architecture | Architecture | Active | Design and document APIs and interfaces | [skills/apiDesign/SKILL.md](../skills/apiDesign/SKILL.md) |
| **architectureDecisionRecords** | Architecture Decision Records | Architecture | Architecture | Active | Document architectural decisions and trade-offs | [skills/architectureDecisionRecords/SKILL.md](../skills/architectureDecisionRecords/SKILL.md) |
| **autonomousLoops** | Autonomous Loops | Architecture | Architecture | Active | Design and validate autonomous execution loops for agents | [skills/autonomousLoops/SKILL.md](../skills/autonomousLoops/SKILL.md) |
| **decomposition** | Decomposition | Architecture | Planning | Active | Break complex tasks into subtasks and dependency mapping | [skills/decomposition/SKILL.md](../skills/decomposition/SKILL.md) |
| **routing** | Routing | Architecture | Orchestration | Active | Agent routing logic and task delegation patterns | [skills/routing/SKILL.md](../skills/routing/SKILL.md) |
| **competitivePlatformAnalysis** | Competitive Platform Analysis | Analysis | Research | Active | Analyze competitive platforms and feature gaps | [skills/competitivePlatformAnalysis/SKILL.md](../skills/competitivePlatformAnalysis/SKILL.md) |
| **contentEngine** | Content Engine | Analysis | Content | Active | Generate content, templates, and boilerplate | [skills/contentEngine/SKILL.md](../skills/contentEngine/SKILL.md) |
| **cost-analyzer** | Cost Analyzer | Analysis | Operations | Active | Analyze spending patterns and optimize costs | [skills/cost-analyzer/SKILL.md](../skills/cost-analyzer/SKILL.md) |
| **cost-aware-llm-pipeline** | Cost-Aware LLM Pipeline | Analysis | Operations | Active | Design cost-efficient LLM invocation patterns | [skills/cost-aware-llm-pipeline/SKILL.md](../skills/cost-aware-llm-pipeline/SKILL.md) |
| **researchSynthesis** | Research Synthesis | Analysis | Research | Active | Synthesize research findings into actionable insights | [skills/researchSynthesis/SKILL.md](../skills/researchSynthesis/SKILL.md) |
| **brandVoice** | Brand Voice | Planning | Marketing | Active | Maintain consistent brand voice and messaging | [skills/brandVoice/SKILL.md](../skills/brandVoice/SKILL.md) |
| **cross-team-synthesis** | Cross-Team Synthesis | Planning | Coordination | Active | Coordinate insights and decisions across teams | [skills/cross-team-synthesis/SKILL.md](../skills/cross-team-synthesis/SKILL.md) |
| **decision-making** | Decision-Making | Planning | Leadership | Active | Facilitate decisions and consensus across teams | [skills/decision-making/SKILL.md](../skills/decision-making/SKILL.md) |
| **planning** | Planning | Planning | Planning | Active | Manus-style persistent file-based planning with context recovery | [skills/planning/SKILL.md](../skills/planning/SKILL.md) |
| **task-intake** | Task Intake | Planning | Coordination | Active | Intake and triage incoming tasks and requests | [skills/task-intake/SKILL.md](../skills/task-intake/SKILL.md) |

---

## Skills by Category

### Code Quality & Review (3 skills)
Focus: Code review, testing, and security validation.

- **codeReview**: Collaborative code review with detailed feedback on style, types, bugs, security
- **securityReview**: Vulnerability detection, auth/data handling checks, API security
- **integration**: Integration testing and multi-component validation

### Documentation (2 skills)
Focus: Documentation creation, review, and maintenance.

- **docReviewer**: Review documentation for completeness, accuracy, consistency
- **docUpdater**: Auto-generate documentation from task outputs and code changes

### Architecture & Design (6 skills)
Focus: System design, agent architecture, routing, and decision documentation.

- **agentArchitectureAudit**: Audit agent hierarchy, capabilities, routing
- **apiDesign**: Design and document APIs and interfaces
- **architectureDecisionRecords**: Document architectural decisions and trade-offs
- **autonomousLoops**: Design and validate autonomous execution loops
- **decomposition**: Break tasks into subtasks with dependency mapping
- **routing**: Agent routing logic and task delegation patterns

### Analysis & Research (5 skills)
Focus: Data analysis, competitive research, cost optimization.

- **competitivePlatformAnalysis**: Analyze competitive platforms and identify gaps
- **contentEngine**: Generate content, templates, boilerplate
- **cost-analyzer**: Analyze spending patterns and optimize costs
- **cost-aware-llm-pipeline**: Design cost-efficient LLM invocation patterns
- **researchSynthesis**: Synthesize research findings into actionable insights

### Planning & Coordination (6 skills)
Focus: Project planning, cross-team coordination, task management.

- **brandVoice**: Maintain consistent brand voice and messaging
- **cross-team-synthesis**: Coordinate insights and decisions across teams
- **decision-making**: Facilitate decisions and consensus
- **planning**: Persistent file-based planning with context recovery (planning-with-files)
- **task-intake**: Intake and triage incoming tasks and requests

---

## Skill Discovery & Usage

### When to Use Each Skill

**For code review questions** → Use **codeReview** for style/quality, **securityReview** for vulnerabilities, **integration** for multi-component testing

**For documentation work** → Use **docReviewer** to audit docs, **docUpdater** to auto-generate from code

**For architecture questions** → Use **agentArchitectureAudit** for agent structure, **apiDesign** for API contracts, **routing** for delegation logic, **decomposition** for task breakdown

**For research & analysis** → Use **competitivePlatformAnalysis** for market analysis, **cost-analyzer** for spending, **researchSynthesis** for insights

**For planning & coordination** → Use **planning** for persistent file-based planning, **task-intake** for triaging work, **decision-making** for consensus, **cross-team-synthesis** for alignment

### Common Workflows

**Code Review Process:**
1. Use **codeReview** for general code quality feedback
2. Use **securityReview** for security-sensitive changes
3. Use **integration** to validate multi-component changes

**Documentation Refresh:**
1. Use **docReviewer** to audit current state
2. Use **docUpdater** to generate missing docs
3. Commit results

**Architecture Decision:**
1. Use **agentArchitectureAudit** to understand current state
2. Use **apiDesign** if designing new interfaces
3. Use **architectureDecisionRecords** to document decision
4. Use **decomposition** to break into implementation tasks

**New Feature Planning:**
1. Use **task-intake** to scope incoming request
2. Use **decomposition** to break into subtasks
3. Use **planning** for persistent tracking
4. Use **agentArchitectureAudit** to assess routing impact

---

## Integration with nxgntch Systems

### Agents Using IDE Skills

| Agent | Skills Used | Location |
|-------|------------|----------|
| **codeReviewer** | codeReview, securityReview, integration | .claude-plugin/agents/README.md |
| **planner** | planning, decomposition, task-intake | .claude-plugin/agents/README.md |
| **docUpdater** | docUpdater, docReviewer | .claude-plugin/agents/README.md |

See [.claude-plugin/agents/README.md](../.claude-plugin/agents/README.md) for complete agent definitions.

### CI/CD Integration Points

- **codeReview**: Runs pre-PR (optional manual invocation)
- **securityReview**: Runs in security check stage
- **integration**: Runs in integration test stage
- **docUpdater**: Runs post-merge to update docs
- Others: On-demand or team assignment

---

## Maintenance & Updates

### Adding a New Skill

1. Create skill in `skills/<skill-id>/SKILL.md` with YAML metadata (id, name, description, category, team, enabled)
2. Add entry to this IDE_SKILLS_INVENTORY.md table
3. Organize under appropriate category (or create new one if needed)
4. Update [docs/INDEX.md](INDEX.md) if new category added
5. Wire into `.claude-plugin/agents/README.md` if agent-based
6. Update tests in [tests/test_documentation_module.py](../tests/test_documentation_module.py)

### Updating Skill Metadata

When a skill's status, category, or description changes:
1. Update `skills/<skill-id>/SKILL.md` YAML header
2. Update this IDE_SKILLS_INVENTORY.md entry
3. Commit changes together
4. Update related phase reports if applicable

### Deprecating a Skill

1. Change "Status" to "Deprecated" in this table
2. Add migration path (recommend replacement skill)
3. Remove from agent config if wired in
4. Keep documentation for reference

---

## Comparison: Platform vs. IDE Skills

| Aspect | Platform Skills | IDE Skills |
|--------|---|---|
| **What they are** | Services offered BY nxgntch | Tools used BY developers TO BUILD nxgntch |
| **Location** | `.claude/skills/` | `skills/` |
| **Documentation** | [PLATFORM_SKILLS_INVENTORY.md](PLATFORM_SKILLS_INVENTORY.md) | [IDE_SKILLS_INVENTORY.md](IDE_SKILLS_INVENTORY.md) (this file) |
| **Audience** | End users of nxgntch | nxgntch team members |
| **Examples** | docOptimizer, costAnalyzer | codeReview, securityReview, planning, docUpdater |
| **Configuration** | [config/agents.yaml](../config/agents.yaml) | [.claude-plugin/agents/README.md](../.claude-plugin/agents/README.md) |
| **Count** | 12 | 22 |

**Navigation:**
- **Looking for platform skills (what nxgntch does)?** → See [PLATFORM_SKILLS_INVENTORY.md](PLATFORM_SKILLS_INVENTORY.md)
- **Looking for IDE skills (how to build nxgntch)?** → See [IDE_SKILLS_INVENTORY.md](IDE_SKILLS_INVENTORY.md) (this file)

---

## See Also

- **Platform Skills**: [PLATFORM_SKILLS_INVENTORY.md](PLATFORM_SKILLS_INVENTORY.md) (what nxgntch offers to users)
- **Agent Configuration**: [.claude-plugin/agents/README.md](../.claude-plugin/agents/README.md)
- **Documentation Index**: [docs/INDEX.md](INDEX.md)
- **Navigation Hub**: [CLAUDE.md](../CLAUDE.md)
- **All Documentation**: [LINKS_NAVIGATION.md](LINKS_NAVIGATION.md)

---

**Last updated**: 2026-08-20  
**Total IDE skills**: 22  
**Status**: Complete for Phase 5.1 (IDE Skills Consolidation)
