# 🏗️ Portal de Automação de Engenharia - PM Nova Petrópolis

Sistema completo de automação de processos de engenharia civil usando **n8n** (backend) e **Streamlit** (frontend) via Docker Compose.

## 📁 Estrutura do Projeto

```
engenharia-portal/
├── docker-compose.yml          # Orquestração dos serviços
├── .env.example                # Variáveis de ambiente
│
├── n8n_data/                   # Persistência do n8n (workflows, execuções)
│
├── shared_files/               # Pasta compartilhada entre n8n e Streamlit (/data)
│   ├── templates/              # Templates .docx para ETP, TR, MD
│   └── output/                 # Documentos gerados
│
└── frontend/                   # Aplicação Streamlit
    ├── app.py                  # Interface web
    ├── Dockerfile              # Imagem do Streamlit
    └── requirements.txt        # Dependências Python
```

### 📌 Padronização de Caminhos

**Importante:** Todos os serviços usam `/data` para arquivos compartilhados:
- **n8n:** Monta em `/data` via `./shared_files:/data`
- **Streamlit:** Monta em `/data` via `./shared_files:/data`
- **Scripts Python:** Buscam arquivos em `/data/templates` e `/data/output`

Esta padronização evita conflitos de caminhos entre os containers.

---

## 🚀 Instalação e Execução

### 1. No WSL 2 (Ubuntu)

```bash
cd /root/pmnova/engenharia-portal

# Iniciar os serviços
bash start-portal.sh

# Ou manualmente:
docker-compose up -d --build

# Verificar status
docker-compose ps

# Ver logs
docker-compose logs -f
```

### 2. Acessar os Serviços

**Dentro do WSL:**
- **Streamlit (Frontend):** http://localhost:8501
- **n8n (Backend):** http://localhost:5678

**Credenciais do n8n:**
- Usuário: `admin`
- Senha: `engenharia2025`

### 3. Primeiros Passos

⚠️ **IMPORTANTE:** Antes de usar o sistema, siga o **[SETUP_CHECKLIST.md](./SETUP_CHECKLIST.md)**

Os passos incluem:
1. ✅ Criar templates .docx
2. ✅ Configurar permissões
3. ✅ Criar workflow no n8n
4. ✅ Testar integração

---

## 🌐 Expor para a Rede Local (Intranet da Prefeitura)

### ⚠️ Importante: Port Forwarding no Windows

Como você está usando WSL 2, o IP do WSL é diferente do IP do Windows. Para acessar de outros computadores da rede, é necessário fazer **port forwarding** das portas do WSL para o Windows.

### 🔍 Passo 1: Descobrir o IP do WSL

No terminal do WSL, execute:

```bash
hostname -I
```

Exemplo de resultado: `172.18.240.15` (anote este IP)

### 🔍 Passo 2: Descobrir o IP do Windows na Rede Local

No PowerShell do Windows, execute:

```powershell
ipconfig
```

Procure por **"Adaptador de Rede Ethernet"** ou **"Wi-Fi"** e anote o **IPv4** (ex: `192.168.1.100`)

### ⚙️ Passo 3: Configurar Port Forwarding

**Abra o PowerShell como Administrador** e execute os seguintes comandos:

```powershell
# Substituir 172.18.240.15 pelo IP do seu WSL (obtido no Passo 1)

# Port Forwarding para Streamlit (porta 8501)
netsh interface portproxy add v4tov4 listenport=8501 listenaddress=0.0.0.0 connectport=8501 connectaddress=172.18.240.15

# Port Forwarding para n8n (porta 5678)
netsh interface portproxy add v4tov4 listenport=5678 listenaddress=0.0.0.0 connectport=5678 connectaddress=172.18.240.15

# Verificar se foi criado
netsh interface portproxy show all
```

### 🔥 Passo 4: Liberar no Firewall do Windows

**No PowerShell (Admin)**, execute:

```powershell
# Liberar porta 8501 (Streamlit)
New-NetFirewallRule -DisplayName "WSL Streamlit" -Direction Inbound -LocalPort 8501 -Protocol TCP -Action Allow

# Liberar porta 5678 (n8n)
New-NetFirewallRule -DisplayName "WSL n8n" -Direction Inbound -LocalPort 5678 -Protocol TCP -Action Allow
```

### 🌐 Passo 5: Acessar de Outros Computadores

Agora, de qualquer computador na mesma rede local (intranet), acesse:

- **Streamlit:** `http://192.168.1.100:8501` (substitua pelo IP do Windows)
- **n8n:** `http://192.168.1.100:5678`

---

## 🗑️ Remover Port Forwarding (se necessário)

```powershell
# Remover regra da porta 8501
netsh interface portproxy delete v4tov4 listenport=8501 listenaddress=0.0.0.0

# Remover regra da porta 5678
netsh interface portproxy delete v4tov4 listenport=5678 listenaddress=0.0.0.0

# Verificar
netsh interface portproxy show all
```

---

## 📋 Script Automatizado de Port Forwarding

Crie um arquivo `setup-port-forwarding.ps1` no Windows:

