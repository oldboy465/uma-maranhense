import re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.services.auth_service import AuthService
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.models.registro_dado import RegistroDado
from app.services.motor_calculo import MotorCalculo
from app.services.auditoria_service import AuditoriaService

minha_universidade_bp = Blueprint('minha_universidade', __name__)

def sanitizar_valor_brasileiro(valor_str):
    """
    Higieniza estritamente os campos:
    - Não permite letras, espaços, pontos ou caracteres especiais.
    - Permite somente números e no máximo uma única vírgula.
    - Retorna float ou None se vazio. Levanta ValueError se formato for violado.
    """
    if valor_str is None:
        return None
    
    val = str(valor_str).strip()
    if val == '' or val == '-':
        return None

    # Rejeita imediatamente se contiver letras, espaços ou pontos
    if re.search(r'[^0-9,]', val):
        raise ValueError("Inserção inválida: não são permitidos letras, espaços ou pontos. Use apenas números e vírgula.")

    # Permite no máximo uma vírgula
    if val.count(',') > 1:
        raise ValueError("Inserção inválida: permitido no máximo uma vírgula decimal.")

    # Converte vírgula para ponto decimal para persistência float
    val_normalizado = val.replace(',', '.')
    return round(float(val_normalizado), 2)


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

    todos_indicadores = ind_repo.listar_todos(apenas_ativos=True)
    indicadores_digitaveis = [i for i in todos_indicadores if not i.is_calculado()]
    indicadores_calculados = [i for i in todos_indicadores if i.is_calculado()]

    matriz_registros = {}
    total_validados = 0
    total_aguardando = 0
    total_rascunhos = 0
    total_devolvidos = 0
    total_solicitados_alteracao = 0

    # Dicionário auxiliar para controlar se a linha inteira pode solicitar alteração
    linha_status_map = {}

    for ind in todos_indicadores:
        matriz_registros[ind.id] = {}
        status_linha_set = set()

        for a in anos_ciclo:
            reg = reg_repo.buscar_por_chave(uni_id, ind.id, a)
            matriz_registros[ind.id][a] = reg
            if reg and reg.valor_numerico is not None:
                status_linha_set.add(reg.status_dado)
                if reg.status_dado == 'VALIDADO':
                    total_validados += 1
                elif reg.status_dado == 'ENVIADO':
                    total_aguardando += 1
                elif reg.status_dado == 'RASCUNHO':
                    total_rascunhos += 1
                elif reg.status_dado == 'DEVOLVIDO':
                    total_devolvidos += 1
                elif reg.status_dado == 'SOLICITADO_ALTERACAO':
                    total_solicitados_alteracao += 1

        # Uma linha é considerada em solicitação de alteração se ao menos uma de suas células estiver assim
        if 'SOLICITADO_ALTERACAO' in status_linha_set:
            linha_status_map[ind.id] = 'SOLICITADO_ALTERACAO'
        elif 'ENVIADO' in status_linha_set:
            linha_status_map[ind.id] = 'ENVIADO'
        elif 'VALIDADO' in status_linha_set:
            linha_status_map[ind.id] = 'VALIDADO'
        elif 'DEVOLVIDO' in status_linha_set:
            linha_status_map[ind.id] = 'DEVOLVIDO'
        else:
            linha_status_map[ind.id] = 'RASCUNHO'

    responsaveis = uni_repo.listar_responsaveis(uni_id)

    return render_template('institucional/minha_universidade.html',
                           universidade=universidade,
                           ano_referencia=exercicio_referencia,
                           anos_ciclo=anos_ciclo,
                           indicadores_digitaveis=indicadores_digitaveis,
                           indicadores_calculados=indicadores_calculados,
                           matriz=matriz_registros,
                           linha_status_map=linha_status_map,
                           total_validados=total_validados,
                           total_aguardando=total_aguardando,
                           total_rascunhos=total_rascunhos,
                           total_devolvidos=total_devolvidos,
                           total_solicitados_alteracao=total_solicitados_alteracao,
                           responsaveis=responsaveis,
                           is_admin=is_admin,
                           universidades_disponiveis=universidades_disponiveis)


