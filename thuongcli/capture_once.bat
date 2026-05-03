@echo off
setlocal
cd /d "%~dp0"

python "input.py"
if %errorlevel% neq 0 (
    echo Co loi khi nhap SAVE_DIR.
    pause
    exit /b 1
)

start "" pythonw "screen_capture_tool.pyw"

endlocal
