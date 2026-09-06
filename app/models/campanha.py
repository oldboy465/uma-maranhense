class Campanha:
    def __init__(self, id=None, nome=None, ano_referencia=None,
                 data_inicio=None, data_fim=None, status='ABERTA', criado_em=None):
        self.id = id
        self.nome = nome
        self.ano_referencia = int(ano_referencia) if ano_referencia is not None else None
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = status  # ABERTA, ENCERRADA
        self.criado_em = criado_em

    def is_aberta(self):
        return self.status == 'ABERTA'

    @classmethod
    def from_dict(cls, dados):
        if not dados:
            return None
        return cls(
            id=dados.get('id'),
            nome=dados.get('nome'),
            ano_referencia=dados.get('ano_referencia'),
            data_inicio=dados.get('data_inicio'),
            data_fim=dados.get('data_fim'),
            status=dados.get('status', 'ABERTA'),
            criado_em=dados.get('criado_em')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'ano_referencia': self.ano_referencia,
            'data_inicio': str(self.data_inicio) if self.data_inicio else None,
            'data_fim': str(self.data_fim) if self.data_fim else None,
            'status': self.status,
            'criado_em': self.criado_em
        }