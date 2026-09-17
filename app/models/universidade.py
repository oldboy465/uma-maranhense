class Universidade:
    def __init__(self, id=None, sigla=None, nome=None, tipo=None, 
                 uf=None, regiao=None, municipio_sede=None, 
                 ano_filiacao=None, status='ATIVA', autonomia_financeira=0, criado_em=None):
        self.id = id
        self.sigla = sigla
        self.nome = nome
        self.tipo = tipo
        self.uf = uf
        self.regiao = regiao
        self.municipio_sede = municipio_sede
        self.ano_filiacao = ano_filiacao
        self.status = status
        self.autonomia_financeira = 1 if (autonomia_financeira in (1, '1', True, 'Sim', 'SIM')) else 0
        self.criado_em = criado_em

    def tem_autonomia(self):
        return bool(self.autonomia_financeira)

    @classmethod
    def from_dict(cls, dados):
        if not dados:
            return None
        return cls(
            id=dados.get('id'),
            sigla=dados.get('sigla'),
            nome=dados.get('nome'),
            tipo=dados.get('tipo'),
            uf=dados.get('uf'),
            regiao=dados.get('regiao'),
            municipio_sede=dados.get('municipio_sede'),
            ano_filiacao=dados.get('ano_filiacao'),
            status=dados.get('status', 'ATIVA'),
            autonomia_financeira=dados.get('autonomia_financeira', 0),
            criado_em=dados.get('criado_em')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'sigla': self.sigla,
            'nome': self.nome,
            'tipo': self.tipo,
            'uf': self.uf,
            'regiao': self.regiao,
            'municipio_sede': self.municipio_sede,
            'ano_filiacao': self.ano_filiacao,
            'status': self.status,
            'autonomia_financeira': self.autonomia_financeira,
            'criado_em': self.criado_em
        }