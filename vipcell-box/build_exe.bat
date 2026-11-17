@echo off
REM ============================================================
REM  Gera o executavel VipcellBox.exe (rodar no Windows)
REM  Precisa de Python 3.9+ instalado e no PATH.
REM ============================================================
echo Instalando dependencias...
python -m pip install --upgrade pip
python -m pip install pyusb pyinstaller

echo.
echo Gerando o executavel...
pyinstaller --onefile --noconsole --name VipcellBox vipcell_box.py

echo.
echo ============================================================
echo  Pronto. O programa esta em:  dist\VipcellBox.exe
echo  (de dois cliques nele para abrir)
echo ============================================================
pause
