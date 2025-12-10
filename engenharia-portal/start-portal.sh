#!/bin/bash

# Script para iniciar o Portal de Engenharia
# Execute: bash start-portal.sh

echo "=========================================="
echo "🏗️  Portal de Engenharia - PMNP"
echo "=========================================="
echo ""

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Iniciando..."
    sudo systemctl start docker
    sleep 3
fi

echo "✓ Docker está ativo"
echo ""

# Criar pasta de output se não existir
mkdir -p shared_files/output
mkdir -p shared_files/templates

# Iniciar serviços
echo "🚀 Iniciando serviços (n8n + Streamlit)..."
docker-compose up -d --build

echo ""
echo "⏳ Aguardando serviços inicializarem..."
sleep 8

# Verificar status
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "=========================================="
    echo "✅ Portal iniciado com sucesso!"
    echo "=========================================="
    echo ""
    echo "📊 Streamlit (Frontend): http://localhost:8501"
    echo "⚙️  n8n (Backend):        http://localhost:5678"
    echo ""
    echo "🔐 Credenciais do n8n:"
    echo "   Usuário: admin"
    echo "   Senha: engenharia2025"
    echo ""
    echo "🌐 Para acessar de outros computadores:"
    echo "   1. Descubra o IP do WSL: hostname -I"
    echo "   2. No Windows (PowerShell Admin), execute:"
    echo "      Set-ExecutionPolicy Bypass -Scope Process -Force"
    echo "      .\\setup-port-forwarding.ps1"
    echo ""
    echo "📋 Comandos úteis:"
    echo "   Ver logs:    docker-compose logs -f"
    echo "   Parar:       docker-compose down"
    echo "   Reiniciar:   docker-compose restart"
    echo ""
else
    echo ""
    echo "❌ Erro ao iniciar serviços"
    echo "Verifique os logs: docker-compose logs"
fi
