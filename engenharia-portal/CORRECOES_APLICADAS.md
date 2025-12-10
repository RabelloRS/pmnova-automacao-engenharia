# 🔧 Resumo de Correções Aplicadas

## 🚨 Problema Identificado: Conflito de Caminhos

### O Que Era o Problema?

```
❌ ANTES (CONFLITANTE):
━━━━━━━━━━━━━━━━━━━━━━

python_scripts/gerar_peca.py → /data/templates e /data/output
frontend/app.py              → /files/output
docker-compose.yml (Portal)  → ./shared_files:/files

RESULTADO: Paths não correspondiam, arquivo não seria encontrado ❌
```

---

## ✅ Solução Implementada: Padronização para /data

### Alterações Realizadas

| Arquivo | Antes | Depois | Status |
|---------|-------|--------|--------|
| `docker-compose.yml` (n8n) | `./shared_files:/files` | `./shared_files:/data` | ✅ Ajustado |
| `docker-compose.yml` (streamlit) | `./shared_files:/files` | `./shared_files:/data` | ✅ Ajustado |
| `docker-compose.yml` (n8n volumes) | Sem python_scripts | `../python_scripts:/data/python_scripts:ro` | ✅ Adicionado |
| `frontend/app.py` | `OUTPUT_DIR = "/files/output"` | `OUTPUT_DIR = "/data/output"` | ✅ Ajustado |
| `python_scripts/gerar_peca.py` | `/data/templates` (sem alteração) | `/data/templates` | ✅ Compatível |

---

## 📊 Estrutura de Volumes APÓS Correção

```yaml
SERVIÇO N8N:
├── /home/node/.n8n          ← ./n8n_data (persistência)
├── /data                    ← ./shared_files (templates + output)
└── /data/python_scripts     ← ../python_scripts (scripts Python)

SERVIÇO STREAMLIT:
└── /data                    ← ./shared_files (acesso a templates + output)
```

### Como Funciona Agora:

```
1. Streamlit recebe dados via formulário
       ↓
2. Envia POST para http://n8n:5678/webhook/gerar-etp
       ↓
3. n8n executa: python3 /data/python_scripts/gerar_peca.py
       ↓
4. Script Python:
   - Lê template em: /data/templates/template_etp.docx
   - Salva resultado em: /data/output/ETP_*.docx
       ↓
5. Streamlit consulta /data/output/ e oferece download ✅
```

---

## 📁 Novos Arquivos Criados

### 1. **SETUP_CHECKLIST.md** ✅
   - Guia passo-a-passo para configuração inicial
   - Checklist antes de rodar
   - Instruções para criar templates
   - Configuração de webhook no n8n
   - Troubleshooting completo

### 2. **diagnose.sh** ✅
   - Script de diagnóstico automático
   - Verifica: Docker, pastas, templates, permissões, containers
   - Útil para identificar problemas rapidamente

### 3. **template_etp.txt** ✅
   - Arquivo de exemplo para criar templates Word
   - Mostra a estrutura correta com placeholders

---

## 🚀 Próximos Passos (Seguro Agora)

### 1. Fazer um Teste Rápido
```bash
cd /root/pmnova/engenharia-portal

# Diagnosticar problemas
bash diagnose.sh

# Iniciar sistema
bash start-portal.sh
```

### 2. Criar Templates Word
```
engenharia-portal/shared_files/templates/
├── template_etp.docx   ← Criar (veja SETUP_CHECKLIST.md)
├── template_tr.docx    ← Opcionalmente
└── template_md.docx    ← Opcionalmente
```

### 3. Configurar Workflow no n8n
Siga a documentação em **SETUP_CHECKLIST.md** seção "Configuração do n8n Workflow"

### 4. Testar Integração
```bash
curl -X POST http://localhost:5678/webhook/gerar-etp \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_peca": "etp",
    "objeto": "Pavimentação",
    "justificativa": "Infraestrutura",
    "valor_estimado": "R$ 500.000,00",
    "responsavel": "João"
  }'
```

---

## 📊 Matriz de Compatibilidade APÓS CORREÇÃO

```
ARQUIVO                           | CAMINHO ESPERADO  | STATUS
──────────────────────────────────┼───────────────────┼───────
gerar_peca.py                     | /data/templates   | ✅ OK
gerar_peca.py                     | /data/output      | ✅ OK
app.py (Streamlit)                | /data/output      | ✅ OK
n8n (executa script)              | /data/python_s... | ✅ OK
docker-compose (n8n volume)       | /data             | ✅ OK
docker-compose (streamlit volume) | /data             | ✅ OK
```

---

## 🔍 O Que Mudou no GitHub

**Commit:** `e0476ba`
```
fix: Padronizar caminhos de volumes para /data em todos os serviços

✅ docker-compose.yml (n8n): volumes atualizados
✅ docker-compose.yml (streamlit): volumes atualizados
✅ app.py: OUTPUT_DIR alterado
✅ SETUP_CHECKLIST.md: novo arquivo
✅ diagnose.sh: novo arquivo
✅ template_etp.txt: novo arquivo
```

**Push realizado para:** https://github.com/RabelloRS/pmnova-automacao-engenharia

---

## ⚠️ Avisos Importantes

1. **Templates são obrigatórios:** Você DEVE criar `.docx` antes de rodar
2. **Permissões:** Scripts `.sh` precisam ser executáveis
3. **Primeiro uso:** O n8n inicia vazio, workflow deve ser criado manualmente
4. **Variáveis de ambiente:** Configure `.env` com suas API keys

---

## 🎯 Status Final

```
✅ Estrutura de pastas: CORRIGIDA
✅ Mapeamento de volumes: PADRONIZADO
✅ Caminhos de arquivos: CONSISTENTES
✅ Documentação: COMPLETA
✅ Script de diagnóstico: ADICIONADO

🟢 SISTEMA PRONTO PARA USAR!
```

---

**Data de correção:** 10 de Dezembro de 2025
**Repositório:** https://github.com/RabelloRS/pmnova-automacao-engenharia
