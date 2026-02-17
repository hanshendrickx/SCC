text
@echo off
setlocal ENABLEEXTENSIONS

REM ============================
REM Project root (adjust once)
REM ============================
cd /d "C:\Users\hansh\django_sandbox\SCC"  || goto :EOF

REM ============================
REM 0. Make this file easy to see
REM ============================
REM Give the window a clear title and color so you recognize it quickly
title SCC DEV SERVER
color 0A

REM ============================
REM 1. Replace .venv (clean + create)
REM ============================
if exist ".venv" (
    echo Removing existing .venv ...
    rmdir /s /q ".venv"
)

echo Creating new .venv with Python 3.12 ...
uv venv .venv --python 3.12
if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    goto :EOF
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    goto :EOF
)

echo Syncing dependencies with uv ...
uv sync
if errorlevel 1 (
    echo uv sync failed.
    pause
    goto :EOF
)

REM ============================
REM 2. Code quality tools
REM ============================
echo Running black ...
uv run black .
echo Running ruff ...
uv run ruff check . --fix

REM ============================
REM 3. Start browser
REM ============================
echo Starting browser at http://127.0.0.1:8000/ ...
start "" "http://127.0.0.1:8000/"

REM ============================
REM 4. Run Django dev server
REM ============================
echo Starting Django development server ...
python manage.py runserver

echo.
echo Server has stopped. Press any key to close.
pause >nul
endlocal
