# Templates de Documentos

Esta pasta contém os templates .docx utilizados pelo sistema de automação.

## Templates Disponíveis:

### 1. `template_etp.docx` - Estudo Técnico Preliminar
**Variáveis disponíveis:**
- `{{OBJETO}}` - Descrição do objeto da contratação
- `{{JUSTIFICATIVA}}` - Justificativa técnica
- `{{VALOR_ESTIMADO}}` - Valor estimado da contratação
- `{{TEXTO_IA}}` - Texto técnico gerado pela IA
- `{{DATA_ATUAL}}` - Data atual (formato DD/MM/AAAA)
- `{{ANO_ATUAL}}` - Ano atual
- `{{HORA_ATUAL}}` - Hora atual

### 2. `template_tr.docx` - Termo de Referência
**Variáveis disponíveis:**
- `{{OBJETO}}` - Objeto da contratação
- `{{JUSTIFICATIVA}}` - Justificativa
- `{{VALOR_ESTIMADO}}` - Valor estimado
- `{{TEXTO_IA}}` - Conteúdo técnico gerado
- `{{DATA_ATUAL}}` - Data
- `{{ESPECIFICACOES}}` - Especificações técnicas
- `{{CRONOGRAMA}}` - Cronograma de execução

### 3. `template_md.docx` - Memorial Descritivo
**Variáveis disponíveis:**
- `{{OBJETO}}` - Descrição do projeto
- `{{LOCAL}}` - Localização da obra
- `{{TEXTO_IA}}` - Descrição técnica completa
- `{{DATA_ATUAL}}` - Data
- `{{AREA_TOTAL}}` - Área total do projeto
- `{{MEMORIAL_CALCULO}}` - Memorial de cálculo

## Como criar um template:

1. Crie um documento Word (.docx)
2. Insira os placeholders no formato `{{NOME_VARIAVEL}}`
3. Use LETRAS MAIÚSCULAS para os nomes das variáveis
4. Salve o arquivo nesta pasta
5. O script Python substituirá automaticamente os placeholders

## Exemplo de uso no documento:

```
ESTUDO TÉCNICO PRELIMINAR

Data: {{DATA_ATUAL}}

1. OBJETO
{{OBJETO}}

2. JUSTIFICATIVA
{{JUSTIFICATIVA}}

3. ESTIMATIVA DE CUSTOS
Valor Estimado: {{VALOR_ESTIMADO}}

4. DESCRIÇÃO TÉCNICA
{{TEXTO_IA}}
```

## Boas Práticas:

- Use formatação consistente (fontes, estilos, margens)
- Inclua cabeçalho e rodapé padrão da Prefeitura
- Teste os templates antes de usar em produção
- Mantenha backups dos templates
- Versione os templates quando fizer alterações significativas
