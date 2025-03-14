#!/bin/bash

# Nome do ambiente virtual
VENV_NAME="venv"

# Criar o ambiente virtual com Python 3.10
python3.10 -m venv $VENV_NAME

# Ativar o ambiente virtual
source $VENV_NAME/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar os requisitos
pip install -r requirements.txt || {
    echo "Erro ao instalar requirements, tentando corrigir..."
    # sudo apt-get update && sudo apt-get install -y portaudio19-dev
    pip install pyaudio
}

# Reativar o ambiente virtual para garantir que tudo esteja certo
source $VENV_NAME/bin/activate

echo "Ambiente virtual configurado e ativado!"
echo "Para desativar o ambiente virtual, execute: deactivate"