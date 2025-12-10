#!/bin/bash

# Script para parar o ambiente
# Execute: bash stop.sh

echo "🛑 Parando n8n..."
docker-compose down

echo ""
echo "✓ n8n parado com sucesso!"
echo ""
echo "Para reiniciar: bash start.sh"
