echo Inicializando Ambiente Virtual
python -m venv aquadepth
echo Instalando Dependencias
pip install -q -r requirements.txt
echo Ativando Ambiente Virtual
./aquadepth/Scripts/activate.bat

