from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.services.auth_service import AuthService
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.models.registro_dado import RegistroDado
from app.services.motor_calculo import MotorCalculo
from app.services.auditoria_service import AuditoriaService

minha_universidade_bp = Blueprint('minha_universidade', __name__)

@minha_universidade_bp.route('/')
def painel():
    if not AuthService.esta_autenticado():
        return redirect(url_for('auth.login'))

    usuario = AuthService.usuario_atual()
    uni_repo = UniversidadeRepository()
    ind_repo = IndicadorRepository()
    reg_repo = RegistroRepository()

    is_admin = (usuario.get('perfil') == 'ADMIN_CAMARA')
    universidades_disponiveis = uni_repo.listar_todas(apenas_ativas=True) if is_admin else []

    if is_admin:
        default_uni = usuario.get('universidade_id') or (universidades_disponiveis[0].id if universidades_disponiveis else 'U31')
        uni_id = request.args.get('universidade_id', default_uni)
    else:
        uni_id = usuario.get('universidade_id')

    if not uni_id:
        flash('Nenhuma instituição vinculada ao seu usuário.', 'warning')
        return redirect(url_for('home.index'))

    universidade = uni_repo.buscar_por_id(uni_id)
    if not universidade and universidades_disponiveis:
        universidade = universidades_disponiveis[0]
        uni_id = universidade.id

    exercicio_referencia = int(request.args.get('ano', 2025))
    anos_ciclo = [2022, 2023, 2024, 2025]

    # Indicadores do Núcleo Essencial (Digitáveis) e Calculados
    todos_indicadores = ind_repo.listar_todos(apenas_ativos=True)
    indicadores_digitaveis = [i for i in todos_indicadores if not i.is_calculado()]
    indicadores_calculados = [i for i in todos_indicadores if i.is_calculado()]

    # Mapeamento de registros por indicador e ano: matriz[indicador_id][ano] -> RegistroDado
    matriz_registros = {}
    total_validados = 0
    total_aguardando = 0
    total_rascunhos = 0
    total_devolvidos = 0

    for ind in todos_indicadores:
        matriz_registros[ind.id] = {}
        for a in anos_ciclo:
            reg = reg_repo.buscar_por_chave(uni_id, ind.id, a)
            matriz_registros[ind.id][a] = reg
            if reg and reg.valor_numerico is not None:
                if reg.status_dado == 'VALIDADO':
                    total_validados += 1
                elif reg.status_dado == 'ENVIADO':
                    total_aguardando += 1
                elif reg.status_dado == 'RASCUNHO':
                    total_rascunhos += 1
                elif reg.status_dado == 'DEVOLVIDO':
                    total_devolvidos += 1

    responsaveis = uni_repo.listar_responsaveis(uni_id)

    return render_template('institucional/minha_universidade.html',
                           universidade=universidade,
                           ano_referencia=exercicio_referencia,
                           anos_ciclo=anos_ciclo,
                           indicadores_digitaveis=indicadores_digitaveis,
                           indicadores_calculados=indicadores_calculados,
                           matriz=matriz_registros,
                           total_validados=total_validados,
                           total_aguardando=total_aguardando,
                           total_rascunhos=total_rascunhos,
                           total_devolvidos=total_devolvidos,
                           responsaveis=responsaveis,
                           is_admin=is_admin,
                           universidades_disponiveis=universidades_disponiveis)

