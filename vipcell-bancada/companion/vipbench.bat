@echo off
REM Lançador do Vipcell Bancada (Windows). Precisa de Python e do platform-tools no PATH.
where python >nul 2>nul || (echo Instale o Python 3 em python.org e marque "Add to PATH" & pause & exit /b 1)
python -m vipbench.cli %*
