"""
Extracción de n-gramas (consulta la tabla precalculada).
"""
from collections import defaultdict
from sqlalchemy import text
import pandas as pd


def _clasificar_ngrama(texto):
    """Clasifica un n-grama por número de palabras."""
    if not isinstance(texto, str):
        return 'otro'
    espacios = texto.count(' ')
    if espacios == 0:
        return 'unigrama'
    elif espacios == 1:
        return 'bigrama'
    elif espacios == 2:
        return 'trigrama'
    return 'otro'


def extraer_y_clasificar(df_anuncios, skill_filtro=None, engine=None, excluir=None, limite=15):
    """
    Consulta los n-gramas precalculados en anuncio_ngramas y los cruza con clasificacion_gramas.
    Devuelve un DataFrame balanceado: 5 unigramas, 5 bigramas, 5 trigramas (o lo que haya).
    """
    excluir_set = set(excluir) if excluir else set()
    
    if df_anuncios.empty or engine is None:
        return pd.DataFrame()

    ids_topic = df_anuncios['id_topic'].dropna().unique().tolist()
    if not ids_topic:
        return pd.DataFrame()

    # 1. Traer los ngramas precalculados de los anuncios filtrados
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

    # 2. Agrupar para contar anuncios, puestos y empresas
    ngram_ids = defaultdict(set)
    ngram_puestos = defaultdict(set)
    ngram_empresas = defaultdict(set)
    
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
    if df_resultado.empty:
        return df_resultado

    # 4. Lógica de balanceo (Unigramas → Bigramas → Trigramas)
    df_resultado['n_grama'] = df_resultado['skill'].apply(_clasificar_ngrama)

    # Separar y ordenar cada grupo por anuncios (desc)
    unigramas = df_resultado[df_resultado['n_grama'] == 'unigrama'].sort_values('anuncios', ascending=False).to_dict('records')
    bigramas = df_resultado[df_resultado['n_grama'] == 'bigrama'].sort_values('anuncios', ascending=False).to_dict('records')
    trigramas = df_resultado[df_resultado['n_grama'] == 'trigrama'].sort_values('anuncios', ascending=False).to_dict('records')
    otros = df_resultado[df_resultado['n_grama'] == 'otro'].sort_values('anuncios', ascending=False).to_dict('records')

    # Cupos iniciales
    cupo = limite // 3
    resto = limite % 3
    cupo_uni = cupo + (1 if resto >= 1 else 0)
    cupo_bi = cupo + (1 if resto >= 2 else 0)
    cupo_tri = cupo

    seleccion_uni = []
    seleccion_bi = []
    seleccion_tri = []

    # Llenar Unigramas
    tomar = min(len(unigramas), cupo_uni)
    seleccion_uni = unigramas[:tomar]
    faltan_uni = cupo_uni - tomar

    # Llenar Bigramas (con lo que haya + relleno de unigramas faltantes)
    tomar_bi = min(len(bigramas), cupo_bi + faltan_uni)
    seleccion_bi = bigramas[:tomar_bi]
    faltan_bi = (cupo_bi + faltan_uni) - tomar_bi

    # Llenar Trigramas (con lo que haya + relleno de bigramas faltantes)
    tomar_tri = min(len(trigramas), cupo_tri + faltan_bi)
    seleccion_tri = trigramas[:tomar_tri]
    faltan_tri = (cupo_tri + faltan_bi) - tomar_tri

    # Si aún falta, rellenar con "otros"
    seleccion_otros = []
    if faltan_tri > 0 and otros:
        seleccion_otros = otros[:faltan_tri]

    # Unir en el orden visual: Unigramas → Bigramas → Trigramas → Otros
    df_final = pd.DataFrame(seleccion_uni + seleccion_bi + seleccion_tri + seleccion_otros)

    if df_final.empty:
        return df_final

    # Eliminar columna auxiliar y resetear índice
    df_final = df_final.drop(columns=['n_grama'], errors='ignore').reset_index(drop=True)

    return df_final