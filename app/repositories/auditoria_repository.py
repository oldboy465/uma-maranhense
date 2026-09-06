import json
from app.repositories.base_repository import BaseRepository
from app.models.auditoria import Auditoria

class AuditoriaRepository(BaseRepository):
    def registrar(self, auditoria):
        sql = """
            INSERT INTO auditoria (usuario_id, universidade_id, tabela_afetada, acao, dados_antigos, dados_novos, ip_origem)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        antigos = json.dumps(auditoria.dados_antigos, ensure_ascii=False) if auditoria.dados_antigos else None
        novos = json.dumps(auditoria.dados_novos, ensure_ascii=False) if auditoria.dados_novos else None
        params = (
            auditoria.usuario_id, auditoria.universidade_id,
            auditoria.tabela_afetada, auditoria.acao,
            antigos, novos, auditoria.ip_origem
        )
        return self.executar_comando(sql, params)

    def listar_ultimas(self, limite=100):
        sql = """
            SELECT a.*, u.nome as usuario_nome, u.email as usuario_email, 
                   uni.sigla as universidade_sigla
            FROM auditoria a
            LEFT JOIN usuarios u ON a.usuario_id = u.id
            LEFT JOIN universidades uni ON a.universidade_id = uni.id
            ORDER BY a.criado_em DESC
            LIMIT %s
        """
        return self.executar_consulta(sql, (limite,))