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
# URL do backend Python (substituiu n8n)
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend:5000/gerar-etp")
OUTPUT_DIR = "/data/output"

# ========================================
# Configuração da Página
# ========================================
st.set_page_config(
    page_title="Sistema de Engenharia - PMNP",
    page_icon="assets/icone_np.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "Sistema de Automação de Engenharia Civil - Prefeitura Municipal de Nova Petrópolis"
    }
)

# ========================================
# CSS Customizado - Identidade Visual PMNP
# ========================================
st.markdown("""
    <style>
    /* Esconde apenas o footer */
    footer {
        display: none !important;
    }
    
    /* Paleta oficial da Prefeitura de Nova Petrópolis */
    :root {
        --pmnp-blue: #1d98bb;
        --pmnp-blue-dark: #156b84;
        --pmnp-blue-light: #e6f5f9;
        --pmnp-green: #28a745;
        --pmnp-gray: #6c757d;
    }
    
    /* Header fullwidth */
    .pmnp-header {
        background: #ffffff;
        padding: 1rem 1.5rem;
        margin: 0;
        width: 100%;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 1.5rem;
        min-height: 85px;
        border-bottom: 4px solid #1d98bb;
        box-sizing: border-box;
    }
    
    .pmnp-brasao-header {
        max-width: 90px;
        height: auto;
        max-height: 85px;
        flex-shrink: 0;
    }
    
    .pmnp-header-logo {
        max-width: 280px;
        height: auto;
        max-height: 75px;
        flex-shrink: 0;
    }
    
    .pmnp-header-divider {
        width: 2px;
        height: 60px;
        background: rgba(29,152,187,0.2);
        margin: 0 1rem;
        flex-shrink: 0;
    }
    
    .pmnp-header-text {
        flex: 1;
    }
    
    .pmnp-header h1 {
        color: #1d98bb;
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
        letter-spacing: -0.5px;
    }
    
    .pmnp-header p {
        color: #666;
        font-size: 0.95rem;
        margin: 0.15rem 0 0 0;
        font-weight: 400;
    }
    
    /* Brasão topo - REMOVIDO - Agora fica no header */
    
    /* Ajuste geral da página */
    .main .block-container {
        padding-top: 0 !important;
        max-width: 1400px;
    }
    
    /* Botões com estilo PMNP */
    .stButton>button {
        background-color: #1d98bb;
        color: white;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 0.6rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #156b84;
        box-shadow: 0 4px 12px rgba(29,152,187,0.3);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 2px solid #1d98bb;
    }
    
    /* Cards e boxes */
    .stInfo {
        background-color: #e6f5f9 !important;
        border-left: 4px solid #1d98bb !important;
    }
    
    .stSuccess {
        background-color: #d4edda !important;
        border-left: 4px solid #28a745 !important;
    }
    
    .stWarning {
        background-color: #fff3cd !important;
        border-left: 4px solid #ffc107 !important;
    }
    
    .stError {
        background-color: #f8d7da !important;
        border-left: 4px solid #dc3545 !important;
    }
    
    /* Footer PMNP */
    .pmnp-footer {
        margin-top: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-top: 4px solid #1d98bb;
        text-align: center;
        color: #495057;
        border-radius: 8px;
    }
    
    .pmnp-footer-brasao {
        max-height: 80px;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    
    .pmnp-footer strong {
        color: #156b84;
        font-size: 1.1rem;
    }
    
    .pmnp-footer p {
        margin: 0.5rem 0;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# ========================================
# Cabeçalho Principal com Logo
# ========================================
import base64

def get_base64_image(image_path):
    """Converte imagem para base64 para embedding no HTML"""
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# Tentar carregar imagens
logo_cabecalho = get_base64_image("assets/logo_cab_text2.png")
brasao = get_base64_image("assets/brasao_np.png")

# ========================================
# Cabeçalho com Logo e Brasão
# ========================================
if logo_cabecalho and brasao:
    st.markdown(f'''
    <div class="pmnp-header">
        <img src="data:image/png;base64,{brasao}" alt="Brasão Nova Petrópolis" class="pmnp-brasao-header">
        <img src="data:image/png;base64,{logo_cabecalho}" alt="Prefeitura Nova Petrópolis" class="pmnp-header-logo">
        <div class="pmnp-header-divider"></div>
        <div class="pmnp-header-text">
            <h1>Sistema de Engenharia</h1>
            <p>Secretaria de Planejamento, Coordenação, Trânsito e Habitação</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
elif logo_cabecalho:
    st.markdown(f'''
    <div class="pmnp-header">
        <img src="data:image/png;base64,{logo_cabecalho}" alt="Prefeitura Nova Petrópolis" class="pmnp-header-logo">
        <div class="pmnp-header-divider"></div>
        <div class="pmnp-header-text">
            <h1>Sistema de Engenharia</h1>
            <p>Secretaria de Planejamento, Coordenação, Trânsito e Habitação</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('<div class="pmnp-header"><div class="pmnp-header-text"><h1>🏗️ Sistema de Engenharia</h1><p>Prefeitura Municipal de Nova Petrópolis</p></div></div>', unsafe_allow_html=True)

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
🌐 Backend Python Ativo  
""")

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🔗 Acesso Rápido")
st.sidebar.markdown("")
st.sidebar.markdown("🔧 **[API Backend →](http://172.22.49.116:5000/health)**")
st.sidebar.markdown("📖 **[Documentação →](https://github.com/RabelloRS/pmnova-automacao-engenharia)**")

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
        st.info("**🤖 Automação Inteligente**\n\nProcessamento direto em Python + IA.")
    
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
        # ========================================
        # SEÇÃO 1: Upload de PDFs da Caixa
        # ========================================
        st.markdown("### 📎 Upload de Planilhas da Caixa (Opcional - Modo Automático)")
        st.info("""
        **💡 Extração Automática:** Envie os PDFs da Caixa e o sistema extrairá automaticamente:
        - 📋 Objeto da obra
        - 💰 Valores (Global, Repasse, Contrapartida)  
        - 📐 Área total (m²)
        - 📊 BDI e Data Base
        
        **Se não enviar PDFs**, preencha manualmente os campos abaixo.
        """)
        
        uploaded_files = st.file_uploader(
            "Carregue os arquivos: PO.pdf, QCI.pdf, PLQ.pdf",
            type=['pdf'],
            accept_multiple_files=True,
            help="Planilhas orçamentárias da Caixa Econômica Federal"
        )
        
        # Mostra arquivos enviados
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} arquivo(s) carregado(s):")
            for uploaded_file in uploaded_files:
                file_size_kb = uploaded_file.size / 1024
                st.text(f"  📄 {uploaded_file.name} ({file_size_kb:.1f} KB)")
        
        st.markdown("---")
        
        # ========================================
        # SEÇÃO 2: Dados do Documento
        # ========================================
        st.markdown("### 📝 Informações do Documento")
        
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
            help="Explique a necessidade e a justificativa técnica (será gerada automaticamente se enviar PDFs)"
        )
        
        col3, col4 = st.columns(2)
        
        with col3:
            setor = st.text_input(
                "Setor Responsável",
                value="Secretaria de Planejamento, Coordenação, Trânsito e Habitação",
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
            # ========================================
            # Processar Upload de PDFs (se houver)
            # ========================================
            pasta_uploads = "/data/uploads"
            os.makedirs(pasta_uploads, exist_ok=True)
            
            pdf_enviados = []
            if uploaded_files:
                with st.spinner("📤 Salvando arquivos PDF..."):
                    for uploaded_file in uploaded_files:
                        # Salvar arquivo na pasta compartilhada
                        caminho_arquivo = os.path.join(pasta_uploads, uploaded_file.name)
                        with open(caminho_arquivo, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        pdf_enviados.append(uploaded_file.name)
                
                st.success(f"✅ {len(pdf_enviados)} PDF(s) salvo(s) em {pasta_uploads}")
            
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
                "data_solicitacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                # Novos campos para extração automática
                "modo_extracao": "automatico" if uploaded_files else "manual",
                "pasta_uploads": pasta_uploads if uploaded_files else None,
                "arquivos_pdf": pdf_enviados if uploaded_files else []
            }
            
            # Mostrar loading
            mensagem_loading = "⏳ Extraindo dados dos PDFs e gerando documento com IA..." if uploaded_files else "⏳ Gerando documento com IA... Aguarde!"
            with st.spinner(mensagem_loading):
                try:
                    # Enviar requisição para o backend Python
                    resposta = requests.post(
                        BACKEND_API_URL,
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
                    st.error("❌ Erro de conexão: Não foi possível conectar ao backend. Verifique se o serviço está rodando.")
                
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
    - **Backend Python:** API de processamento (Flask + OpenAI)
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

# Footer com brasão e informações institucionais
if brasao:
    footer_html = f'''
    <div class="pmnp-footer">
        <img src="data:image/png;base64,{brasao}" alt="Brasão Nova Petrópolis" class="pmnp-footer-brasao">
        <p style="margin-top: 1rem;">
            <strong>Prefeitura Municipal de Nova Petrópolis</strong><br>
            Rua 7 de Setembro, 330 - 2º Piso | CEP 95150-000<br>
            📞 (54) 3281.8400 | ✉️ comunicacao@novapetropolis.rs.gov.br<br>
            🕒 Horário de Atendimento: 8h às 12h e 13h10 às 16h40
        </p>
        <p style="margin-top: 1rem; font-size: 0.85rem; color: #6c757d;">
            Sistema de Engenharia v1.0 | © 2025 - Todos os direitos reservados
        </p>
    </div>
    '''
else:
    footer_html = '''
    <div class="pmnp-footer">
        <p>
            <strong>Prefeitura Municipal de Nova Petrópolis</strong><br>
            © 2025 - Todos os direitos reservados
        </p>
    </div>
    '''

st.markdown(footer_html, unsafe_allow_html=True)
