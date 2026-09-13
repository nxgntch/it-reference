#!/bin/bash
# Stream A: Cleanup & Archive - Delete/move obsolete files
# Run in parallel with other streams

set -e

echo "=== STREAM A: Cleanup & Archive ==="
echo ""

# A1: Delete .backup files
echo "A1: Deleting .backup files..."
find scripts -name "*.backup" -type f -delete 2>/dev/null || true
echo "   ✓ Deleted .backup files"

# A2: Archive scripts/optimize/ (if exists)
echo "A2: Archiving scripts/optimize/..."
if [ -d "scripts/optimize" ]; then
    mkdir -p docs/work/archived
    mv scripts/optimize docs/work/archived/optimize-phase
    echo "   ✓ Archived scripts/optimize/"
else
    echo "   ✓ scripts/optimize/ already archived or removed"
fi

# A3: Remove test_refactor obsolete files
echo "A3: Removing test_refactor obsolete files..."
rm -f scripts/test_refactor/orchestrate_refactor.py 2>/dev/null || true
rm -f scripts/test_refactor/step1_create_shared_data.py 2>/dev/null || true
rm -f scripts/test_refactor/step2_add_fixtures.py 2>/dev/null || true
echo "   ✓ Removed test_refactor obsolete files"

# A4: Archive scripts/phase22/ (if exists)
echo "A4: Archiving scripts/phase22/..."
if [ -d "scripts/phase22" ]; then
    mkdir -p docs/work/archived
    mv scripts/phase22 docs/work/archived/phase22-completion
    echo "   ✓ Archived scripts/phase22/"
else
    echo "   ✓ scripts/phase22/ already archived or removed"
fi

# A5: Flatten scripts/consolidation/
echo "A5: Flattening scripts/consolidation/..."
if [ -d "scripts/consolidation/scripts/consolidation" ]; then
    find scripts/consolidation/scripts/consolidation -type f -exec mv {} scripts/consolidation/ \; 2>/dev/null || true
    rm -rf scripts/consolidation/scripts
    echo "   ✓ Flattened scripts/consolidation/"
else
    echo "   ✓ scripts/consolidation/ already flattened"
fi

# A6: Remove empty scripts/validation/
echo "A6: Removing scripts/validation/..."
rm -rf scripts/validation 2>/dev/null || true
echo "   ✓ Removed scripts/validation/"

# A7: Clean up old test refactor dir if empty
echo "A7: Cleaning up empty directories..."
rmdir scripts/test_refactor 2>/dev/null || true
rmdir scripts/archive 2>/dev/null || true
echo "   ✓ Cleaned empty directories"

echo ""
echo "╔════════════════════════════════════════╗"
echo "║  STREAM A COMPLETE ✓                   ║"
echo "╚════════════════════════════════════════╝"
