# Phase File Organizer Skill

Automates organization of phase documentation by moving summary files to phase-range directories and archiving supporting/detail files. Routes all files through centralized `/docs/` structure using configuration from `config/documentation.yaml`.

## Description

Automates organization of phase documentation by moving summary files to phase-range directories and archiving supporting/detail files. Routes all files through centralized `/docs/` structure using configuration from `config/documentation.yaml`.

## Overview

Implements nxgntch's phase documentation pattern:
- **Summary files** (completion reports, executive summaries, transition guides) → Phase-range folders (phases-1-5, phases-6-10, etc.)
- **Supporting files** (weekly progress, session handoffs, performance baselines) → Centralized archives/ directory
- **Automatically updates READMEs** with file inventories and archive references
- **Configuration-driven**: All paths resolved from `config/documentation.yaml` for consistent routing to `/docs/`

## Configuration Routing

PhaseFileOrganizer automatically resolves all directory paths from `config/documentation.yaml`:

| Path Type | Configuration Source | Default |
|---|---|---|
| docs_root | `documentation.completed.rootPath` | `docs/work/completed/` |
| archives | `{docs_root}/archives/` | `docs/work/completed/archives/` |
| phase ranges | `{docs_root}/phases-*-*/` | `docs/work/completed/phases-*-*/` |

**Configuration**: All paths are defined in `config/documentation.yaml`. Updates to this file automatically affect phaseFileOrganizer's behavior without code changes.

## Usage

```python
from skills.phaseFileOrganizer import PhaseFileOrganizer

# Initialize with automatic config loading (uses config/documentation.yaml)
organizer = PhaseFileOrganizer()

# Organize all phases
result = organizer.organizeAllPhases()

# Or organize specific phase range
result = organizer.organizePhaseRange("phases-1-5")

# Get summary of changes
print(result.summary())

# Or specify custom docs_root (overrides config)
organizer = PhaseFileOrganizer(docs_root="/custom/path/to/docs/work/completed")
```

## API

### PhaseFileOrganizer

Main class for phase file organization.

**Constructor**:
- `docs_root` (str): Root path to docs/work/completed directory

**Methods**:

#### `organizeAllPhases() → OrganizationResult`
Organize all phase ranges and utilities.

Returns: Result object with summary of all moves and updates.

#### `organizePhaseRange(phase_range: str) → OrganizationResult`
Organize a specific phase range (e.g., "phases-1-5").

Returns: Result object with moves and README updates for that range.

#### `identifySummaryFiles(phase_range: str) → List[str]`
Identify which files in a phase range are summary files.

**Returns**: List of summary file paths.

#### `identifySupportingFiles(phase_range: str) → List[str]`
Identify which files in a phase range are supporting/detail files.

**Returns**: List of supporting file paths.

#### `moveToArchives(files: List[str]) → List[str]`
Move files to archives/ directory, organizing by phase.

**Returns**: List of moved file paths in archives.

#### `updatePhaseRangeREADME(phase_range: str, summary_files: List[str], archived_count: int) → str`
Update phase-range README with summary file inventory and archive reference.

**Returns**: Path to updated README.

#### `generateArchivesREADME(all_archives: Dict) → str`
Generate/update archives/README.md with complete index.

**Returns**: Path to generated README.

## File Classification

### Summary Files (Keep in Phase-Range Folders)
- `PHASE*_COMPLETE.md` - Phase completion status
- `PHASE*_COMPLETION_REPORT.md` - Completion report
- `PHASE*_EXECUTIVE_SUMMARY.md` - Executive summary
- `PHASE*_TRANSITION_GUIDE.md` - Transition planning
- `PHASE*_TRACK_*_COMPLETION*.md` - Track completion
- `PHASE*_PLAN.md` - Final phase plan
- `phase*_final_delivery.md` - Final delivery
- `*_enterprise_*.md` - Enterprise planning
- `RELEASE_*.md` - Release notes
- `SECURITY_AUDIT_*.md` - Security audits
- `OWASP_*.md` - Compliance matrices

### Supporting Files (Move to Archives/)
- `*_week*.md` - Weekly progress reports
- `*_day*.md` - Daily status reports
- `*_session*.md` - Session handoffs
- `*_progress.md` - Progress reports
- `*_analysis.md` - Detailed analysis
- `*_plan*.md` - Planning documents (if supporting detail)
- `*_baselines.json` - Performance baselines
- `*_results.json` - Execution results
- `*_strategy*.md` - Strategy details
- `*_implementation*.md` - Implementation logs
- Other phase-specific working documents

## Examples

### Example 1: Organize Phases 1-5

