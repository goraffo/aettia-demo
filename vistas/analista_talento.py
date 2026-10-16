"""
Vista: Analista de Talento
Contiene 3 pestañas: PUESTOS, DOMINIOS, SKILLS.
"""
import streamlit as st
from datetime import datetime, date
from sqlalchemy import text
import pandas as pd

from utils.db import get_engine
from utils.filtros import construir_filtros_puestos
from utils.ngramas import extraer_y_clasificar
from utils.tracking import log_evento, buscar_con_metricas

MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

UMBRAL_BUSQUEDA_EXTENSA = 1000


def _formato_fecha(fecha):
    if not fecha:
        return None
    return f"{fecha.day:02d} de {MESES_ES[fecha.month]} de {fecha.year}"


def _formato_mes_anio(fecha):
    if not fecha:
        return None
    return f"{MESES_ES[fecha.month]} de {fecha.year}"


def render():
    if "talento_paso" not in st.session_state:
        st.session_state.talento_paso = 1

    st.markdown('<div class="estado-nav">Data  >  Analista de Talento</div>', unsafe_allow_html=True)

    tabs = st.tabs(["PUESTOS", "DOMINIOS", "SKILLS"])

    with tabs[0]:
        if st.session_state.talento_paso == 1:
            _render_paso_1()
        else:
            _render_paso_2()
    with tabs[1]:
        from vistas import analista_talento_dominios
        analista_talento_dominios.render()
    with tabs[2]:
        from vistas import analista_talento_skills
        analista_talento_skills.render()


