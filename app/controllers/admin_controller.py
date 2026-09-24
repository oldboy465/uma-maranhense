from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.services.auth_service import AuthService
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.repositories.auditoria_repository import AuditoriaRepository
from app.services.motor_calculo import MotorCalculo
from app.services.auditoria_service import AuditoriaService
from werkzeug.security import generate_password_hash

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

@admin_bp.route('/universidades')
def universidades():
    uni_repo = UniversidadeRepository()
    ano = int(request.args.get('ano', 2025))
    lista_com_estatisticas = uni_repo.listar_com_estatisticas_admin(ano_referencia=ano)

    for item in lista_com_estatisticas:
        u = item['universidade']
        item['responsaveis'] = uni_repo.listar_responsaveis(u.id)

    return render_template('admin/universidades.html',
                           instituicoes=lista_com_estatisticas,
                           ano=ano)

@admin_bp.route('/universidades/<id>/editar', methods=['GET', 'POST'])
def editar_universidade(id):
    uni_repo = UniversidadeRepository()
    universidade = uni_repo.buscar_por_id(id)
    if not universidade:
        abort(404)

    if request.method == 'POST':
        universidade.sigla = request.form.get('sigla', universidade.sigla).strip()
        universidade.nome = request.form.get('nome', universidade.nome).strip()
        universidade.tipo = request.form.get('tipo', universidade.tipo).strip()
        universidade.uf = request.form.get('uf', universidade.uf).strip()
        universidade.regiao = request.form.get('regiao', universidade.regiao).strip()
        universidade.municipio_sede = request.form.get('municipio_sede', universidade.municipio_sede).strip()
        
        autonomia_raw = request.form.get('autonomia_financeira', '0')
        universidade.autonomia_financeira = 1 if autonomia_raw in ('1', 1, 'on', True) else 0

        uni_repo.salvar(universidade)

        AuditoriaService().registrar_evento(
            'universidades', 'UPDATE',
            dados_novos={'id': universidade.id, 'autonomia_financeira': universidade.autonomia_financeira},
            universidade_id=universidade.id
        )

        flash(f'Dados da instituição {universidade.sigla} atualizados com sucesso!', 'success')
        return redirect(url_for('admin.universidades'))

    return render_template('admin/editar_universidade.html', universidade=universidade)

@admin_bp.route('/submissoes')
def submissoes():
    reg_repo = RegistroRepository()
    itens = reg_repo.listar_submissoes_pendentes()
    return render_template('admin/submissoes.html', submissoes=itens)