@minha_universidade_bp.route('/salvar-serie', methods=['POST'])
def salvar_serie():
    """
    Preenche uma série de uma vez (2022 a 2025) para um único indicador.
    O filtro de 'fonte dos dados' foi completamente removido conforme o acordo de 16-09-2026.
    """
    if not AuthService.esta_autenticado():
        return redirect(url_for('auth.login'))

    uni_id = request.form.get('universidade_id')
    if not AuthService.exigir_escrita_universidade(uni_id):
        abort(403)

    ind_id = request.form.get('indicador_id')
    obs = request.form.get('observacao', '').strip()
    anos = [2022, 2023, 2024, 2025]

    reg_repo = RegistroRepository()
    ind_repo = IndicadorRepository()
    indicador = ind_repo.buscar_por_id(ind_id)

    if indicador and indicador.is_calculado():
        flash('Indicadores derivados não aceitam gravação direta de série.', 'warning')
        return redirect(url_for('minha_universidade.painel', universidade_id=uni_id))

    gravados = 0
    for a in anos:
        val_raw = request.form.get(f'valor_{a}', '').strip()
        if val_raw != '':
            try:
                limpo = val_raw.replace('R$', '').replace('.', '').replace(',', '.').strip()
                val_num = round(float(limpo), 2)
            except ValueError:
                continue

            reg = RegistroDado(
                universidade_id=uni_id,
                indicador_id=ind_id,
                ano_referencia=a,
                valor_numerico=val_num,
                status_dado='RASCUNHO',
                fonte_descricao=obs or 'Série declarada pela instituição',
                atualizado_por=session.get('usuario_id')
            )
            reg_repo.salvar(reg)
            gravados += 1
            MotorCalculo().calcular_indicadores_derivados(uni_id, a, usuario_id=session.get('usuario_id'))

    AuditoriaService().registrar_evento(
        'registro_dados', 'UPDATE',
        dados_novos={'acao': 'preencher_serie', 'indicador': ind_id, 'gravados': gravados},
        universidade_id=uni_id
    )

    flash(f'Série do indicador gravada como rascunho ({gravados} exercícios atualizados).', 'success')
    return redirect(url_for('minha_universidade.painel', universidade_id=uni_id))

@minha_universidade_bp.route('/salvar-celula', methods=['POST'])
def salvar_celula():
    """
    Gravação rápida de célula avulsa com salvamento em rascunho.
    """
    if not AuthService.esta_autenticado():
        return {'erro': 'Não autenticado'}, 401

    uni_id = request.form.get('universidade_id')
    if not AuthService.exigir_escrita_universidade(uni_id):
        return {'erro': 'Acesso não autorizado'}, 403

    ind_id = request.form.get('indicador_id')
    ano = int(request.form.get('ano_referencia'))
    valor_raw = request.form.get('valor', '').strip()

    val_num = None
    if valor_raw != '':
        try:
            limpo = valor_raw.replace('R$', '').replace('.', '').replace(',', '.').strip()
            val_num = round(float(limpo), 2)
        except ValueError:
            return {'erro': 'Formato numérico inválido'}, 400

    reg_repo = RegistroRepository()
    reg = RegistroDado(
        universidade_id=uni_id,
        indicador_id=ind_id,
        ano_referencia=ano,
        valor_numerico=val_num,
        status_dado='RASCUNHO',
        atualizado_por=session.get('usuario_id')
    )
    reg_repo.salvar(reg)
    MotorCalculo().calcular_indicadores_derivados(uni_id, ano, usuario_id=session.get('usuario_id'))

    return {'sucesso': True, 'valor': val_num}

@minha_universidade_bp.route('/enviar-lote', methods=['POST'])
def enviar_lote():
    if not AuthService.esta_autenticado():
        return redirect(url_for('auth.login'))

    uni_id = request.form.get('universidade_id')
    if not AuthService.exigir_escrita_universidade(uni_id):
        abort(403)

    reg_repo = RegistroRepository()
    # Atualiza todos os rascunhos da universidade para ENVIADO
    sql = """
        UPDATE registro_dados 
        SET status_dado = 'ENVIADO' 
        WHERE universidade_id = %s AND status_dado IN ('RASCUNHO', 'DEVOLVIDO')
    """
    afetados = reg_repo.executar_comando(sql, (uni_id,))

    AuditoriaService().registrar_evento(
        'registro_dados', 'UPDATE',
        dados_novos={'acao': 'enviar_lote_validacao', 'total': afetados},
        universidade_id=uni_id
    )

    flash(f'{afetados} registro(s) enviados com sucesso para a validação da Câmara!', 'success')
    return redirect(url_for('minha_universidade.painel', universidade_id=uni_id))