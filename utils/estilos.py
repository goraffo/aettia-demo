"""
Estilos centralizados de Aettia.
"""
import streamlit as st


def aplicar_estilos():
    """Inyecta el CSS global de Aettia en la app."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&family=Oswald:wght@500;700&display=swap');

        .stApp { background-color: #333333; }
        section[data-testid="stSidebar"] { display: none; }
        header[data-testid="stHeader"] { background: transparent; }

        /* ==========================================
           BARRA DE NAVEGACIÓN
           ========================================== */
        .aettia-nav {
            background-color: #FBB03B;
            padding: 12px 80px 10px 80px;
            margin: -80px -80px 30px -80px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }
        .aettia-logo {
            font-family: 'Oswald', sans-serif;
            font-weight: 700;
            font-size: 32px;
            color: #333333;
            letter-spacing: 3px;
            margin: 0;
        }
        .aettia-nav img {
            margin-left: 0;
        }

        /* Botón de login dentro de la barra */
        .auth-slot {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .auth-nombre {
            font-family: 'Figtree', sans-serif;
            font-size: 13px;
            font-weight: 700;
            color: #333333;
        }
        .auth-btn {
            background: #333333;
            color: #FFFFFF !important;
            text-decoration: none !important;
            padding: 8px 14px;
            border-radius: 6px;
            font-family: 'Figtree', sans-serif;
            font-size: 13px;
            font-weight: 700;
            white-space: nowrap;
            transition: background-color 180ms ease;
        }
        .auth-btn:hover {
            background: #4D4D4D;
        }

        /* Diálogo de login */
        .auth-opcion {
            display: block;
            text-align: center;
            background: #333333;
            color: #FFFFFF !important;
            text-decoration: none !important;
            padding: 12px 16px;
            margin-bottom: 10px;
            border-radius: 6px;
            font-family: 'Figtree', sans-serif;
            font-size: 15px;
            font-weight: 700;
        }
        .auth-opcion:hover { background: #4D4D4D; }
        .auth-opcion-deshabilitado {
            display: block;
            text-align: center;
            background: #333333;
            color: #888888;
            padding: 12px 16px;
            margin-bottom: 10px;
            border-radius: 6px;
            font-family: 'Figtree', sans-serif;
            font-size: 15px;
            font-weight: 700;
            cursor: not-allowed;
        }
        .auth-nota {
            font-size: 12px;
            color: #888888;
            margin-top: 8px;
        }

        /* ==========================================
           HERO
           ========================================== */
        .aettia-hero {
            min-height: 300px;
            margin: 0 -80px 5px -80px;
            padding: 40px 80px;
            box-sizing: border-box;
            background-color: #3F3F3F;
            background-image:
                radial-gradient(800px 4000px at 88% 25%, rgba(0, 154, 222, 0.20), transparent 70%),
                radial-gradient(520px 300px at 98% 95%, rgba(133, 199, 118, 0.09), transparent 70%),
                radial-gradient(rgba(255, 255, 255, 0.05) 1px, transparent 1px),
                linear-gradient(to bottom, #454545, #3A3A3A);
            background-size: 100% 100%, 100% 100%, 22px 22px, 100% 100%;
            box-shadow:
                inset 0 1px 0 rgba(255, 255, 255, 0.08),
                inset 0 -30px 40px -30px rgba(0, 0, 0, 0.35),
                0 14px 24px -14px rgba(0, 0, 0, 0.55);
            border-width: 0 0 3px 0;
            border-style: solid;
            border-image: linear-gradient(to right, #FBB03B 0%, rgba(251, 176, 59, 0) 75%) 1;
        }

        div[data-testid="stVerticalBlock"] > div:has(.aettia-hero) {
            margin-top: -32px;
        }

        .hero-titulo {
            font-family: 'Figtree', sans-serif;
            font-weight: 700;
            font-size: 56px;
            color: #FFFFFF;
            letter-spacing: 2px;
            line-height: 1.1;
        }
        .hero-divisor {
            width: 80px;
            height: 4px;
            margin: 20px 0;
            background: linear-gradient(to right, #009ADE 50%, #85C776 50%);
        }
        .hero-texto {
            font-family: 'Figtree', sans-serif;
            font-weight: 600;
            font-size: 16px;
            color: #D6D6D6;
            line-height: 1.5;
            max-width: 600px;
        }
        .hero-gancho {
            font-family: 'Figtree', sans-serif;
            font-weight: 700;
            font-size: 20px;
            color: #FFFFFF;
            line-height: 1.4;
            max-width: 600px;
            margin-top: 14px;
            letter-spacing: 0.5px;
        }

        /* ==========================================
           COMPONENTES GENERALES
           ========================================== */
        .estado-nav {
            color: #FBB03B;
            font-family: 'Figtree', sans-serif;
            font-size: 14px;
            letter-spacing: 1px;
            margin-bottom: 20px;
        }
        .nosotros-footer {
            text-align: center;
            color: #777777;
            font-family: 'Figtree', sans-serif;
            font-size: 14px;
            padding: 60px 0 20px 0;
            letter-spacing: 1px;
        }

        /* Cards del home */
        .cards-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        .card-activa {
            background-color: #4D4D4D;
            border-radius: 8px;
            padding: 40px 30px;
            text-align: center;
            text-decoration: none !important;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 200px;
            transition: background-color 0.2s;
        }
        .card-activa:hover {
            background-color: #5A5A5A;
        }
        .card-activa .card-titulo-grande {
            font-family: 'Figtree', sans-serif;
            font-size: 22px;
            font-weight: 700;
            letter-spacing: 2px;
            color: #FBB03B;
            text-decoration: none !important;
        }
        .card-activa .card-subtitulo-secundario {
            font-family: 'Figtree', sans-serif;
            font-size: 14px;
            color: #CCCCCC;
            margin-top: 15px;
            letter-spacing: 1px;
            text-decoration: none !important;
        }
        .card-talento { border-top: 4px solid #009ADE; }
        .card-curricular { border-top: 4px solid #85C776; }
        .card-talento svg { fill: #009ADE; }
        .card-curricular svg { fill: #85C776; }

        .card-inactiva {
            background-color: #4D4D4D;
            border-radius: 8px;
            padding: 40px 30px;
            text-align: center;
            color: #888888;
            font-family: 'Figtree', sans-serif;
            height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .card-inactiva .card-titulo {
            font-family: 'Figtree', sans-serif;
            font-size: 22px;
            font-weight: 600;
            letter-spacing: 1px;
            margin-top: 15px;
            color: #888888;
        }
        .card-subtitulo {
            font-size: 13px;
            color: #AAAAAA;
            margin-top: 8px;
            letter-spacing: 1px;
        }

        /* Botón volver */
        .btn-volver {
            display: inline-block;
            background-color: #4D5D66;
            color: #FFFFFF !important;
            text-decoration: none !important;
            padding: 12px 24px;
            border-radius: 6px;
            font-family: 'Figtree', sans-serif;
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 1px;
        }
        .btn-volver:hover {
            background-color: #5A6B75;
            color: #FFFFFF !important;
        }

        /* Botones nativos de Streamlit */
        .stButton > button {
            background-color: #4D5D66;
            color: #FFFFFF;
            border: none;
            border-radius: 6px;
            padding: 14px 24px;
            font-family: 'Figtree', sans-serif;
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 1px;
            width: 100%;
            white-space: normal;
        }
        .stButton > button:hover {
            background-color: #5A6B75;
            color: #FFFFFF;
        }

        /* Labels de filtros */
        .filtro-label {
            font-family: 'Figtree', sans-serif;
            font-size: 14px;
            color: #009ADE;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }
        .filtro-label-verde {
            font-family: 'Figtree', sans-serif;
            font-size: 14px;
            color: #85C776;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }

        .resumen-busqueda {
            background-color: #DFDEDC;
            border-radius: 8px;
            padding: 20px;
            font-family: 'Figtree', sans-serif;
            font-size: 14px;
            color: #333333;
            line-height: 1.8;
        }
        .barra-nota {
            background-color: #4D4D4D;
            color: #DDDDDD;
            padding: 14px 20px;
            border-radius: 6px;
            font-family: 'Figtree', sans-serif;
            font-size: 13px;
        }
        .sin-resultados {
            font-family: 'Figtree', sans-serif;
            color: #AAAAAA;
            padding: 40px 0;
            text-align: center;
            font-size: 16px;
        }

        /* Chips de los filtros */
        span[data-tag] {
            background-color: #009ADE !important;
            color: #FFFFFF !important;
        }
        span[data-tag] span,
        span[data-tag] button,
        span[data-tag] svg {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
        }
        .st-key-esc_orgs_multiselect span[data-tag],
        .st-key-esc_skills_multiselect span[data-tag],
        .st-key-esc_tipos_multiselect span[data-tag],
        .st-key-tip_tipos_multiselect span[data-tag],
        .st-key-tip_skills_multiselect span[data-tag],
        .st-key-dcs_skills_multiselect span[data-tag],
        .st-key-dcs_tipos_multiselect span[data-tag] {
            background-color: #85C776 !important;
            color: #333333 !important;
        }
        .st-key-esc_orgs_multiselect span[data-tag] span,
        .st-key-esc_skills_multiselect span[data-tag] span,
        .st-key-esc_tipos_multiselect span[data-tag] span,
        .st-key-tip_tipos_multiselect span[data-tag] span,
        .st-key-tip_skills_multiselect span[data-tag] span,
        .st-key-dcs_skills_multiselect span[data-tag] span,
        .st-key-dcs_tipos_multiselect span[data-tag] span,
        .st-key-esc_orgs_multiselect span[data-tag] button,
        .st-key-esc_skills_multiselect span[data-tag] button,
        .st-key-esc_tipos_multiselect span[data-tag] button,
        .st-key-tip_tipos_multiselect span[data-tag] button,
        .st-key-tip_skills_multiselect span[data-tag] button,
        .st-key-dcs_skills_multiselect span[data-tag] button,
        .st-key-dcs_tipos_multiselect span[data-tag] button,
        .st-key-esc_orgs_multiselect span[data-tag] svg,
        .st-key-esc_skills_multiselect span[data-tag] svg,
        .st-key-esc_tipos_multiselect span[data-tag] svg,
        .st-key-tip_tipos_multiselect span[data-tag] svg,
        .st-key-tip_skills_multiselect span[data-tag] svg,
        .st-key-dcs_skills_multiselect span[data-tag] svg,
        .st-key-dcs_tipos_multiselect span[data-tag] svg {
            color: #333333 !important;
            fill: #333333 !important;
            stroke: #333333 !important;
        }

        /* Labels de filtros en azul */
        label[data-testid="stWidgetLabel"] p,
        .stTextInput label p,
        .stSelectbox label p,
        .stDateInput label p,
        .stMultiSelect label p {
            color: #009ADE !important;
            font-family: 'Figtree', sans-serif !important;
            font-weight: 600 !important;
        }

        /* Labels de filtros en verde (Diseñador Curricular) */
        .st-key-esc_dominio label p,
        .st-key-esc_orgs_multiselect label p,
        .st-key-esc_skills_multiselect label p,
        .st-key-esc_tipos_multiselect label p,
        .st-key-esc_fecha_desde_widget label p,
        .st-key-esc_fecha_hasta_widget label p,
        .st-key-esc_limite label p,
        .st-key-tip_dominio label p,
        .st-key-tip_origen label p,
        .st-key-tip_tipos_multiselect label p,
        .st-key-tip_skills_multiselect label p,
        .st-key-tip_fecha_desde_widget label p,
        .st-key-tip_fecha_hasta_widget label p,
        .st-key-tip_limite label p,
        .st-key-dcs_dominio label p,
        .st-key-dcs_origen label p,
        .st-key-dcs_skills_multiselect label p,
        .st-key-dcs_tipos_multiselect label p,
        .st-key-dcs_fecha_desde_widget label p,
        .st-key-dcs_fecha_hasta_widget label p,
        .st-key-dcs_limite label p {
            color: #85C776 !important;
        }

        /* Botones "X" para limpiar fechas */
        .st-key-limpiar_desde button,
        .st-key-limpiar_hasta button,
        .st-key-dom_limpiar_desde button,
        .st-key-dom_limpiar_hasta button,
        .st-key-esc_limpiar_desde button,
        .st-key-esc_limpiar_hasta button,
        .st-key-tip_limpiar_desde button,
        .st-key-tip_limpiar_hasta button,
        .st-key-skl_limpiar_desde button,
        .st-key-skl_limpiar_hasta button,
        .st-key-dcs_limpiar_desde button,
        .st-key-dcs_limpiar_hasta button {
            background-color: #4D5D66 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 0 !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            width: 40px !important;
            height: 40px !important;
            min-width: 40px !important;
        }
        .st-key-limpiar_desde button:hover,
        .st-key-limpiar_hasta button:hover,
        .st-key-dom_limpiar_desde button:hover,
        .st-key-dom_limpiar_hasta button:hover,
        .st-key-esc_limpiar_desde button:hover,
        .st-key-esc_limpiar_hasta button:hover,
        .st-key-tip_limpiar_desde button:hover,
        .st-key-tip_limpiar_hasta button:hover,
        .st-key-skl_limpiar_desde button:hover,
        .st-key-skl_limpiar_hasta button:hover,
        .st-key-dcs_limpiar_desde button:hover,
        .st-key-dcs_limpiar_hasta button:hover {
            background-color: #5A6B75 !important;
        }

        /* Botones en amarillo (Analista de Talento) */
        .st-key-buscar_talento button,
        .st-key-cambiar_busqueda button,
        .st-key-buscar_dominios button,
        .st-key-cambiar_busqueda_dominios button,
        .st-key-buscar_skills button,
        .st-key-cambiar_busqueda_skills button {
            background-color: #FBB03B !important;
            color: #333333 !important;
            font-family: 'Figtree', sans-serif !important;
        }
        .st-key-buscar_talento button p,
        .st-key-cambiar_busqueda button p,
        .st-key-buscar_dominios button p,
        .st-key-cambiar_busqueda_dominios button p,
        .st-key-buscar_skills button p,
        .st-key-cambiar_busqueda_skills button p {
            color: #333333 !important;
            font-family: 'Figtree', sans-serif !important;
            font-weight: 800 !important;
        }
        .st-key-buscar_talento button:hover,
        .st-key-cambiar_busqueda button:hover,
        .st-key-buscar_dominios button:hover,
        .st-key-cambiar_busqueda_dominios button:hover,
        .st-key-buscar_skills button:hover,
        .st-key-cambiar_busqueda_skills button:hover {
            background-color: #E5A033 !important;
            color: #333333 !important;
        }

        /* Botones en amarillo (Diseñador Curricular) */
        .st-key-buscar_escuelas button,
        .st-key-cambiar_busqueda_escuelas button,
        .st-key-buscar_tipos button,
        .st-key-cambiar_busqueda_tipos button,
        .st-key-buscar_skills_dc button,
        .st-key-cambiar_busqueda_skills_dc button {
            background-color: #FBB03B !important;
            color: #333333 !important;
            font-family: 'Figtree', sans-serif !important;
        }
        .st-key-buscar_escuelas button p,
        .st-key-cambiar_busqueda_escuelas button p,
        .st-key-buscar_tipos button p,
        .st-key-cambiar_busqueda_tipos button p,
        .st-key-buscar_skills_dc button p,
        .st-key-cambiar_busqueda_skills_dc button p {
            color: #333333 !important;
            font-family: 'Figtree', sans-serif !important;
            font-weight: 800 !important;
        }
        .st-key-buscar_escuelas button:hover,
        .st-key-cambiar_busqueda_escuelas button:hover,
        .st-key-buscar_tipos button:hover,
        .st-key-cambiar_busqueda_tipos button:hover,
        .st-key-buscar_skills_dc button:hover,
        .st-key-cambiar_busqueda_skills_dc button:hover {
            background-color: #E5A033 !important;
            color: #333333 !important;
        }

        /* ==========================================
           MÓVIL
           ========================================== */
        @media (max-width: 768px) {
            .aettia-hero {
                width: 100vw;
                margin: 0 0 5px calc(50% - 50vw);
                padding: 28px 20px;
                box-sizing: border-box;
            }
            div[data-testid="stVerticalBlock"] > div:has(.aettia-hero) {
                margin-top: -40px !important;
            }
            .hero-titulo {
                font-size: 40px;
            }
            .aettia-nav {
                box-sizing: border-box;
                width: 100vw;
                margin: -80px 0 30px calc(50% - 50vw);
                padding: 10px 15px;
            }
            .aettia-nav img {
                height: 30px !important;
                margin-left: 40px;
                margin-top: -4px;
            }
            .auth-btn {
                padding: 6px 10px;
                font-size: 12px;
            }
            .auth-nombre {
                display: none;
            }
            [data-testid="stMain"], [data-testid="stAppViewContainer"] {
                overflow-x: hidden;
            }
        }
    </style>
    """, unsafe_allow_html=True)