def _render_paso_1():
    engine = get_engine()

    if st.session_state.get("limpiar_fecha_desde_flag"):
        st.session_state.fecha_desde_widget = None
        st.session_state.limpiar_fecha_desde_flag = False
    
    if st.session_state.get("limpiar_fecha_hasta_flag"):
        st.session_state.fecha_hasta_widget = None
        st.session_state.limpiar_fecha_hasta_flag = False

    prev = st.session_state.get('talento_params', {})
    prev_puestos = prev.get('puestos', [])

    st.markdown('<div class="filtro-label">Puesto de trabajo</div>', unsafe_allow_html=True)

    if st.session_state.get("reset_puestos"):
        st.session_state.puestos_multiselect = prev_puestos
        st.session_state.reset_puestos = False

    if "puestos_multiselect" not in st.session_state:
        st.session_state.puestos_multiselect = prev_puestos

    puestos = st.multiselect(
        "Puesto de trabajo",
        options=[],
        accept_new_options=True,
        placeholder="Escribe un puesto y pulsa Enter",
        label_visibility="collapsed",
        key="puestos_multiselect"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        pais_idx = ["Todos", "Peru", "Chile", "Argentina"].index(prev.get('pais', 'Peru')) if prev.get('pais', 'Peru') in ["Todos", "Peru", "Chile", "Argentina"] else 1
        pais = st.selectbox("País", ["Todos", "Peru", "Chile", "Argentina"], index=pais_idx, key="pue_pais")
        
        skill_idx = ["Todas", "habilidad tecnica", "habilidad blanda"].index(prev.get('skill', 'Todas')) if prev.get('skill', 'Todas') in ["Todas", "habilidad tecnica", "habilidad blanda"] else 0
        skill = st.selectbox("Tipo de habilidad", ["Todas", "habilidad tecnica", "habilidad blanda"], index=skill_idx, key="pue_skill")
        
        fecha_desde_prev = prev.get('fecha_desde')
        col_fd1, col_fd2 = st.columns([0.8, 0.2])
        with col_fd1:
            fecha_desde = st.date_input(
                "Desde",
                value=pd.to_datetime(fecha_desde_prev).date() if fecha_desde_prev else None,
                key="fecha_desde_widget"
            )
        with col_fd2:
            if fecha_desde:
                if st.button("✕", key="limpiar_desde", help="Limpiar fecha"):
                    st.session_state.limpiar_fecha_desde_flag = True
                    st.rerun()

    with col2:
        zona_idx = ["Todas", "Capital", "Provincias"].index(prev.get('zona', 'Todas')) if prev.get('zona', 'Todas') in ["Todas", "Capital", "Provincias"] else 0
        zona = st.selectbox("Ubicación", ["Todas", "Capital", "Provincias"], index=zona_idx, key="pue_zona")
        
        dominios_lista = ["Todos"] + _obtener_dominios(engine)
        dominio_prev = prev.get('dominio', 'Todos')
        dominio_idx = dominios_lista.index(dominio_prev) if dominio_prev in dominios_lista else 0
        dominio = st.selectbox("Dominio temático", dominios_lista, index=dominio_idx, key="pue_dominio")
        
        fecha_hasta_prev = prev.get('fecha_hasta')
        col_fh1, col_fh2 = st.columns([0.8, 0.2])
        with col_fh1:
            fecha_hasta = st.date_input(
                "Hasta",
                value=pd.to_datetime(fecha_hasta_prev).date() if fecha_hasta_prev else None,
                key="fecha_hasta_widget"
            )
        with col_fh2:
            if fecha_hasta:
                if st.button("✕", key="limpiar_hasta", help="Limpiar fecha"):
                    st.session_state.limpiar_fecha_hasta_flag = True
                    st.rerun()

    limite = st.selectbox("Límite de resultados", [15], index=0, disabled=True, key="pue_limite")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("BUSCAR", key="buscar_talento", use_container_width=True):
        if not puestos:
            st.warning("Ingresa al menos un puesto de trabajo.")
            return

        st.session_state.talento_params = {
            'puestos': puestos,
            'pais': pais,
            'zona': zona,
            'skill': skill,
            'dominio': dominio,
            'fecha_desde': fecha_desde.strftime('%Y-%m-%d') if fecha_desde else None,
            'fecha_hasta': fecha_hasta.strftime('%Y-%m-%d') if fecha_hasta else None,
            'limite': limite,
        }
        st.session_state.talento_paso = 2
        st.rerun()


def _render_paso_2():
    engine = get_engine()
    params = st.session_state.get('talento_params', {})

    lineas_resumen = ["<div>Mostrando resultados para:</div>"]
    lineas_resumen.append(f"<div><b>Puesto de trabajo:</b> {', '.join(params.get('puestos', []))}</div>")
    if params.get('pais') and params.get('pais') != "Todos":
        lineas_resumen.append(f"<div><b>País:</b> {params.get('pais')}</div>")
    if params.get('zona') and params.get('zona') != "Todas":
        lineas_resumen.append(f"<div><b>Ubicación:</b> {params.get('zona')}</div>")
    if params.get('dominio') and params.get('dominio') != "Todos":
        lineas_resumen.append(f"<div><b>Dominio temático:</b> {params.get('dominio')}</div>")
    if params.get('skill') and params.get('skill') != "Todas":
        lineas_resumen.append(f"<div><b>Tipo de habilidad:</b> {params.get('skill')}</div>")
    if params.get('fecha_desde'):
        fd = pd.to_datetime(params['fecha_desde']).date()
        lineas_resumen.append(f"<div><b>Desde:</b> {_formato_fecha(fd)}</div>")
    if params.get('fecha_hasta'):
        fh = pd.to_datetime(params['fecha_hasta']).date()
        lineas_resumen.append(f"<div><b>Hasta:</b> {_formato_fecha(fh)}</div>")
    lineas_resumen.append(f"<div><b>Límite de resultados:</b> {params.get('limite')}</div>")

    st.markdown(f'<div class="resumen-busqueda">{"".join(lineas_resumen)}</div>', unsafe_allow_html=True)

    if st.button("CAMBIAR BÚSQUEDA", key="cambiar_busqueda", use_container_width=True):
        st.session_state.talento_paso = 1
        st.session_state.reset_puestos = True
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    params_sql = {}
    where, params_sql = construir_filtros_puestos(
        puestos=params.get('puestos'),
        pais=params.get('pais'),
        zona=params.get('zona'),
        dominio=params.get('dominio'),
        fecha_desde=params.get('fecha_desde'),
        fecha_hasta=params.get('fecha_hasta'),
        params_dict=params_sql
    )

    query = f"""
    SELECT id_topic, c_titulo, c_detalle, empresa, pais, dominio
    FROM topics_anuncios
    WHERE {where}
    """

    filtros_para_log = {
        'puestos': params.get('puestos'),
        'pais': params.get('pais'),
        'zona': params.get('zona'),
        'dominio': params.get('dominio'),
        'skill': params.get('skill'),
        'fecha_desde': params.get('fecha_desde'),
        'fecha_hasta': params.get('fecha_hasta'),
    }

    df = buscar_con_metricas(
        engine=engine,
        query=query,
        params=params_sql,
        filtros=filtros_para_log,
        vista="analista",
        pestana="puestos",
    )

    if df is None:
        return

    if df.empty:
        st.markdown('<div class="sin-resultados">No se encontraron resultados</div>', unsafe_allow_html=True)
        return

    if len(df) > UMBRAL_BUSQUEDA_EXTENSA:
        segundos = int(len(df) / 1000 * 30)
        minutos_min = max(1, segundos // 60)
        minutos_max = minutos_min + 1
        st.info(f"🔍 Búsqueda extensa detectada: estamos procesando {len(df):,} anuncios. "
                f"Esto puede tomar entre {minutos_min} y {minutos_max} minutos. Gracias por la paciencia...")

    with st.spinner("Analizando habilidades..."):
        df_gramas = extraer_y_clasificar(
            df,
            skill_filtro=params.get('skill'),
            engine=engine
        )

    if df_gramas.empty:
        st.markdown('<div class="sin-resultados">No se encontraron resultados</div>', unsafe_allow_html=True)
        return

    df_gramas = df_gramas.head(params.get('limite', 15))

    rango = pd.read_sql(text(f"""
        SELECT 
            MIN(c_yr * 100 + CAST(c_mes AS INTEGER)) as periodo_min,
            MAX(c_yr * 100 + CAST(c_mes AS INTEGER)) as periodo_max
        FROM topics_anuncios
        WHERE {where}
    """), engine, params=params_sql)
    
    periodo_min = int(rango['periodo_min'][0])
    periodo_max = int(rango['periodo_max'][0])
    
    fecha_min = date(periodo_min // 100, periodo_min % 100, 1)
    fecha_max = date(periodo_max // 100, periodo_max % 100, 1)

    st.markdown("### RESULTADOS PARA PUESTOS DE TRABAJO")

    col1, col2 = st.columns([0.75, 0.25])
    with col1:
        st.markdown(f"""
        <div class="barra-nota">
            Nota: Los resultados mostrados están basados en anuncios laborales entre {_formato_mes_anio(fecha_min)} y {_formato_mes_anio(fecha_max)}.
        </div>
        """, unsafe_allow_html=True)
    with col2:
        csv = df_gramas.to_csv(index=False).encode('utf-8-sig')
        if st.download_button(
            "⬇ DESCARGAR",
            data=csv,
            file_name=f"resultados_puestos_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        ):
            log_evento(
                accion="descargar",
                vista="analista",
                pestana="puestos",
                resultados=len(df_gramas),
            )

    st.markdown("<br>", unsafe_allow_html=True)

    def color_skill(val):
        if val == "habilidad tecnica":
            return 'color: #009ADE; font-weight: 600;'
        elif val == "habilidad blanda":
            return 'color: #FEBE85; font-weight: 600;'
        return ''

    def color_tipo(val):
        if val == "habilidad tecnica":
            return 'color: #009ADE; font-weight: 600;'
        elif val == "habilidad blanda":
            return 'color: #FEBE85; font-weight: 600;'
        return ''

    styled = df_gramas.style \
        .map(color_skill, subset=['skill']) \
        .map(color_tipo, subset=['tipo']) \
        .format({'anuncios': '{:,}', 'puestos': '{:,}', 'empresas': '{:,}'})

    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True
    )


def _obtener_dominios(engine):
    df = pd.read_sql(text("SELECT nombre FROM dominio WHERE activo = TRUE ORDER BY nombre"), engine)
    return df['nombre'].tolist()