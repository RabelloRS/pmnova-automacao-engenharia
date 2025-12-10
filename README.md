# 🏗️ PMNova - Sistema de Automação para Engenharia Civil Pública

Sistema de automação Low-Code usando **n8n** para processos de engenharia civil em ambiente de Prefeitura Municipal, com capacidade de expansão para scripts complexos de Python (Geoprocessamento, Cálculos de Pavimentação, etc.).

## 📋 Visão Geral

Este projeto utiliza **n8n** (via Docker) como plataforma de automação visual, integrando:
- ✅ Geração automática de peças técnicas (ETP, TR, MD) com IA
- ✅ Scripts Python para cálculos de engenharia
- ✅ Integração com APIs (OpenAI, Ollama, etc.)
- ✅ Manipulação de documentos .docx
- ✅ Arquitetura modular e escalável

---

## 📁 Estrutura de Diretórios

```
pmnova/
├── docker-compose.yml          # Configuração do n8n via Docker
├── .env.example                # Variáveis de ambiente (copie para .env)
├── .gitignore                  # Arquivos ignorados pelo Git
│
├── docker/                     # Configurações adicionais do Docker (futuro)
│
├── workflows/                  # Backups JSON dos fluxos do n8n
│   └── README.md               # Documentação dos workflows
│
├── python_scripts/             # Scripts Python para automações
│   ├── requirements.txt        # Dependências Python
│   ├── setup_python.sh         # Script de configuração do venv
│   ├── gerar_peca.py           # Script exemplo de geração de peças
│   └── venv/                   # Ambiente virtual (criado após setup)
│
├── templates/                  # Templates .docx para documentos
│   ├── template_etp.docx       # Template de Estudo Técnico Preliminar
│   ├── template_tr.docx        # Template de Termo de Referência
│   └── template_md.docx        # Template de Memorial Descritivo
│
└── output/                     # Arquivos gerados pelas automações
    └── .gitkeep
```

---

## 🚀 Instalação e Configuração

### 1️⃣ Pré-requisitos

No seu ambiente WSL 2 (Ubuntu 24), certifique-se de ter instalado:

```bash
# Docker
sudo apt update
sudo apt install -y docker.io docker-compose

# Iniciar Docker
sudo systemctl start docker
sudo systemctl enable docker

# Adicionar seu usuário ao grupo docker (para evitar usar sudo)
sudo usermod -aG docker $USER
# Faça logout e login novamente para aplicar
```

### 2️⃣ Configurar Variáveis de Ambiente

```bash
# Copiar o arquivo de exemplo
cp .env.example .env

# Editar com suas configurações
nano .env
```

**Importante:** Altere a senha do n8n e adicione suas API Keys (OpenAI, etc.).

### 3️⃣ Subir o n8n com Docker Compose

```bash
# Subir o container
docker-compose up -d

# Verificar logs
docker-compose logs -f n8n

# Verificar status
docker-compose ps
```

Acesse o n8n em: **http://localhost:5678**

Credenciais padrão (altere no `.env`):
- **Usuário:** admin
- **Senha:** admin123

### 4️⃣ Configurar Ambiente Python

```bash
# Entrar na pasta de scripts
cd python_scripts

# Executar script de configuração
bash setup_python.sh

# Ou manualmente:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5️⃣ Criar Templates .docx

Crie os arquivos de template na pasta `templates/`:

**Exemplo de `template_etp.docx`:**
- Use placeholders: `{{OBJETO}}`, `{{JUSTIFICATIVA}}`, `{{VALOR_ESTIMADO}}`, `{{TEXTO_IA}}`, `{{DATA_ATUAL}}`, etc.
- O script Python substituirá automaticamente esses marcadores

---

## 🎯 Módulo 1: Gerador de Peças Técnicas (ETP, TR, MD)

### Lógica do Fluxo no n8n

#### **Workflow: "Gerador de Peças Técnicas IA"**

```
┌─────────────────┐
│  1. Webhook     │  Recebe dados do formulário
│  (POST)         │  - objeto
└────────┬────────┘  - justificativa
         │           - valor
         │           - tipo_peca (etp/tr/md)
         ▼