```python
from skills.phaseFileOrganizer import PhaseFileOrganizer

organizer = PhaseFileOrganizer(docs_root="/home/user/it/docs/work/completed")

# Identify files
summary_files = organizer.identifySummaryFiles("phases-1-5")
supporting_files = organizer.identifySupportingFiles("phases-1-5")

print(f"Summary files (keep): {len(summary_files)}")
print(f"Supporting files (archive): {len(supporting_files)}")

# Organize
result = organizer.organizePhaseRange("phases-1-5")
print(result.summary())
```

**Output**:
```
Phase Range: phases-1-5
Summary files kept: 6
  - PHASE3_EXECUTIVE_SUMMARY.md
  - PHASE3_TRANSITION_GUIDE.md
  - PHASE_4_COMPLETION_REPORT.md
  - PHASE_4_ENHANCEMENT_PLAN.md
  - PHASE_5_TRACK_A_COMPLETE.md
  - README.md

Supporting files archived: 25
  - phase2-test-improvements.md → archives/phase2/
  - phase3_adoption_plan.md → archives/phase3/
  - phase5_edge_cases_status.md → archives/phase5/
  [...]

README updated: docs/work/completed/phases-1-5/README.md
```

### Example 2: Organize All Phases

```python
organizer = PhaseFileOrganizer("/home/user/it/docs/work/completed")
result = organizer.organizeAllPhases()

print(f"Total phases organized: {result.phases_processed}")
print(f"Total files archived: {result.total_archived}")
print(f"READMEs updated: {result.readmes_updated}")
```

## Archive Organization

Files are organized in `archives/` by phase:

```
archives/
├── phase1/              # Files from phases-1-5 phase 1
├── phase2/              # Files from phases-1-5 phase 2
├── phase3/              # Files from phases-1-5 phase 3
├── phase5/              # Files from phases-1-5 phase 5
├── phase6/              # Files from phases-6-10
├── phase17/             # Files from phases-16-20
├── phase18/             # Files from phases-16-20
├── phase19/             # Files from phases-16-20
├── utilities/           # Archive utilities reference docs
└── README.md            # Archive index
```

## README Structure

Each phase-range README is updated to include:

1. **Summary**: Overview of phases in that range
2. **Summary Files**: Listed with purposes (e.g., "6 (completion reports, executive summaries)")
3. **Archived Files**: Count and types (e.g., "25 (session handoffs, progress reports)")
4. **Archive Location**: Reference to `../archives/`
5. **Metrics**: File counts, status, completion dates

## Configuration

### File Classification Configuration

Update `SUMMARY_PATTERNS` and `SUPPORTING_PATTERNS` to customize which files are classified as summary vs supporting:

```python
SUMMARY_PATTERNS = [
    "*COMPLETE*.md",
    "*COMPLETION_REPORT*.md",
    "*EXECUTIVE_SUMMARY*.md",
    "*TRANSITION_GUIDE*.md",
    "RELEASE_*.md",
    "SECURITY_*.md",
]

SUPPORTING_PATTERNS = [
    "*_week*.md",
    "*_session*.md",
    "*_progress.md",
    "*_baselines.json",
    "*_results.json",
]
```

### Phase Range Mapping

Define how phases map to ranges:

```python
PHASE_RANGES = {
    "phases-1-5": [1, 2, 3, 4, 5],
    "phases-6-10": [6, 7, 8, 9, 10],
    "phases-11-15": [11, 12, 13, 14, 15, 16],  # 16.5 also maps here
    "phases-16-20": [17, 18, 19, 20],
}
```

## Testing

```bash
pytest tests/test_phaseFileOrganizer.py -v

# Test specific phase range
pytest tests/test_phaseFileOrganizer.py::test_organize_phases_1_5 -v

# Test file classification
pytest tests/test_phaseFileOrganizer.py::test_identify_summary_files -v
```

## Integration with IDE Skills

This skill is available in Claude Code for:
- Automated phase file organization during cleanup operations
- Phase consolidation workflows
- Repository maintenance automation

Use in IDE:
```
/phaseFileOrganizer
```

## Notes

- **Dry-run mode**: Set `dry_run=True` to preview changes without actually moving files
- **Git integration**: Automatically stages moved files (can be disabled)
- **Idempotent**: Safe to run multiple times; skips already-organized files
- **Preserves history**: All files remain in git history, accessible via commits

## See Also

- `../../docs/rules/file-organization.md` - File organization standards
- `docs/work/completed/phases-1-5/README.md` - Example of organized phase range
- `docs/work/completed/archives/README.md` - Archive index

