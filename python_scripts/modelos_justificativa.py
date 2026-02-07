#!/usr/bin/env python3
"""
Busca modelos de justificativa em /data/modelos_justificativa.

- Lê PDFs (.pdf) via pdfplumber e textos (.md/.txt)
- Calcula TF-IDF e ranqueia por similaridade de cosseno
- Retorna top-k exemplos com trecho para few-shot

Uso CLI:
    python modelos_justificativa.py --query "pavimentacao asfaltica" --top_k 3 --base_dir /data/modelos_justificativa

O módulo pode ser importado por outros scripts (ex.: extrator_caixa) para sugerir justificativas.
"""

import argparse
import os
import re
import json
from typing import List, Dict

import pdfplumber
import yaml

# Stopwords simples em PT-BR para reduzir ruído
STOPWORDS_PT = set(
    "a o os as de da do das dos e em para por com sem sob sobre entre como ser que com no na nos nas".split()
)


def _limpar_texto(texto: str) -> str:
    if not texto:
        return ""
    texto = texto.replace("\r", " ").replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def _ler_pdf(caminho: str, max_chars: int = 8000) -> str:
    conteudo = []
    with pdfplumber.open(caminho) as pdf:
        for page in pdf.pages:
            txt = page.extract_text() or ""
            conteudo.append(txt)
            if sum(len(c) for c in conteudo) >= max_chars:
                break
    return _limpar_texto(" ".join(conteudo))[:max_chars]


def _ler_txt(caminho: str, max_chars: int = 8000) -> str:
    with open(caminho, "r", encoding="utf-8", errors="ignore") as f:
        return _limpar_texto(f.read())[:max_chars]


def _parse_metadados(conteudo: str) -> Dict:
    """Tenta ler front matter YAML no topo do arquivo."""
    if not conteudo.startswith("---"):
        return {}
    partes = conteudo.split("---", 2)
    if len(partes) < 3:
        return {}
    try:
        return yaml.safe_load(partes[1]) or {}
    except Exception:
        return {}


def carregar_modelos(base_dir: str) -> List[Dict]:
    modelos = []
    if not os.path.isdir(base_dir):
        return modelos

    for nome in sorted(os.listdir(base_dir)):
        caminho = os.path.join(base_dir, nome)
        if not os.path.isfile(caminho):
            continue

        ext = nome.lower().split(".")[-1]
        try:
            if ext == "pdf":
                texto = _ler_pdf(caminho)
                metadados = {}
            elif ext in {"md", "txt"}:
                bruto = _ler_txt(caminho)
                metadados = _parse_metadados(bruto)
                # remove front matter se existir
                if bruto.startswith("---"):
                    bruto = bruto.split("---", 2)[-1]
                texto = _limpar_texto(bruto)
            else:
                continue

            if texto:
                modelos.append({
                    "arquivo": nome,
                    "caminho": caminho,
                    "texto": texto,
                    "metadados": metadados
                })
        except Exception:
            # Ignora arquivo problemático para não quebrar o fluxo
            continue
    return modelos


def _tokenizar(texto: str) -> List[str]:
    tokens = re.findall(r"[\wáéíóúâêîôûãõç]+", texto.lower())
    return [t for t in tokens if len(t) > 2 and t not in STOPWORDS_PT]


def _vetor_tfidf(tokens_lista: List[List[str]]):
    """Calcula vetores tf-idf simples sem dependências externas."""
    from collections import Counter
    import math

    docs_tf = [Counter(toks) for toks in tokens_lista]
    df = Counter()
    for tf in docs_tf:
        df.update(tf.keys())

    n_docs = len(tokens_lista)
    idf = {term: math.log((n_docs + 1) / (df[term] + 1)) + 1 for term in df}

    vetores = []
    for tf in docs_tf:
        vetor = {term: (freq / sum(tf.values())) * idf.get(term, 0.0) for term, freq in tf.items()}
        vetores.append(vetor)
    return vetores


def _cosine(v1: Dict[str, float], v2: Dict[str, float]) -> float:
    import math
    inter = set(v1.keys()) & set(v2.keys())
    num = sum(v1[t] * v2[t] for t in inter)
    den1 = math.sqrt(sum(x * x for x in v1.values()))
    den2 = math.sqrt(sum(x * x for x in v2.values()))
    if den1 == 0 or den2 == 0:
        return 0.0
    return num / (den1 * den2)


def buscar_modelos_similares(query: str, base_dir: str = "/data/modelos_justificativa", top_k: int = 3) -> List[Dict]:
    if not query:
        return []
    modelos = carregar_modelos(base_dir)
    if not modelos:
        return []

    tokens_docs = [_tokenizar(m["texto"]) for m in modelos]
    tokens_query = _tokenizar(query)
    vetores = _vetor_tfidf(tokens_docs + [tokens_query])
    vet_query = vetores[-1]
    vet_docs = vetores[:-1]

    sims = [_cosine(vet_query, vdoc) for vdoc in vet_docs]
    idx_ordenados = sorted(range(len(sims)), key=lambda i: sims[i], reverse=True)

    resultados = []
    for idx in idx_ordenados[:top_k]:
        modelo = modelos[idx]
        score = float(round(sims[idx], 4))
        trecho = modelo["texto"][:1200]
        resultados.append({
            "arquivo": modelo["arquivo"],
            "score": score,
            "trecho": trecho,
            "metadados": modelo.get("metadados", {})
        })
    return resultados


def main_cli():
    parser = argparse.ArgumentParser(description="Busca modelos de justificativa por similaridade")
    parser.add_argument("--query", required=True, help="Texto/objeto para buscar modelos semelhantes")
    parser.add_argument("--top_k", type=int, default=3, help="Número de exemplos a retornar")
    parser.add_argument("--base_dir", default="/data/modelos_justificativa", help="Pasta onde estão os modelos")
    args = parser.parse_args()

    resultados = buscar_modelos_similares(args.query, base_dir=args.base_dir, top_k=args.top_k)
    print(json.dumps({"query": args.query, "resultados": resultados}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main_cli()
