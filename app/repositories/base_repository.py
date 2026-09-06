from database.connection import get_db_connection

class BaseRepository:
    def __init__(self):
        pass

    def executar_consulta(self, sql, parametros=None):
        sql_sqlite = sql.replace('%s', '?')
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql_sqlite, parametros or ())
            return cursor.fetchall()
        finally:
            conn.close()

    def executar_consulta_um(self, sql, parametros=None):
        sql_sqlite = sql.replace('%s', '?')
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql_sqlite, parametros or ())
            return cursor.fetchone()
        finally:
            conn.close()

    def executar_comando(self, sql, parametros=None):
        sql_sqlite = sql.replace('%s', '?')
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(sql_sqlite, parametros or ())
            afetados = cursor.rowcount
            ultimo_id = cursor.lastrowid
            conn.commit()
            return ultimo_id if ultimo_id else afetados
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()