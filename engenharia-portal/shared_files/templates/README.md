# 📄 Templates de Documentos Técnicos

## ✅ Templates Disponíveis

Esta pasta contém templates Word (`.docx`) profissionalmente formatados para geração automática de documentos técnicos:

| Template | Arquivo | Tamanho | Descrição |
|----------|---------|---------|-----------|
| **ETP** | `template_etp.docx` | ~38 KB | Estudo Técnico Preliminar |
| **TR** | `template_tr.docx` | ~38 KB | Termo de Referência |
| **MD** | `template_md.docx` | ~38 KB | Memorial Descritivo |

---

## 🎨 Características dos Templates

### ✨ Formatação Profissional

- **Cabeçalho oficial** com brasão e identificação da Prefeitura
- **Estilos padronizados** (títulos, subtítulos, parágrafos)
- **Tabelas formatadas** para apresentação de dados técnicos
- **Estrutura hierárquica** clara e organizada
- **Rodapé** com assinatura e identificação do responsável

### 📋 Seções Incluídas

#### Template ETP (Estudo Técnico Preliminar)
1. Identificação (tabela com dados principais)
2. Justificativa e Descrição da Necessidade
3. Estimativa de Custos e Cronograma
4. Conformidade com a Lei nº 14.133/2021

#### Template TR (Termo de Referência)
1. Do Objeto
2. Da Justificativa
3. Das Especificações Técnicas e Quantitativos
4. Das Obrigações da Contratada
5. Dos Critérios de Medição e Pagamento
6. Do Valor Estimado
7. Do Prazo de Execução
8. Da Fundamentação Legal

#### Template MD (Memorial Descritivo)
1. Identificação do Projeto
2. Considerações Iniciais
3. Descrição Geral do Projeto
4. Especificações Técnicas dos Serviços
5. Normas Técnicas Aplicáveis
6. Orçamento e Cronograma
7. Considerações Finais

---

## 🔧 Placeholders (Variáveis)

Os templates utilizam placeholders que são **automaticamente substituídos** pelo sistema durante a geração do documento:

### Dados Extraídos Automaticamente (dos PDFs da Caixa)

| Placeholder | Descrição | Fonte |
|-------------|-----------|-------|
| `{{OBJETO}}` | Descrição completa do objeto | PO.pdf |
| `{{VALOR_GLOBAL}}` | Valor total da obra | QCI.pdf ou PO.pdf |
| `{{VALOR_REPASSE}}` | Valor do repasse federal | QCI.pdf |
| `{{VALOR_CONTRAPARTIDA}}` | Contrapartida municipal | QCI.pdf |
| `{{AREA_TOTAL}}` | Área total em m² | PLQ.pdf |
| `{{BDI}}` | BDI em % | PO.pdf |
| `{{DATA_BASE}}` | Data base do orçamento (MM/AAAA) | PO.pdf |
| `{{LOCAL}}` | Município/UF | PO.pdf |

### Dados do Formulário

| Placeholder | Descrição | Fonte |
|-------------|-----------|-------|
| `{{RESPONSAVEL}}` | Nome do responsável técnico | Formulário Streamlit |
| `{{SETOR}}` | Setor ou secretaria | Formulário Streamlit |
| `{{JUSTIFICATIVA}}` | Justificativa complementar | Formulário Streamlit |

### Dados Gerados pelo Sistema

| Placeholder | Descrição | Fonte |
|-------------|-----------|-------|
| `{{TEXTO_IA}}` | Texto técnico gerado pela IA | GPT-4 (OpenAI) |
| `{{DATA_ATUAL}}` | Data de geração do documento | Sistema |

---

## 📝 Como os Templates São Usados

### Fluxo Automático

```
1. Usuário faz upload dos PDFs (PO, QCI, PLQ)
   ↓
2. Sistema extrai dados automaticamente
   ↓
3. IA (GPT-4) gera texto técnico
   ↓
4. Script Python carrega template correspondente
   ↓
5. Substitui todos os {{PLACEHOLDERS}}
   ↓
6. Salva documento final em /data/output/
   ↓
7. Usuário faz download via Streamlit
```

### Exemplo de Substituição

**Antes (no template):**
```
Objeto: {{OBJETO}}
Valor: R$ {{VALOR_GLOBAL}}
```

**Depois (documento gerado):**
```
Objeto: Recapeamento com CBUQ da Avenida Germânia - 8ª Fase
Valor: R$ 436.247,83
```

---

