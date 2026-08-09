@echo off
REM ============================================================
REM Face Authentication System - Project Cleanup Script (Windows)
REM Organizes documentation and scripts into proper directories
REM ============================================================

echo 🧹 Starting project cleanup...
echo.

REM ── Step 1: Create directory structure ─────────────────────
echo 📁 Creating directory structure...
mkdir docs\fixes 2>nul
mkdir docs\guides 2>nul
mkdir docs\summaries 2>nul
mkdir scripts\debug 2>nul
mkdir scripts\migration 2>nul
mkdir scripts\testing 2>nul
mkdir scripts\validation 2>nul

REM ── Step 2: Move bug fix documentation ─────────────────────
echo 📝 Moving bug fix documentation...
move CRITICAL_BUG_FIX_PERCENTAGE_SCALE.md docs\fixes\ 2>nul
move BUG_FIX_SUMMARY_PERCENTAGE_SCALE.md docs\fixes\ 2>nul
move CRITICAL_FIX_APPLIED.md docs\fixes\ 2>nul
move CRITICAL_FIX_ENCODING_MISMATCH.md docs\fixes\ 2>nul
move CRITICAL_SECURITY_FIX.md docs\fixes\ 2>nul
move CONFIDENCE_FIX_COMPLETE.md docs\fixes\ 2>nul
move FALSE_REJECTION_BUG_FIX.md docs\fixes\ 2>nul
move FALSE_REJECTION_FIX_COMPLETED.md docs\fixes\ 2>nul
move FIX_FACE_NOT_RECOGNIZED_AFTER_REGISTRATION.md docs\fixes\ 2>nul
move FIXES_APPLIED.md docs\fixes\ 2>nul
move NUMPY_FIX_COMPLETED.md docs\fixes\ 2>nul
move NUMPY_SERIALIZATION_FIX.md docs\fixes\ 2>nul
move SECURITY_FIX_UNAUTHORIZED_LOGIN.md docs\fixes\ 2>nul
move SECURITY_ENHANCEMENTS_APPLIED.md docs\fixes\ 2>nul
move DOCKER_BUILD_FIX.md docs\fixes\ 2>nul

REM ── Step 3: Move guides ────────────────────────────────────
echo 📖 Moving guides...
move QUICK_START_GUIDE.md docs\guides\ 2>nul
move QUICK_START.md docs\guides\ 2>nul
move HOW_TO_RUN.md docs\guides\ 2>nul
move MONITORING_GUIDE.md docs\guides\ 2>nul
move CONFIDENCE_PERCENTAGE_GUIDE.md docs\guides\ 2>nul
move QUICK_REFERENCE_FACE_MATCHING.md docs\guides\ 2>nul
move DOCKER_VOLUME_MAPPING_GUIDE.md docs\guides\ 2>nul
move DOCKER_VS_LOCAL_PYTHON.md docs\guides\ 2>nul
move RUN_WITH_DOCKER_ONLY.md docs\guides\ 2>nul
move ADVANCED_FACE_RECOGNITION_EXPLAINED.md docs\guides\ 2>nul
move FACE_RECOGNITION_LOGIC_EXPLAINED.md docs\guides\ 2>nul
move FACE_RECOGNITION_MODELS_EXPLAINED.md docs\guides\ 2>nul
move IMPROVE_FACE_RECOGNITION_ACCURACY.md docs\guides\ 2>nul

REM ── Step 4: Move summaries ─────────────────────────────────
echo 📊 Moving summaries...
move ALL_FIXES_COMPLETED_SUMMARY.md docs\summaries\ 2>nul
move FINAL_SUMMARY.md docs\summaries\ 2>nul
move FINAL_FIX_COMPLETE.md docs\summaries\ 2>nul
move IMPLEMENTATION_SUMMARY.md docs\summaries\ 2>nul
move INTEGRATION_COMPLETE.md docs\summaries\ 2>nul
move REFACTORING_SUMMARY.md docs\summaries\ 2>nul
move SYSTEM_COMPLETE_AND_WORKING.md docs\summaries\ 2>nul
move SYSTEM_COMPLIANCE_ANALYSIS.md docs\summaries\ 2>nul
move SYSTEM_STATUS.md docs\summaries\ 2>nul
move SYSTEM_VERIFICATION_COMPLETE.md docs\summaries\ 2>nul
move TASK_COMPLETE_SECURITY_FIX.md docs\summaries\ 2>nul
move TASK_COMPLETED_SUCCESSFULLY.md docs\summaries\ 2>nul
move INSTALLATION_STATUS.md docs\summaries\ 2>nul
move NUMPY_AND_DEPENDENCIES_STATUS.md docs\summaries\ 2>nul
move MULTI_AGENT_EXECUTION_REPORT.md docs\summaries\ 2>nul
move REFACTORING_CHECKLIST.md docs\summaries\ 2>nul
move RESTART_REQUIRED.md docs\summaries\ 2>nul
move UPDATED_SETTINGS_80_PERCENT.md docs\summaries\ 2>nul
move PROJECT_STRUCTURE.md docs\summaries\ 2>nul

REM ── Step 5: Move debug scripts ─────────────────────────────
echo 🐛 Moving debug scripts...
move debug_encodings.py scripts\debug\ 2>nul
move verify_setup.py scripts\debug\ 2>nul

REM ── Step 6: Move migration scripts ────────────────────────
echo 🔄 Moving migration scripts...
move migrate_encodings.py scripts\migration\ 2>nul
move fix_encodings.py scripts\migration\ 2>nul
move fix_encoding_dimensions.py scripts\migration\ 2>nul
move fix_duplicate_users.py scripts\migration\ 2>nul
move hotfix_confidence_threshold.py scripts\migration\ 2>nul

REM ── Step 7: Move test scripts ──────────────────────────────
echo 🧪 Moving test scripts...
move test_confidence_fix.py scripts\testing\ 2>nul
move test_face_matching.py scripts\testing\ 2>nul
move test_multi_frame_auth.py scripts\testing\ 2>nul

REM ── Step 8: Move validation scripts ────────────────────────
echo ✅ Moving validation scripts...
move validate_dependencies.py scripts\validation\ 2>nul
move validate_encodings.py scripts\validation\ 2>nul

REM ── Step 9: Clean up generated files ───────────────────────
echo 🗑️  Removing generated files...
del project_tree.txt 2>nul

REM ── Step 10: Update .dockerignore ──────────────────────────
echo 🐳 Updating .dockerignore...
findstr /C:"docs/" .dockerignore >nul 2>&1
if errorlevel 1 (
    echo. >> .dockerignore
    echo # Documentation (not needed in container^) >> .dockerignore
    echo docs/ >> .dockerignore
    echo scripts/ >> .dockerignore
    echo *.md >> .dockerignore
    echo !README.md >> .dockerignore
    echo PROJECT_CLEANUP_PLAN.md >> .dockerignore
)

REM ── Step 11: Summary ───────────────────────────────────────
echo.
echo ✅ Cleanup complete!
echo.
echo 📊 Summary:
echo   ✅ Created docs/ directory with subdirectories
echo   ✅ Created scripts/ directory with subdirectories
echo   ✅ Moved ~50 documentation files to docs/
echo   ✅ Moved ~10 script files to scripts/
echo   ✅ Updated .dockerignore
echo.
echo 📁 New structure:
echo   Root: 12 core files (clean!^)
echo   docs/: All documentation
echo   scripts/: All utility scripts
echo.
echo 🚀 Next steps:
echo   1. Review the new structure
echo   2. Test Docker build: docker-compose build
echo   3. Commit changes: git add . ^&^& git commit -m "Organize project structure"
echo.
pause
