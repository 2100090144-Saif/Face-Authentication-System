#!/bin/bash

# ============================================================
# Face Authentication System - Project Cleanup Script
# Organizes documentation and scripts into proper directories
# ============================================================

echo "🧹 Starting project cleanup..."
echo ""

# ── Step 1: Create directory structure ─────────────────────
echo "📁 Creating directory structure..."
mkdir -p docs/fixes
mkdir -p docs/guides
mkdir -p docs/summaries
mkdir -p scripts/debug
mkdir -p scripts/migration
mkdir -p scripts/testing
mkdir -p scripts/validation

# ── Step 2: Move bug fix documentation ─────────────────────
echo "📝 Moving bug fix documentation..."
mv CRITICAL_BUG_FIX_PERCENTAGE_SCALE.md docs/fixes/ 2>/dev/null
mv BUG_FIX_SUMMARY_PERCENTAGE_SCALE.md docs/fixes/ 2>/dev/null
mv CRITICAL_FIX_APPLIED.md docs/fixes/ 2>/dev/null
mv CRITICAL_FIX_ENCODING_MISMATCH.md docs/fixes/ 2>/dev/null
mv CRITICAL_SECURITY_FIX.md docs/fixes/ 2>/dev/null
mv CONFIDENCE_FIX_COMPLETE.md docs/fixes/ 2>/dev/null
mv FALSE_REJECTION_BUG_FIX.md docs/fixes/ 2>/dev/null
mv FALSE_REJECTION_FIX_COMPLETED.md docs/fixes/ 2>/dev/null
mv FIX_FACE_NOT_RECOGNIZED_AFTER_REGISTRATION.md docs/fixes/ 2>/dev/null
mv FIXES_APPLIED.md docs/fixes/ 2>/dev/null
mv NUMPY_FIX_COMPLETED.md docs/fixes/ 2>/dev/null
mv NUMPY_SERIALIZATION_FIX.md docs/fixes/ 2>/dev/null
mv SECURITY_FIX_UNAUTHORIZED_LOGIN.md docs/fixes/ 2>/dev/null
mv SECURITY_ENHANCEMENTS_APPLIED.md docs/fixes/ 2>/dev/null
mv DOCKER_BUILD_FIX.md docs/fixes/ 2>/dev/null

# ── Step 3: Move guides ────────────────────────────────────
echo "📖 Moving guides..."
mv QUICK_START_GUIDE.md docs/guides/ 2>/dev/null
mv QUICK_START.md docs/guides/ 2>/dev/null
mv HOW_TO_RUN.md docs/guides/ 2>/dev/null
mv MONITORING_GUIDE.md docs/guides/ 2>/dev/null
mv CONFIDENCE_PERCENTAGE_GUIDE.md docs/guides/ 2>/dev/null
mv QUICK_REFERENCE_FACE_MATCHING.md docs/guides/ 2>/dev/null
mv DOCKER_VOLUME_MAPPING_GUIDE.md docs/guides/ 2>/dev/null
mv DOCKER_VS_LOCAL_PYTHON.md docs/guides/ 2>/dev/null
mv RUN_WITH_DOCKER_ONLY.md docs/guides/ 2>/dev/null
mv ADVANCED_FACE_RECOGNITION_EXPLAINED.md docs/guides/ 2>/dev/null
mv FACE_RECOGNITION_LOGIC_EXPLAINED.md docs/guides/ 2>/dev/null
mv FACE_RECOGNITION_MODELS_EXPLAINED.md docs/guides/ 2>/dev/null
mv IMPROVE_FACE_RECOGNITION_ACCURACY.md docs/guides/ 2>/dev/null

# ── Step 4: Move summaries ─────────────────────────────────
echo "📊 Moving summaries..."
mv ALL_FIXES_COMPLETED_SUMMARY.md docs/summaries/ 2>/dev/null
mv FINAL_SUMMARY.md docs/summaries/ 2>/dev/null
mv FINAL_FIX_COMPLETE.md docs/summaries/ 2>/dev/null
mv IMPLEMENTATION_SUMMARY.md docs/summaries/ 2>/dev/null
mv INTEGRATION_COMPLETE.md docs/summaries/ 2>/dev/null
mv REFACTORING_SUMMARY.md docs/summaries/ 2>/dev/null
mv SYSTEM_COMPLETE_AND_WORKING.md docs/summaries/ 2>/dev/null
mv SYSTEM_COMPLIANCE_ANALYSIS.md docs/summaries/ 2>/dev/null
mv SYSTEM_STATUS.md docs/summaries/ 2>/dev/null
mv SYSTEM_VERIFICATION_COMPLETE.md docs/summaries/ 2>/dev/null
mv TASK_COMPLETE_SECURITY_FIX.md docs/summaries/ 2>/dev/null
mv TASK_COMPLETED_SUCCESSFULLY.md docs/summaries/ 2>/dev/null
mv INSTALLATION_STATUS.md docs/summaries/ 2>/dev/null
mv NUMPY_AND_DEPENDENCIES_STATUS.md docs/summaries/ 2>/dev/null
mv MULTI_AGENT_EXECUTION_REPORT.md docs/summaries/ 2>/dev/null
mv REFACTORING_CHECKLIST.md docs/summaries/ 2>/dev/null
mv RESTART_REQUIRED.md docs/summaries/ 2>/dev/null
mv UPDATED_SETTINGS_80_PERCENT.md docs/summaries/ 2>/dev/null
mv PROJECT_STRUCTURE.md docs/summaries/ 2>/dev/null

