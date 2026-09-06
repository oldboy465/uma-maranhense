import sqlite3
from pathlib import Path
from config.settings import Config

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db_connection():
    """
    Retorna conexao ativa com o banco SQLite embarcado com factory de dicionario.
    Cria a pasta data caso nao exista.
    """
    caminho_db = Path(Config.DB_PATH)
    caminho_db.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(caminho_db), timeout=30.0)
    conn.row_factory = dict_factory
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn