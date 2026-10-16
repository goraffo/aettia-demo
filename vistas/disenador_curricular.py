"""
Vista: Diseñador Curricular
Contiene 3 pestañas: ESCUELAS, TIPOS, SKILLS.
"""
import streamlit as st


def render():
    st.markdown('<div class="estado-nav">Data  >  Diseñador Curricular</div>', unsafe_allow_html=True)

    tabs = st.tabs(["ESCUELAS", "TIPOS", "SKILLS"])

    with tabs[0]:
        from vistas import disenador_curricular_escuelas
        disenador_curricular_escuelas.render()

    with tabs[1]:
        from vistas import disenador_curricular_tipos
        disenador_curricular_tipos.render()

    with tabs[2]:
        from vistas import disenador_curricular_skills
        disenador_curricular_skills.render()