# ── Step 5: Move debug scripts ─────────────────────────────
echo "🐛 Moving debug scripts..."
mv debug_encodings.py scripts/debug/ 2>/dev/null
mv verify_setup.py scripts/debug/ 2>/dev/null

# ── Step 6: Move migration scripts ────────────────────────
echo "🔄 Moving migration scripts..."
mv migrate_encodings.py scripts/migration/ 2>/dev/null
mv fix_encodings.py scripts/migration/ 2>/dev/null
mv fix_encoding_dimensions.py scripts/migration/ 2>/dev/null
mv fix_duplicate_users.py scripts/migration/ 2>/dev/null
mv hotfix_confidence_threshold.py scripts/migration/ 2>/dev/null

# ── Step 7: Move test scripts ──────────────────────────────
echo "🧪 Moving test scripts..."
mv test_confidence_fix.py scripts/testing/ 2>/dev/null
mv test_face_matching.py scripts/testing/ 2>/dev/null
mv test_multi_frame_auth.py scripts/testing/ 2>/dev/null

# ── Step 8: Move validation scripts ────────────────────────
echo "✅ Moving validation scripts..."
mv validate_dependencies.py scripts/validation/ 2>/dev/null
mv validate_encodings.py scripts/validation/ 2>/dev/null

# ── Step 9: Clean up generated files ───────────────────────
echo "🗑️  Removing generated files..."
rm -f project_tree.txt 2>/dev/null

# ── Step 10: Update .dockerignore ──────────────────────────
echo "🐳 Updating .dockerignore..."
if ! grep -q "^docs/" .dockerignore 2>/dev/null; then
    echo "" >> .dockerignore
    echo "# Documentation (not needed in container)" >> .dockerignore
    echo "docs/" >> .dockerignore
    echo "scripts/" >> .dockerignore
    echo "*.md" >> .dockerignore
    echo "!README.md" >> .dockerignore
    echo "PROJECT_CLEANUP_PLAN.md" >> .dockerignore
fi

# ── Step 11: Create index files ────────────────────────────
echo "📋 Creating index files..."

# Create docs/README.md
cat > docs/README.md << 'EOF'
# Documentation

This directory contains all project documentation organized by category.

## Structure

- **fixes/** - Bug fix documentation and technical details
- **guides/** - User guides and how-to documents
- **summaries/** - Project summaries and status reports

## Quick Links

### Guides
- [Quick Start Guide](guides/QUICK_START_GUIDE.md)
- [Docker Guide](guides/DOCKER_VOLUME_MAPPING_GUIDE.md)
- [Face Recognition Explained](guides/FACE_RECOGNITION_LOGIC_EXPLAINED.md)

### Latest Fixes
- [Percentage Scale Fix](fixes/CRITICAL_BUG_FIX_PERCENTAGE_SCALE.md)
- [NumPy Serialization Fix](fixes/NUMPY_FIX_COMPLETED.md)
- [False Rejection Fix](fixes/FALSE_REJECTION_FIX_COMPLETED.md)

### Summaries
- [All Fixes Completed](summaries/ALL_FIXES_COMPLETED_SUMMARY.md)
- [System Verification](summaries/SYSTEM_VERIFICATION_COMPLETE.md)
- [System Compliance](summaries/SYSTEM_COMPLIANCE_ANALYSIS.md)
EOF

# Create scripts/README.md
cat > scripts/README.md << 'EOF'
# Utility Scripts

This directory contains utility scripts for debugging, testing, and maintenance.

## Structure

- **debug/** - Debugging and verification scripts
- **migration/** - Database migration and fix scripts
- **testing/** - Test scripts for features
- **validation/** - Validation and health check scripts

## Usage

### Debug Scripts
```bash
python scripts/debug/debug_encodings.py
python scripts/debug/verify_setup.py
```

### Migration Scripts
```bash
python scripts/migration/migrate_encodings.py
python scripts/migration/fix_encodings.py
```

### Test Scripts
```bash
python scripts/testing/test_confidence_fix.py
python scripts/testing/test_face_matching.py
```

### Validation Scripts
```bash
python scripts/validation/validate_dependencies.py
python scripts/validation/validate_encodings.py
```
EOF

# ── Step 12: Summary ───────────────────────────────────────
echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📊 Summary:"
echo "  ✅ Created docs/ directory with subdirectories"
echo "  ✅ Created scripts/ directory with subdirectories"
echo "  ✅ Moved ~50 documentation files to docs/"
echo "  ✅ Moved ~10 script files to scripts/"
echo "  ✅ Updated .dockerignore"
echo "  ✅ Created index files"
echo ""
echo "📁 New structure:"
echo "  Root: 12 core files (clean!)"
echo "  docs/: All documentation"
echo "  scripts/: All utility scripts"
echo ""
echo "🚀 Next steps:"
echo "  1. Review the new structure"
echo "  2. Test Docker build: docker-compose build"
echo "  3. Commit changes: git add . && git commit -m 'Organize project structure'"
echo ""
