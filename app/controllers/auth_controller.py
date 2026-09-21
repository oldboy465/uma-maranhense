from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.auth_service import AuthService
from app.repositories.usuario_repository import UsuarioRepository
from app.services.auditoria_service import AuditoriaService
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/entrar', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if AuthService.esta_autenticado():
        usuario_atual = AuthService.usuario_atual()
        if usuario_atual and usuario_atual.get('precisa_trocar_senha'):
            return redirect(url_for('auth.trocar_senha'))
        if AuthService.exigir_admin():
            return redirect(url_for('admin.painel'))
        return redirect(url_for('minha_universidade.painel'))

    if request.method == 'POST':
        login_ou_email = request.form.get('email', '').strip()
        senha = request.form.get('senha', '')

        auth_service = AuthService()
        usuario, erro = auth_service.autenticar(login_ou_email, senha)

        if erro:
            flash(erro, 'danger')
            return render_template('public/login.html', email=login_ou_email)

        AuditoriaService().registrar_evento('usuarios', 'LOGIN', dados_novos={'login': login_ou_email})

        # Redirecionamento mandatorio no primeiro acesso
        if usuario.precisa_trocar_senha:
            flash('Por segurança institucional, altere sua senha de acesso inicial.', 'warning')
            return redirect(url_for('auth.trocar_senha'))

        if usuario.is_admin():
            return redirect(url_for('admin.painel'))
        return redirect(url_for('minha_universidade.painel'))

    return render_template('public/login.html')

@auth_bp.route('/sair')
@auth_bp.route('/logout')
def logout():
    AuditoriaService().registrar_evento('usuarios', 'LOGOUT')
    AuthService().logout()
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('home.index'))

@auth_bp.route('/trocar-senha', methods=['GET', 'POST'])
def trocar_senha():
    if not AuthService.esta_autenticado():
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nova_senha = request.form.get('nova_senha', '')
        confirmacao = request.form.get('confirmacao', '')

        if len(nova_senha) < 6:
            flash('A nova senha deve ter no mínimo 6 caracteres.', 'danger')
            return render_template('institucional/trocar_senha.html')

        if nova_senha != confirmacao:
            flash('As senhas digitadas não coincidem.', 'danger')
            return render_template('institucional/trocar_senha.html')

        if nova_senha == '123456':
            flash('A nova senha não pode ser a senha padrão 123456.', 'warning')
            return render_template('institucional/trocar_senha.html')

        hash_senha = generate_password_hash(nova_senha)
        user_id = session.get('usuario_id')
        
        repo = UsuarioRepository()
        repo.alterar_senha(user_id, hash_senha)
        session['precisa_trocar_senha'] = False

        AuditoriaService().registrar_evento('usuarios', 'UPDATE', dados_novos={'acao': 'troca_senha_efetuada'})
        flash('Senha atualizada com sucesso! Acesso regular liberado.', 'success')

        if AuthService.exigir_admin():
            return redirect(url_for('admin.painel'))
        return redirect(url_for('minha_universidade.painel'))

    return render_template('institucional/trocar_senha.html')