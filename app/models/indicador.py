class Indicador:
    def __init__(self, id=None, codigo=None, nome=None, dimensao=None,
                 tipo_dado=None, tipo_agregacao=None, origem='INFORMADO',
                 unidade_medida=None, descricao=None, obrigatorio=1, ativo=1):
        self.id = id
        self.codigo = codigo
        self.nome = nome
        self.dimensao = dimensao
        self.tipo_dado = tipo_dado  # INTEIRO, MONETARIO, PERCENTUAL, DECIMAL, TEXTO
        self.tipo_agregacao = tipo_agregacao  # ESTOQUE, FLUXO, RAZAO, NAO_ADITIVO
        self.origem = origem  # INFORMADO, CALCULADO
        self.unidade_medida = unidade_medida
        self.descricao = descricao
        self.obrigatorio = bool(obrigatorio)
        self.ativo = bool(ativo)

    def is_calculado(self):
        return self.origem == 'CALCULADO'

    def is_monetario(self):
        return self.tipo_dado == 'MONETARIO'

    @classmethod
    def from_dict(cls, dados):
        if not dados:
            return None
        return cls(
            id=dados.get('id'),
            codigo=dados.get('codigo'),
            nome=dados.get('nome'),
            dimensao=dados.get('dimensao'),
            tipo_dado=dados.get('tipo_dado'),
            tipo_agregacao=dados.get('tipo_agregacao'),
            origem=dados.get('origem', 'INFORMADO'),
            unidade_medida=dados.get('unidade_medida'),
            descricao=dados.get('descricao'),
            obrigatorio=dados.get('obrigatorio', 1),
            ativo=dados.get('ativo', 1)
        )

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'nome': self.nome,
            'dimensao': self.dimensao,
            'tipo_dado': self.tipo_dado,
            'tipo_agregacao': self.tipo_agregacao,
            'origem': self.origem,
            'unidade_medida': self.unidade_medida,
            'descricao': self.descricao,
            'obrigatorio': self.obrigatorio,
            'ativo': self.ativo
        }