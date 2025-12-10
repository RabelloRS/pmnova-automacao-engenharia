# ⚡ 5 PASSOS PARA COMEÇAR COM O WORKFLOW

## Seu sistema está **95% pronto**. Faltam apenas estas 5 ações:

---

## ✅ PASSO 1: Verificar Volumes (2 minutos)

Certifique-se de que seu `docker-compose.yml` tem:

```yaml
services:
  n8n:
    volumes:
      - ./n8n_data:/home/node/.n8n
      - ./shared_files:/data
      - ../python_scripts:/data/python_scripts:ro  ← IMPORTANTE!
```

**Se não tiver, adicione e reinicie:**
```bash
docker-compose down
docker-compose up -d
```

---

## ✅ PASSO 2: Obter API Key OpenAI (3 minutos)

1. Acesse: https://platform.openai.com/api-keys
2. Faça login com sua conta OpenAI
3. Clique em **"Create new secret key"**
4. Copie a chave (começa com `sk-`)
5. Guarde em local seguro

---

## ✅ PASSO 3: Importar Workflow no n8n (2 minutos)

1. Abra: **http://localhost:5678**
2. Faça login (admin / engenharia2025)
3. Clique em **"+"** (New Workflow)
4. Pressione **Ctrl + V** (ou **Cmd + V** no Mac)
5. Abra o arquivo: `engenharia-portal/workflows/gerador-pecas-tecnicas.json`
6. Copie todo o conteúdo
7. Cole na tela do n8n (Ctrl + V)
8. Os 5 nodes aparecerão automaticamente ✨

---

## ✅ PASSO 4: Configurar Credencial OpenAI (2 minutos)

1. No workflow importado, clique no node **"IA (Escreve Texto Técnico)"**
2. Na seção **Credential**, clique em **"Create New"**
3. Cole sua **API Key da OpenAI** (da Passo 2)
4. Clique em **"Save"**
5. Clique em **"Test"** para validar
6. Se aparecer verde (✓), sucesso! ✅

---

## ✅ PASSO 5: Testar (2 minutos)

### Teste via cURL:

```bash
curl -X POST http://localhost:5678/webhook/gerar-etp \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_peca": "etp",
    "objeto": "Pavimentação asfáltica da Rua Principal",
    "justificativa": "Melhoria da infraestrutura viária do município",
    "valor_estimado": "R$ 500.000,00"
  }'
```

**Se retornar sucesso:**
```json
{
  "status": "success",
  "arquivo": "/data/output/ETP_Pavimentação_asfáltica_20241210.docx",
  "timestamp": "2024-12-10T10:00:00Z"
}
```

### Teste via Streamlit:

1. Acesse: **http://localhost:8501**
2. Clique em **"Gerador de ETP/TR"**
3. Preencha o formulário
4. Clique em **"Gerar Documento"**
5. Aguarde (30-60 segundos)
6. Download do arquivo ✅

---

## 🎯 Fluxo Completo

```
Usuário preenche formulário no Streamlit
            ↓
POST para n8n (http://n8n:5678/webhook/gerar-etp)
            ↓
GPT-4 gera texto técnico baseado no prompt
            ↓
Script Python lê template_etp.docx
            ↓
Substitui placeholders pelo texto gerado
            ↓
Salva arquivo em /data/output/
            ↓
Streamlit oferece download ✅
```

---

## 📋 Checklist Final

- [ ] Volumes no docker-compose.yml corretos?
- [ ] API Key OpenAI obtida?
- [ ] Workflow importado no n8n?
- [ ] Credencial configurada e testada (verde ✓)?
- [ ] Teste com cURL retornou sucesso?
- [ ] Teste via Streamlit funcionou?

✅ **Se todas as caixas estão marcadas, PARABÉNS! Sistema 100% operacional!**

---

## 🆘 Algo Deu Errado?

### "AttributeError: 'NoneType' object..."
```
→ Solução: Verificar se template_etp.docx existe em shared_files/templates/
```

### "python3: can't open file /data/python_scripts/gerar_peca.py"
```
→ Solução: Adicionar volume em docker-compose.yml
   - ../python_scripts:/data/python_scripts:ro
```

### "401 Unauthorized (OpenAI)"
```
→ Solução: API Key expirada ou inválida
→ Gerar nova em: https://platform.openai.com/api-keys
```

### "Connection refused to n8n"
```
→ Solução: n8n não está rodando
   docker-compose logs -f n8n
   docker-compose restart n8n
```

---

## 🚀 Depois de Pronto

Você pode:

1. **Customizar o prompt** de IA (edite no node "IA")
2. **Adicionar mais templates** (TR, MD)
3. **Implementar validações** (adicione nodes Code)
4. **Configurar alertas** (email, Slack)
5. **Fazer backup** (download do workflow JSON)

---

**Tempo Total: ~11 minutos ⏱️**

**Resultado: Sistema completo funcionando! 🎉**

---

Próximo: Leia **WORKFLOW_GUIDE.md** para detalhes técnicos.
