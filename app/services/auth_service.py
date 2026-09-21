from flask import session
from app.repositories.usuario_repository import UsuarioRepository

class AuthService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()

    def autenticar(self, login_ou_email, senha):
        """
        Autentica o usuario aceitando login pela sigla (ex: uema, udesc),
        pelo e-mail institucional ou usuario admin.
        """
        identificador = (login_ou_email or '').strip()
        usuario = self.usuario_repo.buscar_por_identificador(identificador)

        if not usuario or not usuario.ativo:
            return None, "Usuário inativo ou não localizado."
        
        if not usuario.verificar_senha(senha):
            return None, "Credenciais inválidas."

        # Estabelece a sessao no padrao seguro do Flask
        session.clear()
        session['usuario_id'] = usuario.id
        session['nome'] = usuario.nome
        session['email'] = usuario.email
        session['perfil'] = usuario.perfil
        session['universidade_id'] = usuario.universidade_id
        session['precisa_trocar_senha'] = bool(usuario.precisa_trocar_senha)

        return usuario, None

    def logout(self):
        session.clear()

    @staticmethod
    def usuario_atual():
        if 'usuario_id' not in session:
            return None
        return {
            'id': session.get('usuario_id'),
            'nome': session.get('nome'),
            'email': session.get('email'),
            'perfil': session.get('perfil'),
            'universidade_id': session.get('universidade_id'),
            'precisa_trocar_senha': session.get('precisa_trocar_senha', False)
        }

    @staticmethod
    def esta_autenticado():
        return 'usuario_id' in session

    @staticmethod
    def exigir_admin():
        return session.get('perfil') == 'ADMIN_CAMARA'

    @staticmethod
    def exigir_escrita_universidade(universidade_id):
        """
        Regra estrita de negocio:
        O Admin da Camara pode editar os dados de qualquer universidade.
        A universidade logada so possui permissao de lancamento e edicao
        para os dados vinculados ao seu proprio identificador institucional.
        """
        if session.get('perfil') == 'ADMIN_CAMARA':
            return True
        usuario_uni_id = session.get('universidade_id')
        if not usuario_uni_id or not universidade_id:
            return False
        return str(usuario_uni_id).strip().upper() == str(universidade_id).strip().upper()