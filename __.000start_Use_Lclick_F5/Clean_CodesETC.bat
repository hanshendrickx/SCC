cd C:\Users\hansh\django_sandbox\SCC
call .venv\Scripts\activate.bat
python manage.py list_urls
black .
ruff check . --fix