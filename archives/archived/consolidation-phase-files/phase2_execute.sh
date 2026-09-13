#!/bin/bash
set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPTS_DIR/../.." && pwd)"

cd "$REPO_ROOT"

echo "╔════════════════════════════════════════════╗"
echo "║  PHASE 2: EXCEPTION CONSOLIDATION          ║"
echo "║  4 Streams • ~20 min • 150+ LOC savings    ║"
echo "╚════════════════════════════════════════════╝"
echo ""

rm -f /tmp/phase2_*.log

echo "Starting Phase 2 streams in parallel..."
echo ""

python "$SCRIPTS_DIR/phase2_stream_a_validation_error.py" > /tmp/phase2_a.log 2>&1 &
PID_A=$!
echo "[PID $PID_A] Stream A: ValidationError consolidation"

python "$SCRIPTS_DIR/phase2_stream_b_exit_code.py" > /tmp/phase2_b.log 2>&1 &
PID_B=$!
echo "[PID $PID_B] Stream B: ExitCode consolidation"

python "$SCRIPTS_DIR/phase2_stream_c_validation_errors.py" > /tmp/phase2_c.log 2>&1 &
PID_C=$!
echo "[PID $PID_C] Stream C: ConfigValidationError/SkillValidationError"

python "$SCRIPTS_DIR/phase2_stream_d_config_validator.py" > /tmp/phase2_d.log 2>&1 &
PID_D=$!
echo "[PID $PID_D] Stream D: ConfigValidator consolidation"

echo ""
echo "Waiting for all streams to complete..."
echo ""

wait $PID_A $PID_B $PID_C $PID_D || true

echo "═════════════════════════════════════════════"
echo "  STREAM RESULTS"
echo "═════════════════════════════════════════════"
echo ""

echo "--- STREAM A: ValidationError ---"
cat /tmp/phase2_a.log
echo ""

echo "--- STREAM B: ExitCode ---"
cat /tmp/phase2_b.log
echo ""

echo "--- STREAM C: ConfigValidationError/SkillValidationError ---"
cat /tmp/phase2_c.log
echo ""

echo "--- STREAM D: ConfigValidator ---"
cat /tmp/phase2_d.log
echo ""

echo "═════════════════════════════════════════════"
echo "  CREATING COMMITS"
echo "═════════════════════════════════════════════"
echo ""

git add -A

echo "Commit 1: Consolidate exception classes..."
git commit -m "refactor(consolidation): consolidate exception class definitions

- Consolidate ValidationError -> scripts/utils/exceptions.py
- Consolidate ExitCode -> scripts/utils/exceptions.py
- Update 30+ import statements
- Remove duplicate definitions from scriptError.py, syncDoc.py, cli/base.py
- Savings: ~150 lines

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>" || echo "No changes to commit"

git add -A

echo "Commit 2: Consolidate ConfigValidator variants..."
git commit -m "refactor(consolidation): consolidate ConfigValidator definitions

- Consolidate ConfigValidator variants
- Remove duplicates from validation.py and validate_config_semantic.py
- Update 10+ import statements
- Savings: ~50 lines

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>" || echo "No changes to commit"

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║  PHASE 2 COMPLETE                          ║"
echo "║  Ready: git push origin main               ║"
echo "╚════════════════════════════════════════════╝"
echo ""

git log --oneline -3

echo ""
echo "Next: git push origin main"
