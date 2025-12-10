#!/bin/bash

# Script para iniciar o ambiente completo
# Execute: bash start.sh

echo "================================================"
echo "🏗️  PMNova - Sistema de Automação"
echo "================================================"
echo ""

# Verificar se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando. Iniciando..."
    sudo systemctl start docker
    sleep 3
fi

echo "✓ Docker está ativo"
echo ""

# Verificar se arquivo .env existe
if [ ! -f .env ]; then
    echo "⚠️  Arquivo .env não encontrado!"
    echo "Copiando .env.example para .env..."
    cp .env.example .env
    echo "✓ Arquivo .env criado"
    echo ""
    echo "⚠️  IMPORTANTE: Edite o arquivo .env e configure suas credenciais!"
    echo "   nano .env"
    echo ""
    read -p "Pressione ENTER para continuar..."
fi

# Subir containers
echo "🚀 Iniciando n8n..."
docker-compose up -d

echo ""
echo "⏳ Aguardando n8n inicializar..."
sleep 5

# Verificar status
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "================================================"
    echo "✅ n8n iniciado com sucesso!"
    echo "================================================"
    echo ""
    echo "📊 Acesse o n8n em: http://localhost:5678"
    echo ""
    echo "🔐 Credenciais padrão:"
    echo "   Usuário: admin"
    echo "   Senha: admin123"
    echo ""
    echo "⚠️  Altere a senha em produção!"
    echo ""
    echo "📋 Comandos úteis:"
    echo "   Ver logs:    docker-compose logs -f n8n"
    echo "   Parar:       docker-compose down"
    echo "   Reiniciar:   docker-compose restart n8n"
    echo ""
else
    echo ""
    echo "❌ Erro ao iniciar n8n"
    echo "Verifique os logs: docker-compose logs n8n"
fi
