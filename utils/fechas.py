import streamlit as st
import pandas as pd
from sqlalchemy import text
from utils.db import get_engine

@st.cache_data(ttl=3600)
def obtener_rango_fechas_analista():
    """Devuelve (fecha_min, fecha_max) para los anuncios de empleo."""
    try:
        engine = get_engine()
        query = """
            SELECT 
                MIN(c_yr * 100 + c_mes) as min_periodo, 
                MAX(c_yr * 100 + c_mes) as max_periodo
            FROM topics_anuncios
            WHERE c_yr IS NOT NULL AND c_mes IS NOT NULL
        """
        df = pd.read_sql(text(query), engine)
        
        min_p = int(df['min_periodo'][0])
        max_p = int(df['max_periodo'][0])
        
        fecha_min = pd.to_datetime(f"{min_p // 100}-{min_p % 100:02d}-01").date()
        fecha_max = pd.to_datetime(f"{max_p // 100}-{max_p % 100:02d}-01").date()
        
        return fecha_min, fecha_max
    except Exception as e:
        print(f"⚠️ Error obteniendo fechas (Analista): {e}")
        # Fallback por si la tabla está vacía
        return pd.to_datetime('2020-01-01').date(), pd.to_datetime('2026-12-31').date()

@st.cache_data(ttl=3600)
def obtener_rango_fechas_disenador():
    """Devuelve (fecha_min, fecha_max) para las detecciones de productos."""
    try:
        engine = get_engine()
        query = """
            SELECT 
                MIN(c_yr * 100 + c_mes) as min_periodo, 
                MAX(c_yr * 100 + c_mes) as max_periodo
            FROM producto_detecciones
            WHERE c_yr IS NOT NULL AND c_mes IS NOT NULL
        """
        df = pd.read_sql(text(query), engine)
        
        min_p = int(df['min_periodo'][0])
        max_p = int(df['max_periodo'][0])
        
        fecha_min = pd.to_datetime(f"{min_p // 100}-{min_p % 100:02d}-01").date()
        fecha_max = pd.to_datetime(f"{max_p // 100}-{max_p % 100:02d}-01").date()
        
        return fecha_min, fecha_max
    except Exception as e:
        print(f"⚠️ Error obteniendo fechas (Diseñador): {e}")
        return pd.to_datetime('2020-01-01').date(), pd.to_datetime('2026-12-31').date()