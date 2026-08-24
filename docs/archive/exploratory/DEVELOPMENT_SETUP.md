# Development Setup Guide

**Quick setup for local development with optimized dependencies.**

---

## Installation Methods

### Method 1: Minimal Setup (Fastest) ⚡
Best for: Quick testing, fast startup
```bash
pip install -r requirements-minimal.txt
```

**Includes**: ponytail, pytest, yaml, dotenv  
**Time**: ~15 seconds  
**Best for**: Running tests, quick iterations

### Method 2: Standard Setup (Recommended) ⭐
Best for: Normal development
```bash
pip install -e ".[dev]"
```

**Includes**: All dev tools (black, ruff, mypy, pytest)  
**Time**: ~30 seconds  
**Best for**: Most development work

### Method 3: Full Setup (Everything)
Best for: Code quality checks, profiling
```bash
pip install -r requirements-dev.txt
```

**Includes**: All tools + testing + quality tools  
**Time**: ~45 seconds  
**Best for**: Pre-commit checks, CI/CD prep

---

## Quick Setup (5 minutes)

### Step 1: Create Virtual Environment
```bash
python -m venv venv

# Activate
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
# Use minimal setup for fastest startup
pip install -r requirements-minimal.txt
```

### Step 3: Setup Environment File
```bash
# Copy template
cp setup/.env.example .env.local

# Edit with your settings (at minimum set API key)
nano .env.local  # or use your editor
```

### Step 4: Verify Setup
```bash
# Run tests to verify installation
pytest tests/ -v --co -q | head -20
```

---

## Dependency Hierarchy

```
Base Requirements (pyproject.toml)
└─ ponytail>=1.0.0

Development Dependencies (optional-dependencies.dev)
├─ pytest>=7.0
├─ pytest-asyncio>=0.21.0
├─ pytest-cov>=4.0
├─ black>=23.0
├─ ruff>=0.1.0
└─ mypy>=1.0

System Dependencies (for specific features)
├─ pyyaml (YAML config parsing)
├─ jsonschema (config validation)
└─ python-dotenv (environment files)
```

### When to Install What

| Scenario | Command | Why |
|----------|---------|-----|
| **Running tests** | `pip install -r requirements-minimal.txt` | Fast, essential only |
| **Normal coding** | `pip install -e ".[dev]"` | All tools for development |
| **Code quality** | Add `-e ".[dev]"` then run black/ruff/mypy | Format + lint + type check |
| **CI/CD prep** | Same as normal, then run checks | Ensure everything passes |

---

## Configuration Files

### Required Files
| File | Purpose | Status |
|------|---------|--------|
| `.env.local` | Local environment variables | Create from `.env.example` |
| `config/startup-critical.yaml` | Minimal startup config | Provided ✓ |

### Optional Files
| File | Purpose | When to Create |
|------|---------|----------------|
| `.env.local.secrets` | Sensitive overrides | For secrets not in `.env.example` |
| `local-settings.yaml` | Local overrides | For machine-specific config |

---

## Development Workflows

### Workflow 1: Fast Testing
```bash
# Install minimal deps
pip install -r requirements-minimal.txt

# Run specific tests
pytest tests/test_orchestrator.py -v

# Run with coverage
pytest tests/ --cov=app
```

**Speed**: ✓✓✓ Fastest  
**Use for**: Quick iterations, debugging

### Workflow 2: Full Development
```bash
# Install dev tools
pip install -e ".[dev]"

# Format code
black app/ tests/

# Lint code
ruff check app/ tests/

# Type check
mypy app/

# Run tests
pytest tests/ -v
```

**Speed**: ✓✓ Medium  
**Use for**: Feature development, before commit

### Workflow 3: Pre-Commit Checks
```bash
# Same as full development, but:
# 1. Format with black
# 2. Lint with ruff
# 3. Type check with mypy
# 4. Run tests with pytest
# 5. Check coverage >= 85%

# All-in-one:
black app/ tests/ && \
ruff check app/ tests/ && \
mypy app/ && \
pytest tests/ --cov=app --cov-report=term-missing
```

**Speed**: ✓ Slowest (but thorough)  
**Use for**: Before pushing, before creating PR

---

## Performance Optimization

### Reduce Startup Time

1. **Use minimal requirements**
   ```bash
   pip install -r requirements-minimal.txt  # 50% faster than dev
   ```

2. **Profile startup**
   ```bash
   python scripts/startup-profiler.py
   ```

3. **Check initialization**
   ```bash
   PROFILING_ENABLED=true python -c "from app import startup; startup.initialize()"
   ```

### Reduce Test Time

1. **Run only changed tests**
   ```bash
   pytest -k "test_name"  # Run specific test
   pytest --lf              # Run last failed
   pytest --ff              # Run failed first
   ```

2. **Skip slow tests**
   ```bash
   pytest -m "not slow"     # Skip @pytest.mark.slow tests
   pytest -m "unit"         # Run only unit tests
   ```

3. **Use parallel testing**
   ```bash
   pip install pytest-xdist
   pytest -n auto           # Run tests in parallel
   ```

---

## Troubleshooting

### Slow Startup?
```bash
# Profile it
python scripts/startup-profiler.py

# Check for unnecessary imports
python -c "import cProfile; cProfile.run('from app import startup')"
```

### Import Errors?
```bash
# Reinstall with no cache
pip install --no-cache-dir -r requirements-minimal.txt

# Check what's installed
pip list | grep -E "ponytail|pytest|pyyaml"
```

### Test Failures?
```bash
# Check dependencies are correct version
pip show pytest pytest-asyncio

# Run with verbose output
pytest tests/ -vv -s

# Run with print statements visible
pytest tests/ -s
```

### Environment Issues?
```bash
# Verify .env.local is loaded
python -c "import os; print(os.getenv('ANTHROPIC_API_KEY', 'NOT SET'))"

# Check which config files are loaded
PROFILING_ENABLED=true LOG_LEVEL=DEBUG pytest -k "test_config" -s
```

---

## IDE Setup

### VS Code
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestPath": "${workspaceFolder}/venv/bin/pytest"
}
```

### PyCharm
1. **File → Settings → Project → Python Interpreter**
2. **Add Interpreter → Existing Environment**
3. Select `venv/bin/python` (or `venv\Scripts\python.exe` on Windows)
4. **OK**

---

## Useful Commands

```bash
# See what's installed
pip list

# Check specific package version
pip show pytest

# Update all packages (dev only!)
pip install --upgrade -r requirements-dev.txt

# See dependencies tree
pip install pipdeptree
pipdeptree

# Clean up (remove unused packages)
pip install pip-autoremove
pip-autoremove -p package_name
```

---

## Next Steps

1. **Setup**: Follow "Quick Setup" above
2. **Read**: `setup/LOCAL_STARTUP.md` for startup optimization
3. **Profile**: `python scripts/startup-profiler.py` to see timing
4. **Develop**: Use appropriate workflow based on your task
5. **Test**: Run `pytest tests/ -v` before committing

---

**Need Help?**
- **Setup issues**: See "Troubleshooting" section above
- **Performance**: Run `python scripts/startup-profiler.py`
- **Dependencies**: Check `pyproject.toml` and `requirements-*.txt`
- **Documentation**: See `ROOT_STRUCTURE.md` for project overview

---

**Last Updated**: 2026-08-23 · **Optimized for local development**
