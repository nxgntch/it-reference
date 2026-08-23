# Reference Repo Workflow Integration

Practical implementation guide for using nxgntch/it-reference in your daily development workflow.

---

## **Quick Start (5 minutes)**

### **1. Add Shell Aliases**

Add to your `~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`:

```bash
# Quick access to reference materials
alias ref-docs='cd nxgntch-it-reference'
alias ref-sync='bash nxgntch-it/scripts/sync-reference-docs.sh'
alias ref-skills='cd nxgntch-it-reference/skills/planning'
alias ref-phases='cd nxgntch-it-reference/docs/archive'

# View reference materials quickly
alias ref-view='code nxgntch-it-reference'
```

After adding:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### **2. Clone Both Repos**

```bash
# If not already done
git clone https://github.com/nxgntch/it.git
git clone https://github.com/nxgntch/it-reference.git

# Organize locally
mkdir -p ~/nxgntch-workspace
cd ~/nxgntch-workspace
git clone https://github.com/nxgntch/it.git nxgntch-it
git clone https://github.com/nxgntch/it-reference.git nxgntch-it-reference
```

### **3. Set Up Auto-Sync (Optional)**

```bash
# Create cron job to keep reference cache updated (monthly)
crontab -e

# Add this line:
0 0 1 * * cd ~/nxgntch-workspace/nxgntch-it && bash scripts/sync-reference-docs.sh
```

---

## **Daily Workflow Patterns**

### **Pattern 1: Regular Development (No Reference Needed)**

```bash
cd ~/nxgntch-workspace/nxgntch-it

# Work on current features - reference not loaded
git checkout -b feat/new-feature
npm run dev              # Fast startup
pytest tests/            # Uses startup-critical.yaml

# Make changes, commit, push
git add -A
git commit -m "feat: new feature"
git push
```

**Reference repo**: Not touched (stays fast ✅)

---

### **Pattern 2: Need Historical Context**

```bash
cd ~/nxgntch-workspace/nxgntch-it

# "How did Phase 5 handle cost tracking?"
# Quick option: browse reference on GitHub
open https://github.com/nxgntch/it-reference/blob/master/docs/archive/PHASE_5_COST_TRACKING_README.md

# Local option: sync and browse
bash scripts/sync-reference-docs.sh
code .reference-cache/docs/archive/

# Find answer, then back to work
```

**Reference repo**: Used for read-only context

---

### **Pattern 3: Designing New Skill**

```bash
cd ~/nxgntch-workspace/nxgntch-it

# Step 1: Review similar skills
ref-skills    # Jump to skills/planning in reference
# Review: SKILL.md, examples.md, templates/

# Step 2: Create new skill in ACTIVE repo
mkdir it/skills/myNewSkill
cp .reference-cache/skills/planning/templates/SKILL.md it/skills/myNewSkill/SKILL.md

# Step 3: Develop in nxgntch-it (main repo)
git checkout -b feat/my-new-skill
# Edit it/skills/myNewSkill/SKILL.md
# Add tests, config, documentation

# Step 4: Complete and push
git commit -m "feat: add myNewSkill"
git push -u origin feat/my-new-skill

# Step 5: Archive planning materials (after merge)
# Move design docs to it-reference (covered below)
```

**Reference repo**: Used for inspiration, not modified

---

### **Pattern 4: Phase Completion & Archival**

```bash
# After Phase 10 work is complete and merged to main

# Step 1: Collect Phase 10 artifacts
mkdir -p ~/phase-10-archive
cp -r nxgntch-it/[planning-docs] ~/phase-10-archive/

# Step 2: Add to reference repo
cd ~/nxgntch-workspace/nxgntch-it-reference
mkdir -p docs/archive/phase-10
mv ~/phase-10-archive/* docs/archive/phase-10/

# Step 3: Commit and push
git add -A
git commit -m "docs: archive Phase 10 planning materials

- Add Phase 10 completion report
- Archive skill planning materials
- Document architectural decisions"
git push

# Step 4: Clean up main repo
cd ../nxgntch-it
rm -rf [planning-docs]
git commit -m "cleanup: remove archived Phase 10 materials"
git push
```

**Both repos**: Main repo stays light, reference repo grows

---

## **IDE Integration**

### **VS Code Setup**

**`.vscode/settings.json`** (in nxgntch-it):

```json
{
  "search.exclude": {
    "**/node_modules": true,
    "**/.reference-cache": true,
    ".reference-cache/**": true
  },
  "files.exclude": {
    ".reference-cache": true
  },
  "workspace.folders": [
    {
      "path": "."
    },
    {
      "path": "../nxgntch-it-reference",
      "name": "Reference (Archive)"
    }
  ]
}
```

**Workspace file** (`nxgntch-workspace.code-workspace`):

