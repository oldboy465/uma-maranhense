from app.repositories.base_repository import BaseRepository
from app.models.convenio import Convenio

class ConvenioRepository(BaseRepository):
    def buscar_por_id(self, convenio_id):
        sql = "SELECT * FROM convenios WHERE id = %s LIMIT 1"
        res = self.executar_consulta_um(sql, (convenio_id,))
        return Convenio.from_dict(res) if res else None

    def listar_por_universidade(self, universidade_id, ano_referencia=None):
        sql = "SELECT * FROM convenios WHERE universidade_id = %s"
        params = [universidade_id]
        if ano_referencia:
            sql += " AND ano_referencia = %s"
            params.append(ano_referencia)
        sql += " ORDER BY ano_referencia DESC, valor_global DESC"
        linhas = self.executar_consulta(sql, params)
        return [Convenio.from_dict(l) for l in linhas]

    def totalizar_por_ano_e_universidade(self, universidade_id, ano_referencia):
        sql = """
            SELECT 
                COALESCE(SUM(valor_global), 0.00) as total_global,
                COALESCE(SUM(valor_liberado), 0.00) as total_liberado,
                COUNT(*) as total_instrumentos
            FROM convenios
            WHERE universidade_id = %s AND ano_referencia = %s
        """
        return self.executar_consulta_um(sql, (universidade_id, ano_referencia))

    def salvar(self, conv):
        v_global = round(conv.valor_global, 2)
        v_liberado = round(conv.valor_liberado, 2)
        if conv.id:
            sql = """
                UPDATE convenios 
                SET universidade_id = %s, ano_referencia = %s, orgao_concedente = %s, 
                    numero_instrumento = %s, objeto = %s, valor_global = %s, 
                    valor_liberado = %s, data_inicio = %s, data_fim = %s
                WHERE id = %s
            """
            params = (conv.universidade_id, conv.ano_referencia, conv.orgao_concedente,
                      conv.numero_instrumento, conv.objeto, v_global, v_liberado,
                      conv.data_inicio, conv.data_fim, conv.id)
            return self.executar_comando(sql, params)
        else:
            sql = """
                INSERT INTO convenios (universidade_id, ano_referencia, orgao_concedente, numero_instrumento, objeto, valor_global, valor_liberado, data_inicio, data_fim)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (conv.universidade_id, conv.ano_referencia, conv.orgao_concedente,
                      conv.numero_instrumento, conv.objeto, v_global, v_liberado,
                      conv.data_inicio, conv.data_fim)
            return self.executar_comando(sql, params)

    def excluir(self, convenio_id):
        sql = "DELETE FROM convenios WHERE id = %s"
        return self.executar_comando(sql, (convenio_id,))