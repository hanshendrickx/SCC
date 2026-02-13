Set-Location "C:\Users\hansh\django_sandbox\SCC"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/hanshendrickx/SCC.git
git pull --rebase origin main
git push -u origin main