```json
{
  "folders": [
    {
      "path": "nxgntch-it",
      "name": "nxgntch/it (Active)"
    },
    {
      "path": "nxgntch-it-reference",
      "name": "nxgntch/it-reference (Archive)"
    }
  ],
  "settings": {
    "search.exclude": {
      ".reference-cache": true
    }
  }
}
```

**Usage**:
```bash
# Open both repos in one workspace
code ~/nxgntch-workspace/nxgntch-workspace.code-workspace
```

### **JetBrains IDE Setup**

1. **File → Open → nxgntch-it**
2. **File → Project Structure → Modules → Add module**
3. **Select nxgntch-it-reference**
4. **Mark nxgntch-it-reference as "Read-only"**
   - Right-click folder → Mark Directory As → Excluded

---

## **Git Workflow Integration**

### **Pre-Commit Hook**

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Prevent accidentally committing reference cache to main repo

if git diff --cached --name-only | grep -q "^\.reference-cache/"; then
    echo "Error: .reference-cache should not be committed to main repo"
    echo "Run: git reset .reference-cache/"
    exit 1
fi

exit 0
```

```bash
chmod +x .git/hooks/pre-commit
```

### **Branch Strategy**

```bash
# Main repo branches (active work)
feat/new-skill              # New features go here
fix/bug-name                # Bug fixes
docs/architecture-update    # Documentation

# Reference repo (archive only)
archive/phase-10            # Phase completions
docs/update                 # Reference updates
```

---

## **Automation Scripts**

### **Script 1: Daily Sync** (`scripts/daily-sync.sh`)

```bash
#!/bin/bash
# Keep reference materials up-to-date

echo "🔄 Syncing reference documentation..."

# Sync reference materials locally
bash scripts/sync-reference-docs.sh

# Verify reference repo is up-to-date with remote
cd ../nxgntch-it-reference
git fetch origin main
if ! git diff --quiet HEAD origin/main; then
    echo "⚠️  Reference repo has updates. Pulling..."
    git pull origin main
fi

cd ../nxgntch-it
echo "✅ Reference sync complete"
```

**Usage**:
```bash
bash scripts/daily-sync.sh
```

### **Script 2: Archive Phase Materials** (`scripts/archive-phase.sh`)

```bash
#!/bin/bash
# Archive completed phase materials to reference repo

PHASE=$1

if [ -z "$PHASE" ]; then
    echo "Usage: bash scripts/archive-phase.sh phase-10"
    exit 1
fi

echo "📦 Archiving $PHASE materials..."

# Create archive directory
mkdir -p ../nxgntch-it-reference/docs/archive/$PHASE

