"""
Vista: Diseñador Curricular -> Pestaña SKILLS
Paso 1: filtros
Paso 2: resultados (productos que matchean la skill)
"""
import re
import unicodedata
import streamlit as st
from datetime import datetime, date
from sqlalchemy import text
import pandas as pd

from utils.db import get_engine
from utils.filtros import construir_filtros_skills_dc
from utils.tracking import log_evento, buscar_con_metricas


MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

MESES_NOMBRE_A_NUM = {v: k for k, v in MESES_ES.items()}

UMBRAL_BUSQUEDA_EXTENSA = 1000
LIMITE_RESULTADOS = 15


def _formato_fecha(fecha):
    if not fecha:
        return None
    return f"{fecha.day:02d} de {MESES_ES[fecha.month]} de {fecha.year}"


def _formato_mes_anio(periodo):
    if not periodo:
        return None
    anio = periodo // 100
    mes = periodo % 100
    return f"{MESES_ES[mes]} {anio}"


def _periodo_desde_mes_anio(texto):
    if not texto:
        return 0
    partes = texto.split()
    if len(partes) != 2:
        return 0
    mes = MESES_NOMBRE_A_NUM.get(partes[0], 0)
    anio = int(partes[1])
    return anio * 100 + mes


def _contar_temporadas(periodos):
    if not periodos:
        return 0
    periodos_ordenados = sorted(set(periodos))
    temporadas = 1
    for i in range(1, len(periodos_ordenados)):
        if periodos_ordenados[i] - periodos_ordenados[i-1] > 1:
            temporadas += 1
    return temporadas


def _primera_aparicion_ultima_temporada(periodos):
    """Devuelve el primer período de la última temporada (racha consecutiva)."""
    if not periodos:
        return None
    ordenados = sorted(set(periodos))
    inicio_ultima = ordenados[-1]
    for i in range(len(ordenados) - 1, 0, -1):
        if ordenados[i] - ordenados[i-1] > 1:
            inicio_ultima = ordenados[i]
            break
        inicio_ultima = ordenados[i-1]
    return inicio_ultima


