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
    uni_id = usuario.get('universidade_id')
    
    # Se for admin visualizando como gestor, aceita parametro via query string
    if usuario.get('perfil') == 'ADMIN_CAMARA':
        uni_id = request.args.get('universidade_id', uni_id or 'U01')

    if not uni_id:
        flash('Nenhuma instituição vinculada ao seu usuário.', 'warning')
        return redirect(url_for('home.index'))

    uni_repo = UniversidadeRepository()
    ind_repo = IndicadorRepository()
    reg_repo = RegistroRepository()

    universidade = uni_repo.buscar_por_id(uni_id)
    ano_referencia = int(request.args.get('ano', 2024))

    indicadores = ind_repo.listar_todos(apenas_ativos=True)
    registros = reg_repo.listar_por_universidade_e_ano(uni_id, ano_referencia)
    mapa_registros = {r['indicador_id']: r for r in registros}

    return render_template('institucional/minha_universidade.html',
                           universidade=universidade,
                           ano=ano_referencia,
                           indicadores=indicadores,
                           registros=mapa_registros)

@minha_universidade_bp.route('/salvar-indicador', methods=['POST'])
def salvar_indicador():
    if not AuthService.esta_autenticado():
        return redirect(url_for('auth.login'))

    uni_id = request.form.get('universidade_id')
    if not AuthService.exigir_escrita_universidade(uni_id):
        abort(403)

    ind_id = request.form.get('indicador_id')
    ano = int(request.form.get('ano_referencia'))
    valor_raw = request.form.get('valor', '').strip()
    acao = request.form.get('acao', 'salvar_rascunho')  # salvar_rascunho ou enviar

    reg_repo = RegistroRepository()
    ind_repo = IndicadorRepository()
    indicador = ind_repo.buscar_por_id(ind_id)

    # Indicadores calculados não aceitam entrada manual
    if indicador and indicador.is_calculado():
        flash('Indicadores derivados são calculados automaticamente pelo sistema.', 'warning')
        return redirect(url_for('minha_universidade.painel', universidade_id=uni_id, ano=ano))

    # Conversão de formato monetário/numérico brasileiro (1.234,56 -> 1234.56)
    valor_numerico = None
    if valor_raw:
        try:
            limpo = valor_raw.replace('R$', '').replace('.', '').replace(',', '.').strip()
            valor_numerico = round(float(limpo), 2)
        except ValueError:
            flash('Formato numérico inválido. Use o padrão brasileiro (ex: 1.250,50).', 'danger')
            return redirect(url_for('minha_universidade.painel', universidade_id=uni_id, ano=ano))

    status_destino = 'ENVIADO' if acao == 'enviar' else 'RASCUNHO'

    registro = RegistroDado(
        universidade_id=uni_id,
        indicador_id=ind_id,
        ano_referencia=ano,
        valor_numerico=valor_numerico,
        status_dado=status_destino,
        fonte_tipo=request.form.get('fonte_tipo'),
        fonte_descricao=request.form.get('fonte_descricao'),
        fonte_url=request.form.get('fonte_url'),
        atualizado_por=session.get('usuario_id')
    )
    reg_repo.salvar(registro)

    # Dispara o recálculo dos indicadores derivados dependentes
    MotorCalculo().calcular_indicadores_derivados(uni_id, ano, usuario_id=session.get('usuario_id'))

    AuditoriaService().registrar_evento(
        'registro_dados', 'UPDATE',
        dados_novos={'indicador': ind_id, 'ano': ano, 'valor': valor_numerico, 'status': status_destino},
        universidade_id=uni_id
    )

    msg = 'Registro submetido para validação da Câmara!' if status_destino == 'ENVIADO' else 'Rascunho salvo com sucesso.'
    flash(msg, 'success')
    return redirect(url_for('minha_universidade.painel', universidade_id=uni_id, ano=ano))