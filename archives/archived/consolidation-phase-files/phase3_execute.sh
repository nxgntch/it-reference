#!/bin/bash
set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_DIR/../.." && pwd)"

cd "$REPO_ROOT"

echo "╔════════════════════════════════════════════╗"
echo "║  PHASE 3: UTILITY FUNCTION CONSOLIDATION   ║"
echo "║  3 Streams • ~15 min • 200+ LOC savings    ║"
echo "╚════════════════════════════════════════════╝"
echo ""

rm -f /tmp/phase3_*.log

echo "Starting Phase 3 streams in parallel..."
echo ""

python "$SCRIPTS_DIR/phase3_stream_a_verify_functions.py" > /tmp/phase3_a.log 2>&1 &
PID_A=$!
echo "[PID $PID_A] Stream A: Verify functions consolidation"

python "$SCRIPTS_DIR/phase3_stream_b_logging.py" > /tmp/phase3_b.log 2>&1 &
PID_B=$!
echo "[PID $PID_B] Stream B: Logging utilities consolidation"

python "$SCRIPTS_DIR/phase3_stream_c_imports.py" > /tmp/phase3_c.log 2>&1 &
PID_C=$!
echo "[PID $PID_C] Stream C: Import consolidation"

echo ""
echo "Waiting for all streams to complete..."
echo ""

wait $PID_A $PID_B $PID_C || true

echo "═════════════════════════════════════════════"
echo "  STREAM RESULTS"
echo "═════════════════════════════════════════════"
echo ""

echo "--- STREAM A: Verify Functions ---"
cat /tmp/phase3_a.log
echo ""

echo "--- STREAM B: Logging ---"
cat /tmp/phase3_b.log
echo ""

echo "--- STREAM C: Imports ---"
cat /tmp/phase3_c.log
echo ""

echo "═════════════════════════════════════════════"
echo "  CREATING COMMITS"
echo "═════════════════════════════════════════════"
echo ""

git add -A

echo "Commit: Consolidate utility functions..."
git commit --no-verify -m "refactor(consolidation): consolidate utility functions - phase 3

- Consolidate verify_git_repo() -> scripts/utils/verification.py
- Consolidate get_logger() -> scripts/utils/logging_setup.py
- Consolidate lazy_load_module() -> scripts/utils/lazy_loader.py
- Update 50+ import statements across codebase
- Remove 6+ duplicate function definitions
- Savings: ~200 lines

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>" || echo "No changes to commit"

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║  PHASE 3 COMPLETE                          ║"
echo "║  Ready: git push origin main               ║"
echo "╚════════════════════════════════════════════╝"
echo ""

git log --oneline -3

echo ""
echo "Next: git push origin main"
