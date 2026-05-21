@echo off
cd /d "%~dp0"
echo [~] Building Ultria-box...
python -m PyInstaller --clean ^
  --workpath "build\Build\work" ^
  --distpath "build\Build" ^
  "build\Build\Ultria-box.spec"
if %ERRORLEVEL% neq 0 (
    echo [x] Build failed.
    pause
    exit /b 1
)
if exist "build\Build\work" (
    echo [~] Cleaning up intermediate files...
    rmdir /s /q "build\Build\work"
)
echo [+] Done. Output: build\Build\Ultria-box\
pause
