@echo off
REPLACE .venv BY NEW .venv: Follow step by step
rmdir /s /q .venv
uv venv .venv --python 3.12
.venv\Scripts\activate.bat
uv sync
black .
ruff check . --fix
ping