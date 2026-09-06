from flask import session
from app.repositories.usuario_repository import UsuarioRepository

class AuthService:
    def __init__(self):
        self.usuario_repo = UsuarioRepository()

    def autenticar(self, email, senha):
        usuario = self.usuario_repo.buscar_por_email(email)
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
        session['precisa_trocar_senha'] = usuario.precisa_trocar_senha

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
            'precisa_trocar_senha': session.get('precisa_trocar_senha')
        }

    @staticmethod
    def esta_autenticado():
        return 'usuario_id' in session

    @staticmethod
    def exigir_admin():
        return session.get('perfil') == 'ADMIN_CAMARA'

    @staticmethod
    def exigir_escrita_universidade(universidade_id):
        if session.get('perfil') == 'ADMIN_CAMARA':
            return True
        return session.get('universidade_id') == universidade_id