from app.repositories.base_repository import BaseRepository
from app.models.universidade import Universidade

class UniversidadeRepository(BaseRepository):
    def buscar_por_id(self, universidade_id):
        sql = "SELECT * FROM universidades WHERE id = %s LIMIT 1"
        res = self.executar_consulta_um(sql, (universidade_id,))
        return Universidade.from_dict(res) if res else None

    def buscar_por_sigla(self, sigla):
        sql = "SELECT * FROM universidades WHERE LOWER(sigla) = LOWER(%s) LIMIT 1"
        res = self.executar_consulta_um(sql, (sigla,))
        return Universidade.from_dict(res) if res else None

    def listar_todas(self, apenas_ativas=True):
        sql = "SELECT * FROM universidades"
        if apenas_ativas:
            sql += " WHERE status = 'ATIVA'"
        sql += " ORDER BY sigla ASC"
        linhas = self.executar_consulta(sql)
        return [Universidade.from_dict(l) for l in linhas]

    def listar_por_regiao(self, regiao):
        sql = "SELECT * FROM universidades WHERE regiao = %s AND status = 'ATIVA' ORDER BY sigla ASC"
        linhas = self.executar_consulta(sql, (regiao,))
        return [Universidade.from_dict(l) for l in linhas]

    def listar_responsaveis(self, universidade_id):
        sql = """
            SELECT * FROM universidades_responsaveis 
            WHERE universidade_id = %s 
            ORDER BY FIELD(tipo, 'REITOR', 'PRO_REITOR', 'REPRESENTANTE_CAMARA', 'RESPONSAVEL_TECNICO')
        """
        return self.executar_consulta(sql, (universidade_id,))

    def salvar(self, uni):
        sql_existe = "SELECT id FROM universidades WHERE id = %s"
        existe = self.executar_consulta_um(sql_existe, (uni.id,))
        if existe:
            sql = """
                UPDATE universidades 
                SET sigla = %s, nome = %s, tipo = %s, uf = %s, regiao = %s, 
                    municipio_sede = %s, ano_filiacao = %s, status = %s
                WHERE id = %s
            """
            params = (uni.sigla, uni.nome, uni.tipo, uni.uf, uni.regiao,
                      uni.municipio_sede, uni.ano_filiacao, uni.status, uni.id)
            return self.executar_comando(sql, params)
        else:
            sql = """
                INSERT INTO universidades (id, sigla, nome, tipo, uf, regiao, municipio_sede, ano_filiacao, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (uni.id, uni.sigla, uni.nome, uni.tipo, uni.uf, uni.regiao,
                      uni.municipio_sede, uni.ano_filiacao, uni.status)
            return self.executar_comando(sql, params)