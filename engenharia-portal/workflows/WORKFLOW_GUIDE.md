# 🚀 Workflow n8n - Gerador de Peças Técnicas

## 📋 O Que É Este Workflow?

Este é um workflow completo do **n8n** que:

1. ✅ Recebe dados do Streamlit via Webhook
2. ✅ Chama a IA (GPT-4) para gerar texto técnico profissional
3. ✅ Executa script Python para criar arquivo .docx
4. ✅ Retorna o resultado ao Streamlit para download

**Fluxo Visual:**
```
Streamlit (POST) 
    ↓
Webhook (n8n)
    ↓
IA/GPT-4 (Gera texto)
    ↓
Python Script (Cria .docx)
    ↓
Formata JSON
    ↓
Responde Streamlit ✅
```

---

## 📥 Como Importar no n8n

### Passo 1: Preparar o Arquivo JSON

O arquivo `gerador-pecas-tecnicas.json` já está pronto em:
```
engenharia-portal/workflows/gerador-pecas-tecnicas.json
```

### Passo 2: Abrir n8n

1. Acesse: **http://localhost:5678**
2. Faça login (admin / engenharia2025)

### Passo 3: Importar o Workflow

**Opção A (Recomendada - Colar JSON):**

1. Clique em **"+"** (New Workflow)
2. Pressione **Ctrl + V** (Windows/Linux) ou **Cmd + V** (Mac)
3. Cole o conteúdo do arquivo `gerador-pecas-tecnicas.json`
4. Os nodes aparecerão automaticamente na tela

**Opção B (Upload de Arquivo):**

1. Clique em **"+"** (New Workflow)
2. Clique em **"..."** (Menu) → **"Import from file"**
3. Selecione o arquivo `gerador-pecas-tecnicas.json`

---

## 🔑 Configurar Credenciais da OpenAI

### Passo 1: Obter API Key da OpenAI

1. Acesse: https://platform.openai.com/api-keys
2. Clique em **"Create new secret key"**
3. Copie a chave (começa com `sk-`)

### Passo 2: Adicionar Credencial no n8n

1. No workflow importado, clique no node **"IA (Escreve Texto Técnico)"**
2. Na aba **Credential**, clique em **"Create New"**
3. Cole sua **API Key**
4. Clique em **"Save"**

### Passo 3: Testar Credencial

1. Clique no botão **"Test"** para validar a conexão
2. Se verde (✓), está funcionando!

---

## 📊 Detalhes dos Nodes

### 1️⃣ **Webhook (Recebe Pedido)**
- **Tipo:** Webhook
- **Path:** `gerar-etp`
- **Método:** POST
- **Função:** Aguarda requisição do Streamlit

**Dados esperados:**
```json
{
  "tipo_peca": "etp",
  "objeto": "Pavimentação asfáltica",
  "justificativa": "Melhoria da infraestrutura",
  "valor_estimado": "R$ 500.000,00"
}
```

---

### 2️⃣ **IA (Escreve Texto Técnico)**
- **Tipo:** OpenAI (GPT-4)
- **Função:** Gera texto técnico profissional

**System Prompt:**
- Persona: Engenheiro Civil Sênior na Prefeitura
- Lei de Licitações: Lei Federal nº 14.133/2021
- Estilo: Formal, impessoal, técnico
- Foco: Interesse público, economicidade, eficácia

**User Prompt Dinâmico:**
```
Com base nos dados abaixo, redija o texto completo para a seção de 
JUSTIFICATIVA E DESCRIÇÃO TÉCNICA para um documento do tipo [ETP/TR/MD].

Dados:
Objeto: [objeto do formulário]
Motivação: [justificativa]
Valor Estimado: [valor]
```

---

### 3️⃣ **Python (Gera .DOCX)**
- **Tipo:** Execute Command
- **Função:** Roda script Python para criar documento Word

**Comando:**
```bash
python3 /data/python_scripts/gerar_peca.py '{ "tipo": "etp", "dados": {...} }'
```

**O script:**
- Lê template em `/data/templates/template_etp.docx`
- Substitui placeholders: `{{OBJETO}}`, `{{TEXTO_IA}}`, etc.
- Salva resultado em `/data/output/ETP_*.docx`

---

### 4️⃣ **Formata Resposta JSON**
- **Tipo:** Code (JavaScript)
- **Função:** Processa saída do Python e formata resposta

**Output:**
```json
{
  "status": "success",
  "arquivo": "/data/output/ETP_documento_20241210.docx",
  "timestamp": "2024-12-10T10:00:00Z"
}
```

---

### 5️⃣ **Responde ao Streamlit**
- **Tipo:** Respond to Webhook
- **Função:** Envia resposta JSON de volta para o Streamlit

