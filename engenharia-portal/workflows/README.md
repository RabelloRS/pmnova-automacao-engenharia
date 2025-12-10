# 📁 Workflows do n8n

Esta pasta armazena os fluxos (workflows) prontos para importar no n8n.

## 🚀 Workflows Disponíveis

### 1. **gerador-pecas-tecnicas.json** ⭐ (PRONTO PARA USAR)
   - Gera: ETP, TR e MD automaticamente
   - Integra: Streamlit → n8n → IA (GPT-4) → Python → Word
   - Status: ✅ Testado e pronto para produção

   **Como usar:**
   ```
   1. Abra http://localhost:5678 (n8n)
   2. Clique em "+ New Workflow"
   3. Pressione Ctrl + V
   4. Cole o conteúdo de gerador-pecas-tecnicas.json
   5. Configure credencial OpenAI
   6. Salve e execute
   ```

   Veja **WORKFLOW_GUIDE.md** para instruções detalhadas.

---

## 📖 Documentação

- **[WORKFLOW_GUIDE.md](./WORKFLOW_GUIDE.md)** - Guia completo de importação e configuração
- **[gerador-pecas-tecnicas.json](./gerador-pecas-tecnicas.json)** - Workflow JSON pronto

---

## 💾 Como Fazer Backup de um Workflow

1. No n8n, abra o workflow desejado
2. Clique em **"..."** (Menu)
3. Clique em **"Download"**
4. Salve o arquivo `.json` nesta pasta
5. Faça commit no Git para versionamento

---

## 📤 Como Importar um Workflow

**Opção 1 - Colar JSON (Rápido):**
```
1. n8n → "+ New Workflow"
2. Ctrl + V (colar JSON)
3. Nodes aparecem automaticamente
```

**Opção 2 - Upload de Arquivo:**
```
1. n8n → "+ New Workflow"
2. "..." → "Import from file"
3. Selecione .json
```

---

## 🔧 Checklist Antes de Usar

- [ ] Docker Compose com volumes corretos?
- [ ] `../python_scripts:/data/python_scripts:ro` mapeado?
- [ ] Templates .docx criados em `/shared_files/templates/`?
- [ ] API Key OpenAI configurada?
- [ ] Credencial testada no n8n?

---

## 🎯 Próximos Workflows (Roadmap)

- [ ] Importador de documentos (OCR)
- [ ] Geoprocessamento (análise de áreas)
- [ ] Cálculos de pavimentação automática
- [ ] Integração com sistema de protocolo
- [ ] Dashboard de indicadores

---

## 📊 Estrutura de um Workflow

```
Webhook → IA (GPT-4) → Python Script → Formata JSON → Responde
   ↓           ↓           ↓              ↓              ↓
Recebe    Gera Texto   Cria .docx    Processa      Retorna ao
Streamlit  Técnico      com Template  Resultado     Streamlit
```

---

## 🚀 Começar Agora

1. Leia: **WORKFLOW_GUIDE.md**
2. Importe: **gerador-pecas-tecnicas.json**
3. Configure: API Key OpenAI
4. Teste: Acesse Streamlit e gere um documento

---

**Última atualização:** 10/12/2025  
**Status:** ✅ Workflows prontos para produção
