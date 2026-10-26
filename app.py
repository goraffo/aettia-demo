import streamlit as st
import base64
from pathlib import Path

st.set_page_config(
    page_title="Aettia",
    page_icon="assets/Logo Aettia.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ METADATOS PARA COMPARTIR (WhatsApp/Redes) ============
st.markdown("""
    <head>
        <meta property="og:title" content="Aettia - Hot Skills">
        <meta property="og:description" content="Plataforma de análisis de habilidades clave en oferta académica y demanda laboral en Latinoamérica.">
        <meta property="og:image" content="https://www.aettia.com/assets/Logo%20Aettia.png">
        <meta property="og:type" content="website">
    </head>
""", unsafe_allow_html=True)

from utils.estilos import aplicar_estilos
aplicar_estilos()

# ============ LOGO ============
def _logo_base64():
    ruta = Path(__file__).parent / "assets" / "Logo Aettia.png"
    if ruta.exists():
        return base64.b64encode(ruta.read_bytes()).decode()
    return None

# ============ LEER QUERY PARAMS PARA NAVEGACIÓN ============
if "vista" not in st.session_state:
    st.session_state.vista = "home"

params = st.query_params
if "vista" in params:
    nueva_vista = params.get("vista")
    if nueva_vista in ("talento", "curricular", "home"):
        # Log de navegación (solo si cambia de vista)
        if nueva_vista != st.session_state.vista:
            from utils.tracking import log_evento
            log_evento(accion="navegar", vista=nueva_vista)

        st.session_state.vista = nueva_vista
        if nueva_vista == "talento":
            st.session_state.talento_paso = 1
            st.session_state.dominios_paso = 1
            st.session_state.pop("puestos_input", None)
            st.session_state.pop("talento_params", None)
            st.session_state.pop("dominios_params", None)
        elif nueva_vista == "curricular":
            st.session_state.escuelas_paso = 1
            st.session_state.pop("escuelas_params", None)
        st.query_params.clear()
        st.rerun()

# ============ NAV SUPERIOR CON LOGO ============
logo_b64 = _logo_base64()

if logo_b64:
    logo_html = f'<img src="data:image/png;base64,{logo_b64}" alt="Aettia" style="height:42px;">'
else:
    logo_html = '<div class="aettia-logo">AETTIA</div>'

st.markdown(f"""
<div class="aettia-nav">
    <div>{logo_html}</div>
    <div></div>
</div>
""", unsafe_allow_html=True)

# ============ CONTENIDO SEGÚN VISTA ============
if st.session_state.vista == "home":
    # ===== HERO =====
    st.markdown("""
    <div style="
        min-height: 300px;
        background: linear-gradient(to bottom, #FFFFFF 50%, #00D1C3 100%);
        margin: 0 -80px 5px -80px;
        padding: 40px 120px;
        box-sizing: border-box;
    ">
        <div style="
            font-family: 'Figtree', sans-serif;
            font-weight: 700;
            font-size: 56px;
            color: #333333;
            letter-spacing: 2px;
            line-height: 1.1;
        ">Hot Skills</div>
        <div style="
            width: 80px;
            height: 4px;
            background-color: #333333;
            margin-top: 20px;
            margin-bottom: 20px;
        "></div>
        <div style="
            font-family: 'Figtree', sans-serif;
            font-weight: 600;
            font-size: 16px;
            color: #333333;
            line-height: 1.5;
            max-width: 600px;
        ">AETTIA no es un directorio de cursos ni un portal de empleo. Es una plataforma de inteligencia que responde a una pregunta que nadie más responde:<br><br>¿Qué skills demandan las empresas y qué programas las están formando?</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="cards-grid">
        <a href="?vista=talento" target="_self" class="card-activa">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF" width="56" height="56">
                <circle cx="12" cy="7" r="4"/>
                <path d="M12 13c-3.87 0-7 2.13-7 4.75V20h14v-2.25C19 15.13 15.87 13 12 13z"/>
            </svg>
            <div class="card-titulo-grande">ANALISTA DE TALENTO</div>
            <div class="card-subtitulo-secundario">Conoce las skills más demandadas</div>
        </a>
        <a href="?vista=curricular" target="_self" class="card-activa">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#FFFFFF" width="56" height="56">
                <path d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3z"/>
                <path d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/>
            </svg>
            <div class="card-titulo-grande">DISEÑADOR CURRICULAR</div>
            <div class="card-subtitulo-secundario">Conoce los productos académicos ofertados</div>
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div class="cards-grid">
        <div class="card-inactiva">
            <div class="card-titulo">REPORTES</div>
            <div class="card-subtitulo">PRÓXIMAMENTE</div>
        </div>
        <div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nosotros-footer">
        ─────────────────────────────<br><br>
        Aettia es una plataforma de análisis no oficial para el mercado de educación continua y oferta laboral en Latinoamérica.<br>
        Toda la información presentada se basa en fuentes de acceso público y puede no ser completamente precisa. 
        Aettia no está afiliada a ninguna organización educativa ni portal de empleo.
    </div>
    """, unsafe_allow_html=True)


elif st.session_state.vista == "talento":
    st.markdown('<a href="?vista=home" target="_self" class="btn-volver">← Volver al inicio</a>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    from vistas import analista_talento
    analista_talento.render()


elif st.session_state.vista == "curricular":
    st.markdown('<a href="?vista=home" target="_self" class="btn-volver">← Volver al inicio</a>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    from vistas import disenador_curricular
    disenador_curricular.render()