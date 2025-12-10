# Workflows do n8n

Esta pasta armazena os backups dos fluxos (workflows) criados no n8n.

## Como fazer backup de um workflow:

1. Acesse o n8n em http://localhost:5678
2. Abra o workflow desejado
3. Clique nos 3 pontinhos (menu) → "Download"
4. Salve o arquivo JSON nesta pasta

## Como restaurar um workflow:

1. Acesse o n8n
2. Clique em "+ Workflow"
3. Clique nos 3 pontinhos → "Import from File"
4. Selecione o arquivo JSON desta pasta

## Workflows Disponíveis:

- `gerador_pecas_tecnicas.json` - Gerador de ETP, TR e MD com IA
- _(adicione outros workflows aqui)_

## Boas Práticas:

- Mantenha backups atualizados dos workflows
- Use nomes descritivos para os arquivos
- Documente alterações importantes
- Versione os arquivos (ex: `workflow_v1.json`, `workflow_v2.json`)
