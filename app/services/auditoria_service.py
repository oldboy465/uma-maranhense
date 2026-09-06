from flask import request, session
from app.repositories.auditoria_repository import AuditoriaRepository
from app.models.auditoria import Auditoria

class AuditoriaService:
    def __init__(self):
        self.auditoria_repo = AuditoriaRepository()

    def registrar_evento(self, tabela, acao, dados_antigos=None, dados_novos=None, universidade_id=None):
        try:
            usuario_id = session.get('usuario_id')
            uni_id = universidade_id or session.get('universidade_id')
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            if ip and ',' in ip:
                ip = ip.split(',')[0].strip()

            registro = Auditoria(
                usuario_id=usuario_id,
                universidade_id=uni_id,
                tabela_afetada=tabela,
                acao=acao,
                dados_antigos=dados_antigos,
                dados_novos=dados_novos,
                ip_origem=ip
            )
            self.auditoria_repo.registrar(registro)
        except Exception:
            # Falhas na auditoria nao devem interromper a transacao do usuario
            pass