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

    def listar_todas(self, apenas_ativas=True, autonomia=None):
        """
        Lista universidades com suporte a filtro de status e autonomia_financeira.
        autonomia pode ser: None (todas), 1/True (Sim) ou 0/False (Não).
        """
        sql = "SELECT * FROM universidades WHERE 1=1"
        params = []
        if apenas_ativas:
            sql += " AND status = 'ATIVA'"
        if autonomia is not None:
            sql += " AND COALESCE(autonomia_financeira, 0) = %s"
            params.append(1 if autonomia in (1, '1', True, 'Sim') else 0)
        sql += " ORDER BY sigla ASC"
        linhas = self.executar_consulta(sql, params)
        return [Universidade.from_dict(l) for l in linhas]

    def listar_por_regiao(self, regiao):
        sql = "SELECT * FROM universidades WHERE LOWER(regiao) = LOWER(%s) AND status = 'ATIVA' ORDER BY sigla ASC"
        linhas = self.executar_consulta(sql, (regiao,))
        return [Universidade.from_dict(l) for l in linhas]

    def listar_com_estatisticas_admin(self, ano_referencia=2025):
        """
        Lista as 31 instituições com percentual de cobertura do exercício
        e contagem de gestores com acesso, conforme exigido no painel da Câmara.
        """
        sql = """
            SELECT 
                u.*,
                COALESCE((
                    SELECT COUNT(DISTINCT r.indicador_id) * 100.0 / NULLIF((SELECT COUNT(*) FROM indicadores WHERE ativo = 1), 0)
                    FROM registro_dados r
                    WHERE r.universidade_id = u.id 
                      AND r.ano_referencia = %s 
                      AND r.status_dado = 'VALIDADO'
                ), 0.0) as percentual_cobertura,
                (
                    SELECT COUNT(*) 
                    FROM usuarios usr 
                    WHERE usr.universidade_id = u.id 
                      AND usr.ativo = 1
                ) as total_gestores
            FROM universidades u
            WHERE u.status = 'ATIVA'
            ORDER BY u.sigla ASC
        """
        linhas = self.executar_consulta(sql, (ano_referencia,))
        resultado = []
        for l in linhas:
            uni = Universidade.from_dict(l)
            resultado.append({
                'universidade': uni,
                'cobertura': round(float(l.get('percentual_cobertura') or 0.0), 1),
                'total_gestores': int(l.get('total_gestores') or 0)
            })
        return resultado

    def listar_responsaveis(self, universidade_id):
        sql = """
            SELECT * FROM universidades_responsaveis 
            WHERE universidade_id = %s 
            ORDER BY 
                CASE tipo
                    WHEN 'REITOR' THEN 1
                    WHEN 'PRO_REITOR' THEN 2
                    WHEN 'REPRESENTANTE_CAMARA' THEN 3
                    WHEN 'RESPONSAVEL_TECNICO' THEN 4
                    ELSE 5
                END ASC,
                nome ASC
        """
        return self.executar_consulta(sql, (universidade_id,))

    def salvar(self, uni):
        sql_existe = "SELECT id FROM universidades WHERE id = %s"
        existe = self.executar_consulta_um(sql_existe, (uni.id,))
        autonomia = 1 if getattr(uni, 'autonomia_financeira', 0) in (1, '1', True) else 0

        if existe:
            sql = """
                UPDATE universidades 
                SET sigla = %s, nome = %s, tipo = %s, uf = %s, regiao = %s, 
                    municipio_sede = %s, ano_filiacao = %s, status = %s,
                    autonomia_financeira = %s
                WHERE id = %s
            """
            params = (uni.sigla, uni.nome, uni.tipo, uni.uf, uni.regiao,
                      uni.municipio_sede, uni.ano_filiacao, uni.status,
                      autonomia, uni.id)
            return self.executar_comando(sql, params)
        else:
            sql = """
                INSERT INTO universidades (id, sigla, nome, tipo, uf, regiao, municipio_sede, ano_filiacao, status, autonomia_financeira)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (uni.id, uni.sigla, uni.nome, uni.tipo, uni.uf, uni.regiao,
                      uni.municipio_sede, uni.ano_filiacao, uni.status, autonomia)
            return self.executar_comando(sql, params)