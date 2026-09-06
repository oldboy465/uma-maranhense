"""
Configuração de acesso ao banco de dados SQLite nativo.
Redireciona para o conector centralizado em database/connection.py.
"""
from database.connection import get_db_connection

__all__ = ['get_db_connection']