┌─────────────────┐
│  2. Set         │  Prepara dados e monta prompt
│  (Variables)    │  
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. HTTP        │  Chama API de LLM
│  Request        │  - OpenAI GPT-4
└────────┬────────┘  ou Ollama (local)
         │
         ▼
┌─────────────────┐
│  4. Code        │  Processa resposta da IA
│  (JavaScript)   │  Extrai texto gerado
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. Execute     │  Executa script Python
│  Command        │  python3 /data/python_scripts/gerar_peca.py
└────────┬────────┘  Gera .docx na pasta /data/output
         │
         ▼
┌─────────────────┐
│  6. Respond     │  Retorna sucesso + link do arquivo
│  to Webhook     │
└─────────────────┘
```

### Implementação Detalhada dos Nodes

#### **Node 1: Webhook**
- **Tipo:** Webhook
- **Path:** `gerar-peca-tecnica`
- **Método:** POST
- **Dados esperados (JSON):**
```json
{
  "tipo_peca": "etp",
  "objeto": "Contratação de empresa para pavimentação asfáltica",
  "justificativa": "Melhoria da infraestrutura viária do município",
  "valor_estimado": "R$ 500.000,00",
  "setor": "Secretaria de Obras",
  "responsavel": "João Silva"
}
```

#### **Node 2: Set (Preparação de Dados)**
- **Tipo:** Set
- **Variáveis:**
  - `objeto` → `{{ $json.body.objeto }}`
  - `justificativa` → `{{ $json.body.justificativa }}`
  - `valor` → `{{ $json.body.valor_estimado }}`
  - `tipo_peca` → `{{ $json.body.tipo_peca }}`
  - `prompt_ia` → Template do prompt:

```
Você é um engenheiro civil especialista em licitações públicas.

Redija um texto técnico profissional para um {{tipo_peca.toUpperCase()}} (Estudo Técnico Preliminar) com as seguintes informações:

OBJETO: {{objeto}}
JUSTIFICATIVA: {{justificativa}}
VALOR ESTIMADO: {{valor}}

O texto deve conter:
1. Descrição detalhada do objeto
2. Justificativa técnica fundamentada
3. Estimativa de custos e cronograma
4. Referências normativas (NBR, legislação)

Use linguagem técnica, objetiva e formal.
```

#### **Node 3: HTTP Request (Chamada à API de IA)**

**Opção A - OpenAI:**
```
Method: POST
URL: https://api.openai.com/v1/chat/completions
Authentication: Header Auth
  - Name: Authorization
  - Value: Bearer {{$env.OPENAI_API_KEY}}

Body (JSON):
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "Você é um engenheiro civil especialista."
    },
    {
      "role": "user",
      "content": "{{$json.prompt_ia}}"
    }
  ],
  "temperature": 0.7
}
```

**Opção B - Ollama (Local):**
```
Method: POST
URL: http://host.docker.internal:11434/api/generate
Body (JSON):
{
  "model": "llama2",
  "prompt": "{{$json.prompt_ia}}",
  "stream": false
}
```

#### **Node 4: Code (Processar Resposta)**
- **Tipo:** Code (JavaScript)
- **Código:**
```javascript
// Para OpenAI
const textoIA = $input.item.json.choices[0].message.content;

// Para Ollama
// const textoIA = $input.item.json.response;

return {
  texto_ia: textoIA,
  objeto: $input.item.json.objeto,
  justificativa: $input.item.json.justificativa,
  valor: $input.item.json.valor,
  tipo_peca: $input.item.json.tipo_peca
};
```

#### **Node 5: Execute Command (Gerar Documento)**
- **Tipo:** Execute Command
- **Comando:**
```bash
python3 /data/python_scripts/gerar_peca.py '{"tipo": "{{$json.tipo_peca}}", "dados": {"OBJETO": "{{$json.objeto}}", "JUSTIFICATIVA": "{{$json.justificativa}}", "VALOR_ESTIMADO": "{{$json.valor}}", "TEXTO_IA": "{{$json.texto_ia}}", "objeto_resumido": "{{$json.objeto.slice(0,30)}}"}}'
```

#### **Node 6: Respond to Webhook**
- **Tipo:** Respond to Webhook
- **Resposta:**
```json
{
  "status": "success",
  "mensagem": "Peça técnica gerada com sucesso!",
  "tipo": "{{$json.tipo_peca.toUpperCase()}}",
  "arquivo": "{{$json.arquivo}}",
  "timestamp": "{{$now}}"
}
```

---

## 🐍 Scripts Python

### `gerar_peca.py`

Script principal que:
1. Recebe parâmetros via JSON (tipo de peça + dados)
2. Carrega o template .docx correspondente
3. Substitui os placeholders `{{VARIAVEL}}` pelos valores reais
4. Salva o arquivo na pasta `/data/output`

**Uso no terminal (para testes):**
```bash
cd python_scripts
source venv/bin/activate

