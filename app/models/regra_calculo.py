class RegraCalculo:
    def __init__(self, id=None, indicador_destino_id=None, formula=None,
                 descricao=None, ordem_execucao=1):
        self.id = id
        self.indicador_destino_id = indicador_destino_id
        self.formula = formula
        self.descricao = descricao
        self.ordem_execucao = int(ordem_execucao) if ordem_execucao is not None else 1

    @classmethod
    def from_dict(cls, dados):
        if not dados:
            return None
        return cls(
            id=dados.get('id'),
            indicador_destino_id=dados.get('indicador_destino_id'),
            formula=dados.get('formula'),
            descricao=dados.get('descricao'),
            ordem_execucao=dados.get('ordem_execucao', 1)
        )

    def to_dict(self):
        return {
            'id': self.id,
            'indicador_destino_id': self.indicador_destino_id,
            'formula': self.formula,
            'descricao': self.descricao,
            'ordem_execucao': self.ordem_execucao
        }