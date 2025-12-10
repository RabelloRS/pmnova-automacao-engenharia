#!/bin/bash

# diagnose.sh
# Script para diagnosticar problemas no Portal de Engenharia
# Execute: bash diagnose.sh

echo "=================================================="
echo "🔍 Diagnóstico - Portal de Engenharia"
echo "=================================================="
echo ""

# 1. Verificar Docker
echo "1️⃣  Docker e Docker Compose:"
if command -v docker &> /dev/null; then
    echo "   ✓ Docker instalado: $(docker --version)"
else
    echo "   ✗ Docker NÃO instalado"
fi

if command -v docker-compose &> /dev/null; then
    echo "   ✓ Docker Compose instalado: $(docker-compose --version)"
else
    echo "   ✗ Docker Compose NÃO instalado"
fi

echo ""

# 2. Verificar estrutura de pastas
echo "2️⃣  Estrutura de Diretórios:"
folders=("n8n_data" "shared_files" "shared_files/templates" "shared_files/output" "frontend")
for folder in "${folders[@]}"; do
    if [ -d "$folder" ]; then
        echo "   ✓ Pasta '$folder' existe"
    else
        echo "   ✗ Pasta '$folder' NÃO existe"
    fi
done

echo ""

# 3. Verificar templates
echo "3️⃣  Templates .docx:"
templates=$(find shared_files/templates -name "*.docx" 2>/dev/null | wc -l)
if [ $templates -gt 0 ]; then
    echo "   ✓ Encontrados $templates template(s)"
    find shared_files/templates -name "*.docx" -exec basename {} \;
else
    echo "   ✗ Nenhum template .docx encontrado"
    echo "   ⚠️  Crie pelo menos template_etp.docx"
fi

echo ""

# 4. Verificar permissões de scripts
echo "4️⃣  Permissões de Execução:"
scripts=("start-portal.sh" "stop-portal.sh" "setup-port-forwarding.ps1")
for script in "${scripts[@]}"; do
    if [ -x "$script" ]; then
        echo "   ✓ Script '$script' é executável"
    else
        echo "   ⚠️  Script '$script' NÃO é executável"
        echo "      Execute: chmod +x $script"
    fi
done

echo ""

# 5. Verificar arquivos de configuração
echo "5️⃣  Arquivos de Configuração:"
files=("docker-compose.yml" "frontend/Dockerfile" "frontend/requirements.txt" "frontend/app.py")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        lines=$(wc -l < "$file")
        echo "   ✓ '$file' existe ($lines linhas)"
    else
        echo "   ✗ '$file' NÃO existe"
    fi
done

echo ""

# 6. Verificar containers rodando
echo "6️⃣  Status dos Containers:"
if docker ps &> /dev/null; then
    count=$(docker ps --filter "name=engenharia" --quiet | wc -l)
    if [ $count -gt 0 ]; then
        echo "   ✓ $count container(s) rodando:"
        docker ps --filter "name=engenharia" --format "   - {{.Names}}: {{.Status}}"
    else
        echo "   ℹ️  Nenhum container rodando"
        echo "   Execute: bash start-portal.sh"
    fi
else
    echo "   ✗ Não consegui conectar ao Docker"
fi

echo ""

# 7. Verificar conectividade
echo "7️⃣  Conectividade:"
if docker ps &> /dev/null; then
    if curl -s http://localhost:8501 &> /dev/null; then
        echo "   ✓ Streamlit respondendo em http://localhost:8501"
    else
        echo "   ⚠️  Streamlit não respondendo"
    fi

    if curl -s http://localhost:5678 &> /dev/null; then
        echo "   ✓ n8n respondendo em http://localhost:5678"
    else
        echo "   ⚠️  n8n não respondendo"
    fi
fi

echo ""

# 8. Verificar volumes e paths
echo "8️⃣  Volumes e Mapeamentos:"
echo "   docker-compose.yml volumes:"
grep -A 5 "volumes:" docker-compose.yml | grep -E "^\s+-" | head -10

echo ""

# 9. Resumo
echo "=================================================="
echo "📊 Resumo:"
echo ""
echo "Se tudo está ✓, execute:"
echo "  bash start-portal.sh"
echo ""
echo "Se houver ⚠️ ou ✗, consulte SETUP_CHECKLIST.md"
echo "=================================================="
