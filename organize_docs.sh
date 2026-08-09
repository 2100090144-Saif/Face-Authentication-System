#!/bin/bash
# Script to organize markdown documentation files
# This moves all root .md files (except README.md) to docs/archive/

echo "========================================"
echo " Documentation Organization Script"
echo "========================================"
echo ""

# Create docs/archive directory if it doesn't exist
if [ ! -d "docs/archive" ]; then
    echo "Creating docs/archive directory..."
    mkdir -p "docs/archive"
fi

echo ""
echo "Moving markdown files to docs/archive..."
echo ""

# Move all .md files except README.md
for file in *.md; do
    if [ "$file" != "README.md" ]; then
        echo "Moving $file"
        mv "$file" "docs/archive/" 2>/dev/null || true
    fi
done

echo ""
echo "========================================"
echo " Organization Complete!"
echo "========================================"
echo ""
echo "Summary:"
echo "- Consolidated documentation in docs/ folder"
echo "- Original files archived in docs/archive/"
echo "- README.md remains in root directory"
echo ""
echo "Next steps:"
echo "1. Review docs/README.md for navigation"
echo "2. Check docs/archive/ to verify files moved"
echo "3. Delete docs/archive/ if you don't need backups"
echo ""
