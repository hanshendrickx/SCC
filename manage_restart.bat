REM manage restart script
REM Activate
call C:\Users\hansh\django_sandbox\rest-framework-tutorial\.venv\Scripts\activate.bat
REM Confirm
python -V
black .
ruff check . --fix
uv sync 
python C:\Users\hansh\django_sandbox\rest-framework-tutorial\manage.py check
python C:\Users\hansh\django_sandbox\rest-framework-tutorial\manage.py runserver
cmd
Cd C:\Users\hansh\django_sandbox
cd C:\Users\hansh\django_sandbox\rest-framework-tutorial\
call .venv\Scripts\activate.bat
python manage.py check
REM python manage.py createsuperuser 
start http://127.0.0.1:8000/
python manage.py runserver
