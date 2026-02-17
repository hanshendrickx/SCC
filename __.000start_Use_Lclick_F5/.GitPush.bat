@echo off
prompt $P$G
cd %USERPROFILE%
cd c:\Users\hansh\django_sandbox\SCC\
call .venv\Scripts\activate/bat
git remote add origin https://github.com/hanshendrickx/SCC.git
git status
git add .
git commit -m "Update code after check links and start server, black and ruff checks"
git push origin main