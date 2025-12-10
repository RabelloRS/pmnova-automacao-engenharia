# 🚀 GUIA RÁPIDO - Portal de Engenharia

## ⚡ Começar Agora (5 minutos)

```bash
# 1. Ir para a pasta do Portal
cd /root/pmnova/engenharia-portal

# 2. Diagnosticar problemas (opcional)
bash diagnose.sh

# 3. Iniciar sistema
bash start-portal.sh

# Aguarde 20-30 segundos...
```

## 🌐 Acessar

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **Streamlit** | http://localhost:8501 | Sem login |
| **n8n** | http://localhost:5678 | admin / engenharia2025 |

---

## 📋 Se Algo Não Funcionar

### Erro 1: "Template não encontrado"
```bash
# Abra Word e crie:
# File: engenharia-portal/shared_files/templates/template_etp.docx
# Content:
# OBJETO: {{OBJETO}}
# JUSTIFICATIVA: {{JUSTIFICATIVA}}
```

### Erro 2: "Arquivo não encontrado para download"
```bash
chmod -R 777 /root/pmnova/engenharia-portal/shared_files/
```

### Erro 3: "Não consegue conectar ao n8n"
```bash
docker-compose logs -f n8n
docker-compose restart n8n
```

---

## 📖 Documentação Completa

| Documento | Propósito |
|-----------|----------|
| **SETUP_CHECKLIST.md** | Guia passo-a-passo detalhado |
| **CORRECOES_APLICADAS.md** | O que foi corrigido |
| **AUDITORIA_CONCLUIDA.md** | Resumo e status final |
| **diagnose.sh** | Script de diagnóstico |

---

## 🔧 Configurar Workflow no n8n (Importante!)

1. Acesse http://localhost:5678
2. Crie novo workflow
3. Adicione nodes:
   - **Webhook** (Path: `gerar-etp`)
   - **Set** (Preparar dados)
   - **HTTP** (Chamar IA)
   - **Code** (Processar)
   - **Execute Command** (Rodar Python)
   - **Respond** (Retornar resultado)

Veja **SETUP_CHECKLIST.md** para configuração completa de cada node.

---

## 🧪 Testar Integração

```bash
curl -X POST http://localhost:5678/webhook/gerar-etp \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_peca": "etp",
    "objeto": "Pavimentação",
    "justificativa": "Infraestrutura viária",
    "valor_estimado": "R$ 500.000,00",
    "responsavel": "João Silva"
  }'
```

---

## 📦 Estrutura de Volumes (Corrigida)

```
/data (interior dos containers)
├── templates/          ← Seus templates .docx
│   ├── template_etp.docx
│   ├── template_tr.docx
│   └── template_md.docx
│
├── output/             ← Arquivos gerados
│   └── ETP_*.docx
│
└── python_scripts/     ← Scripts (read-only)
    ├── gerar_peca.py
    └── requirements.txt
```

---

## 🎯 Fluxo de Uso

```
1. Streamlit (http://localhost:8501)
   ↓
2. Clica em "Gerador de ETP/TR"
   ↓
3. Preenche formulário
   ↓
4. Clica "Gerar Documento"
   ↓
5. n8n processa via webhook
   ↓
6. IA gera texto técnico
   ↓
7. Script Python cria .docx
   ↓
8. Arquivo salvo em /data/output
   ↓
9. Streamlit oferece download
   ↓
10. User faz download ✅
```

---

## 📊 Verificar Status

```bash
# Ver containers rodando
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Logs de um serviço específico
docker-compose logs -f streamlit
docker-compose logs -f n8n

# Testar conectividade
curl http://localhost:8501
curl http://localhost:5678
```

---

## 🛑 Parar Sistema

```bash
bash stop-portal.sh

# Ou manualmente:
docker-compose down
```

---

## 🌐 Acessar de Outros Computadores (WSL 2)

No **PowerShell do Windows (Admin)**:
```powershell
cd \path\to\engenharia-portal
.\setup-port-forwarding.ps1
```

Depois acesse:
- `http://SEU_IP_WINDOWS:8501`
- `http://SEU_IP_WINDOWS:5678`

---

## 💡 Dicas

✅ Use `diagnose.sh` antes de rodar  
✅ Sempre crie templates antes de usar  
✅ Configure .env com suas API keys  
✅ Leia SETUP_CHECKLIST.md para detalhes  
✅ Verifique logs se algo não funcionar  

---

## 🔗 Links Úteis

- 📍 Repositório: https://github.com/RabelloRS/pmnova-automacao-engenharia
- 📚 Documentação n8n: https://docs.n8n.io/
- 📚 Documentação Streamlit: https://docs.streamlit.io/

---

**Data:** 10/12/2025  
**Status:** ✅ PRONTO PARA USAR  
**Próximo:** Execute `bash start-portal.sh` 🚀
