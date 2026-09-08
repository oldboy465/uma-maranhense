from app.repositories.base_repository import BaseRepository
from app.models.registro_dado import RegistroDado

class RegistroRepository(BaseRepository):
    def buscar_por_chave(self, universidade_id, indicador_id, ano_referencia):
        sql = """
            SELECT * FROM registro_dados 
            WHERE universidade_id = %s AND indicador_id = %s AND ano_referencia = %s 
            LIMIT 1
        """
        res = self.executar_consulta_um(sql, (universidade_id, indicador_id, ano_referencia))
        return RegistroDado.from_dict(res) if res else None

    def listar_por_universidade_e_ano(self, universidade_id, ano_referencia, apenas_validados=False):
        sql = """
            SELECT r.*, i.codigo as indicador_codigo, i.nome as indicador_nome, 
                   i.dimensao, i.tipo_dado, i.origem, i.unidade_medida
            FROM registro_dados r
            INNER JOIN indicadores i ON r.indicador_id = i.id
            WHERE r.universidade_id = %s AND r.ano_referencia = %s
        """
        if apenas_validados:
            sql += " AND r.status_dado = 'VALIDADO'"
        sql += " ORDER BY i.dimensao ASC, i.nome ASC"
        return self.executar_consulta(sql, (universidade_id, ano_referencia))

    def listar_submissoes_pendentes(self):
        sql = """
            SELECT r.*, u.sigla as universidade_sigla, u.nome as universidade_nome,
                   i.codigo as indicador_codigo, i.nome as indicador_nome, i.dimensao,
                   usr.nome as usuario_nome
            FROM registro_dados r
            INNER JOIN universidades u ON r.universidade_id = u.id
            INNER JOIN indicadores i ON r.indicador_id = i.id
            LEFT JOIN usuarios usr ON r.atualizado_por = usr.id
            WHERE r.status_dado = 'ENVIADO'
            ORDER BY r.atualizado_em ASC
        """
        return self.executar_consulta(sql)

    def salvar(self, reg):
        """
        Insere ou atualiza o registro verificando a existência prévia da chave única
        (universidade_id, indicador_id, ano_referencia), garantindo compatibilidade
        universal com SQLite local e MySQL em produção.
        """
        val_num = round(reg.valor_numerico, 4) if reg.valor_numerico is not None else None
        registro_existente = self.buscar_por_chave(reg.universidade_id, reg.indicador_id, reg.ano_referencia)

        if registro_existente:
            sql = """
                UPDATE registro_dados
                SET valor_numerico = %s,
                    valor_texto = %s,
                    status_dado = %s,
                    fonte_tipo = %s,
                    fonte_descricao = %s,
                    fonte_url = %s,
                    parecer_devolucao = %s,
                    atualizado_por = %s
                WHERE universidade_id = %s AND indicador_id = %s AND ano_referencia = %s
            """
            params = (
                val_num, reg.valor_texto, reg.status_dado,
                reg.fonte_tipo, reg.fonte_descricao, reg.fonte_url,
                reg.parecer_devolucao, reg.atualizado_por,
                reg.universidade_id, reg.indicador_id, reg.ano_referencia
            )
            return self.executar_comando(sql, params)
        else:
            sql = """
                INSERT INTO registro_dados (
                    universidade_id, indicador_id, ano_referencia, 
                    valor_numerico, valor_texto, status_dado, 
                    fonte_tipo, fonte_descricao, fonte_url, 
                    parecer_devolucao, atualizado_por
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                reg.universidade_id, reg.indicador_id, reg.ano_referencia,
                val_num, reg.valor_texto, reg.status_dado,
                reg.fonte_tipo, reg.fonte_descricao, reg.fonte_url,
                reg.parecer_devolucao, reg.atualizado_por
            )
            return self.executar_comando(sql, params)

    def atualizar_status(self, id_registro, novo_status, parecer=None):
        sql = """
            UPDATE registro_dados 
            SET status_dado = %s, parecer_devolucao = %s 
            WHERE id = %s
        """
        return self.executar_comando(sql, (novo_status, parecer, id_registro))

    def listar_para_painel_publico(self, indicador_id, anos):
        if not anos:
            return []
        format_strings = ','.join(['%s'] * len(anos))
        sql = f"""
            SELECT r.universidade_id, u.sigla, u.regiao, u.uf, r.ano_referencia, r.valor_numerico
            FROM registro_dados r
            INNER JOIN universidades u ON r.universidade_id = u.id
            WHERE r.indicador_id = %s 
              AND r.ano_referencia IN ({format_strings})
              AND r.status_dado = 'VALIDADO'
              AND u.status = 'ATIVA'
            ORDER BY r.ano_referencia ASC, u.sigla ASC
        """
        params = [indicador_id] + list(anos)
        return self.executar_consulta(sql, params)