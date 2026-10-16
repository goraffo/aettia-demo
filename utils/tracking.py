"""
Módulo de tracking de métricas de uso.

Solo inserta si TRACKING=true en variables de entorno.
En local (TRACKING no definida o false), no se loguea nada.
"""
import os
import json
import uuid
import hashlib
import streamlit as st
from datetime import datetime
from sqlalchemy import text

from utils.db import get_engine

# ==== CONFIG ====
TRACKING_ACTIVO = os.getenv("TRACKING", "false").lower() == "true"
IP_SALT = os.getenv("IP_SALT", "aettia_default_salt")
ORIGEN = os.getenv("ORIGEN", "local")


# ==== UTILIDADES ====

def _hash_ip(ip):
    """Hashea la IP con SHA256 + salt. Devuelve None si no hay IP."""
    if not ip:
        return None
    return hashlib.sha256(f"{IP_SALT}{ip}".encode()).hexdigest()[:32]


def _obtener_session_id():
    """ID de sesión anónimo, vive mientras la pestaña esté abierta."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = hashlib.sha256(
            str(uuid.uuid4()).encode()
        ).hexdigest()[:16]
    return st.session_state.session_id


def _truncar(valor, max_len):
    """Trunca un string a max_len caracteres."""
    if valor is None:
        return None
    texto = str(valor)
    return texto[:max_len] if len(texto) > max_len else texto


def _empaquetar_filtros(filtros):
    """Convierte los filtros a JSON, truncando strings largos."""
    if not filtros:
        return None
    limpios = {}
    for k, v in filtros.items():
        if isinstance(v, str) and len(v) > 200:
            limpios[k] = v[:200] + "...[truncado]"
        elif isinstance(v, list):
            limpios[k] = [str(x)[:200] for x in v]
        else:
            limpios[k] = v
    return json.dumps(limpios, ensure_ascii=False, default=str)


# ==== FUNCIÓN PRINCIPAL ====

def log_evento(accion, vista=None, pestana=None, filtros=None,
               resultados=None, duracion_seg=None, error_msg=None):
    """
    Inserta un evento en metricas_user.

    Parámetros:
    - accion: 'navegar' | 'buscar' | 'descargar' | 'error'
    - vista: 'analista' | 'curricular' | 'home'
    - pestana: 'puestos' | 'skills' | 'dominios' | 'escuelas' | 'tipos'
    - filtros: dict con los filtros aplicados
    - resultados: cantidad de filas devueltas
    - duracion_seg: segundos que tardó la acción
    - error_msg: mensaje de error (solo si accion='error')

    No hace nada si TRACKING_ACTIVO es False.
    """
    if not TRACKING_ACTIVO:
        return

    try:
        engine = get_engine()
        ip = getattr(st.context, "ip_address", None)
        session_id = _obtener_session_id()

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO metricas_user
                (timestamp, session_id, ip_hash, vista, pestana, accion,
                 filtros_json, resultados, duracion_seg, error_msg, origen)
                VALUES
                (:timestamp, :session_id, :ip_hash, :vista, :pestana, :accion,
                 :filtros_json, :resultados, :duracion_seg, :error_msg, :origen)
            """), {
                "timestamp": datetime.now(),
                "session_id": session_id,
                "ip_hash": _hash_ip(ip),
                "vista": vista,
                "pestana": pestana,
                "accion": accion,
                "filtros_json": _empaquetar_filtros(filtros),
                "resultados": resultados,
                "duracion_seg": duracion_seg,
                "error_msg": _truncar(error_msg, 500),
                "origen": ORIGEN,
            })
            conn.commit()
    except Exception as e:
        # Nunca romper la app por un fallo del tracking
        print(f"⚠️ tracking error: {e}")


# ==== WRAPPER PARA BÚSQUEDAS ====

def buscar_con_metricas(engine, query, params, filtros, vista, pestana,
                        mensaje_spinner="Buscando anuncios..."):
    """
    Ejecuta una búsqueda en BD, loguea la métrica y maneja errores.

    Devuelve el DataFrame o None si hubo error.

    Parámetros:
    - engine: conexión SQLAlchemy
    - query: SQL (string)
    - params: dict de parámetros para la query
    - filtros: dict con los filtros usados (para el log)
    - vista: 'analista' | 'curricular'
    - pestana: 'puestos' | 'skills' | 'dominios' | 'escuelas' | 'tipos'
    - mensaje_spinner: texto que se muestra mientras carga
    """
    import pandas as pd

    inicio = datetime.now()
    try:
        with st.spinner(mensaje_spinner):
            df = pd.read_sql(text(query), engine, params=params)

        duracion_seg = (datetime.now() - inicio).total_seconds()

        log_evento(
            accion="buscar",
            vista=vista,
            pestana=pestana,
            filtros=filtros,
            resultados=len(df),
            duracion_seg=duracion_seg,
        )
        return df

    except Exception as e:
        duracion_seg = (datetime.now() - inicio).total_seconds()

        log_evento(
            accion="error",
            vista=vista,
            pestana=pestana,
            filtros=filtros,
            duracion_seg=duracion_seg,
            error_msg=str(e),
        )
        st.error(f"Error en la búsqueda: {e}")
        return None