python gerar_peca.py '{
  "tipo": "etp",
  "dados": {
    "OBJETO": "Contratação de serviços",
    "JUSTIFICATIVA": "Necessidade do serviço",
    "VALOR_ESTIMADO": "R$ 100.000,00",
    "TEXTO_IA": "Texto gerado pela IA aqui...",
    "objeto_resumido": "contratacao_servicos"
  }
}'
```

---

## 🧪 Testando o Fluxo

### 1. Via cURL:
```bash
curl -X POST http://localhost:5678/webhook/gerar-peca-tecnica \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_peca": "etp",
    "objeto": "Pavimentação da Rua Principal",
    "justificativa": "Melhoria da infraestrutura viária",
    "valor_estimado": "R$ 500.000,00",
    "setor": "Secretaria de Obras",
    "responsavel": "João Silva"
  }'
```

### 2. Via Interface do n8n:
- Clique em "Execute Workflow"
- Preencha os dados no node Webhook
- Acompanhe a execução passo a passo

---

## 📦 Volumes Mapeados

O `docker-compose.yml` mapeia as seguintes pastas:

| Pasta Local | Pasta no Container | Permissão |
|-------------|-------------------|-----------|
| `./python_scripts` | `/data/python_scripts` | Read/Write |
| `./templates` | `/data/templates` | Read Only |
| `./output` | `/data/output` | Read/Write |
| `./workflows` | `/data/workflows` | Read/Write |

Isso permite que:
- O n8n execute scripts Python locais
- Leia templates da pasta local
- Salve arquivos gerados localmente
- Você edite os arquivos sem recriar o container

---

## 🔧 Comandos Úteis

```bash
# Iniciar n8n
docker-compose up -d

# Parar n8n
docker-compose down

# Ver logs
docker-compose logs -f n8n

# Reiniciar n8n
docker-compose restart n8n

# Acessar shell do container
docker exec -it pmnova-n8n /bin/sh

# Backup de workflows (exportar do n8n via interface)
# Salvar na pasta: ./workflows/

# Restaurar workflow (importar no n8n via interface)
```

---

## 🔐 Segurança

⚠️ **Importante em Produção:**

1. **Altere as credenciais padrão** no arquivo `.env`
2. **Use HTTPS** configurando um proxy reverso (Nginx/Caddy)
3. **Restrinja acesso** ao n8n via firewall
4. **Não commite** o arquivo `.env` no Git
5. **Configure backups** automáticos dos workflows

---

## 🚀 Próximos Módulos (Roadmap)

- [ ] **Módulo 2:** Cálculos de Pavimentação Asfáltica
- [ ] **Módulo 3:** Geoprocessamento (análise de áreas, mapas)
- [ ] **Módulo 4:** Integração com sistema de protocolo
- [ ] **Módulo 5:** Dashboard de indicadores
- [ ] **Módulo 6:** OCR e processamento de documentos escaneados

---

## 📚 Recursos Adicionais

- [Documentação oficial do n8n](https://docs.n8n.io/)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Ollama Documentation](https://ollama.ai/docs)

---

## 📝 Licença

Projeto interno da Prefeitura Municipal.

---

## 👨‍💻 Suporte

Para dúvidas ou problemas, consulte a equipe de TI ou Engenharia.

---

**Desenvolvido para otimizar processos de engenharia civil pública** 🏗️
