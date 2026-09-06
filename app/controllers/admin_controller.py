from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.services.auth_service import AuthService
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.repositories.auditoria_repository import AuditoriaRepository
from app.services.motor_calculo import MotorCalculo
from app.services.auditoria_service import AuditoriaService

admin_bp = Blueprint('admin', __name__)

@admin_bp.before_request
def verificar_acesso_admin():
    if not AuthService.esta_autenticado() or not AuthService.exigir_admin():
        abort(403)

@admin_bp.route('/')
def painel():
    reg_repo = RegistroRepository()
    submissoes_pendentes = reg_repo.listar_submissoes_pendentes()
    return render_template('admin/painel.html', submissoes=submissoes_pendentes)

@admin_bp.route('/submissoes')
def submissoes():
    reg_repo = RegistroRepository()
    itens = reg_repo.listar_submissoes_pendentes()
    return render_template('admin/submissoes.html', submissoes=itens)

@admin_bp.route('/submissoes/<int:registro_id>/decisao', methods=['POST'])
def decidir_submissao(registro_id):
    decisao = request.form.get('decisao')  # VALIDAR ou DEVOLVER
    parecer = request.form.get('parecer', '').strip()

    if decisao == 'DEVOLVER' and not parecer:
        flash('Para devolver uma submissão, o parecer analítico é obrigatório.', 'warning')
        return redirect(url_for('admin.submissoes'))

    novo_status = 'VALIDADO' if decisao == 'VALIDAR' else 'DEVOLVER'
    reg_repo = RegistroRepository()
    reg_repo.atualizar_status(registro_id, novo_status, parecer if novo_status == 'DEVOLVER' else None)

    # Dispara recálculo se aprovado
    registro = reg_repo.executar_consulta_um("SELECT * FROM registro_dados WHERE id = %s", (registro_id,))
    if registro and novo_status == 'VALIDADO':
        MotorCalculo().calcular_indicadores_derivados(registro['universidade_id'], registro['ano_referencia'])

    AuditoriaService().registrar_evento('registro_dados', 'VALIDACAO', dados_novos={'id': registro_id, 'status': novo_status})
    flash(f'Registro {novo_status.lower()} com sucesso!', 'success')
    return redirect(url_for('admin.submissoes'))

@admin_bp.route('/auditoria')
def auditoria():
    aud_repo = AuditoriaRepository()
    registros = aud_repo.listar_ultimas(100)
    return render_template('admin/auditoria.html', auditoria=registros)