**Response:**
```json
{
  "status": "success",
  "arquivo": "/data/output/ETP_documento.docx",
  "timestamp": "2024-12-10T10:00:00Z"
}
```

---

## ✅ Checklist de Configuração

- [ ] Arquivo `gerador-pecas-tecnicas.json` existe em `/workflows/`?
- [ ] Docker-compose.yml tem volume `../python_scripts:/data/python_scripts:ro`?
- [ ] n8n está rodando (`http://localhost:5678`)?
- [ ] Workflow foi importado com sucesso?
- [ ] API Key da OpenAI foi adicionada na credencial?
- [ ] Credencial foi testada (verde ✓)?
- [ ] Template `template_etp.docx` existe em `/shared_files/templates/`?

---

## 🧪 Testar o Workflow

### Teste 1: Via n8n (Rápido)

1. No workflow, clique em **"Execute Workflow"**
2. O node Webhook fica em modo de espera (cinza)
3. Em outro terminal, execute:

```bash
curl -X POST http://localhost:5678/webhook/gerar-etp \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_peca": "etp",
    "objeto": "Pavimentação asfáltica da Rua Principal",
    "justificativa": "Melhoria da infraestrutura viária e segurança dos pedestres",
    "valor_estimado": "R$ 500.000,00"
  }'
```

4. Verifique o resultado na tela do n8n (histórico de execução)

### Teste 2: Via Streamlit (Integrado)

1. Acesse: **http://localhost:8501**
2. Clique em **"Gerador de ETP/TR"** no menu
3. Preencha o formulário
4. Clique em **"Gerar Documento"**
5. Aguarde (30-60 segundos)
6. Faça o download do arquivo gerado ✅

---

## 🐛 Troubleshooting

### Erro: "Credencial não encontrada"
```
✗ Solução: Configure a credencial OpenAI (veja Passo 2 acima)
```

### Erro: "Can't open file /data/python_scripts/gerar_peca.py"
```
✗ Solução: Adicione volume no docker-compose.yml:
   - ../python_scripts:/data/python_scripts:ro

✗ Depois: docker-compose up -d
```

### Erro: "Template não encontrado"
```
✗ Solução: Crie template_etp.docx em shared_files/templates/
```

### Erro: "OpenAI API Error"
```
✗ Solução: Verifique se API Key está correta e ativa
✗ Consulte: https://platform.openai.com/account/api-keys
```

### Workflow não recebe dados do Streamlit
```
✗ Solução: Verifique URL no Streamlit:
   N8N_WEBHOOK_URL=http://n8n:5678/webhook/gerar-etp

✗ Teste curl acima para validar conexão
```

---

## 🔄 Editar Workflow

Se precisar alterar o prompt de IA, sistema, ou lógica:

1. Clique no node desejado
2. Edite os parâmetros
3. Clique em **"Save"** (Ctrl + S)
4. Teste novamente

**Nó importante para customização:**
- **Node "IA":** Altere o "System Prompt" para mudar comportamento da IA

---

## 📈 Próximos Passos

Após o workflow estar funcionando:

1. **Criar variações:** Crie nodes adicionais para TR e MD
2. **Adicionar validações:** Use nodes Code para validar entrada
3. **Implementar retry:** Configure tentativas em caso de falha
4. **Adicionar logs:** Integre com sistema de logging
5. **Backup automático:** Configure backup de workflows

---

## 💾 Exportar Workflow

Para fazer backup ou compartilhar:

1. Clique em **"..."** (Menu do workflow)
2. Clique em **"Download"**
3. Arquivo `.json` será salvo localmente
4. Guarde em local seguro ou commit no Git

---

## 🔗 Referências

- 📚 [Documentação n8n - Webhooks](https://docs.n8n.io/nodes/n8n-nodes-base.webhook/)
- 📚 [Documentação n8n - OpenAI](https://docs.n8n.io/nodes/n8n-nodes-base.openai/)
- 📚 [Documentação n8n - Execute Command](https://docs.n8n.io/nodes/n8n-nodes-base.executeCommand/)
- 🔑 [Gerenciar API Keys - OpenAI](https://platform.openai.com/api-keys)

---

## 📝 Changelog

**v1.0.0 - 10/12/2025**
- ✅ Workflow inicial criado
- ✅ 5 nodes implementados
- ✅ Integração Streamlit ↔ n8n ↔ Python
- ✅ Suporte OpenAI/GPT-4

---

**Data:** 10 de Dezembro de 2025  
**Status:** ✅ Pronto para usar  
**Arquivo:** `gerador-pecas-tecnicas.json`

