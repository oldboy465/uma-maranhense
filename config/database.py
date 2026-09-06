import pymysql
from pymysql.cursors import DictCursor
from config.settings import Config

def get_db_connection():
    """
    Retorna uma conexao ativa com o banco MySQL utilizando DictCursor
    para devolver registros em formato de dicionario legivel.
    """
    return pymysql.connect(
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
        charset='utf8mb4',
        cursorclass=DictCursor,
        autocommit=False
    )