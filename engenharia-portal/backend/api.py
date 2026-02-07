#!/usr/bin/env python3
"""
API Backend para Geração de Peças Técnicas
Substitui o n8n por um servidor Python simples e direto
"""

from flask import Flask, request, jsonify
import json
import os
import sys
from datetime import datetime

app = Flask(__name__)

# Configurar caminhos
sys.path.insert(0, '/data/python_scripts')

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({"status": "ok", "service": "engenharia-api"}), 200

@app.route('/gerar-etp', methods=['POST'])
def gerar_documento():
    """
    Endpoint principal que processa:
    1. Extração de PDFs (se modo automático)
    2. Geração de texto com IA
    3. Criação do documento .docx
    """
    try:
        dados = request.json
        app.logger.info(f"Requisição recebida: {dados.get('tipo_peca', 'N/A')}")
        
        # Passo 1: Verificar modo de extração
        modo_extracao = dados.get('modo_extracao', 'manual')
        
        if modo_extracao == 'automatico':
            # Modo automático: extrair dados dos PDFs
            app.logger.info("Modo automático - extraindo dados de PDFs")
            try:
                from extrator_caixa import extrair_dados_pdfs
                pasta_uploads = dados.get('pasta_uploads', '/data/uploads')
                dados_extraidos = extrair_dados_pdfs(pasta_uploads)
                
                # Merge dados extraídos com dados do formulário
                dados_merged = {
                    'tipo_peca': dados.get('tipo_peca'),
                    'OBJETO': dados_extraidos.get('OBJETO', dados.get('objeto', '')),
                    'VALOR_GLOBAL': dados_extraidos.get('VALOR_GLOBAL', dados.get('valor_estimado', '')),
                    'VALOR_REPASSE': dados_extraidos.get('VALOR_REPASSE', '0,00'),
                    'VALOR_CONTRAPARTIDA': dados_extraidos.get('VALOR_CONTRAPARTIDA', '0,00'),
                    'AREA_TOTAL': dados_extraidos.get('AREA_TOTAL', '0,00'),
                    'BDI': dados_extraidos.get('BDI', '0,00'),
                    'DATA_BASE': dados_extraidos.get('DATA_BASE', ''),
                    'LOCAL': dados_extraidos.get('LOCAL', 'Nova Petrópolis/RS'),
                    'justificativa': dados.get('justificativa', ''),
                    'setor': dados.get('setor', ''),
                    'responsavel': dados.get('responsavel', ''),
                    'arquivos_processados': dados_extraidos.get('arquivos_processados', [])
                }
            except Exception as e:
                app.logger.error(f"Erro na extração de PDFs: {e}")
                return jsonify({
                    "status": "erro",
                    "mensagem": f"Erro ao extrair PDFs: {str(e)}"
                }), 500
        else:
            # Modo manual: usar apenas dados do formulário
            app.logger.info("Modo manual - usando dados do formulário")
            dados_merged = {
                'tipo_peca': dados.get('tipo_peca'),
                'OBJETO': dados.get('objeto', ''),
                'VALOR_GLOBAL': dados.get('valor_estimado', ''),
                'VALOR_REPASSE': '0,00',
                'VALOR_CONTRAPARTIDA': '0,00',
                'AREA_TOTAL': '0,00',
                'BDI': '0,00',
                'DATA_BASE': '',
                'LOCAL': 'Nova Petrópolis/RS',
                'justificativa': dados.get('justificativa', ''),
                'setor': dados.get('setor', ''),
                'responsavel': dados.get('responsavel', ''),
                'arquivos_processados': []
            }
        
        # Passo 2: Gerar texto com IA (OpenAI)
        app.logger.info("Gerando texto com IA...")
        try:
            from openai import OpenAI
            
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY não configurada")
            
            client = OpenAI(api_key=api_key)
            
            prompt = f"""Redija justificativa técnica para {dados_merged['tipo_peca'].upper()}. 

Objeto: {dados_merged['OBJETO']}
Valor estimado: R$ {dados_merged['VALOR_GLOBAL']}
Área total: {dados_merged['AREA_TOTAL']} m²
Local: {dados_merged['LOCAL']}
Informações adicionais: {dados_merged['justificativa']}

Use linguagem formal, impessoal e técnica, conforme Lei 14.133/2021. Foque no interesse público e economicidade."""
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": "Você é um Engenheiro Civil Sênior especializado em redigir documentos técnicos para licitações públicas conforme Lei 14.133/2021."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            texto_ia = response.choices[0].message.content
            app.logger.info(f"Texto IA gerado: {len(texto_ia)} caracteres")
            
        except Exception as e:
            app.logger.error(f"Erro ao gerar texto IA: {e}")
            # Fallback: usar justificativa do formulário
            texto_ia = dados_merged['justificativa']
        
        # Passo 3: Gerar documento .docx
        app.logger.info("Gerando documento .docx...")
        try:
            from gerar_peca import gerar_documento
            
            payload = {
                'tipo': dados_merged['tipo_peca'],
                'dados': {
                    'OBJETO': dados_merged['OBJETO'],
                    'JUSTIFICATIVA': texto_ia,
                    'VALOR_GLOBAL': dados_merged['VALOR_GLOBAL'],
                    'VALOR_REPASSE': dados_merged['VALOR_REPASSE'],
                    'VALOR_CONTRAPARTIDA': dados_merged['VALOR_CONTRAPARTIDA'],
                    'AREA_TOTAL': dados_merged['AREA_TOTAL'],
                    'BDI': dados_merged['BDI'],
                    'DATA_BASE': dados_merged['DATA_BASE'],
                    'LOCAL': dados_merged['LOCAL'],
                    'SETOR': dados_merged['setor'],
                    'RESPONSAVEL': dados_merged['responsavel']
                }
            }
            
            resultado = gerar_documento(payload)
            
            if resultado and resultado.get('status') == 'sucesso':
                app.logger.info(f"Documento gerado: {resultado.get('arquivo')}")
                return jsonify({
                    "status": "sucesso",
                    "arquivo": resultado.get('arquivo'),
                    "path": resultado.get('path', '/data/output'),
                    "timestamp": datetime.now().isoformat(),
                    "modo_extracao": modo_extracao,
                    "arquivos_pdf_processados": dados_merged.get('arquivos_processados', [])
                }), 200
            else:
                raise Exception(f"Erro na geração: {resultado}")
                
        except Exception as e:
            app.logger.error(f"Erro ao gerar documento: {e}")
            return jsonify({
                "status": "erro",
                "mensagem": f"Erro ao gerar documento: {str(e)}"
            }), 500
    
    except Exception as e:
        app.logger.error(f"Erro geral: {e}")
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro no processamento: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Rodar servidor
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
