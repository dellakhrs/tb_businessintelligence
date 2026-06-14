import os
from urllib.parse import quote_plus

import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

load_dotenv()


def _setting(name: str, default: str | int = "") -> str | int:
    env_value = os.getenv(f"DB_{name.upper()}")
    if env_value is not None:
        return env_value

    try:
        return st.secrets["mysql"].get(name, default)
    except (KeyError, FileNotFoundError):
        return default


@st.cache_resource
def get_engine() -> Engine:
    host = str(_setting("host", "localhost"))
    port = int(_setting("port", 3306))
    database = str(_setting("database", "bi_pariwisata"))
    user = quote_plus(str(_setting("user", "root")))
    password = quote_plus(str(_setting("password", "")))

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={"connect_timeout": 3},
    )


def get_server_engine() -> Engine:
    host = str(_setting("host", "localhost"))
    port = int(_setting("port", 3306))
    user = quote_plus(str(_setting("user", "root")))
    password = quote_plus(str(_setting("password", "")))
    url = f"mysql+pymysql://{user}:{password}@{host}:{port}"
    return create_engine(url, pool_pre_ping=True, connect_args={"connect_timeout": 3})


def database_enabled() -> bool:
    return str(os.getenv("DB_ENABLED", "false")).lower() in {"1", "true", "yes", "on"}
