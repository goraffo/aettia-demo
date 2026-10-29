import os
from functools import lru_cache
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()


@lru_cache(maxsize=1)
def get_engine():
    """Retorna una conexión reutilizable a PostgreSQL.
    
    Lee credenciales de variables de entorno.
    Defaults para desarrollo local:
    - DB_USER=postgres
    - DB_HOST=localhost
    - DB_PORT=5432
    - DB_NAME=skillbd
    """
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "skillbd")
    return create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}?client_encoding=utf8",
        pool_pre_ping=True,
        pool_recycle=1800,
    )