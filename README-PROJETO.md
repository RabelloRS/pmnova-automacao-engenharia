# 🏗️ PM Nova - Sistema de Automação de Engenharia Civil

Sistema completo de automação de processos de engenharia civil pública usando **n8n** e **Streamlit** via Docker Compose.

## 📋 Sobre o Projeto

Este repositório contém dois sistemas de automação:

1. **Sistema Base (n8n):** Estrutura inicial para automação com n8n
2. **Portal de Engenharia (n8n + Streamlit):** Sistema completo com interface web

### Funcionalidades

- ✅ Geração automática de peças técnicas (ETP, TR, MD) com IA
- ✅ Interface web amigável (Streamlit)
- ✅ Orquestração de workflows (n8n)
- ✅ Integração com APIs de LLM (OpenAI, Ollama)
- ✅ Processamento de documentos .docx
- ✅ Scripts Python para cálculos de engenharia
- ✅ Containerização completa com Docker

## 🚀 Quick Start

### Portal de Engenharia (Recomendado)

```bash
cd engenharia-portal
bash start-portal.sh
```

Acesse:
- **Frontend:** http://localhost:8501
- **Backend:** http://localhost:5678

### Sistema Base n8n

```bash
bash start.sh
```

Acesse: http://localhost:5678

## 📁 Estrutura do Repositório

```
pmnova/
├── engenharia-portal/      # Portal completo (n8n + Streamlit)
│   ├── frontend/           # Interface Streamlit
│   ├── shared_files/       # Arquivos compartilhados
│   └── docker-compose.yml
│
├── workflows/              # Backups dos fluxos n8n
├── python_scripts/         # Scripts Python
├── templates/              # Templates de documentos
├── output/                 # Arquivos gerados
└── docker-compose.yml      # n8n standalone
```

## 🛠️ Tecnologias

- **n8n** - Automação de workflows
- **Streamlit** - Interface web Python
- **Docker & Docker Compose** - Containerização
- **Python 3.9** - Scripts e processamento
- **OpenAI/Ollama** - Integração com IA

## 📚 Documentação

Consulte os arquivos README.md em cada pasta:
- [Portal de Engenharia](./engenharia-portal/README.md)
- [Sistema Base](./README.md)

## 🔐 Credenciais Padrão

**n8n:**
- Usuário: `admin`
- Senha: `admin123` (sistema base) ou `engenharia2025` (portal)

⚠️ **Altere em produção!**

## 🌐 Acesso Remoto (WSL 2)

Para acessar de outros computadores na rede local, execute no Windows (PowerShell Admin):

```powershell
cd engenharia-portal
.\setup-port-forwarding.ps1
```

## 📝 Licença

Projeto interno da Prefeitura Municipal.

## 👨‍💻 Desenvolvido por

Equipe de Tecnologia e Engenharia - Prefeitura Municipal de Nova Petrópolis

---

**Versão:** 1.0.0 | **Data:** Dezembro/2025