def _normalizar_input(texto):
    """Minusculas, sin tildes, sin caracteres raros, espacios colapsados."""
    if not texto:
        return ""
    texto = str(texto).strip().lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto = re.sub(r'[^a-z0-9\s]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def render():
    if "dcs_paso" not in st.session_state:
        st.session_state.dcs_paso = 1

    if st.session_state.dcs_paso == 1:
        _render_paso_1()
    else:
        _render_paso_2()


def _render_paso_1():
    engine = get_engine()

    if st.session_state.get("dcs_limpiar_fecha_desde_flag"):
        st.session_state.dcs_fecha_desde_widget = None
        st.session_state.dcs_limpiar_fecha_desde_flag = False

    if st.session_state.get("dcs_limpiar_fecha_hasta_flag"):
        st.session_state.dcs_fecha_hasta_widget = None
        st.session_state.dcs_limpiar_fecha_hasta_flag = False

    prev = st.session_state.get('dcs_params', {})
    prev_skills = prev.get('skills_buscadas', [])

    st.markdown('<div class="filtro-label-verde">Skills</div>', unsafe_allow_html=True)

    if st.session_state.get("reset_dcs"):
        st.session_state.dcs_skills_multiselect = prev_skills
        st.session_state.reset_dcs = False

    if "dcs_skills_multiselect" not in st.session_state:
        st.session_state.dcs_skills_multiselect = prev_skills

    skills_buscadas_raw = st.multiselect(
        "Skills",
        options=[],
        accept_new_options=True,
        placeholder="Escribe una skill y pulsa Enter",
        label_visibility="collapsed",
        key="dcs_skills_multiselect"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        dominios_df = _obtener_dominios(engine)
        dominios_lista = ["Todos"] + dominios_df['nombre'].tolist()
        dominios_a_id = dict(zip(dominios_df['nombre'], dominios_df['id_dominio']))

        dominio_prev = prev.get('dominio', 'Todos')
        dominio_idx = dominios_lista.index(dominio_prev) if dominio_prev in dominios_lista else 0
        dominio = st.selectbox(
            "Dominio temático",
            dominios_lista,
            index=dominio_idx,
            key="dcs_dominio"
        )

    with col2:
        origen_prev = prev.get('origen', 'Todos')
        opciones_origen = ["Todos", "Peruano", "Extranjero"]
        origen_idx = opciones_origen.index(origen_prev) if origen_prev in opciones_origen else 0
        origen = st.selectbox(
            "Origen",
            opciones_origen,
            index=origen_idx,
            key="dcs_origen"
        )

    col3, col4 = st.columns(2)

    with col3:
        tipos_disponibles = _obtener_tipos(engine)
        tipos_prev = prev.get('tipos', tipos_disponibles)
        if not tipos_prev:
            tipos_prev = tipos_disponibles
        if st.session_state.get("reset_dcs_tipos"):
            st.session_state.dcs_tipos_multiselect = tipos_prev
            st.session_state.reset_dcs_tipos = False
        if "dcs_tipos_multiselect" not in st.session_state:
            st.session_state.dcs_tipos_multiselect = tipos_prev

        tipos = st.multiselect(
            "Tipo de producto",
            options=tipos_disponibles,
            accept_new_options=False,
            placeholder="Selecciona tipos",
            key="dcs_tipos_multiselect"
        )

    with col4:
        limite = st.selectbox(
            "Límite de resultados",
            [LIMITE_RESULTADOS],
            index=0,
            disabled=True,
            key="dcs_limite"
        )

    col5, col6 = st.columns(2)

    with col5:
        fecha_desde_prev = prev.get('fecha_desde')
        col_fd1, col_fd2 = st.columns([0.8, 0.2])
        with col_fd1:
            fecha_desde = st.date_input(
                "Desde",
                value=pd.to_datetime(fecha_desde_prev).date() if fecha_desde_prev else None,
                key="dcs_fecha_desde_widget"
            )
        with col_fd2:
            if fecha_desde:
                if st.button("✕", key="dcs_limpiar_desde", help="Limpiar fecha"):
                    st.session_state.dcs_limpiar_fecha_desde_flag = True
                    st.rerun()

    with col6:
        fecha_hasta_prev = prev.get('fecha_hasta')
        col_fh1, col_fh2 = st.columns([0.8, 0.2])
        with col_fh1:
            fecha_hasta = st.date_input(
                "Hasta",
                value=pd.to_datetime(fecha_hasta_prev).date() if fecha_hasta_prev else None,
                key="dcs_fecha_hasta_widget"
            )
        with col_fh2:
            if fecha_hasta:
                if st.button("✕", key="dcs_limpiar_hasta", help="Limpiar fecha"):
                    st.session_state.dcs_limpiar_fecha_hasta_flag = True
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("BUSCAR", key="buscar_skills_dc", use_container_width=True):
        if not skills_buscadas_raw:
            st.warning("Ingresa al menos una skill.")
            return

        skills_norm = []
        for s in skills_buscadas_raw:
            s_norm = _normalizar_input(s)
            if s_norm and s_norm not in skills_norm:
                skills_norm.append(s_norm)

        if not skills_norm:
            st.warning("Las skills ingresadas no son válidas.")
            return

        st.session_state.dcs_params = {
            'skills_buscadas': skills_norm,
            'skills_buscadas_original': skills_buscadas_raw,
            'dominio': dominio,
            'dominio_id': dominios_a_id.get(dominio) if dominio != "Todos" else None,
            'origen': origen,
            'tipos': tipos,
            'fecha_desde': fecha_desde.strftime('%Y-%m-%d') if fecha_desde else None,
            'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d') if fecha_hasta else None,
            'limite': limite,
        }
        st.session_state.dcs_paso = 2
        st.rerun()


def _render_paso_2():
    engine = get_engine()
    params = st.session_state.get('dcs_params', {})

    lineas_resumen = ["<div>Mostrando resultados para:</div>"]
    lineas_resumen.append(f"<div><b>Skills:</b> {', '.join(params.get('skills_buscadas_original', []))}</div>")
    if params.get('dominio') and params.get('dominio') != "Todos":
        lineas_resumen.append(f"<div><b>Dominio temático:</b> {params.get('dominio')}</div>")
    if params.get('origen') and params.get('origen') != "Todos":
        lineas_resumen.append(f"<div><b>Origen:</b> {params.get('origen')}</div>")

    tipos_actuales = params.get('tipos', [])
    tipos_disponibles = _obtener_tipos(engine)
    if tipos_actuales and set(tipos_actuales) != set(tipos_disponibles):
        lineas_resumen.append(f"<div><b>Tipo de producto:</b> {', '.join(tipos_actuales)}</div>")

    if params.get('fecha_desde'):
        fd = pd.to_datetime(params['fecha_desde']).date()
        lineas_resumen.append(f"<div><b>Desde:</b> {_formato_fecha(fd)}</div>")
    if params.get('fecha_hasta'):
        fh = pd.to_datetime(params['fecha_hasta']).date()
        lineas_resumen.append(f"<div><b>Hasta:</b> {_formato_fecha(fh)}</div>")
    lineas_resumen.append(f"<div><b>Límite de resultados:</b> {LIMITE_RESULTADOS}</div>")

    st.markdown(f'<div class="resumen-busqueda">{"".join(lineas_resumen)}</div>', unsafe_allow_html=True)

    if st.button("CAMBIAR BÚSQUEDA", key="cambiar_busqueda_skills_dc", use_container_width=True):
        st.session_state.dcs_paso = 1
        st.session_state.reset_dcs = True
        st.session_state.reset_dcs_tipos = True
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    params_sql = {}
    where, params_sql = construir_filtros_skills_dc(
        skills_buscadas=params.get('skills_buscadas'),
        dominio_id=params.get('dominio_id'),
        tipos=params.get('tipos'),
        origen=params.get('origen'),
        params_dict=params_sql
    )

    rango_desde_sql = ""
    rango_hasta_sql = ""

    if params.get('fecha_desde'):
        rango_desde_sql = "AND (pd.c_yr * 100 + CAST(pd.c_mes AS INTEGER)) >= :rango_desde"
        params_sql['rango_desde'] = int(params['fecha_desde'][:4]) * 100 + int(params['fecha_desde'][5:7])
    if params.get('fecha_hasta'):
        rango_hasta_sql = "AND (pd.c_yr * 100 + CAST(pd.c_mes AS INTEGER)) <= :rango_hasta"
        params_sql['rango_hasta'] = int(params['fecha_hasta'][:4]) * 100 + int(params['fecha_hasta'][5:7])

    rango_desde_sub = ""
    rango_hasta_sub = ""
    if params.get('fecha_desde'):
        rango_desde_sub = "AND (c_yr * 100 + CAST(c_mes AS INTEGER)) >= :rango_desde"
    if params.get('fecha_hasta'):
        rango_hasta_sub = "AND (c_yr * 100 + CAST(c_mes AS INTEGER)) <= :rango_hasta"

    subquery_fechas = ""
    if params.get('fecha_desde') or params.get('fecha_hasta'):
        subquery_fechas = f"""
            AND pm.id_master IN (
                SELECT id_master FROM producto_detecciones 
                WHERE 1=1 {rango_desde_sub} {rango_hasta_sub}
            )
        """

    query_master = f"""
    SELECT 
        pm.id_master,
        pm.producto AS nombre,
        pm.tipo,
        o.nombre AS escuela
    FROM producto_master pm
    JOIN organizacion o ON o.id_org = pm.id_org
    WHERE {where}
    {subquery_fechas}
    """

    filtros_para_log = {
        'skills_buscadas': params.get('skills_buscadas_original'),
        'dominio': params.get('dominio'),
        'origen': params.get('origen'),
        'tipos': params.get('tipos'),
        'fecha_desde': params.get('fecha_desde'),
        'fecha_hasta': params.get('fecha_hasta'),
    }

    df_master = buscar_con_metricas(
        engine=engine,
        query=query_master,
        params=params_sql,
        filtros=filtros_para_log,
        vista="curricular",
        pestana="skills",
        mensaje_spinner="Buscando productos...",
    )

    if df_master is None:
        return

    if df_master.empty:
        st.markdown('<div class="sin-resultados">No se encontraron resultados</div>', unsafe_allow_html=True)
        return

    ids_master = df_master['id_master'].tolist()

    placeholders = ', '.join([f':id_{i}' for i in range(len(ids_master))])
    params_det = {f'id_{i}': v for i, v in enumerate(ids_master)}

    if params.get('fecha_desde'):
        params_det['rango_desde'] = params_sql['rango_desde']
    if params.get('fecha_hasta'):
        params_det['rango_hasta'] = params_sql['rango_hasta']

    query_det = f"""
    SELECT 
        pd.id_master,
        pd.c_yr,
        pd.c_mes
    FROM producto_detecciones pd
    WHERE pd.id_master IN ({placeholders})
    ORDER BY pd.id_master, pd.c_yr, CAST(pd.c_mes AS INTEGER)
    """

    with st.spinner("Analizando apariciones..."):
        df_det = pd.read_sql(text(query_det), engine, params=params_det)

    resultados = []

    for _, row in df_master.iterrows():
        id_m = row['id_master']
        dets = df_det[df_det['id_master'] == id_m]

        if dets.empty:
            continue

        periodos = [(int(d['c_yr']) * 100 + int(d['c_mes'])) for _, d in dets.iterrows()]

        p_hasta = params_sql.get('rango_hasta') if params.get('fecha_hasta') else None

        periodos_rango = [p for p in periodos if p_hasta is None or p <= p_hasta]

        temporadas = _contar_temporadas(periodos_rango)
        primera = _primera_aparicion_ultima_temporada(periodos_rango)

        resultados.append({
            'nombre': row['nombre'],
            'escuela': row['escuela'],
            'tipo': row['tipo'],
            'desde': _formato_mes_anio(primera),
            'apariciones': temporadas
        })

    if not resultados:
        st.markdown('<div class="sin-resultados">No se encontraron resultados</div>', unsafe_allow_html=True)
        return

    df_final = pd.DataFrame(resultados)
    df_final['_periodo_orden'] = df_final['desde'].apply(_periodo_desde_mes_anio)
    df_final = df_final.sort_values('_periodo_orden', ascending=False).head(LIMITE_RESULTADOS)
    df_final = df_final.drop(columns=['_periodo_orden']).reset_index(drop=True)

    num_tipos = len(params.get('tipos', []))
    if num_tipos >= 2:
        df_final = df_final[['nombre', 'tipo', 'escuela', 'desde', 'apariciones']]
    else:
        df_final = df_final[['nombre', 'escuela', 'desde', 'apariciones']]

    st.markdown("### RESULTADOS PARA SKILLS")

    rango = pd.read_sql(text(f"""
        SELECT 
            MIN(pd.c_yr * 100 + CAST(pd.c_mes AS INTEGER)) as periodo_min,
            MAX(pd.c_yr * 100 + CAST(pd.c_mes AS INTEGER)) as periodo_max
        FROM producto_detecciones pd
        JOIN producto_master pm ON pm.id_master = pd.id_master
        WHERE {where}
        {subquery_fechas}
    """), engine, params=params_sql)

    if pd.notna(rango['periodo_min'][0]):
        fecha_min = _formato_mes_anio(int(rango['periodo_min'][0]))
        fecha_max = _formato_mes_anio(int(rango['periodo_max'][0]))
        texto_nota = f"Nota: Los resultados mostrados están basados en hallazgos entre {fecha_min} y {fecha_max}."
    else:
        texto_nota = "Nota: Sin hallazgos en el rango seleccionado."

    col1, col2 = st.columns([0.75, 0.25])
    with col1:
        st.markdown(f'''
        <div class="barra-nota">
            {texto_nota}<br>
            <b style="color: #85C776;">Columnas:</b> <b>desde</b> — mes en que inició su temporada más reciente. <b>apariciones</b> — número de temporadas en que estuvo activo.
        </div>
        ''', unsafe_allow_html=True)
    with col2:
        csv = df_final.to_csv(index=False).encode('utf-8-sig')
        if st.download_button(
            "⬇ DESCARGAR",
            data=csv,
            file_name=f"resultados_skills_dc_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        ):
            log_evento(
                accion="descargar",
                vista="curricular",
                pestana="skills",
                resultados=len(df_final),
            )

    st.markdown("<br>", unsafe_allow_html=True)

    styled = df_final.style \
        .set_properties(**{'color': '#FFFFFF'}) \
        .set_table_styles([
            {'selector': 'th', 'props': [('color', '#85C776'), ('font-weight', '700')]}
        ])

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True
    )


def _obtener_dominios(engine):
    df = pd.read_sql(text("SELECT id_dominio, nombre FROM dominio WHERE activo = TRUE ORDER BY nombre"), engine)
    return df


def _obtener_tipos(engine):
    df = pd.read_sql(text("SELECT DISTINCT tipo FROM producto_master WHERE tipo IS NOT NULL ORDER BY tipo"), engine)
    return df['tipo'].tolist()