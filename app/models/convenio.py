class Convenio:
    def __init__(self, id=None, universidade_id=None, ano_referencia=None,
                 orgao_concedente=None, numero_instrumento=None, objeto=None,
                 valor_global=0.0, valor_liberado=0.0, data_inicio=None, data_fim=None):
        self.id = id
        self.universidade_id = universidade_id
        self.ano_referencia = int(ano_referencia) if ano_referencia is not None else None
        self.orgao_concedente = orgao_concedente
        self.numero_instrumento = numero_instrumento
        self.objeto = objeto
        self.valor_global = round(float(valor_global), 2) if valor_global is not None else 0.0
        self.valor_liberado = round(float(valor_liberado), 2) if valor_liberado is not None else 0.0
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    @property
    def valor_global_formatado(self):
        val = round(self.valor_global, 2)
        formatado = f"{val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {formatado}"

    @property
    def valor_liberado_formatado(self):
        val = round(self.valor_liberado, 2)
        formatado = f"{val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"R$ {formatado}"

    @classmethod
    def from_dict(cls, dados):
        if not dados:
            return None
        return cls(
            id=dados.get('id'),
            universidade_id=dados.get('universidade_id'),
            ano_referencia=dados.get('ano_referencia'),
            orgao_concedente=dados.get('orgao_concedente'),
            numero_instrumento=dados.get('numero_instrumento'),
            objeto=dados.get('objeto'),
            valor_global=dados.get('valor_global', 0.0),
            valor_liberado=dados.get('valor_liberado', 0.0),
            data_inicio=dados.get('data_inicio'),
            data_fim=dados.get('data_fim')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'universidade_id': self.universidade_id,
            'ano_referencia': self.ano_referencia,
            'orgao_concedente': self.orgao_concedente,
            'numero_instrumento': self.numero_instrumento,
            'objeto': self.objeto,
            'valor_global': self.valor_global,
            'valor_liberado': self.valor_liberado,
            'data_inicio': str(self.data_inicio) if self.data_inicio else None,
            'data_fim': str(self.data_fim) if self.data_fim else None
        }