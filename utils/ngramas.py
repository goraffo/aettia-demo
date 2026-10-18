"""
Extracción de n-gramas (ahora consulta la tabla precalculada).
"""
from collections import defaultdict
from sqlalchemy import text
import pandas as pd


def extraer_y_clasificar(df_anuncios, skill_filtro=None, engine=None, excluir=None):
    """
    Consulta los n-gramas precalculados en anuncio_ngramas y los cruza con clasificacion_gramas.
    """
    excluir_set = set(excluir) if excluir else set()
    
    if df_anuncios.empty or engine is None:
        return pd.DataFrame()

    ids_topic = df_anuncios['id_topic'].dropna().unique().tolist()
    if not ids_topic:
        return pd.DataFrame()

    # 1. Traer los ngramas precalculados de los anuncios filtrados
    # Para no saturar la memoria, lo hacemos por lotes (o directo si es menor a 50k)
    placeholders = ', '.join([f':id_{i}' for i in range(len(ids_topic))])
    params = {f'id_{i}': v for i, v in enumerate(ids_topic)}
    
    query_ngramas = f"""
        SELECT id_topic, ngrama 
        FROM anuncio_ngramas 
        WHERE id_topic IN ({placeholders})
    """
    
    try:
        df_ngramas = pd.read_sql(text(query_ngramas), engine, params=params)
    except Exception as e:
        print(f"Error consultando ngramas: {e}")
        return pd.DataFrame()

    if df_ngramas.empty:
        return pd.DataFrame()

    # 2. Agrupar para contar anuncios, puestos y empresas (igual que antes)
    # Pero ahora es instantáneo porque solo iteramos sobre los ngramas encontrados
    ngram_ids = defaultdict(set)
    ngram_puestos = defaultdict(set)
    ngram_empresas = defaultdict(set)
    
    # Crear diccionario rápido de anuncios
    dict_anuncios = df_anuncios.set_index('id_topic')[['c_titulo', 'empresa']].to_dict('index')

    for _, row in df_ngramas.iterrows():
        ng = row['ngrama']
        if ng in excluir_set:
            continue
            
        id_t = row['id_topic']
        ngram_ids[ng].add(id_t)
        
        if id_t in dict_anuncios:
            ngram_puestos[ng].add(dict_anuncios[id_t]['c_titulo'])
            ngram_empresas[ng].add(dict_anuncios[id_t]['empresa'])

    # 3. Cruzar con clasificacion_gramas
    clasif = pd.read_sql(text("SELECT ngrama, tipo FROM clasificacion_gramas"), engine)
    mapa_tipo = dict(zip(clasif['ngrama'], clasif['tipo']))

    resultados = []
    for ng, ids in ngram_ids.items():
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