# Copy phase documentation
if [ -d "docs/archive/$PHASE" ]; then
    cp -r docs/archive/$PHASE/* ../nxgntch-it-reference/docs/archive/$PHASE/
fi

# Copy phase planning materials
if [ -d "it/skills/planning/$PHASE" ]; then
    cp -r it/skills/planning/$PHASE/* ../nxgntch-it-reference/skills/planning/
fi

# Commit to reference repo
cd ../nxgntch-it-reference
git add -A
git commit -m "docs: archive $PHASE materials"
git push

# Remove from main repo
cd ../nxgntch-it
git rm -r docs/archive/$PHASE it/skills/planning/$PHASE 2>/dev/null || true
git commit -m "cleanup: remove archived $PHASE materials"
git push

echo "✅ $PHASE archived successfully"
```

**Usage**:
```bash
bash scripts/archive-phase.sh phase-10
```

### **Script 3: Quick Reference Search** (`scripts/ref-search.sh`)

```bash
#!/bin/bash
# Search reference materials

QUERY=$1

if [ -z "$QUERY" ]; then
    echo "Usage: bash scripts/ref-search.sh 'search term'"
    exit 1
fi

echo "🔍 Searching reference materials for: $QUERY"

# Search in phases
echo "📄 In phase documentation:"
grep -r "$QUERY" ../nxgntch-it-reference/docs/archive/ 2>/dev/null | head -5

# Search in planning
echo "📋 In skill planning:"
grep -r "$QUERY" ../nxgntch-it-reference/skills/planning/ 2>/dev/null | head -5
```

**Usage**:
```bash
bash scripts/ref-search.sh "cost tracking"
```

---

## **CI/CD Integration**

### **GitHub Actions** (`.github/workflows/reference-sync.yml`)

```yaml
name: Sync Reference Docs

on:
  schedule:
    # Weekly sync of reference materials
    - cron: '0 0 * * 0'
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Sync reference materials
        run: bash scripts/sync-reference-docs.sh
      
      - name: Cache reference materials
        uses: actions/cache@v3
        with:
          path: .reference-cache
          key: ref-docs-${{ github.run_id }}
```

### **Local Pre-Push Hook** (`.git/hooks/pre-push`)

```bash
#!/bin/bash
# Warn if pushing with local reference-cache

if git diff --cached --name-only | grep -q "\.reference-cache"; then
    echo "⚠️  Warning: .reference-cache is staged for commit"
    echo "This should not be committed. Unstaging..."
    git reset .reference-cache/
fi
```

---

## **Team Documentation**

### **ONBOARDING.md** (for new developers)

```markdown
# Onboarding: Reference Repo Workflow

## First Time Setup

1. Clone both repos:
   ```bash
   git clone https://github.com/nxgntch/it.git nxgntch-it
   git clone https://github.com/nxgntch/it-reference.git nxgntch-it-reference
   ```

2. Add shell aliases (see WORKFLOW_INTEGRATION.md)

3. Open workspace in VS Code:
   ```bash
   code nxgntch-workspace.code-workspace
   ```

## Daily Work

- **Most of the time**: Work in `nxgntch-it/` (main repo)
- **When stuck**: Check reference repo for historical context
- **Reference repo stays read-only** - never edit it directly

## Common Tasks

See [WORKFLOW_INTEGRATION.md](WORKFLOW_INTEGRATION.md) for:
- Creating new skills
- Archiving completed phases
- Searching historical context
- CI/CD integration
```

---

## **Monitoring & Maintenance**

### **Weekly Checklist**

```bash
# Check both repos are in sync
git -C nxgntch-it status
git -C nxgntch-it-reference status

# Verify no accidental commits to reference
git -C nxgntch-it-reference log --oneline -5

# Check reference cache size (if using)
du -sh nxgntch-it/.reference-cache

# Update reference if behind remote
git -C nxgntch-it-reference pull origin main
```

### **Monthly Maintenance**

```bash
# Clean up old reference cache
bash nxgntch-it/scripts/sync-reference-docs.sh --force

# Archive any completed work
# (see archive-phase.sh script above)

# Update team documentation
# (SKILLS_AGENTS_INVENTORY.md, etc)
```

---

## **Quick Command Reference**

| Task | Command |
|------|---------|
| **Sync reference locally** | `bash nxgntch-it/scripts/sync-reference-docs.sh` |
| **Search reference** | `bash nxgntch-it/scripts/ref-search.sh 'term'` |
| **Archive phase** | `bash nxgntch-it/scripts/archive-phase.sh phase-X` |
| **View reference** | `code nxgntch-it-reference` |
| **Check both repos** | `git status -uno && git -C ../nxgntch-it-reference status` |
| **Pull reference updates** | `git -C nxgntch-it-reference pull` |

---

## **Workflow Checklist**

### **Before Starting New Feature**
- [ ] Work in `nxgntch-it/` (main repo)
- [ ] Use `startup-critical.yaml` config
- [ ] Keep reference cache disabled (not needed)

### **When Designing New Skill**
- [ ] Check reference for similar skills: `ref-skills`
- [ ] Review templates: `.reference-cache/skills/planning/templates/`
- [ ] Create in main repo: `it/skills/newSkill/`
- [ ] Reference stays read-only

### **When Archiving Phase**
- [ ] Collect phase artifacts
- [ ] Run: `bash scripts/archive-phase.sh phase-X`
- [ ] Verify in reference repo on GitHub
- [ ] Verify removed from main repo

### **After Phase Complete**
- [ ] Run `daily-sync.sh` to update cache
- [ ] Update `SKILLS_AGENTS_INVENTORY.md`
- [ ] Verify all planning materials archived
- [ ] Main repo size reduced (✅ = lightweight)

---

## **Troubleshooting**

### **Reference cache taking too much space**

```bash
# Remove and recreate
rm -rf nxgntch-it/.reference-cache
bash nxgntch-it/scripts/sync-reference-docs.sh
```

### **Accidentally edited reference repo**

```bash
cd nxgntch-it-reference
git checkout main  # Discard changes
```

### **Reference out of sync with remote**

```bash
cd nxgntch-it-reference
git fetch origin
git pull origin main
```

### **Can't find historical skill design**

```bash
bash nxgntch-it/scripts/ref-search.sh "skill-name"
```

---

## **Best Practices**

✅ **DO**
- Keep reference repo in separate directory
- Use shell aliases for quick access
- Archive phase materials after completion
- Search reference before designing new features
- Run weekly sync check

❌ **DON'T**
- Edit files in reference repo from main workspace
- Commit `.reference-cache/` to main repo
- Delete historical materials (keep for reference)
- Include reference in startup path (it's optional)
- Manually sync instead of using scripts

---

## **Performance Impact**

| Action | Overhead |
|--------|----------|
| **Daily development** | 0ms (reference not loaded) |
| **Sync reference locally** | ~2 seconds (one-time) |
| **Search reference** | ~500ms (optional) |
| **Load full config** | +20ms (optional, CI only) |

**Bottom line**: Reference repo is completely optional for day-to-day work. Only used when you explicitly need it.

---

**Last updated**: 2026-08-22
