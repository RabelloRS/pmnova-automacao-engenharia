#!/bin/bash

# Script para parar o Portal de Engenharia
# Execute: bash stop-portal.sh

echo "🛑 Parando Portal de Engenharia..."
docker-compose down

echo ""
echo "✓ Serviços parados com sucesso!"
echo ""
echo "Para reiniciar: bash start-portal.sh"
