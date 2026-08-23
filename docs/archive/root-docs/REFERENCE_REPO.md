# Reference Repository Guide

**Primary Reference**: [`nxgntch/it-reference`](https://github.com/nxgntch/it-reference)

This document explains how to access archived skills, agents, and documentation.

## Repository Structure

### Active (nxgntch/it) 
Contains runtime code and current documentation:
- `it/app/` - Application code (FastAPI)
- `it/config/` - Configuration files
- `it/docs/` - Active documentation
- `it/scripts/` - Utility scripts
- `it/tests/` - Test suite

### Reference (nxgntch/it-reference)
Contains archived documentation NOT needed for startup:
- `docs/archive/` - Completed phase documentation (Phases 1-8)
- `skills/planning/` - Skill design and planning materials

## Accessing Reference Materials

### Option 1: Browse on GitHub
Visit [`nxgntch/it-reference`](https://github.com/nxgntch/it-reference) directly

### Option 2: Clone Reference Repo
```bash
git clone https://github.com/nxgntch/it-reference.git reference-docs
```

### Option 3: Auto-Sync Reference Docs
```bash
bash scripts/sync-reference-docs.sh
# Creates .reference-cache/ with full archive
```

## What's in the Reference Repo

### Historical Phase Documentation
- `PHASE_1_COMPLETION_REPORT.md` - Foundation phase
- `PHASE_2_COMPLETION_REPORT.md` - Integration phase
- `PHASE_3_COMPLETION_REPORT.md` - Security hardening
- `PHASE_4_COMPLETION_REPORT.md` - Cost control
- Plus additional historical context

### Skill Planning Materials
- `SKILL.md` - Planning skill definition
- `scripts/` - Planning automation tools
- `templates/` - Reusable templates
- `examples.md` - Skill examples
- `reference.md` - Planning reference

## When to Use Each Repo

| Need | Repository | Why |
|------|-----------|-----|
| **Running nxgntch** | nxgntch/it | Has all runtime code |
| **Current development** | nxgntch/it | Active guides and rules |
| **Historical context** | nxgntch/it-reference | Lightweight startup |
| **Completed phase reports** | nxgntch/it-reference | Archives only |
| **Future planning** | nxgntch/it-reference | Design materials |
| **Performance critical** | nxgntch/it | Pre-optimized startup |

## Adding New Skills/Agents

When creating new skills or agents:

1. **Active development**: Work in `it/skills/` or `it/config/`
2. **Documentation**: Add to `it/docs/` for active docs
3. **Archive**: Move planning materials to `nxgntch/it-reference` after completion
4. **Reference**: Link completed docs to reference repo

## Sync Strategy

```bash
# Main repo stays lightweight
# Reference repo holds all historical context

# Development workflow:
1. Clone nxgntch/it
2. Work on new skills/agents
3. Document in it/docs/
4. Push to nxgntch/it
5. After completion, archive planning to nxgntch/it-reference
6. Run sync-reference-docs.sh for offline access (optional)
```

## CI/CD Integration

### Build Pipeline
```bash
# Fast path - uses startup-critical config
pytest tests/  # Uses lazy-loaded config

# Optional: include reference docs
bash scripts/sync-reference-docs.sh
pytest tests/  # Full config available
```

### Deployment
```bash
# Docker build uses nxgntch/it only
# Reference repo available but not required
docker build -t nxgntch:latest .
```

## FAQ

**Q: Where are the old Phase 1-8 docs?**
A: In [`nxgntch/it-reference`](https://github.com/nxgntch/it-reference) for historical reference

**Q: Can I edit archived docs?**
A: Yes, they're in a public repo. Submit PRs to `nxgntch/it-reference`

**Q: Do I need the reference repo to run nxgntch?**
A: No, it's optional. Runtime startup doesn't load it.

**Q: How do I access planning templates?**
A: Clone `nxgntch/it-reference` or run `scripts/sync-reference-docs.sh`

**Q: Will reference docs be kept in sync?**
A: Yes, we'll cherry-pick important updates from it-reference back to it/ as needed

## Links

- **Main Repository**: https://github.com/nxgntch/it
- **Reference Repository**: https://github.com/nxgntch/it-reference
- **Startup Optimization**: [`STARTUP_OPTIMIZATION.md`](STARTUP_OPTIMIZATION.md)
- **Configuration**: [`config/startup-critical.yaml`](config/startup-critical.yaml)
