deactivate
rmdir /s /q .venv
uv venv .venv
call .venv\Scripts\activate.bat
python -V
uv sync