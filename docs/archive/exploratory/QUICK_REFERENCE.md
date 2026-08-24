# Quick Reference Card

**One-page developer cheatsheet for local development.**

---

## One-Time Setup

```bash
# Clone repo
git clone https://github.com/nxgntch/it.git
cd it

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies (choose one)
pip install -r requirements-minimal.txt    # ⚡ Fastest
pip install -e ".[dev]"                     # ⭐ Recommended
pip install -r requirements-dev.txt         # 📚 Full

# Setup environment
cp setup/.env.example .env.local
nano .env.local  # Add ANTHROPIC_API_KEY

# Verify setup
pytest tests/ --collect-only | head -20
```

---

## Daily Commands

### Running Tests
```bash
pytest tests/                          # All tests
pytest tests/test_file.py              # Specific file
pytest -k "test_name"                  # Specific test
pytest -m "not slow"                   # Skip slow tests
pytest --lf                            # Last failed
pytest --cov=app                       # With coverage
```

### Code Quality
```bash
black app/ tests/                      # Format
ruff check app/ tests/                 # Lint
mypy app/                              # Type check
```

### Startup & Debugging
```bash
python scripts/startup-profiler.py     # Profile startup
PROFILING_ENABLED=true pytest -s       # Debug with profiling
LOG_LEVEL=DEBUG pytest -s              # Debug with logs
```

### Git Workflow
```bash
git status                             # Check changes
git add -A && git commit -m "..."      # Commit
git push origin branch-name            # Push
gh pr create --title "..." --body "..."# Create PR
```

---

## Common Patterns

### Testing a Single Feature
```bash
# 1. Install minimal deps
pip install -r requirements-minimal.txt

# 2. Run related tests
pytest tests/test_feature.py -v -s

# 3. If all pass, run full suite
pytest tests/ --cov=app
```

### Before Committing
```bash
# 1. Format code
black app/ tests/

# 2. Lint and type check
ruff check app/ tests/
mypy app/

# 3. Run all tests
pytest tests/ --cov=app --cov-report=term-missing

# 4. Commit
git add -A
git commit -m "feat(module): description"

# 5. Push
git push origin feature-branch
```

### Debugging Startup Issues
```bash
# 1. Profile startup
python scripts/startup-profiler.py

# 2. Check environment
python -c "import os; print(os.getenv('ANTHROPIC_API_KEY'))"

# 3. Debug initialization
PROFILING_ENABLED=true LOG_LEVEL=DEBUG python -c "from app import startup; startup.initialize()"

# 4. Check config
python scripts/validate-config.py
```

---

## Environment Variables

### Required
```bash
ANTHROPIC_API_KEY=sk-ant-...           # LLM API key
```

### Optional
```bash
DEBUG=true                             # Enable debug mode
LOG_LEVEL=DEBUG                        # Logging level
DATABASE_URL=sqlite:///./local.db      # Local database
LAZY_LOAD_CONFIG=true                  # Lazy load config
PROFILING_ENABLED=true                 # Profile startup
```

---

## File Locations

```
setup/
  ├─ .env.example              ← Copy to .env.local
  ├─ LOCAL_STARTUP.md          ← Startup guide
  └─ DEVELOPMENT_SETUP.md      ← Full setup guide

config/
  ├─ startup-critical.yaml     ← Minimal startup config
  ├─ agents.yaml               ← Agent definitions
  ├─ skills.yaml               ← Skill registry
  └─ ...other configs

app/
  ├─ core/                     ← Core modules
  ├─ agents/                   ← Agent implementations
  ├─ db/                       ← Database
  └─ lib/                      ← Utilities

tests/
  └─ test_*.py                 ← Test files (match app structure)

scripts/
  ├─ startup-profiler.py       ← Profile startup time
  └─ validate-config.py        ← Validate configs
```

---

## Keyboard Shortcuts (IDE)

### VS Code
```
Ctrl+Shift+P          Command palette
Ctrl+K Ctrl+T         Run all tests
Ctrl+K Ctrl+U         Format document
Ctrl+`                Open terminal
Ctrl+J                Toggle panel
```

### PyCharm
```
Ctrl+Shift+A          Find action
Ctrl+Shift+F10        Run current test
Ctrl+Alt+L            Reformat code
Alt+F12               Open terminal
```

---

## Dependencies Quick Check

```bash
# See installed versions
pip list | grep -E "pytest|ponytail|pyyaml"

# Update everything (dev only)
pip install --upgrade -r requirements-dev.txt

# See dependency tree
pip install pipdeptree && pipdeptree

# Check for security issues
pip install safety && safety check
```

---

## Troubleshooting Quick Fixes

| Problem | Command |
|---------|---------|
| Slow startup | `python scripts/startup-profiler.py` |
| Import error | `pip install --no-cache-dir -r requirements-minimal.txt` |
| Test failures | `pytest tests/ -vv -s` |
| Missing env var | `nano .env.local` then verify with `python -c "import os; print(os.getenv('VAR'))"` |
| Config error | `python scripts/validate-config.py` |
| Git confusion | `git status` then `git log --oneline -5` |

---

## Learning Resources

| Topic | Location |
|-------|----------|
| **Project overview** | `CLAUDE.md` |
| **Root structure** | `ROOT_STRUCTURE.md` |
| **Startup optimization** | `setup/LOCAL_STARTUP.md` |
| **Full setup guide** | `setup/DEVELOPMENT_SETUP.md` |
| **API reference** | `docs/specifications/API_SPECIFICATION.md` |
| **Architecture** | `docs/guides/architecture/` |
| **Development rules** | `.claude/rules/README.md` |

---

## Emergency Commands

```bash
# Reinstall everything from scratch
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Hard reset (WARNING: loses uncommitted changes)
git reset --hard HEAD

# Clear all caches
find . -type d -name __pycache__ -exec rm -r {} +
find . -type d -name .pytest_cache -exec rm -r {} +
rm -rf .mypy_cache .ruff_cache

# Validate everything works
pytest tests/ -x --tb=short
```

---

**Pro Tips:**
- 💡 Use `requirements-minimal.txt` for fastest startup during development
- 💡 Run `startup-profiler.py` if startup feels slow
- 💡 Use `pytest -m "not slow"` to skip slow tests during iteration
- 💡 Run `black` + `ruff` before every commit
- 💡 Check `PROFILING_ENABLED=true` logs when debugging

---

**Last Updated**: 2026-08-23 · **Quick reference for local development**
