# 📋 Checklist de Pré-Execução - Portal de Engenharia

## ✅ Correções Aplicadas

### 1. Padronização de Caminhos (/data)
- ✅ docker-compose.yml (Portal): Volumes atualizados para `/data`
- ✅ app.py (Streamlit): OUTPUT_DIR alterado para `/data/output`
- ✅ python_scripts/gerar_peca.py: Já utiliza `/data` (compatível)

### 2. Mapeamento de Volumes Completo
```yaml
# n8n:
  - ./n8n_data:/home/node/.n8n
  - ./shared_files:/data
  - ../python_scripts:/data/python_scripts:ro

# streamlit:
  - ./shared_files:/data
```

---

## 🚀 Pré-requisitos Antes de Executar

### ✓ Passo 1: Templates .docx
**Criação de um template mínimo:**

1. Abra **Microsoft Word** ou **LibreOffice Writer**
2. Crie um novo documento
3. Digite o seguinte conteúdo:

```
ESTUDO TÉCNICO PRELIMINAR

OBJETO:
{{OBJETO}}

JUSTIFICATIVA:
{{JUSTIFICATIVA}}

VALOR ESTIMADO:
{{VALOR_ESTIMADO}}

RESPONSÁVEL TÉCNICO:
{{RESPONSAVEL}}

DATA:
{{DATA_ATUAL}}

DESCRIÇÃO TÉCNICA:
{{TEXTO_IA}}
```

4. Salve como `template_etp.docx` em:
   ```
   engenharia-portal/shared_files/templates/template_etp.docx
   ```

5. Repita para `template_tr.docx` e `template_md.docx` (opcionalmente)

### ✓ Passo 2: Permissões de Execução
```bash
cd /root/pmnova/engenharia-portal

# Tornar scripts executáveis
chmod +x start-portal.sh
chmod +x stop-portal.sh
chmod +x setup-port-forwarding.ps1
```

### ✓ Passo 3: Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar se necessário (credenciais n8n)
nano .env
```

---

## 🎯 Configuração do n8n Workflow

**Após iniciar o Portal**, siga estes passos:

### 1. Acessar n8n
- URL: `http://localhost:5678`
- Credenciais: `admin` / `engenharia2025`

### 2. Criar Novo Workflow
1. Clique em `+ Workflow`
2. Nomeie como: "Gerador de Peças Técnicas"
3. Adicione um **Webhook Node**:
   - **Path:** `gerar-etp`
   - **Method:** POST

### 3. Conectar Nodes (Sequência)
```
Webhook → Set Variables → HTTP Request → Code → Execute Command → Respond to Webhook
```

### 4. Configuração de cada Node:

#### Node: Webhook
- Method: `POST`
- Path: `gerar-etp`

#### Node: Set (Preparar Dados)
- **Variável:** `payload`
- **Valor:** `{{ $json.body }}`

#### Node: HTTP Request (Chamar IA)
- **Method:** POST
- **URL:** `https://api.openai.com/v1/chat/completions`
- **Headers:** 
  - `Authorization: Bearer {{ $env.OPENAI_API_KEY }}`
  - `Content-Type: application/json`
- **Body (JSON):**
```json
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "Você é um engenheiro civil especialista."
    },
    {
      "role": "user",
      "content": "Redija um texto técnico para ETP com os dados:\nObjeto: {{ $json.body.objeto }}\nJustificativa: {{ $json.body.justificativa }}"
    }
  ],
  "temperature": 0.7
}
```

#### Node: Code (Processar Resposta)
```javascript
const textoIA = $input.item.json.choices[0].message.content;

return {
  texto_ia: textoIA,
  objeto: $input.item.json.body.objeto,
  justificativa: $input.item.json.body.justificativa,
  valor_estimado: $input.item.json.body.valor_estimado,
  responsavel: $input.item.json.body.responsavel
};
```

#### Node: Execute Command
- **Command:**
```bash
python3 /data/python_scripts/gerar_peca.py '{"tipo": "etp", "dados": {"OBJETO": "{{ $json.objeto }}", "JUSTIFICATIVA": "{{ $json.justificativa }}", "VALOR_ESTIMADO": "{{ $json.valor_estimado }}", "RESPONSAVEL": "{{ $json.responsavel }}", "TEXTO_IA": "{{ $json.texto_ia }}", "objeto_resumido": "documento"}}'
```

#### Node: Respond to Webhook
- **Response Body:**
```json
{
  "status": "success",
  "mensagem": "Documento gerado com sucesso!",
  "arquivo": "ETP_documento_timestamp.docx"
}
```

---

## 🧪 Teste Rápido (Curl)

Após configurar o webhook, teste com:

```bash
curl -X POST http://localhost:5678/webhook/gerar-etp \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_peca": "etp",
    "objeto": "Pavimentação asfáltica",
    "justificativa": "Melhoria da infraestrutura",
    "valor_estimado": "R$ 500.000,00",
    "responsavel": "João Silva"
  }'
```

---

## 🚀 Iniciar o Sistema

```bash
cd /root/pmnova/engenharia-portal

# Iniciar (cria imagens, containers e aplica volumes)
bash start-portal.sh

# Aguardar ~30 segundos para tudo subir
```

### Verificar Status:
```bash
docker-compose ps
```

### Acessar:
- **Streamlit:** http://localhost:8501
- **n8n:** http://localhost:5678

---

## 🌐 Acesso na Rede Local (WSL 2)

No **PowerShell do Windows (Admin)**:
```powershell
cd \path\to\engenharia-portal
.\setup-port-forwarding.ps1
```

Depois acesse de outro computador:
- `http://SEU_IP_WINDOWS:8501`
- `http://SEU_IP_WINDOWS:5678`

---

## 🐛 Troubleshooting

### Erro: "Template não encontrado"
```
✗ Solução: Crie template_etp.docx em shared_files/templates/
```

### Erro: "Arquivo não encontrado para download"
```
✗ Solução: Verifique permissões: chmod -R 777 shared_files/
```

### Erro: "Não consegue conectar ao n8n"
```bash
# Reiniciar serviço
docker-compose restart n8n

# Ver logs
docker-compose logs -f n8n
```

### Container do Streamlit não sobe
```bash
# Forçar rebuild
docker-compose up -d --build streamlit

# Ver logs
docker-compose logs -f streamlit
```

---

## 📊 Estrutura de Pastas Final

```
engenharia-portal/
├── shared_files/
│   ├── templates/
│   │   ├── template_etp.docx       ← Criar isto
│   │   ├── template_tr.docx        ← Opcionalmente
│   │   └── template_md.docx        ← Opcionalmente
│   └── output/
│       └── (arquivos gerados)
│
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
└── docker-compose.yml              ← JÁ ATUALIZADO
```

---

## ✅ Checklist Final

- [ ] Templates criados em `shared_files/templates/`
- [ ] Permissões de execução adicionadas aos scripts
- [ ] Variáveis de ambiente configuradas (`.env`)
- [ ] Docker instalado e rodando
- [ ] Executou `bash start-portal.sh`
- [ ] Streamlit acessível em `http://localhost:8501`
- [ ] n8n acessível em `http://localhost:5678`
- [ ] Workflow criado no n8n com webhook `/gerar-etp`
- [ ] Teste com curl retornou sucesso
- [ ] Arquivo gerado disponível em `shared_files/output/`

---

**Após completar este checklist, o sistema estará 100% operacional!** 🚀

