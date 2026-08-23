# Documentation Status & Index

**Last Updated**: 2026-08-22  
**Phase**: Phase 10 (Platform Maturity)

---

## Main Repository (Active Work)

### Core Navigation
- **[CLAUDE.md](CLAUDE.md)** - Project navigation hub and quick links
- **[README.md](README.md)** - Project overview
- **[AUDIT.md](AUDIT.md)** - Living audit trail with metrics and completion status

### Phase 10 Documentation
- **[SESSION_COMPLETION_SUMMARY.md](SESSION_COMPLETION_SUMMARY.md)** - Complete session overview (15 commits, optimization work)
- **[STARTUP_OPTIMIZATION.md](STARTUP_OPTIMIZATION.md)** - Startup cost reduction details (43% size, 60% speed)
- **[WORKFLOW_INTEGRATION.md](WORKFLOW_INTEGRATION.md)** - Complete workflow guide (500+ lines)
- **[REFERENCE_REPO.md](REFERENCE_REPO.md)** - Two-repository architecture guide
- **[TESTING_STRATEGY.md](TESTING_STRATEGY.md)** - Testing organization and guidelines (677/681 passing)
- **[SKILLS_AGENTS_INVENTORY.md](SKILLS_AGENTS_INVENTORY.md)** - Active skills and agents reference

### Development Rules & Standards
- **[it/.claude/rules/](it/.claude/rules/)** - 15+ development rule files:
  - `code-review-checklist.md` - Security review guidelines
  - `coding-style.md` - Naming and style conventions
  - `testing.md` - Test standards and TDD practices
  - `security.md` - Security best practices
  - `git-workflow.md` - Commit conventions
  - `communication-and-style.md` - Writing and documentation style
  - Plus 9 more specialized rules

### IDE Configuration
- **[it/.claude/IDE_SETUP.md](it/.claude/IDE_SETUP.md)** - IDE setup instructions
- **[it/.claude/WORKFLOWS.md](it/.claude/WORKFLOWS.md)** - Common development workflows
- **[it/.claude/settings.json](it/.claude/settings.json)** - Claude Code settings
- **[it/.claude/keybindings.json](it/.claude/keybindings.json)** - Custom keybindings

### Automation & Scripts
- **[scripts/daily-sync.sh](scripts/daily-sync.sh)** - Daily workflow sync
- **[scripts/archive-phase.sh](scripts/archive-phase.sh)** - Phase completion archival
- **[scripts/ref-search.sh](scripts/ref-search.sh)** - Reference material search
- **[scripts/sync-reference-docs.sh](scripts/sync-reference-docs.sh)** - Reference cache sync

---

## Reference Repository (Archive)

**Repository**: https://github.com/nxgntch/it-reference

### Historical Documentation
- **`docs/archive/phase-1/` through `phase-2.4/`** - Completed phase documentation
  - Phase completion reports
  - Architectural decisions
  - Performance metrics
  - Task planning documents

### Skill Planning & Design
- **`skills/planning/`** - Archived skill design materials:
  - Design templates
  - Planning examples
  - Skill architecture patterns
  - Historical implementations

### Recently Archived
- `docs/archive/phase-2.4/TEST_ANALYSIS.md` - Phase 2.4 test analysis
- `docs/archive/phase-2.4/TEST_STATUS.md` - Phase 2.4 test status
- `docs/archive/phase-2.4/WEEK3_SUMMARY.md` - Phase 2.4 week 3 summary

---

## Documentation Organization

### Main Repo Size
- **Total**: 27MB (lightweight startup)
- **Docs**: 500KB (active phase only)
- **Config**: 100KB (essential configurations)
- **Code**: 25MB (application code)

### What's NOT in Main Repo (Archived)
- ❌ Phase 1-9 documentation (in reference repo)
- ❌ Historical test reports
- ❌ Archived skill planning materials
- ❌ Legacy phase completion reports

### What IS in Main Repo (Active)
- ✅ Phase 10 work and planning
- ✅ Development rules and standards
- ✅ Current architecture documentation
- ✅ API specifications
- ✅ Deployment guides
- ✅ IDE configuration
- ✅ Workflow automation scripts

---

## Quick Access

| Need | Location |
|------|----------|
| **Project overview** | [README.md](README.md) |
| **Navigation hub** | [CLAUDE.md](CLAUDE.md) |
| **Living metrics** | [AUDIT.md](AUDIT.md) |
| **Development rules** | [it/.claude/rules/README.md](it/.claude/rules/README.md) |
| **Workflow setup** | [WORKFLOW_INTEGRATION.md](WORKFLOW_INTEGRATION.md) |
| **Testing strategy** | [TESTING_STRATEGY.md](TESTING_STRATEGY.md) |
| **Phase 10 status** | [SESSION_COMPLETION_SUMMARY.md](SESSION_COMPLETION_SUMMARY.md) |
| **IDE setup** | [it/.claude/IDE_SETUP.md](it/.claude/IDE_SETUP.md) |
| **Test archive** | https://github.com/nxgntch/it-reference/tree/main/tests |
| **Historical context** | https://github.com/nxgntch/it-reference |

---

## Documentation Maintenance

### When to Archive
- Phase completion → move to reference repo (use `bash scripts/archive-phase.sh`)
- Historical analysis → move to reference repo
- Outdated guides → remove or archive

### When to Keep
- Active phase work
- Development standards (evergreen)
- API documentation
- Configuration reference
- Current roadmap

### Sync with Reference Repo
```bash
# One-time sync
bash scripts/sync-reference-docs.sh

# Auto-sync (weekly)
bash scripts/daily-sync.sh
```

---

## Testing Architecture

### Main Repo (`tests/`)
- ✅ **677/681 active tests** (99.4% passing)
- ✅ Run on every commit (CI/CD gate)
- ✅ Validate current Phase 10 functionality
- ✅ Developer feedback loop (pytest locally)

### Reference Repo (`nxgntch-it-reference/tests/`)
- 📚 `archive/` - Old phase test implementations
- 📊 `benchmarks/` - Performance data by phase
- 📈 `coverage-reports/` - Coverage snapshots
- 📖 `TEST_ARCHIVE_GUIDE.md` - Archive management

**Strategy**: Keep active tests in main, archive historical materials to reference repo.

---

## File Cleanup Complete ✅

**Archived to reference repo**:
- `WEEK3_SUMMARY.md` - Phase 2.4 specific (✅ moved)
- `TEST_ANALYSIS.md` - Historical analysis (✅ moved)
- `TEST_STATUS.md` - Historical status (✅ moved)

**Result**: Main repo is now clean with only active Phase 10 documentation.

**Test Archive Structure**: Created in reference repo for historical materials.
- Phase-specific test implementations
- Performance benchmarks
- Coverage reports by phase

---

**Status**: Ready for Phase 10 work and team collaboration.
