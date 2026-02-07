# Modelos de justificativa

Use esta pasta para guardar textos de justificativa de licitações que servirão como exemplos ou few-shots para a IA.

## Formato sugerido de cada arquivo
- Um arquivo `.md` ou `.txt` por caso.
- Nomeie de forma descritiva, ex.: `2024-05-pavimentacao-bairro-centro.md`.
- Inclua um cabeçalho simples (pode ser YAML) com metadados para facilitar busca:

```
---
objeto: Pavimentação Bairro Centro
modalidade: Concorrencia
valor_total: 4.362.478,30
repasse: 3.962.478,30
contrapartida: 400.000,00
local: Nova Petrópolis/RS
data_base: 01/2024
tags: [pavimentacao, recapeamento, mobilidade]
---
```

- Após o cabeçalho, coloque o texto completo da justificativa.

## Boas práticas
- Textos claros, 3-5 parágrafos, tom institucional.
- Referenciar Lei 14.133/2021 quando aplicável.
- Destacar necessidade, impacto, urgência, riscos de não executar.
- Citar números relevantes (valores, áreas, prazos) quando houver.

## Como o sistema usa estes modelos
- No modo automático, o extrator lê o OBJETO dos PDFs e busca o exemplo mais parecido nesta pasta.
- O melhor trecho é injetado no prompt da IA apenas como inspiração; o texto final é reescrito com os dados atuais.
- Você pode substituir/editar os arquivos a qualquer momento; basta manter nomes descritivos.

## Próximos passos possíveis
- Criar um índice/embeddings para buscar o melhor exemplo e injetar no prompt da IA.
- Integrar busca automática no fluxo Streamlit/n8n.
