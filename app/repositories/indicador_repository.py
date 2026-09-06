from app.repositories.base_repository import BaseRepository
from app.models.indicador import Indicador

class IndicadorRepository(BaseRepository):
    def buscar_por_id(self, indicador_id):
        sql = "SELECT * FROM indicadores WHERE id = %s LIMIT 1"
        res = self.executar_consulta_um(sql, (indicador_id,))
        return Indicador.from_dict(res) if res else None

    def buscar_por_codigo(self, codigo):
        sql = "SELECT * FROM indicadores WHERE codigo = %s LIMIT 1"
        res = self.executar_consulta_um(sql, (codigo,))
        return Indicador.from_dict(res) if res else None

    def listar_todos(self, apenas_ativos=True):
        sql = "SELECT * FROM indicadores"
        if apenas_ativos:
            sql += " WHERE ativo = 1"
        sql += " ORDER BY dimensao ASC, nome ASC"
        linhas = self.executar_consulta(sql)
        return [Indicador.from_dict(l) for l in linhas]

    def listar_por_dimensao(self, dimensao, apenas_ativos=True):
        sql = "SELECT * FROM indicadores WHERE dimensao = %s"
        if apenas_ativos:
            sql += " AND ativo = 1"
        sql += " ORDER BY nome ASC"
        linhas = self.executar_consulta(sql, (dimensao,))
        return [Indicador.from_dict(l) for l in linhas]

    def salvar(self, ind):
        sql_existe = "SELECT id FROM indicadores WHERE id = %s"
        existe = self.executar_consulta_um(sql_existe, (ind.id,))
        if existe:
            sql = """
                UPDATE indicadores 
                SET codigo = %s, nome = %s, dimensao = %s, tipo_dado = %s, 
                    tipo_agregacao = %s, origem = %s, unidade_medida = %s, 
                    descricao = %s, obrigatorio = %s, ativo = %s
                WHERE id = %s
            """
            params = (ind.codigo, ind.nome, ind.dimensao, ind.tipo_dado,
                      ind.tipo_agregacao, ind.origem, ind.unidade_medida,
                      ind.descricao, 1 if ind.obrigatorio else 0,
                      1 if ind.ativo else 0, ind.id)
            return self.executar_comando(sql, params)
        else:
            sql = """
                INSERT INTO indicadores (id, codigo, nome, dimensao, tipo_dado, tipo_agregacao, origem, unidade_medida, descricao, obrigatorio, ativo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (ind.id, ind.codigo, ind.nome, ind.dimensao, ind.tipo_dado,
                      ind.tipo_agregacao, ind.origem, ind.unidade_medida,
                      ind.descricao, 1 if ind.obrigatorio else 0,
                      1 if ind.ativo else 0)
            return self.executar_comando(sql, params)