@echo off
setlocal
set "venv_name=venv"

echo Inicializando Ambiente Virtual
python -m venv %venv_name%

echo Instalando Dependencias
python utils/postvenv.py --source %venv_name% --require requirements.txt

endlocal
