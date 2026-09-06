from werkzeug.security import generate_password_hash, check_password_hash

class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha_hash=None, 
                 perfil=None, universidade_id=None, precisa_trocar_senha=1, 
                 ativo=1, criado_em=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.perfil = perfil
        self.universidade_id = universidade_id
        self.precisa_trocar_senha = bool(precisa_trocar_senha)
        self.ativo = bool(ativo)
        self.criado_em = criado_em

    def definir_senha(self, senha_pura):
        self.senha_hash = generate_password_hash(senha_pura)

    def verificar_senha(self, senha_pura):
        if not self.senha_hash:
            return False
        return check_password_hash(self.senha_hash, senha_pura)

    def is_admin(self):
        return self.perfil == 'ADMIN_CAMARA'

    def is_gestor(self):
        return self.perfil == 'GESTOR_INSTITUCIONAL'

    @classmethod
    def from_dict(cls, dados):
        if not dados:
            return None
        return cls(
            id=dados.get('id'),
            nome=dados.get('nome'),
            email=dados.get('email'),
            senha_hash=dados.get('senha_hash'),
            perfil=dados.get('perfil'),
            universidade_id=dados.get('universidade_id'),
            precisa_trocar_senha=dados.get('precisa_trocar_senha', 1),
            ativo=dados.get('ativo', 1),
            criado_em=dados.get('criado_em')
        )

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'perfil': self.perfil,
            'universidade_id': self.universidade_id,
            'precisa_trocar_senha': self.precisa_trocar_senha,
            'ativo': self.ativo,
            'criado_em': self.criado_em
        }