from database.connection import get_db_connection

class BaseRepository:
    def __init__(self):
        pass

    def executar_consulta(self, sql, parametros=None):
        """
        Executa uma consulta SELECT e retorna uma lista de dicionarios.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, parametros or ())
                resultado = cursor.fetchall()
            return resultado
        finally:
            conn.close()

    def executar_consulta_um(self, sql, parametros=None):
        """
        Executa uma consulta SELECT e retorna um unico registro (dicionario) ou None.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, parametros or ())
                resultado = cursor.fetchone()
            return resultado
        finally:
            conn.close()

    def executar_comando(self, sql, parametros=None):
        """
        Executa um comando INSERT, UPDATE ou DELETE com controle de transacao.
        Retorna o lastrowid inserido ou o numero de linhas afetadas.
        """
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, parametros or ())
                afetados = cursor.rowcount
                ultimo_id = cursor.lastrowid
            conn.commit()
            return ultimo_id if ultimo_id else afetados
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()