@admin_bp.route('/submissoes/<int:registro_id>/decisao', methods=['POST'])
def decidir_submissao(registro_id):
    """
    Decisão independente por indicador:
    - Se for validação de novo lançamento (ENVIADO): VALIDAR aprova e homologa; DEVOLVER rejeita individualmente.
    - Se for solicitação de alteração (SOLICITADO_ALTERACAO):
        * APROVAR_ALTERACAO: Zera a linha do indicador na IES e a reabre como RASCUNHO editável.
        * RECUSAR_ALTERACAO: Mantém o valor anterior intacto e o reclassifica como VALIDADO.
    """
    decisao = request.form.get('decisao')
    parecer = request.form.get('parecer', '').strip()

    reg_repo = RegistroRepository()
    registro = reg_repo.buscar_por_id(registro_id)

    if not registro:
        flash('Registro não localizado na base de dados.', 'danger')
        return redirect(url_for('admin.submissoes'))

    # Caso 1: Tratamento de Solicitação de Alteração de Indicador
    if registro.status_dado == 'SOLICITADO_ALTERACAO':
        if decisao == 'APROVAR_ALTERACAO':
            reg_repo.liberar_e_zerar_indicador(registro.universidade_id, registro.indicador_id)
            MotorCalculo().calcular_indicadores_derivados(registro.universidade_id, registro.ano_referencia)
            AuditoriaService().registrar_evento('registro_dados', 'ALTERACAO_AUTORIZADA',
                                                dados_novos={'indicador_id': registro.indicador_id, 'universidade_id': registro.universidade_id})
            flash('Solicitação de alteração aceita. A linha do indicador foi zerada e reaberta para preenchimento da universidade!', 'success')
        else:
            reg_repo.rejeitar_pedido_alteracao(registro.universidade_id, registro.indicador_id, parecer=parecer)
            AuditoriaService().registrar_evento('registro_dados', 'ALTERACAO_RECUSADA',
                                                dados_novos={'indicador_id': registro.indicador_id, 'parecer': parecer})
            flash('Solicitação de alteração recusada. Os dados anteriores foram preservados.', 'warning')

        return redirect(url_for('admin.submissoes'))

    # Caso 2: Validação ou Rejeição de Lançamento Direto (ENVIADO)
    if decisao == 'DEVOLVER' and not parecer:
        flash('Para rejeitar ou devolver um indicador, o parecer analítico é obrigatório.', 'warning')
        return redirect(url_for('admin.submissoes'))

    if decisao == 'VALIDAR':
        novo_status = 'VALIDADO'
        reg_repo.atualizar_status(registro_id, novo_status, parecer=None)
        MotorCalculo().calcular_indicadores_derivados(registro.universidade_id, registro.ano_referencia)
        flash('Indicador validado com sucesso! Já está refletido nos cálculos públicos.', 'success')
    else:
        novo_status = 'DEVOLVIDO'
        reg_repo.atualizar_status(registro_id, novo_status, parecer=parecer)
        flash('Indicador devolvido para correção da universidade. Os demais indicadores não foram afetados.', 'warning')

    AuditoriaService().registrar_evento('registro_dados', 'VALIDACAO',
                                        dados_novos={'id': registro_id, 'indicador_id': registro.indicador_id, 'status': novo_status, 'parecer': parecer})

    return redirect(url_for('admin.submissoes'))

@admin_bp.route('/usuarios')
def usuarios():
    usr_repo = UsuarioRepository()
    usuarios_lista = usr_repo.listar_todos()
    return render_template('admin/usuarios.html', usuarios=usuarios_lista)

@admin_bp.route('/usuarios/<int:usuario_id>/resetar-senha', methods=['POST'])
def resetar_senha_usuario(usuario_id):
    usr_repo = UsuarioRepository()
    usuario = usr_repo.buscar_por_id(usuario_id)

    if not usuario:
        flash('Usuário não localizado no sistema.', 'danger')
        return redirect(url_for('admin.usuarios'))

    hash_padrao = generate_password_hash("123456")
    usr_repo.resetar_senha_para_padrao(usuario_id, hash_padrao)

    AuditoriaService().registrar_evento(
        'usuarios', 'UPDATE',
        dados_novos={'acao': 'reset_senha_admin', 'usuario_alvo': usuario.email, 'usuario_id': usuario_id}
    )

    flash(f'A senha do usuário {usuario.nome} ({usuario.email}) foi resetada para 123456 com redefinição forçada!', 'success')
    return redirect(url_for('admin.usuarios'))

@admin_bp.route('/indicadores')
def indicadores():
    ind_repo = IndicadorRepository()
    indicadores_lista = ind_repo.listar_todos(apenas_ativos=False)
    return render_template('admin/indicadores.html', indicadores=indicadores_lista)

@admin_bp.route('/registros')
def registros():
    reg_repo = RegistroRepository()
    sql = """
        SELECT r.*, u.sigla as universidade_sigla, i.nome as indicador_nome
        FROM registro_dados r
        INNER JOIN universidades u ON r.universidade_id = u.id
        INNER JOIN indicadores i ON r.indicador_id = i.id
        ORDER BY r.atualizado_em DESC
        LIMIT 100
    """
    registros_lista = reg_repo.executar_consulta(sql)
    return render_template('admin/registros.html', registros=registros_lista)

@admin_bp.route('/auditoria')
def auditoria():
    aud_repo = AuditoriaRepository()
    registros_aud = aud_repo.listar_ultimas(100)
    return render_template('admin/auditoria.html', auditoria=registros_aud)