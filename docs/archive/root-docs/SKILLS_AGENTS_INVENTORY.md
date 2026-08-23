# Skills & Agents Inventory

Master reference for all active skills and agents with links to their definitions and documentation.

## Active Skills (Phase 10)

| Skill | Location | Status | Reference |
|-------|----------|--------|-----------|
| **codeReview** | `it/skills/codeReview/` | ✅ Active (v1.1) | [`SKILL.md`](https://github.com/nxgntch/it/blob/main/it/skills/codeReview/SKILL.md) |
| **docReviewer** | `it/skills/docReviewer/` | ✅ Active (v1.1) | [`SKILL.md`](https://github.com/nxgntch/it/blob/main/it/skills/docReviewer/SKILL.md) |
| **docUpdater** | `it/skills/docUpdater/` | ✅ Active (v1.1) | [`SKILL.md`](https://github.com/nxgntch/it/blob/main/it/skills/docUpdater/SKILL.md) |
| **brandVoice** | `it/skills/brandVoice/` | ✅ Active | [`SKILL.md`](https://github.com/nxgntch/it/blob/main/it/skills/brandVoice/SKILL.md) |
| **codeGeneration** | `it/skills/codeGeneration/` | ✅ Active | [`SKILL.md`](https://github.com/nxgntch/it/blob/main/it/skills/codeGeneration/SKILL.md) |

**See full list**: [`it/skills/`](it/skills/) directory

## Active Agents (Phase 10)

| Agent | Role | Model | Location | Config |
|-------|------|-------|----------|--------|
| **executor** | Critical execution | haiku | `it/agents/` | [`config/startup-critical.yaml`](config/startup-critical.yaml) |
| **router** | Request routing | haiku | `it/agents/` | [`config/startup-critical.yaml`](config/startup-critical.yaml) |

**See full config**: [`it/config/agents.yaml`](it/config/agents.yaml)

## Historical Skills (Phase 1-9 Archive)

Archived skills and planning materials are in the reference repository:

### Location
📦 [`nxgntch/it-reference`](https://github.com/nxgntch/it-reference)

### Contents
- `skills/planning/` - All skill planning and design materials
  - Design templates
  - Examples and reference
  - Planning scripts and automation
  
**Access archived skills**:
```bash
# Option 1: Browse on GitHub
https://github.com/nxgntch/it-reference/tree/master/skills/planning

# Option 2: Clone reference repo
git clone https://github.com/nxgntch/it-reference.git reference-docs

# Option 3: Auto-sync
bash scripts/sync-reference-docs.sh
```

## Historical Phases (Phase 1-8 Archive)

Complete phase documentation archived in reference repository:

### Location
📦 [`nxgntch/it-reference/docs/archive/`](https://github.com/nxgntch/it-reference/tree/master/docs/archive)

### Contents
- `PHASE_1_COMPLETION_REPORT.md` - Foundation phase
- `PHASE_2_COMPLETION_REPORT.md` - Integration phase
- `PHASE_3_COMPLETION_REPORT.md` - Security hardening
- `PHASE_4_COMPLETION_REPORT.md` - Cost control
- Plus additional historical context and progress reports

## IDE Skills

**Platform Skills** (available in VS Code/JetBrains plugins):
See [`it/config/skills.yaml`](it/config/skills.yaml) for complete configuration.

**Reference**: [`it/.claude/SKILLS_INVENTORY.md`](it/.claude/SKILLS_INVENTORY.md)

## Adding New Skills/Agents

### Workflow

1. **Create skill definition** in `it/skills/`
   ```
   it/skills/mySkill/
   ├── SKILL.md          # Skill definition
   └── [optional files]
   ```

2. **Register in config**
   ```yaml
   # it/config/skills.yaml
   skills:
     - id: mySkill
       name: My Skill
       type: ide | platform
   ```

3. **Document**
   - Add to `it/docs/guides/development/IDE_SKILLS_INVENTORY.md`
   - Update `SKILLS_AGENTS_INVENTORY.md` (this file)

4. **Archive planning materials** (after completion)
   - Move design docs to `nxgntch/it-reference`
   - Keep implementation in `nxgntch/it`

## Configuration Reference

### Critical Config (Loaded at Startup)
- **File**: [`config/startup-critical.yaml`](config/startup-critical.yaml)
- **Contains**: 2 core agents, essential models
- **Load time**: ~40ms

### Full Config (Lazy Loaded)
- **File**: [`config/agents.yaml`](it/config/agents.yaml)
- **Contains**: All agent definitions
- **Loaded**: On-demand when needed

### Skills Registry
- **File**: [`config/skills.yaml`](it/config/skills.yaml)
- **Contains**: All skill definitions
- **Loaded**: On-demand

## Repository References

### nxgntch/it (Primary)
- **URL**: https://github.com/nxgntch/it
- **Contains**: Runtime code, active documentation, configuration
- **Size**: ~27MB (optimized startup)
- **Use for**: Development, deployment, current skills/agents

### nxgntch/it-reference (Archive)
- **URL**: https://github.com/nxgntch/it-reference
- **Contains**: Historical phases, planning materials, archived skills
- **Size**: ~570KB
- **Use for**: Historical context, learning, design inspiration

## Quick Links

| Resource | Link |
|----------|------|
| Active Skills | [`it/skills/`](it/skills/) |
| Skill Configuration | [`it/config/skills.yaml`](it/config/skills.yaml) |
| Agent Configuration | [`it/config/agents.yaml`](it/config/agents.yaml) |
| Startup Config | [`config/startup-critical.yaml`](config/startup-critical.yaml) |
| Phase Documentation | [`nxgntch/it-reference/docs/archive/`](https://github.com/nxgntch/it-reference/tree/master/docs/archive) |
| Skill Planning | [`nxgntch/it-reference/skills/planning/`](https://github.com/nxgntch/it-reference/tree/master/skills/planning) |
| Full Reference | [`REFERENCE_REPO.md`](REFERENCE_REPO.md) |

## Notes

- ✅ **Phase 10**: Current development phase (active skills above)
- 📦 **Archive**: Phases 1-9 complete (see nxgntch/it-reference)
- 🚀 **Optimized**: Startup loads only critical skills/agents
- 🔄 **Maintained**: Both repos kept in sync for reference purposes
- 📚 **Historical**: Planning materials available for future development

Last updated: 2026-08-22
