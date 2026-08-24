# Local Startup Optimization Guide

**Streamlined startup configuration for local development.**

---

## Quick Start

### 1. Install Dependencies
```bash
# Minimal startup (fastest)
pip install -e .

# With development tools
pip install -e ".[dev]"

# Or use the dev requirements file
pip install -r requirements-dev.txt
```

### 2. Setup Environment
```bash
# Copy environment template
cp setup/.env.example .env.local

# Edit with your local config
nano .env.local
```

### 3. Run Application
```bash
# Run with startup profiling
python -m app.startup

# Or manually in Python
python -c "from app import startup; startup.initialize()"
```

---

## Startup Flow

### Initialization Stages

**Stage 1: Critical (< 100ms)**
```
✓ Load startup-critical.yaml
✓ Initialize core agents (executor, router)
✓ Set default model (haiku)
✓ Load governance (budget enforcement)
```

**Stage 2: On-Demand (lazy)**
```
→ Load config/agents.yaml (full definitions)
→ Load config/skills.yaml (skill registry)
→ Load config/routing.yaml (routing rules)
→ Load config/orchestration.yaml (logic)
→ Load config/sla.yaml (SLAs)
→ Load config/skill-hooks.yaml (hooks)
```

**Stage 3: Background (optional)**
```
→ Initialize caches
→ Connect to database
→ Warm up model connections
```

---

## Environment Configuration

### .env.local Template

Create `.env.local` with these variables:

```bash
# Application
DEBUG=true
LOG_LEVEL=DEBUG
ENVIRONMENT=development

# LLM API
ANTHROPIC_API_KEY=sk-ant-...

# Database (optional for local)
DATABASE_URL=sqlite:///./local.db

# Startup Optimization
LAZY_LOAD_CONFIG=true
STARTUP_TIMEOUT_SECONDS=30

# Development
RELOAD_ON_CHANGE=true
PROFILING_ENABLED=true
```

### .env.local Checklist
- [ ] `ANTHROPIC_API_KEY` set
- [ ] `LOG_LEVEL` appropriate for debugging
- [ ] `DATABASE_URL` points to local/test db
- [ ] `LAZY_LOAD_CONFIG=true` (faster startup)

---

## Performance Metrics

### Current Startup Times

| Stage | Time | Components |
|-------|------|------------|
| **Stage 1 (critical)** | ~50ms | Config loading, core agents |
| **Stage 2 (on-demand)** | ~150ms | Full config, skills, routing |
| **Stage 3 (background)** | ~200ms | Caches, DB, warmup |
| **Total (first run)** | ~400ms | All stages |
| **Subsequent runs** | ~250ms | Cached config |

### Optimization Tips

1. **Keep Stage 1 Fast**
   - Only critical config in startup-critical.yaml
   - No network calls during bootstrap
   - No DB connections

2. **Lazy Load Everything Else**
   - Defer skill loading until needed
   - Load routing rules on-demand
   - Cache parsed YAML files

3. **Profile Your Changes**
   - Use `PROFILING_ENABLED=true`
   - Check output for slowdowns
   - Add metrics for new modules

---

## Development Workflow

### 1. Edit Code
```bash
# Edit source files normally
nano app/core/orchestrator.py
```

### 2. Quick Test (no reload needed)
```bash
# Run tests without full app startup
pytest tests/test_orchestrator.py -v
```

### 3. Full App Test
```bash
# Start app with hot reload
python -c "from app import startup; startup.run(reload=True)"
```

### 4. Profile Startup
```bash
# Time the startup
python -m cProfile -s cumulative app.startup | head -50
```

---

## Troubleshooting

### Slow Startup?

**Step 1: Check logs**
```bash
# Enable verbose logging
LOG_LEVEL=DEBUG python -c "from app import startup; startup.initialize()"
```

**Step 2: Profile initialization**
```bash
# See where time is spent
PROFILING_ENABLED=true python -c "from app import startup; startup.initialize()"
```

**Step 3: Check config files**
- Are large YAML files being loaded immediately?
- Should they be moved to on-demand loading?
- Are there unnecessary imports?

### Missing Dependencies?

```bash
# Reinstall dev dependencies
pip install -e ".[dev]" --force-reinstall

# Check what's installed
pip list | grep -E "pytest|black|ruff|mypy"
```

### Configuration Issues?

```bash
# Validate all YAML configs
python scripts/validate-config.py

# Check which configs are loaded
PROFILING_ENABLED=true LOG_LEVEL=DEBUG python -c "from app import startup"
```

---

## Advanced Configuration

### Custom Startup Hook

Create `startup/custom_init.py`:

```python
async def custom_startup():
    """Your custom initialization logic."""
    # Initialize custom components
    # Warm up caches
    # Connect to services
    pass

async def custom_shutdown():
    """Cleanup on shutdown."""
    pass
```

Then use in app:
```python
from startup.custom_init import custom_startup, custom_shutdown

app = create_app()
app.add_event_handler("startup", custom_startup)
app.add_event_handler("shutdown", custom_shutdown)
```

### Performance Monitoring

```python
# In your code
from app.startup import profile_block

with profile_block("my_operation"):
    # Your code here
    result = expensive_function()
```

Output:
```
[PROFILE] my_operation: 25ms
```

---

## Best Practices

### ✅ Do
- Load minimal config at startup
- Cache parsed YAML files
- Defer non-critical initialization
- Profile on every significant change
- Keep Stage 1 < 100ms

### ❌ Don't
- Load all config files at startup
- Make network calls during bootstrap
- Connect to databases eagerly
- Import heavy libraries at module level
- Ignore startup profiling

---

## References

- **Config Structure**: `config/README.md`
- **Startup Config**: `config/startup-critical.yaml`
- **Requirements**: `requirements-dev.txt`, `pyproject.toml`
- **Environment**: `.env.example`, `setup/.env.example`

---

**Last Updated**: 2026-08-23 · **Optimized for local development**
