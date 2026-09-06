class RegistroDado:
    def __init__(self, id=None, universidade_id=None, indicador_id=None,
                 ano_referencia=None, valor_numerico=None, valor_texto=None,
                 status_dado='RASCUNHO', fonte_tipo=None, fonte_descricao=None,
                 fonte_url=None, parecer_devolucao=None, atualizado_por=None,
                 criado_em=None, atualizado_em=None):
        self.id = id
        self.universidade_id = universidade_id
        self.indicador_id = indicador_id
        self.ano_referencia = int(ano_referencia) if ano_referencia is not None else None
        self.valor_numerico = float(valor_numerico) if valor_numerico is not None else None
        self.valor_texto = valor_texto
        self.status_dado = status_dado  # RASCUNHO, ENVIADO, VALIDADO, DEVOLVIDO
        self.fonte_tipo = fonte_tipo
        self.fonte_descricao = fonte_descricao
        self.fonte_url = fonte_url
        self.parecer_devolucao = parecer_devolucao
        self.atualizado_por = atualizado_por
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def is_validado(self):
        return self.status_dado == 'VALIDADO'

    def is_editavel_por_gestor(self):
        return self.status_dado in ('RASCUNHO', 'DEVOLVIDO')

    @property
    def valor_formatado_br(self):
        """
        Formata o valor numerico para padrao brasileiro com arredondamento
        em duas casas decimais para dizimas ou valores fracionados.
        """
        if self.valor_numerico is None:
            return self.valor_texto or '-'
        val = round(self.valor_numerico, 2)
        return f"{val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    @classmethod
    def from_dict(cls, dados):
        if not dados:
            return None
        return cls(
            id=dados.get('id'),
            universidade_id=dados.get('universidade_id'),
            indicador_id=dados.get('indicador_id'),
            ano_referencia=dados.get('ano_referencia'),
            valor_numerico=dados.get('valor_numerico'),
            valor_texto=dados.get('valor_texto'),
            status_dado=dados.get('status_dado', 'RASCUNHO'),
            fonte_tipo=dados.get('fonte_tipo'),
            fonte_descricao=dados.get('fonte_descricao'),
            fonte_url=dados.get('fonte_url'),
            parecer_devolucao=dados.get('parecer_devolucao'),
            atualizado_por=dados.get('atualizado_por'),
            criado_em=dados.get('criado_em'),
            atualizado_em=dados.get('atualizado_em')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'universidade_id': self.universidade_id,
            'indicador_id': self.indicador_id,
            'ano_referencia': self.ano_referencia,
            'valor_numerico': self.valor_numerico,
            'valor_texto': self.valor_texto,
            'status_dado': self.status_dado,
            'fonte_tipo': self.fonte_tipo,
            'fonte_descricao': self.fonte_descricao,
            'fonte_url': self.fonte_url,
            'parecer_devolucao': self.parecer_devolucao,
            'atualizado_por': self.atualizado_por,
            'criado_em': self.criado_em,
            'atualizado_em': self.atualizado_em
        }