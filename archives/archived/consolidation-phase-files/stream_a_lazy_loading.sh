#!/bin/bash
set -e

cd "$(dirname "$(dirname "$(dirname "${BASH_SOURCE[0]}")")")"

echo "=== STREAM A: Lazy Loading Consolidation ==="
echo ""

# A1: Find imports
echo "[A1] Finding imports of lazy loading modules..."
IMPORT_COUNT=$(grep -r "lazy_load_agents\|lazy_load_skills" scripts --include="*.py" | grep -v "scripts/consolidation/" | wc -l || echo "0")
echo "  Found: $IMPORT_COUNT files"

# A2: Update imports
if [ "$IMPORT_COUNT" -gt 0 ]; then
    echo "[A2] Updating imports..."
    grep -r "from scripts.utils.lazy_load_agents import" scripts --include="*.py" --files-with-matches | grep -v "scripts/consolidation/" | while read FILE; do
        sed -i 's/from scripts\.utils\.lazy_load_agents import/from scripts.utils.lazy_loader import/g' "$FILE"
    done
    grep -r "from scripts.utils.lazy_load_skills import" scripts --include="*.py" --files-with-matches | grep -v "scripts/consolidation/" | while read FILE; do
        sed -i 's/from scripts\.utils\.lazy_load_skills import/from scripts.utils.lazy_loader import/g' "$FILE"
    done
    echo "  Updated: 2 files"
fi

# A3: Delete old lazy loading modules
echo "[A3] Deleting old lazy loading modules..."
rm -f scripts/utils/lazy_load_agents.py scripts/utils/lazy_load_skills.py
echo "  Deleted: lazy_load_agents.py, lazy_load_skills.py"

# A4: Verify
echo "[A4] Verifying lazy_loader.py exists..."
if [ -f "scripts/utils/lazy_loader.py" ]; then
    echo "  OK: lazy_loader.py found"
else
    echo "  ERROR: lazy_loader.py not found"
fi

echo ""
echo "[SUCCESS] Stream A Complete - Lazy loading consolidated"
