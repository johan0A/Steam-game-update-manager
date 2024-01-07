@echo off
echo Creating virtual environment...
py -m venv venv
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Installing required libraries...
pip install PyQt5 vdf bs4
pip install -U steam[client]
pip install tk
echo Done. The virtual environment is ready.
pause