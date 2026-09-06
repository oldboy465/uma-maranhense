from app.repositories.base_repository import BaseRepository
from app.models.regra_calculo import RegraCalculo

class RegraRepository(BaseRepository):
    def buscar_por_id(self, regra_id):
        sql = "SELECT * FROM regras_calculo WHERE id = %s LIMIT 1"
        res = self.executar_consulta_um(sql, (regra_id,))
        return RegraCalculo.from_dict(res) if res else None

    def buscar_por_indicador_destino(self, indicador_destino_id):
        sql = "SELECT * FROM regras_calculo WHERE indicador_destino_id = %s LIMIT 1"
        res = self.executar_consulta_um(sql, (indicador_destino_id,))
        return RegraCalculo.from_dict(res) if res else None

    def listar_ordenadas(self):
        sql = """
            SELECT r.*, i.codigo as destino_codigo, i.nome as destino_nome 
            FROM regras_calculo r
            INNER JOIN indicadores i ON r.indicador_destino_id = i.id
            ORDER BY r.ordem_execucao ASC, r.id ASC
        """
        linhas = self.executar_consulta(sql)
        return [RegraCalculo.from_dict(l) for l in linhas]

    def salvar(self, regra):
        if regra.id:
            sql = """
                UPDATE regras_calculo 
                SET indicador_destino_id = %s, formula = %s, descricao = %s, ordem_execucao = %s
                WHERE id = %s
            """
            params = (regra.indicador_destino_id, regra.formula, regra.descricao, regra.ordem_execucao, regra.id)
            return self.executar_comando(sql, params)
        else:
            sql = """
                INSERT INTO regras_calculo (indicador_destino_id, formula, descricao, ordem_execucao)
                VALUES (%s, %s, %s, %s)
            """
            params = (regra.indicador_destino_id, regra.formula, regra.descricao, regra.ordem_execucao)
            return self.executar_comando(sql, params)

    def excluir(self, regra_id):
        sql = "DELETE FROM regras_calculo WHERE id = %s"
        return self.executar_comando(sql, (regra_id,))