```powershell
# setup-port-forwarding.ps1
# Execute como Administrador

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Port Forwarding WSL 2 - Sistema PMNP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obter IP do WSL automaticamente
$wslIP = (wsl hostname -I).Trim()

Write-Host "IP do WSL detectado: $wslIP" -ForegroundColor Green
Write-Host ""

# Adicionar port forwarding
Write-Host "Configurando port forwarding..." -ForegroundColor Yellow

netsh interface portproxy add v4tov4 listenport=8501 listenaddress=0.0.0.0 connectport=8501 connectaddress=$wslIP
netsh interface portproxy add v4tov4 listenport=5678 listenaddress=0.0.0.0 connectport=5678 connectaddress=$wslIP

Write-Host "✓ Port forwarding configurado!" -ForegroundColor Green
Write-Host ""

# Liberar firewall
Write-Host "Configurando firewall..." -ForegroundColor Yellow

New-NetFirewallRule -DisplayName "WSL Streamlit" -Direction Inbound -LocalPort 8501 -Protocol TCP -Action Allow -ErrorAction SilentlyContinue
New-NetFirewallRule -DisplayName "WSL n8n" -Direction Inbound -LocalPort 5678 -Protocol TCP -Action Allow -ErrorAction SilentlyContinue

Write-Host "✓ Firewall configurado!" -ForegroundColor Green
Write-Host ""

# Mostrar regras ativas
Write-Host "Regras de port forwarding ativas:" -ForegroundColor Cyan
netsh interface portproxy show all

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✓ Configuração concluída!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Acesse de outros computadores:" -ForegroundColor Yellow
Write-Host "  Streamlit: http://SEU_IP_WINDOWS:8501" -ForegroundColor White
Write-Host "  n8n:       http://SEU_IP_WINDOWS:5678" -ForegroundColor White
Write-Host ""
```

**Para executar:**

```powershell
# No PowerShell (Admin)
Set-ExecutionPolicy Bypass -Scope Process -Force
.\setup-port-forwarding.ps1
```

---

## 🔧 Comandos Úteis

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f streamlit
docker-compose logs -f n8n

# Reiniciar um serviço
docker-compose restart streamlit

# Reconstruir imagem do Streamlit (após alterar código)
docker-compose up -d --build streamlit

# Acessar shell do container
docker exec -it engenharia-streamlit /bin/bash
docker exec -it engenharia-n8n /bin/sh

# Verificar IP do WSL
hostname -I
```

---

## 🔐 Segurança

⚠️ **Em ambiente de produção:**

1. **Altere as credenciais padrão** do n8n
2. **Configure HTTPS** usando Nginx/Caddy como proxy reverso
3. **Restrinja o acesso** por IP no firewall
4. **Use VPN** se for acessar de fora da rede local
5. **Faça backups** regulares da pasta `n8n_data`

---

## 🎯 Como Usar o Sistema

### 1. Configurar Webhook no n8n

1. Acesse o n8n: http://localhost:5678
2. Crie um novo workflow
3. Adicione um node **Webhook** com:
   - **Path:** `gerar-etp`
   - **Method:** POST
4. Conecte os nodes seguintes conforme a documentação do projeto principal

### 2. Usar a Interface Streamlit

1. Acesse: http://localhost:8501
2. No menu lateral, selecione **"Gerador de ETP/TR"**
3. Preencha o formulário:
   - Tipo de peça (ETP/TR/MD)
   - Objeto da obra
   - Justificativa
   - Valor estimado
   - Responsável
4. Clique em **"Gerar Documento"**
5. Aguarde o processamento (a IA pode levar 30-60 segundos)
6. Faça o download do arquivo gerado

### 3. Templates

Coloque seus templates .docx em:
- `/root/pmnova/engenharia-portal/shared_files/templates/`

Use placeholders: `{{OBJETO}}`, `{{TEXTO_IA}}`, `{{DATA_ATUAL}}`, etc.

---

## 🐛 Troubleshooting

### Problema: "Erro de conexão ao n8n"

**Solução:**
```bash
# Verificar se n8n está rodando
docker-compose ps

# Reiniciar n8n
docker-compose restart n8n
```

### Problema: "Port forwarding não funciona"

**Solução:**
```powershell
# No PowerShell (Admin), reiniciar WSL
wsl --shutdown

# Aguardar 10 segundos e iniciar novamente
wsl

# Refazer port forwarding
.\setup-port-forwarding.ps1
```

### Problema: "Arquivo não encontrado para download"

**Solução:**
- Verifique se o volume está mapeado corretamente no `docker-compose.yml`
- Verifique permissões da pasta: `chmod -R 777 shared_files/`

---

## 📚 Recursos Adicionais

- [Documentação do Streamlit](https://docs.streamlit.io/)
- [Documentação do n8n](https://docs.n8n.io/)
- [WSL 2 Networking](https://learn.microsoft.com/en-us/windows/wsl/networking)

---

## 📝 Changelog

**v1.0.0 - Dezembro/2025**
- ✅ Interface Streamlit completa
- ✅ Integração com n8n via webhook
- ✅ Sistema de upload/download de arquivos
- ✅ Docker Compose com rede compartilhada
- ✅ Documentação de port forwarding

---

**Desenvolvido para a Prefeitura Municipal de Nova Petrópolis** 🏗️
