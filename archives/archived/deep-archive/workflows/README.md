# IDE Automation Workflows

**Status**: ✅ Active | **Version**: 1.0 | **Last Updated**: 2026-09-10  
**Maintainer**: nxgntch team

Multi-step automation workflows for complex IDE tasks: phase consolidation, state management, and cross-system execution.

## What It Does

Orchestrates multi-step processes:
- **Phase Consolidation**: Consolidate documentation and state across phases
- **State Management**: Track progress across long-running operations
- **Error Handling**: Stop on errors and report failures
- **Integration**: Coordinate across IDE, shell scripts, and Python tools

## Available Workflows

| Workflow | Purpose | Status |
|----------|---------|--------|
| `consolidation_execution.js` | Phase consolidation (legacy) | Phase 30 |
| `consolidation_phase_30_plus_execution.js` | Phase 30+ consolidation engine | Phase 41 |

## Quick Start

Workflows are JavaScript/Node.js orchestration files. They execute via the IDE's workflow runner:

```bash
# List available workflows
ls -la docs/work/workflows/

# Run a workflow manually (if Node.js available)
node docs/work/workflows/consolidation_phase_30_plus_execution.js
```

## Common Patterns

### Pattern 1: Inspect a Workflow
```bash
# View workflow structure
head -50 docs/work/workflows/consolidation_phase_30_plus_execution.js
```

### Pattern 2: Run a Workflow
Workflows typically auto-run via the IDE. Manual execution requires Node.js:
```bash
# Node.js based (if Node installed)
node docs/work/workflows/consolidation_phase_30_plus_execution.js
```

### Pattern 3: Check Workflow Status
Workflows log output to IDE console or session logs. Check:
- IDE console output during workflow execution
- `.claude/logs/` (if logging is enabled)

## Configuration

**Auto-Run**: Workflows may auto-run on specific triggers (configurable via IDE settings).

**Manual Invocation**: Requires IDE workflow runner support or Node.js available.

**Customization**: Edit workflow files to change behavior (advanced):
```bash
nano docs/work/workflows/consolidation_phase_30_plus_execution.js
```

## Architecture

Workflows follow a simple pattern:
```javascript
const workflow = async () => {
  // Phase 1: Setup
  console.log("🚀 Starting workflow...");
  
  // Phase 2: Execute
  // Call APIs, run commands, coordinate tasks
  
  // Phase 3: Verify
  // Check results, report status
  
  return { success: true, message: "Done" };
};
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Workflow not running | Check IDE version supports workflows; may require manual trigger |
| Workflow hangs | Check IDE logs for errors; workflows may timeout on large operations |
| "Node not found" | Node.js may not be available; install via `npm` or system package manager |
| Syntax errors | Workflows are JavaScript; check for parse errors in `.js` file |

## See Also

- **IDE Guide**: [`docs/guides/ide/workflows.md`](../../guides/ide/workflows.md) — Workflow documentation
- **Work Hub**: [`docs/work/`](../) — Project work and deliverables
- **IDE Config**: [`docs/guides/ide/`](../../guides/ide/) — Main IDE configuration