## 🛠️ Personalização dos Templates

### Para Editar os Templates:

1. **Abra o arquivo** `.docx` no Microsoft Word ou LibreOffice
2. **Edite o conteúdo**, mas **PRESERVE os placeholders** `{{VARIAVEL}}`
3. **Ajuste formatação** (fontes, cores, margens) conforme necessário
4. **Salve** o arquivo mantendo o mesmo nome

### ⚠️ Cuidados Importantes:

- ✅ **PRESERVE** todos os placeholders `{{VARIAVEL}}`
- ✅ **NÃO remova** as chaves duplas `{{ }}`
- ✅ **Mantenha** a estrutura de seções
- ✅ **Use** fontes padrão (Arial, Times New Roman)
- ❌ **NÃO** use caracteres especiais nos nomes de placeholders

---

## 🔄 Regenerar Templates

Se você precisar **recriar** os templates do zero (com formatação padrão):

```bash
cd /root/pmnova/python_scripts
python3 gerar_templates.py
```

**Atenção:** Isso irá **sobrescrever** os templates existentes!

---

## 📊 Exemplo de Documento Gerado

### Entrada:
- **PDFs:** PO.pdf, QCI.pdf, PLQ.pdf (Avenida Germânia)
- **Formulário:** Justificativa adicional, Responsável Técnico
- **IA:** Gera texto técnico profissional

### Saída:
```
📄 TR_Recapeamento_Avenida_Germania_20251210_143025.docx

Conteúdo:
- Cabeçalho oficial da Prefeitura
- Objeto: "Recapeamento com CBUQ da Avenida Germânia - 8ª Fase"
- Valor Global: R$ 436.247,83
- Repasse: R$ 396.000,00
- Contrapartida: R$ 40.247,83
- Área: 3.885,00 m²
- BDI: 21,00%
- Texto técnico gerado pela IA (3-5 parágrafos profissionais)
- Justificativa complementar do usuário
- Rodapé com assinatura do responsável técnico
```

---

## 🎯 Dicas de Uso

### Para Melhores Resultados:

1. **Use os PDFs originais da Caixa** - Garante extração precisa
2. **Preencha a justificativa** - Complementa o texto da IA
3. **Revise o documento gerado** - Sempre faça revisão final
4. **Ajuste seções específicas** - Adicione detalhes técnicos se necessário
5. **Mantenha templates atualizados** - Revise periodicamente conforme legislação

### Campos que Podem Necessitar Edição Manual:

- **Prazo de execução** (no TR)
- **Detalhes de serviços específicos** (no MD)
- **Cronograma físico-financeiro** (se não estiver em anexo)
- **Normas técnicas específicas** (depende do tipo de obra)

---

## 📚 Conformidade Legal

Os templates foram desenvolvidos em conformidade com:

- ✅ **Lei Federal nº 14.133/2021** (Nova Lei de Licitações)
- ✅ **Lei Complementar nº 101/2000** (Lei de Responsabilidade Fiscal)
- ✅ **Diretrizes da Caixa Econômica Federal**
- ✅ **Normas ABNT** aplicáveis à construção civil

---

## 🆘 Suporte

### Problemas Comuns:

**❌ "Placeholder não foi substituído"**
- Verifique se o nome está escrito corretamente
- Confirme que os dados foram extraídos dos PDFs
- Veja logs em `/data/logs/`

**❌ "Formatação estranha no documento gerado"**
- Abra o template original e verifique formatação
- Certifique-se de que não há caracteres especiais
- Recrie o template com `gerar_templates.py`

**❌ "Falta seção no documento"**
- Verifique se o template correto está sendo usado
- Confirme que o tipo de peça está correto (ETP/TR/MD)

---

## 📁 Estrutura de Arquivos

```
shared_files/templates/
├── template_etp.docx       ← Estudo Técnico Preliminar
├── template_tr.docx        ← Termo de Referência
├── template_md.docx        ← Memorial Descritivo
└── README.md              ← Este arquivo
```

---

## 🔗 Referências

- **Script Gerador:** `/root/pmnova/python_scripts/gerar_templates.py`
- **Script Processador:** `/root/pmnova/python_scripts/gerar_peca.py`
- **Documentação Completa:** `/root/pmnova/engenharia-portal/EXTRACAO_AUTOMATICA.md`

---

**Última atualização:** 10/12/2025  
**Versão:** 1.0  
**Autor:** Sistema de Automação - Prefeitura Municipal de Nova Petrópolis/RS
