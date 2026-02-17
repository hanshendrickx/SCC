@echo off
prompt $P$G
cd %USERPROFILE%
cd c:\Users\hansh\django_sandbox\SCC\
call .venv\Scripts\activate.bat
uv sync
uv run black .
uv run ruff check . --fix
start "" "http://127.0.0.1:8000/"
REM check and start SCC
start "" http://127.0.0.1:8000/
python manage.py check
python manage.py runserver


