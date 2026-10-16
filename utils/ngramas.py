"""
Extracción de n-gramas y cruce con clasificacion_gramas.
"""
import re
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from sqlalchemy import text
import pandas as pd

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

STOP_WORDS = set(stopwords.words('spanish'))
SPECIAL_CHARS = re.compile(r'[^\w\s]')


def is_valid_ngram(ngram):
    words = ngram.split()
    forbidden = {"y", "de", "a"}
    if SPECIAL_CHARS.search(ngram):
        return False
    if all(w in STOP_WORDS or re.match(r'^\d+$', w) for w in words):
        return False
    if words[0] in forbidden or words[-1] in forbidden:
        return False
    return True


def extract_ngrams(texto, n):
    if not isinstance(texto, str):
        return []
    tokens = word_tokenize(texto.lower())
    ngrams = [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
    return [ng for ng in ngrams if is_valid_ngram(ng)]


def extraer_y_clasificar(df_anuncios, skill_filtro=None, engine=None, excluir=None):
    """
    Extrae n-gramas de c_titulo + c_detalle y los cruza con clasificacion_gramas.
    Devuelve DataFrame con columnas: SKILL, tipo, anuncios, puestos, empresas
    
    Parametros:
    - skill_filtro: 'Todas' | 'habilidad tecnica' | 'habilidad blanda'
    - excluir: lista/set de n-gramas a excluir del ranking (ej: skills buscadas)
    """
    excluir_set = set(excluir) if excluir else set()

    ngram_ids = defaultdict(set)
    ngram_puestos = defaultdict(set)
    ngram_empresas = defaultdict(set)

    for _, row in df_anuncios.iterrows():
        id_b = row['id_topic']
        titulo = row['c_titulo']
        empresa = row['empresa']

        for col in ['c_titulo', 'c_detalle']:
            texto = row[col]
            if not isinstance(texto, str):
                continue
            for n in [1, 2, 3]:
                for ng in set(extract_ngrams(texto, n)):
                    ngram_ids[ng].add(id_b)
                    ngram_puestos[ng].add(titulo)
                    ngram_empresas[ng].add(empresa)

    # Cruce con clasificacion_gramas
    clasif = pd.read_sql(text("SELECT ngrama, tipo FROM clasificacion_gramas"), engine)
    mapa_tipo = dict(zip(clasif['ngrama'], clasif['tipo']))

    resultados = []
    for ng, ids in ngram_ids.items():
        if ng in excluir_set:
            continue
        tipo = mapa_tipo.get(ng)
        if tipo is None:
            continue
        if skill_filtro and skill_filtro not in (None, "Todas"):
            if tipo != skill_filtro:
                continue
        resultados.append({
            'skill': ng,
            'tipo': tipo,
            'anuncios': len(ids),
            'puestos': len(ngram_puestos[ng]),
            'empresas': len(ngram_empresas[ng])
        })

    df_resultado = pd.DataFrame(resultados)
    if not df_resultado.empty:
        df_resultado = df_resultado.sort_values('anuncios', ascending=False)
    return df_resultado