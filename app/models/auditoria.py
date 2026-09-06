import json

class Auditoria:
    def __init__(self, id=None, usuario_id=None, universidade_id=None,
                 tabela_afetada=None, acao=None, dados_antigos=None,
                 dados_novos=None, ip_origem=None, criado_em=None):
        self.id = id
        self.usuario_id = usuario_id
        self.universidade_id = universidade_id
        self.tabela_afetada = tabela_afetada
        self.acao = acao  # INSERT, UPDATE, DELETE, LOGIN, VALIDACAO
        self.dados_antigos = dados_antigos
        self.dados_novos = dados_novos
        self.ip_origem = ip_origem
        self.criado_em = criado_em

    @classmethod
    def from_dict(cls, dados):
        if not dados:
            return None
        
        antigos = dados.get('dados_antigos')
        if isinstance(antigos, str):
            try:
                antigos = json.loads(antigos)
            except Exception:
                pass

        novos = dados.get('dados_novos')
        if isinstance(novos, str):
            try:
                novos = json.loads(novos)
            except Exception:
                pass

        return cls(
            id=dados.get('id'),
            usuario_id=dados.get('usuario_id'),
            universidade_id=dados.get('universidade_id'),
            tabela_afetada=dados.get('tabela_afetada'),
            acao=dados.get('acao'),
            dados_antigos=antigos,
            dados_novos=novos,
            ip_origem=dados.get('ip_origem'),
            criado_em=dados.get('criado_em')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'universidade_id': self.universidade_id,
            'tabela_afetada': self.tabela_afetada,
            'acao': self.acao,
            'dados_antigos': self.dados_antigos,
            'dados_novos': self.dados_novos,
            'ip_origem': self.ip_origem,
            'criado_em': self.criado_em
        }