# IDE Configuration Duplicates Archive

**Date Archived**: 2026-09-13  
**Reason**: Consolidated duplicate IDE-specific configuration files  
**Total Size**: ~5-7MB  
**Commit**: Archive phase consolidation  

---

## Overview

This archive contains IDE-specific configuration directories that were duplicated across multiple skills directories throughout the repository. These configs were created to support development in different IDE environments (VS Code, Cursor, Claude, etc.) but resulted in significant repository bloat and maintenance burden.

---

## Contents

### planning-with-files IDE Configs (13 directories)
```
.agents/
.codebuddy/
.codex/
.codex-plugin/
.continue/
.cursor/
.factory/
.gemini/
.github/
.kiro/
.mastracode/
.opencode/
.pi/
```

### ponytail IDE Configs (14 directories)
```
ponytail_.agents/
ponytail_.claude-plugin/
ponytail_.clinerules/
ponytail_.codex-plugin/
ponytail_.cursor/
ponytail_.devin-plugin/
ponytail_.github/
ponytail_.grok-plugin/
ponytail_.kiro/
ponytail_.openclaw/
ponytail_.opencode/
ponytail_.qoder/
ponytail_.qoder-plugin/
ponytail_.windsurf/
```

### superpowers IDE Configs (10 directories)
```
superpowers_.agents/
superpowers_.claude-plugin/
superpowers_.codex-plugin/
superpowers_.cursor-plugin/
superpowers_.devin-plugin/
superpowers_.github/
superpowers_.hermes-plugin/
superpowers_.kimi-plugin/
superpowers_.opencode/
superpowers_.pi/
```

**Total**: 37 IDE-specific configuration directories archived

---

## Why These Were Archived

### Problem
- **Duplication**: Each IDE had its own config directory with identical or near-identical template structures
- **Bloat**: Added 5-7MB to repository size
- **Maintenance Burden**: Changes to templates required updates across multiple directories
- **Confusion**: Multiple "canonical" locations for template files
- **Scalability**: Each new IDE added duplicate directories

### Solution
- **Single Source of Truth**: Templates now live only in `skills/*/templates/` directories
- **IDE-Agnostic**: IDE configs should be auto-generated from CI/CD or stored in user's local dotfiles
- **Repository Health**: Reduced bloat, easier to maintain
- **Clarity**: Clear separation between project resources and IDE-specific configs

---

## What This Means

### For Development
1. IDE-specific settings should go in **local dotfiles**, not the repository
   - VS Code: `~/.config/Code/User/settings.json` or `.vscode/` in project root
   - Cursor: `~/.cursor/` or `.cursor/` in project root
   - Claude: Use `~/.claude/` for user settings

2. Project-level templates are in canonical locations:
   - `skills/planning-with-files/templates/`
   - `skills/ponytail/templates/`
   - `skills/superpowers/templates/`

### For Template Usage
All template references should point to the canonical location:
- ✅ `skills/planning-with-files/templates/`
- ❌ `skills/planning-with-files/.cursor/skills/planning-with-files/templates/`

### For IDE Configuration
Consider using environment variables or configuration files:
```bash
# Use environment-specific config
export IDE_CONFIG_PATH="${HOME}/.cursor/settings.json"
export TEMPLATE_PATH="./skills/planning-with-files/templates"
```

---

## Recovery Instructions

If you need to restore IDE-specific configs:

```bash
# List archived configs for a skill
ls -la docs/work/archived/ide-config-duplicates/ | grep planning-with-files

# Restore a specific config
cp -r docs/work/archived/ide-config-duplicates/.cursor \
      skills/planning-with-files/.cursor
```

---

## Size Impact

### Before Archival
- `skills/planning-with-files/`: ~2.5MB (including IDE configs)
- `skills/ponytail/`: ~3.2MB (including IDE configs)
- `skills/superpowers/`: ~1.8MB (including IDE configs)
- **Total Bloat**: ~5-7MB across 3 skills directories

### After Archival
- `skills/planning-with-files/`: ~200KB (templates only)
- `skills/ponytail/`: ~400KB (templates + benchmarks)
- `skills/superpowers/`: ~150KB (templates only)
- **Size Freed**: ~5-7MB

### Repository Impact
- Total `.git` size reduction: ~5-7MB
- Repository clone time: Faster
- Maintenance burden: Significantly reduced

---

## Related Documentation

- **Consolidation Status**: `docs/work/current/CONSOLIDATION_STATUS.md`
- **Archive Index**: `docs/work/archived/README.md`
- **Archived Analysis Reports**: `docs/work/archived/analysis-reports/`
- **Project Root Consolidation**: `docs/work/completed/archived-root-files/`

---

## Maintenance Going Forward

### Prevention Measures
1. Add `.gitignore` rules in skills directories to exclude IDE configs
2. Document in CONTRIBUTING.md that IDE configs should be user-local only
3. Add pre-commit hook to prevent IDE config directories in skills/

### Quarterly Reviews
- Scan for re-accumulation of IDE configs
- Review template consolidation status
- Verify no stale IDE references in documentation

### Automation (Suggested)
```bash
# Add to .pre-commit-config.yaml
- repo: local
  hooks:
    - id: no-ide-configs-in-skills
      name: Prevent IDE configs in skills/
      entry: bash -c 'find skills -type d -name ".\(agents\|cursor\|codex\)" && exit 1'
      language: system
      pass_filenames: false
      stages: [commit, push]
```

---

## Archived By

- **Date**: 2026-09-13
- **Reason**: Repository cleanup and consolidation phase
- **Approved**: Consolidation strategy
- **Size Freed**: ~5-7MB

---

**Last Updated**: 2026-09-13  
**Status**: ✅ Complete - All IDE configs archived, canonical locations preserved
