"""
Sistema de Engenharia - PM Nova Petrópolis
Portal de Automação de Processos de Engenharia Civil
"""

import streamlit as st
import requests
import os
from datetime import datetime
import time

# ========================================
# Configurações
# ========================================
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://n8n:5678/webhook/gerar-etp")
OUTPUT_DIR = "/files/output"

# ========================================
# Configuração da Página
# ========================================
st.set_page_config(
    page_title="Sistema de Engenharia - PMNP",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# CSS Customizado
# ========================================
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #1f77b4;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #145a8a;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        color: #155724;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        color: #0c5460;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# Cabeçalho Principal
# ========================================
st.markdown('<h1 class="main-header">🏗️ Sistema de Engenharia - PM Nova Petrópolis</h1>', unsafe_allow_html=True)

# ========================================
# Menu Lateral
# ========================================
st.sidebar.title("📋 Menu de Opções")
st.sidebar.markdown("---")

menu_option = st.sidebar.radio(
    "Selecione o módulo:",
    ["🏠 Início", "📝 Gerador de ETP/TR", "📊 Consultar Documentos", "ℹ️ Sobre"]
)

st.sidebar.markdown("---")
st.sidebar.info(f"""
**Sistema Ativo**  
🕒 {datetime.now().strftime('%d/%m/%Y %H:%M')}  
🌐 Conectado ao n8n  
""")

# ========================================
# Página: Início
# ========================================
if menu_option == "🏠 Início":
    st.header("Bem-vindo ao Portal de Automação")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**📝 Gerador de Peças Técnicas**\n\nCrie ETP, TR e MD automaticamente com auxílio de IA.")
    
    with col2:
        st.info("**📊 Consultar Documentos**\n\nAcesse documentos gerados anteriormente.")
    
    with col3:
        st.info("**🤖 Automação Inteligente**\n\nSistema integrado com n8n e IA.")
    
    st.markdown("---")
    st.success("✅ Sistema operacional. Selecione um módulo no menu lateral para começar.")

# ========================================
# Página: Gerador de ETP/TR
# ========================================
elif menu_option == "📝 Gerador de ETP/TR":
    st.header("📝 Gerador de Peças Técnicas")
    st.markdown("Preencha os dados abaixo para gerar automaticamente uma peça técnica (ETP, TR ou MD).")
    
    # Formulário
    with st.form("form_gerar_peca"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            tipo_peca = st.selectbox(
                "Tipo de Peça Técnica",
                ["ETP - Estudo Técnico Preliminar", "TR - Termo de Referência", "MD - Memorial Descritivo"],
                help="Selecione o tipo de documento a ser gerado"
            )
        
        with col2:
            valor_estimado = st.number_input(
                "Valor Estimado (R$)",
                min_value=0.0,
                value=100000.0,
                step=1000.0,
                format="%.2f",
                help="Valor estimado da contratação"
            )
        
        objeto = st.text_input(
            "Objeto da Obra/Contratação",
            placeholder="Ex: Contratação de empresa para pavimentação asfáltica da Rua Principal",
            help="Descreva brevemente o objeto da contratação"
        )
        
        justificativa = st.text_area(
            "Justificativa",
            placeholder="Descreva a justificativa técnica para a contratação...",
            height=150,
            help="Explique a necessidade e a justificativa técnica"
        )
        
        col3, col4 = st.columns(2)
        
        with col3:
            setor = st.text_input(
                "Setor Responsável",
                value="Secretaria de Obras e Infraestrutura",
                help="Setor ou secretaria responsável"
            )
        
        with col4:
            responsavel = st.text_input(
                "Responsável Técnico",
                placeholder="Nome do Engenheiro Responsável",
                help="Nome do engenheiro ou responsável técnico"
            )
        
        # Botão de submit
        submit_button = st.form_submit_button("🚀 Gerar Documento")
    
    # Processar quando o formulário for enviado
    if submit_button:
        # Validações
        if not objeto or not justificativa:
            st.error("❌ Por favor, preencha todos os campos obrigatórios (Objeto e Justificativa).")
        else:
            # Extrair tipo de peça (sigla)
            tipo_sigla = tipo_peca.split(" - ")[0].lower()
            
            # Preparar dados para envio
            payload = {
                "tipo_peca": tipo_sigla,
                "objeto": objeto,
                "justificativa": justificativa,
                "valor_estimado": f"R$ {valor_estimado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                "setor": setor,
                "responsavel": responsavel,
                "data_solicitacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            
            # Mostrar loading
            with st.spinner("⏳ Gerando documento com IA... Aguarde!"):
                try:
                    # Enviar requisição para o webhook do n8n
                    response = requests.post(
                        N8N_WEBHOOK_URL,
                        json=payload,
                        timeout=120  # 2 minutos de timeout
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("✅ Documento gerado com sucesso!")
                        
                        # Mostrar informações do resultado
                        st.markdown("### 📄 Detalhes do Documento")
                        
                        col_info1, col_info2 = st.columns(2)
                        
                        with col_info1:
                            st.info(f"""
                            **Tipo:** {tipo_peca}  
                            **Objeto:** {objeto[:50]}...  
                            **Valor:** {payload['valor_estimado']}
                            """)
                        
                        with col_info2:
                            st.info(f"""
                            **Status:** {result.get('status', 'Concluído')}  
                            **Timestamp:** {result.get('timestamp', datetime.now().strftime('%d/%m/%Y %H:%M'))}  
                            **Responsável:** {responsavel}
                            """)
                        
                        # Verificar se há arquivo gerado
                        if 'arquivo' in result:
                            arquivo_path = result['arquivo']
                            arquivo_nome = os.path.basename(arquivo_path)
                            
                            st.markdown("### 📥 Download")
                            st.markdown(f"**Arquivo:** `{arquivo_nome}`")
                            
                            # Botão de download (se o arquivo existir no volume compartilhado)
                            if os.path.exists(arquivo_path):
                                with open(arquivo_path, "rb") as file:
                                    st.download_button(
                                        label="⬇️ Baixar Documento",
                                        data=file,
                                        file_name=arquivo_nome,
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                                    )
                            else:
                                st.warning(f"⚠️ Arquivo gerado: `{arquivo_nome}`. Aguarde o processamento ou verifique a pasta `/files/output`.")
                        
                        # Mostrar resposta completa (debug)
                        with st.expander("🔍 Ver resposta completa da API"):
                            st.json(result)
                    
                    else:
                        st.error(f"❌ Erro ao gerar documento. Status: {response.status_code}")
                        st.code(response.text)
                
                except requests.exceptions.Timeout:
                    st.error("❌ Timeout: O servidor demorou muito para responder. Tente novamente.")
                
                except requests.exceptions.ConnectionError:
                    st.error("❌ Erro de conexão: Não foi possível conectar ao n8n. Verifique se o serviço está rodando.")
                
                except Exception as e:
                    st.error(f"❌ Erro inesperado: {str(e)}")

# ========================================
# Página: Consultar Documentos
# ========================================
elif menu_option == "📊 Consultar Documentos":
    st.header("📊 Documentos Gerados")
    st.markdown("Lista de documentos disponíveis na pasta de output.")
    
    if os.path.exists(OUTPUT_DIR):
        arquivos = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.docx')]
        
        if arquivos:
            st.success(f"✅ Encontrados {len(arquivos)} documento(s).")
            
            for arquivo in sorted(arquivos, reverse=True):
                arquivo_path = os.path.join(OUTPUT_DIR, arquivo)
                
                col_a, col_b, col_c = st.columns([3, 1, 1])
                
                with col_a:
                    st.text(f"📄 {arquivo}")
                
                with col_b:
                    # Data de modificação
                    if os.path.exists(arquivo_path):
                        timestamp = os.path.getmtime(arquivo_path)
                        data = datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y %H:%M")
                        st.text(f"🕒 {data}")
                
                with col_c:
                    # Botão de download
                    if os.path.exists(arquivo_path):
                        with open(arquivo_path, "rb") as file:
                            st.download_button(
                                label="⬇️ Baixar",
                                data=file,
                                file_name=arquivo,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                key=arquivo
                            )
                
                st.markdown("---")
        else:
            st.info("ℹ️ Nenhum documento encontrado. Gere seu primeiro documento no menu 'Gerador de ETP/TR'.")
    else:
        st.warning("⚠️ Pasta de output não encontrada. Verifique a configuração dos volumes.")

# ========================================
# Página: Sobre
# ========================================
elif menu_option == "ℹ️ Sobre":
    st.header("ℹ️ Sobre o Sistema")
    
    st.markdown("""
    ### 🏗️ Sistema de Automação de Engenharia Civil
    
    **Prefeitura Municipal de Nova Petrópolis**
    
    Este portal foi desenvolvido para automatizar processos de engenharia civil pública, 
    integrando tecnologias modernas de automação e inteligência artificial.
    
    #### 🔧 Tecnologias Utilizadas:
    - **Streamlit:** Interface web interativa
    - **n8n:** Orquestração de workflows
    - **Docker:** Containerização e deploy
    - **Python:** Scripts de processamento
    - **IA/LLM:** Geração inteligente de textos técnicos
    
    #### 📋 Funcionalidades:
    - ✅ Geração automática de peças técnicas (ETP, TR, MD)
    - ✅ Integração com APIs de IA (OpenAI, Ollama)
    - ✅ Processamento de documentos .docx
    - ✅ Consulta e download de documentos gerados
    
    #### 👨‍💻 Desenvolvido por:
    Equipe de Tecnologia e Engenharia - PMNP
    
    ---
    
    **Versão:** 1.0.0  
    **Data:** Dezembro/2025
    """)
    
    st.info("💡 Para suporte técnico, entre em contato com a equipe de TI.")

# ========================================
# Footer
# ========================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>© 2025 Prefeitura Municipal de Nova Petrópolis - Todos os direitos reservados</div>",
    unsafe_allow_html=True
)