@minha_universidade_bp.route('/salvar-celula', methods=['POST'])
def salvar_celula():
    """
    Gravação rápida assíncrona ao mudar valor da célula.
    Garante sanitização estrita e bloqueio em células não-editáveis.
    """
    if not AuthService.esta_autenticado():
        return {'erro': 'Não autenticado'}, 401

    uni_id = request.form.get('universidade_id')
    if not AuthService.exigir_escrita_universidade(uni_id):
        return {'erro': 'Acesso não autorizado para esta universidade'}, 403

    ind_id = request.form.get('indicador_id')
    ano = int(request.form.get('ano_referencia'))
    valor_raw = request.form.get('valor', '')

    reg_repo = RegistroRepository()
    reg_existente = reg_repo.buscar_por_chave(uni_id, ind_id, ano)

    # Impede edição de campos bloqueados (ENVIADO, VALIDADO ou SOLICITADO_ALTERACAO)
    if reg_existente and not reg_existente.is_editavel_por_gestor() and not AuthService.exigir_admin():
        return {'erro': 'Campo bloqueado para alteração direta.'}, 400

    try:
        val_num = sanitizar_valor_brasileiro(valor_raw)
    except ValueError as e:
        return {'erro': str(e)}, 400

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


@minha_universidade_bp.route('/enviar-validacao', methods=['POST'])
def enviar_validacao():
    """
    Submete todos os campos em RASCUNHO/DEVOLVIDO da tabela direta para validação da Câmara.
    Após submissão, os campos ficam bloqueados em modo visualização.
    """
    if not AuthService.esta_autenticado():
        return redirect(url_for('auth.login'))

    uni_id = request.form.get('universidade_id')
    if not AuthService.exigir_escrita_universidade(uni_id):
        AuditoriaService().registrar_evento('seguranca', 'ACESSO_NEGADO', dados_novos={'acao': 'tentativa_envio_validacao', 'alvo': uni_id})
        abort(403)

    reg_repo = RegistroRepository()
    sql = """
        UPDATE registro_dados 
        SET status_dado = 'ENVIADO' 
        WHERE universidade_id = %s 
          AND status_dado IN ('RASCUNHO', 'DEVOLVIDO')
          AND valor_numerico IS NOT NULL
    """
    afetados = reg_repo.executar_comando(sql, (uni_id,))

    AuditoriaService().registrar_evento(
        'registro_dados', 'SUBMISSAO',
        dados_novos={'acao': 'enviar_para_validacao', 'registros_submetidos': afetados},
        universidade_id=uni_id
    )

    if afetados > 0:
        flash(f'{afetados} indicador(es) enviados para validação do Admin! Os campos agora estão bloqueados para edição.', 'success')
    else:
        flash('Nenhum dado novo ou pendente de envio encontrado para submissão.', 'info')

    return redirect(url_for('minha_universidade.painel', universidade_id=uni_id))


@minha_universidade_bp.route('/solicitar-alteracao', methods=['POST'])
def solicitar_alteracao():
    """
    Envia pedido formal ao Admin para alteração de um indicador específico.
    Bloqueia o indicador até decisão da Câmara.
    """
    if not AuthService.esta_autenticado():
        return redirect(url_for('auth.login'))

    uni_id = request.form.get('universidade_id')
    ind_id = request.form.get('indicador_id')

    if not AuthService.exigir_escrita_universidade(uni_id):
        AuditoriaService().registrar_evento('seguranca', 'ACESSO_NEGADO', dados_novos={'acao': 'tentativa_solicitar_alteracao', 'alvo': uni_id})
        abort(403)

    reg_repo = RegistroRepository()
    afetados = reg_repo.solicitar_alteracao_indicador(uni_id, ind_id, usuario_id=session.get('usuario_id'))

    AuditoriaService().registrar_evento(
        'registro_dados', 'SOLICITACAO_ALTERACAO',
        dados_novos={'indicador_id': ind_id, 'universidade_id': uni_id, 'registros_afetados': afetados},
        universidade_id=uni_id
    )

    flash('Solicitação de alteração enviada para a validação do Admin. A linha permanecerá bloqueada até análise da Câmara.', 'info')
    return redirect(url_for('minha_universidade.painel', universidade_id=uni_id))