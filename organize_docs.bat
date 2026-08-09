@echo off
REM Script to organize markdown documentation files
REM This moves all root .md files (except README.md) to docs/archive/

echo ========================================
echo  Documentation Organization Script
echo ========================================
echo.

REM Create docs/archive directory if it doesn't exist
if not exist "docs\archive" (
    echo Creating docs\archive directory...
    mkdir "docs\archive"
)

echo.
echo Moving markdown files to docs\archive...
echo.

REM Move all .md files except README.md
for %%f in (*.md) do (
    if /i not "%%f"=="README.md" (
        echo Moving %%f
        move "%%f" "docs\archive\" >nul 2>&1
    )
)

echo.
echo ========================================
echo  Organization Complete!
echo ========================================
echo.
echo Summary:
echo - Consolidated documentation in docs/ folder
echo - Original files archived in docs/archive/
echo - README.md remains in root directory
echo.
echo Next steps:
echo 1. Review docs/README.md for navigation
echo 2. Check docs/archive/ to verify files moved
echo 3. Delete docs/archive/ if you don't need backups
echo.
pause
