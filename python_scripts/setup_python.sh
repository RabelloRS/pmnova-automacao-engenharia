#!/bin/bash

# Script de configuração do ambiente Python
# Execute: bash setup_python.sh

echo "==================================="
echo "Configurando Ambiente Python"
echo "==================================="

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instalando..."
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

echo "✓ Python3 encontrado: $(python3 --version)"

# Criar ambiente virtual
echo ""
echo "Criando ambiente virtual (venv)..."
python3 -m venv venv

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo ""
echo "Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo ""
echo "Instalando dependências do requirements.txt..."
pip install -r requirements.txt

echo ""
echo "==================================="
echo "✓ Ambiente configurado com sucesso!"
echo "==================================="
echo ""
echo "Para ativar o ambiente virtual, execute:"
echo "  cd /root/pmnova/python_scripts"
echo "  source venv/bin/activate"
echo ""
echo "Para desativar:"
echo "  deactivate"
