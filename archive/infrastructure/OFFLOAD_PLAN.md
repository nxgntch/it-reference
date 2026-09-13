# Archive Offload Plan

**Purpose**: Move archived and historical documentation to nxgntch/it-reference to reduce main repo size while preserving complete project history.

## Documents to Offload

### Phase 11 Documentation (10 files)
Located in `docs/archive/phase-11/` and `docs/archive/phase-11-root-docs/`

**API & Usage** (3 files):
- PHASE_11_API_REFERENCE.md
- PHASE_11_USAGE_EXAMPLES.md
- PHASE_11_WEEK2_PLAN.md

**Planning & Status** (5 files):
- PHASE_11_ERROR_RECOVERY.md
- PHASE_11_INDEX.md
- PHASE_11_PLAN.md
- PHASE_11_SKILL_EXTENSIONS.md
- PHASE_11_WEEKLY_STATUS.md

**README**:
- README.md

### Historical Documentation (7 files)
Located in `docs/archive/root-docs/`

**Session & Planning**:
- DOCUMENTATION_STATUS.md
- SESSION_COMPLETION_SUMMARY.md
- STARTUP_OPTIMIZATION.md (Phase 10)
- TESTING_STRATEGY.md (Phase 10)
- WORKFLOW_INTEGRATION.md

**Reference**:
- REFERENCE_REPO.md
- SKILLS_AGENTS_INVENTORY.md

## Impact

**Current State**:
- Main repo: 17 archived files
- Archive size: ~140 KB
- Total docs: 8 active + 17 archived = 25 files

**After Offload**:
- Main repo: 3 active files (AUDIT.md, CLAUDE.md, README.md)
- Reference repo: Contains complete Phase 11-12 history
- Main repo size: ~200 KB smaller
- Cleaner navigation: Only current docs visible

## Steps

Run the provided script:
```bash
bash scripts/offload-to-reference.sh
```

Then follow the instructions to:
1. Copy archives to reference repo
2. Commit to reference repo
3. Remove from main repo

## Result

**Main Repo** (Clean & Focused):
- AUDIT.md — Living audit trail
- CLAUDE.md — Navigation hub
- README.md — Project overview
- scripts/offload-to-reference.sh — This utility

**Reference Repo** (Complete History):
- Phase 11 complete documentation
- Planning and architectural decisions
- Historical status and completion records

## Access

After offload, historical docs remain accessible via:
```
https://github.com/nxgntch/it-reference/tree/main/docs/archive
```

Link from CLAUDE.md:
```
**📚 Reference Repository** → [`nxgntch/it-reference`](https://github.com/nxgntch/it-reference)
Historical documentation, archived phases, planning materials
```

---

**Status**: Ready for offload. Run `bash scripts/offload-to-reference.sh` to proceed.
