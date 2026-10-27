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

        .aettia-nav {
            background-color: #FBB03B;
            padding: 14px 30px;
            margin: -80px -80px 30px -80px;
            display: flex;
            justify-content: space-between;
            align-items: center;
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
            margin-left: 80px;
        }

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

        /* Grid de cards clickeables */
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

        /* Botón "Volver al inicio" como link */
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
        .card-icono { font-size: 42px; }

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

        /* Chips del multiselect en azul */
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

        /* Chips verdes (para Diseñador Curricular) */
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

        /* Labels de todos los filtros en azul */
        label[data-testid="stWidgetLabel"] p,
        .stTextInput label p,
        .stSelectbox label p,
        .stDateInput label p,
        .stMultiSelect label p {
            color: #009ADE !important;
            font-family: 'Figtree', sans-serif !important;
            font-weight: 600 !important;
        }

        /* Labels verdes en Diseñador Curricular */
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

        @media (max-width: 768px) {
            .aettia-nav {
                margin: -80px -20px 30px -20px;
                padding: 10px 15px;
            }
            .aettia-nav img {
                height: 30px !important;
                margin-left: 40px;
            }
        }
    </style>
    """, unsafe_allow_html=True)