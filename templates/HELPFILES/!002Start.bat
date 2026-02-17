@echo off
cd c:\Users\hansh\django_sandbox\SCC\
.venv\Scripts\activate.bat
black .
ruff check . --fix
REM check and start SCC
rem Give the server a moment to start before opening the browser
REM ping 127.0.0.1 -n 3 >nul
start "" http://127.0.0.1:8000/
REM python manage.py check
python manage.py runserver
pause