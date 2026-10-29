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


def _obtener_usuario_id(engine):
    """ID interno del usuario logueado, o None. Nunca rompe el tracking."""
    try:
        if not getattr(st.user, "is_logged_in", False):
            return None
        uid = st.session_state.get("usuario_id")
        if uid is None:
            with engine.connect() as conn:
                row = conn.execute(
                    text("SELECT id FROM usuarios WHERE google_sub = :sub"),
                    {"sub": st.user.sub},
                ).fetchone()
            uid = row[0] if row else None
            if uid is not None:
                st.session_state.usuario_id = uid
        return uid
    except Exception as e:
        print(f"⚠️ tracking: no se pudo obtener usuario_id: {e}")
        return None


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
    """
    if not TRACKING_ACTIVO:
        return

    try:
        engine = get_engine()
        ip = getattr(st.context, "ip_address", None)
        session_id = _obtener_session_id()
        
        # Obtenemos el usuario_id de forma aislada
        usuario_id = _obtener_usuario_id(engine)

        with engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO metricas_user
                (timestamp, session_id, ip_hash, usuario_id, vista, pestana, accion,
                 filtros_json, resultados, duracion_seg, error_msg, origen)
                VALUES
                (:timestamp, :session_id, :ip_hash, :usuario_id, :vista, :pestana, :accion,
                 :filtros_json, :resultados, :duracion_seg, :error_msg, :origen)
            """), {
                "timestamp": datetime.now(),
                "session_id": session_id,
                "ip_hash": _hash_ip(ip),
                "usuario_id": usuario_id,
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
        print(f"⚠️ tracking error: {e}")


# ==== WRAPPER PARA BÚSQUEDAS ====

def buscar_con_metricas(engine, query, params, filtros, vista, pestana,
                        mensaje_spinner="Buscando anuncios..."):
    """
    Ejecuta una búsqueda en BD, loguea la métrica y maneja errores.
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