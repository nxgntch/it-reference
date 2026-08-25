# Task-Observer Automated Log Sync

This document describes the automated log synchronization setup between nxgntch/it (main repo) and nxgntch/it-logs (logs-only repo).

## Architecture

```
nxgntch/it                          nxgntch/it-logs
├── .claude/observer/logs/  ─┐      ├── observer/logs/
├── .claude/observer/metrics/├──→   ├── logs/
├── logs/                    │      ├── reports/
└── scripts/                 │      └── (logs data only)
    ├── offload-logs.sh      │
    ├── sync-from-logs.sh    │
    └── daily-sync.sh        │
                             │
beforeStop Hook ─────────────┘
    └── syncObserverLogs.sh
        (orchestrates offload + sync + commit/push)
```

## Automated Sync Flow

### When It Runs
- **Automatically**: On `beforeStop` hook (when you end a Claude Code session)
- **Manually**: `bash .claude/hooks/syncObserverLogs.sh`

### What It Does
1. **Offload**: Runs `scripts/offload-logs.sh` 
   - Collects logs from `.claude/observer/logs/` and `logs/`
   - Pushes to `../it-logs/observer/logs/` and related directories
   
2. **Sync Back**: Runs `scripts/sync-from-logs.sh`
   - Pulls aggregated metrics and reports from it-logs
   - Stores latest metrics in `.claude/observer/metrics/latest.jsonl`
   
3. **Commit & Push**: 
   - Commits all changes in it-logs repo
   - Pushes to remote (git@github.com:nxgntch/it-logs.git)

### Log Categories Synced
- `observer/logs/` — Task observations, audit trails
- `logs/sessions/` — Session logs
- `logs/events/` — Event logs
- `logs/metrics/` — Performance metrics
- `logs/errors/` — Error logs
- `logs/audit/` — Audit trail logs
- `reports/` — Daily/weekly/monthly analysis reports

## Setup Requirements

### Prerequisites
- Both repos must exist as siblings: `~/it` and `~/it-logs`
  ```bash
  cd ~
  git clone https://github.com/nxgntch/it.git
  git clone https://github.com/nxgntch/it-logs.git
  ```
- Both repos must have git remotes configured (for push)
- SSH keys configured for GitHub authentication (for automated push)

### Directories Created
When first synced, these directories are created:
```
.claude/observer/
├── logs/              (task observations, audit)
├── metrics/           (performance metrics snapshots)
└── reports/           (daily, weekly, monthly reports)
    ├── daily/
    ├── weekly/
    └── monthly/
```

## Manual Sync

To manually trigger log sync without ending session:

```bash
bash .claude/hooks/syncObserverLogs.sh
```

Expected output:
```
[Sync] Syncing observer logs to it-logs repo...
[Sync] Running offload script...
[Sync] Running sync-back script...
[Sync] ✓ Observer logs synced to it-logs (X files)
```

## Monitoring

### Check What's Synced
```bash
# View latest synced logs
ls -lah ../it-logs/observer/logs/
ls -lah ../it-logs/logs/

# View latest metrics pulled back
cat .claude/observer/metrics/latest.jsonl | jq '.'

# View sync history
git -C ../it-logs log --oneline | head -10
```

### Verify Sync Completed
```bash
# Last commit in it-logs should be recent
git -C ../it-logs log --oneline -1
# Should show: "logs: task-observer session logs (X files) - YYYY-MM-DD HH:MM:SS UTC"
```

## Troubleshooting

### "Logs repo not found at ../it-logs"
- Clone it-logs as sibling: `git clone https://github.com/nxgntch/it-logs.git ../it-logs`
- Verify it exists: `ls -la ../it-logs`

### Push fails silently
- Check git remote: `git -C ../it-logs remote -v`
- Verify SSH key works: `ssh -T git@github.com`
- Check branch: `git -C ../it-logs branch`

### Logs not appearing in it-logs
- Check offload script output: `bash scripts/offload-logs.sh` (manual run)
- Verify logs exist locally: `ls -la .claude/observer/logs/`
- Check git status in it-logs: `git -C ../it-logs status`

## Hook Configuration

The sync hook is wired into `.claude/settings.json`:

```json
{
  "hooks": {
    "beforeStop": [
      ".claude/hooks/beforeStop.sh",
      ".claude/hooks/syncObserverLogs.sh"
    ]
  }
}
```

This ensures logs are synced every time you end a session.

## Performance Impact

- **Sync duration**: Typically 2-5 seconds (depends on log volume)
- **Network calls**: One push to it-logs repo per session
- **Storage**: Logs archived to it-logs, cleaned from main repo

## Related Files

- **Hook script**: `.claude/hooks/syncObserverLogs.sh`
- **Config**: `.claude/config/archive-automation.yaml`
- **Offload script**: `scripts/offload-logs.sh`
- **Sync-back script**: `scripts/sync-from-logs.sh`
- **Settings**: `.claude/settings.json` (hooks section)

## Next Steps

1. Verify both repos are cloned and have git remotes
2. End a session or run: `bash .claude/hooks/syncObserverLogs.sh`
3. Check it-logs for new commits: `git -C ../it-logs log --oneline -5`
4. Monitor `.claude/observer/metrics/latest.jsonl` for synced metrics
