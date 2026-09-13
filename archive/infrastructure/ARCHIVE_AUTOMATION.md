# Archive Automation Workflow

**Automated system for managing document archives** — archives are automatically offloaded to the reference repository with links updated.

## Overview

When documents are archived in the main repository, they are automatically:
1. ✅ Offloaded to `nxgntch/it-reference`
2. ✅ Links updated to point to reference repo
3. ✅ Local archives cleaned up
4. ✅ Changes committed and pushed

This keeps the main repository focused on current documentation while preserving complete history.

## How It Works

### Automatic Trigger (Git Hook)

The system automatically detects when archive files are committed and runs the offload workflow:

```bash
git add docs/archive/some-doc.md
git commit -m "chore: archive old documentation"
# Post-commit hook automatically offloads and updates links
```

### Manual Trigger

You can also run the workflow manually:

```bash
bash scripts/archive-workflow.sh          # Dry-run mode
bash scripts/archive-workflow.sh --auto   # Execute + auto-commit
```

## Components

### 1. Archive Workflow Script

**File**: `scripts/archive-workflow.sh`

**Functions**:
- Detect pending archives not yet in reference repo
- Copy archives to reference repository
- Commit and push to reference repo
- Update links in main repo documentation
- Clean up local archive copies

### 2. Git Hook

**File**: `.git/hooks/post-commit`

**Trigger**: Runs automatically after every commit that touches `docs/archive/`

**Behavior**:
- Detects archive changes in the commit
- Automatically runs archive-workflow.sh
- Offloads, updates links, and cleans up
- Pushes changes to both repositories

### 3. Configuration

**File**: `.claude/config/archive-automation.yaml`

**Settings**:
- auto_offload_enabled: Enable automatic offload
- auto_update_links: Update links in main repo
- auto_cleanup: Remove local archives after offload
- Reference repo configuration
- Link update rules
- Trigger patterns

## Workflow Example

### Archive Phase 11 Documentation

```bash
# Step 1: Move docs to archive
mkdir -p docs/archive/phase-11-old
mv docs/old-phase-11-docs.md docs/archive/phase-11-old/
git add docs/archive/
git commit -m "chore: archive old Phase 11 documentation"
```

**Automatic workflow triggers:**
- ✅ Copies archive to reference repo
- ✅ Updates links in main repo docs
- ✅ Removes local archive copy
- ✅ Commits to both repositories
- ✅ Pushes both commits

**Result:**
- Main repo: Clean, only current docs
- Reference repo: Complete history preserved
- Links: Updated to reference repo
- Size: Main repo smaller

## Configuration

### Enable/Disable Automation

Edit `.claude/config/archive-automation.yaml`:

```yaml
archive_workflow:
  auto_offload_enabled: true
  auto_update_links: true
  auto_cleanup: true
```

### Customize Link Updates

Add new link patterns in configuration:

```yaml
link_updates:
  - from: "docs/archive/my-docs/"
    to: "https://github.com/nxgntch/it-reference/tree/master/docs/archive/my-docs/"
    files: ["README.md", "CLAUDE.md"]
```

## Manual Operations

### Run Without Hook

If the git hook doesn't trigger:

```bash
bash scripts/archive-workflow.sh --auto
```

### Check Archive Status

```bash
# Files in main repo
ls -la docs/archive/

# Files in reference repo
ls -la ../it-reference/docs/archive/
```

## Logging

Archive workflow activity is logged to:

**File**: `.claude/observer/logs/archive-workflow.log`

**View logs**:
```bash
tail -f .claude/observer/logs/archive-workflow.log
```

## Troubleshooting

### Hook Not Triggering

Check if hook is installed:
```bash
ls -la .git/hooks/post-commit

# If missing, reinstall
cp .claude/hooks/post-commit-archive-workflow.sh .git/hooks/post-commit
chmod +x .git/hooks/post-commit
```

### Reference Repo Not Found

Clone reference repo:
```bash
git clone https://github.com/nxgntch/it-reference.git ../it-reference

# Retry workflow
bash scripts/archive-workflow.sh --auto
```

## Best Practices

### 1. Archive Before Deleting

Always move to `docs/archive/` before deleting:

```bash
mv docs/old-file.md docs/archive/old-file.md
git add docs/archive/
git commit -m "chore: archive old file"
```

### 2. Use Descriptive Archive Names

```
docs/archive/phase-11-complete-docs/
docs/archive/session-2026-08-22-planning/
```

### 3. Batch Archive Commits

Group related archives together:

```bash
git add docs/archive/phase-10/ docs/archive/phase-11-old/
git commit -m "chore: archive Phase 10-11 planning docs"
```

## Related Documentation

- **OFFLOAD_PLAN.md** — Original offload plan
- **.claude/config/archive-automation.yaml** — Configuration
- **.claude/observer/logs/** — Workflow logs

---

**Status**: Automation system active. Archive workflow runs automatically on commit.

To disable: Set `auto_offload_enabled: false` in configuration.
