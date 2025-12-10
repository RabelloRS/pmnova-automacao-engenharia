#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Extração de Dados de PDFs da Caixa Econômica Federal

Este script lê automaticamente os arquivos técnicos da Caixa:
- PO.pdf (Planilha Orçamentária)
- QCI.pdf (Quadro de Composição do Investimento)
- PLQ.pdf (Planilha de Levantamento de Quantitativos)

E extrai os dados principais para preencher automaticamente os documentos
técnicos (ETP, TR, MD), eliminando erros de digitação manual.

Autor: Sistema de Automação - Prefeitura Municipal
Data: Dezembro 2025
"""

import pdfplumber
import sys
import json
import re
import os
from datetime import datetime

def limpar_moeda(valor_str):
    """
    Converte valores monetários para formato limpo.
    
    Args:
        valor_str: String no formato 'R$ 436.247,83'
    
    Returns:
        String limpa: '436.247,83'
    """
    if not valor_str: 
        return "0,00"
    return valor_str.strip().replace('R$', '').strip()

def extrair_dados_caixa(caminho_pasta_arquivos):
    """
    Extrai dados técnicos dos PDFs da Caixa.
    
    Args:
        caminho_pasta_arquivos: Caminho absoluto da pasta com os PDFs
    
    Returns:
        Dict com dados extraídos: OBJETO, VALOR_GLOBAL, VALOR_REPASSE, etc.
    """
    
    dados = {
        "OBJETO": "Objeto não encontrado",
        "VALOR_GLOBAL": "0,00",
        "VALOR_REPASSE": "0,00",
        "VALOR_CONTRAPARTIDA": "0,00",
        "LOCAL": "Nova Petrópolis/RS",
        "DATA_BASE": "",
        "BDI": "0,00",
        "AREA_TOTAL": "0,00",
        "MUNICIPIO": "Nova Petrópolis",
        "UF": "RS",
        "TIMESTAMP": datetime.now().isoformat()
    }

    # =====================================
    # 1. LER PLANILHA ORÇAMENTÁRIA (PO.pdf)
    # =====================================
    caminho_po = os.path.join(caminho_pasta_arquivos, "PO.pdf")
    if os.path.exists(caminho_po):
        try:
            with pdfplumber.open(caminho_po) as pdf:
                texto_completo = ""
                for page in pdf.pages:
                    texto_pagina = page.extract_text()
                    if texto_pagina:
                        texto_completo += texto_pagina + "\n"
                
                # Extrair Objeto (APELIDO DO EMPREENDIMENTO)
                match_obj = re.search(
                    r'APELIDO DO EMPREENDIMENTO[:\s]+(.*?)(?=MUNICÍPIO|$)', 
                    texto_completo, 
                    re.DOTALL | re.IGNORECASE
                )
                if match_obj:
                    objeto = match_obj.group(1).replace('\n', ' ').strip()
                    # Limpar múltiplos espaços
                    objeto = re.sub(r'\s+', ' ', objeto)
                    dados["OBJETO"] = objeto
                
                # Extrair Município
                match_municipio = re.search(
                    r'MUNICÍPIO[:\s]+(.*?)(?=UF|ESTADO|$)', 
                    texto_completo, 
                    re.IGNORECASE
                )
                if match_municipio:
                    dados["MUNICIPIO"] = match_municipio.group(1).strip()
                
                # Extrair UF
                match_uf = re.search(r'UF[:\s]+([A-Z]{2})', texto_completo, re.IGNORECASE)
                if match_uf:
                    dados["UF"] = match_uf.group(1).upper()
                
                # Extrair Valor Total (padrão: grandes valores com vírgula e 2 decimais)
                # Procura valores no formato XXX.XXX,XX (com ou sem R$)
                valores_encontrados = re.findall(
                    r'R?\$?\s*([\d]{1,3}(?:\.[\d]{3})*,[\d]{2})', 
                    texto_completo
                )
                
                # Pega o maior valor (provavelmente é o total)
                if valores_encontrados:
                    valores_numericos = []
                    for val in valores_encontrados:
                        # Converte para float para comparar
                        val_num = float(val.replace('.', '').replace(',', '.'))
                        valores_numericos.append((val, val_num))
                    
                    # Ordena e pega o maior
                    valores_numericos.sort(key=lambda x: x[1], reverse=True)
                    dados["VALOR_GLOBAL"] = valores_numericos[0][0]
                
                # Extrair BDI (formato: "BDI 1 21,00%" ou "BDI: 21,00%")
                match_bdi = re.search(
                    r'BDI\s*\d*\s*([\d,]+)\s*%', 
                    texto_completo, 
                    re.IGNORECASE
                )
                if match_bdi:
                    dados["BDI"] = match_bdi.group(1)

                # Data Base (formato: DATA BASE 01/2024 ou DATA BASE: 01/2024)
                match_data = re.search(
                    r'DATA\s+BASE[:\s]+([\d]{2}/[\d]{4}|[\d]{2}/[\d]{2}/[\d]{4})', 
                    texto_completo, 
                    re.IGNORECASE
                )
                if match_data:
                    dados["DATA_BASE"] = match_data.group(1)
        
        except Exception as e:
            dados["erro_po"] = f"Erro ao processar PO.pdf: {str(e)}"

    # ======================================================
    # 2. LER QCI (QCI.pdf) - Repasse e Contrapartida
    # ======================================================
    caminho_qci = os.path.join(caminho_pasta_arquivos, "QCI.pdf")
    if os.path.exists(caminho_qci):
        try:
            with pdfplumber.open(caminho_qci) as pdf:
                primeira_pag = pdf.pages[0].extract_text()
                
                if primeira_pag:
                    # Regex para capturar Repasse
                    # Procura "REPASSE" seguido de valor na próxima linha ou mesma linha
                    match_repasse = re.search(
                        r'REPASSE[:\s]+([\d]{1,3}(?:\.[\d]{3})*,[\d]{2})', 
                        primeira_pag, 
                        re.IGNORECASE
                    )
                    if match_repasse:
                        dados["VALOR_REPASSE"] = match_repasse.group(1)
                    
                    # Regex para Contrapartida
                    match_cp = re.search(
                        r'CONTRAPARTIDA[:\s]+([\d]{1,3}(?:\.[\d]{3})*,[\d]{2})', 
                        primeira_pag, 
                        re.IGNORECASE
                    )
                    if match_cp:
                        dados["VALOR_CONTRAPARTIDA"] = match_cp.group(1)
                    
                    # Se não achou com regex, tenta busca por padrão de tabela
                    # (fallback para formatos mais complexos)
                    if dados["VALOR_REPASSE"] == "0,00":
                        # Procura qualquer valor grande que possa ser repasse
                        valores_grandes = re.findall(
                            r'([\d]{3}\.[\d]{3},[\d]{2})', 
                            primeira_pag
                        )
                        if len(valores_grandes) >= 2:
                            # Assume: primeiro grande = repasse, último = total
                            dados["VALOR_REPASSE"] = valores_grandes[0]
                            if dados["VALOR_GLOBAL"] == "0,00":
                                dados["VALOR_GLOBAL"] = valores_grandes[-1]
        
        except Exception as e:
            dados["erro_qci"] = f"Erro ao processar QCI.pdf: {str(e)}"

    # ================================================
    # 3. LER PLQ (PLQ.pdf) - Área Total (m²)
    # ================================================
    caminho_plq = os.path.join(caminho_pasta_arquivos, "PLQ.pdf")
    if os.path.exists(caminho_plq):
        try:
            with pdfplumber.open(caminho_plq) as pdf:
                texto_plq = ""
                for page in pdf.pages:
                    texto_pagina = page.extract_text()
                    if texto_pagina:
                        texto_plq += texto_pagina + "\n"
                
                # Tenta achar metragem quadrada (padrão: M2 ou m² seguido de número)
                match_area = re.search(
                    r'(?:M2|m²|m2)\s*([\d]{1,3}(?:\.[\d]{3})*,[\d]{2})', 
                    texto_plq, 
                    re.IGNORECASE
                )
                if match_area:
                    dados["AREA_TOTAL"] = match_area.group(1)
                
                # Fallback: procura por "ÁREA" seguida de valor
                if dados["AREA_TOTAL"] == "0,00":
                    match_area_alt = re.search(
                        r'ÁREA[:\s]+([\d]{1,3}(?:\.[\d]{3})*,[\d]{2})', 
                        texto_plq, 
                        re.IGNORECASE
                    )
                    if match_area_alt:
                        dados["AREA_TOTAL"] = match_area_alt.group(1)
        
        except Exception as e:
            dados["erro_plq"] = f"Erro ao processar PLQ.pdf: {str(e)}"

    # ================================================
    # 4. CÁLCULOS DERIVADOS
    # ================================================
    # Se temos Repasse e Contrapartida, mas não temos Global, soma
    if dados["VALOR_GLOBAL"] == "0,00":
        try:
            repasse_num = float(dados["VALOR_REPASSE"].replace('.', '').replace(',', '.'))
            cp_num = float(dados["VALOR_CONTRAPARTIDA"].replace('.', '').replace(',', '.'))
            total = repasse_num + cp_num
            # Formata de volta para BRL
            dados["VALOR_GLOBAL"] = f"{total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            pass
    
    # Monta LOCAL completo
    dados["LOCAL"] = f"{dados['MUNICIPIO']}/{dados['UF']}"

    return dados

def main():
    """Função principal - processa argumentos e executa extração."""
    
    # O argumento é a pasta onde os PDFs estão salvos (dentro do container)
    if len(sys.argv) < 2:
        print(json.dumps({
            "erro": "Uso: python3 extrator_caixa.py <caminho_pasta_uploads>",
            "exemplo": "python3 extrator_caixa.py /data/uploads"
        }))
        sys.exit(1)
    
    pasta_arquivos = sys.argv[1]
    
    # Validação: pasta existe?
    if not os.path.exists(pasta_arquivos):
        print(json.dumps({
            "erro": f"Pasta não encontrada: {pasta_arquivos}",
            "dica": "Verifique se os PDFs foram enviados corretamente"
        }))
        sys.exit(1)
    
    # Validação: tem pelo menos um PDF?
    pdfs_na_pasta = [f for f in os.listdir(pasta_arquivos) if f.endswith('.pdf')]
    if not pdfs_na_pasta:
        print(json.dumps({
            "erro": "Nenhum arquivo PDF encontrado na pasta",
            "pasta": pasta_arquivos,
            "dica": "Certifique-se de enviar PO.pdf, QCI.pdf ou PLQ.pdf"
        }))
        sys.exit(1)
    
    try:
        # Executa extração
        dados_extraidos = extrair_dados_caixa(pasta_arquivos)
        
        # Adiciona metadados
        dados_extraidos["arquivos_processados"] = pdfs_na_pasta
        dados_extraidos["status"] = "sucesso"
        
        # Retorna JSON
        print(json.dumps(dados_extraidos, ensure_ascii=False, indent=2))
    
    except Exception as e:
        print(json.dumps({
            "erro": str(e),
            "tipo_erro": type(e).__name__,
            "status": "falha"
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()
