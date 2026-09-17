from flask import Blueprint, render_template, request
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.repositories.convenio_repository import ConvenioRepository
from app.services.estatistica_service import EstatisticaService

dimensoes_bp = Blueprint('dimensoes', __name__)

@dimensoes_bp.route('/academico')
def academico():
    uni_repo = UniversidadeRepository()
    reg_repo = RegistroRepository()
    ano = int(request.args.get('ano', 2024))

    registros_mat = reg_repo.listar_para_painel_publico('ACA_GRAD_TOTAL', [ano])
    registros_cur = reg_repo.listar_para_painel_publico('ACA_CURSOS_GRAD', [ano])

    valores_mat = [r['valor_numerico'] for r in registros_mat if r.get('valor_numerico') is not None]
    valores_cur = [r['valor_numerico'] for r in registros_cur if r.get('valor_numerico') is not None]

    total_matriculas = round(sum(valores_mat), 0) if valores_mat else 0
    total_cursos = round(sum(valores_cur), 0) if valores_cur else 0

    return render_template('public/academico.html',
                           ano=ano,
                           total_matriculas=total_matriculas,
                           n_matriculas=len(valores_mat),
                           total_cursos=total_cursos,
                           n_cursos=len(valores_cur))

@dimensoes_bp.route('/pessoas')
def pessoas():
    reg_repo = RegistroRepository()
    ano = int(request.args.get('ano', 2024))

    reg_doc = reg_repo.listar_para_painel_publico('PES_DOCENTES_TOTAL', [ano])
    reg_tec = reg_repo.listar_para_painel_publico('PES_TECNICOS_TOTAL', [ano])

    val_doc = [r['valor_numerico'] for r in reg_doc if r.get('valor_numerico') is not None]
    val_tec = [r['valor_numerico'] for r in reg_tec if r.get('valor_numerico') is not None]

    total_docentes = round(sum(val_doc), 0) if val_doc else 0
    total_tecnicos = round(sum(val_tec), 0) if val_tec else 0

    return render_template('public/pessoas.html',
                           ano=ano,
                           total_docentes=total_docentes,
                           n_docentes=len(val_doc),
                           total_tecnicos=total_tecnicos,
                           n_tecnicos=len(val_tec))

@dimensoes_bp.route('/financas')
def financas():
    reg_repo = RegistroRepository()
    ano = int(request.args.get('ano', 2024))

    reg_liq = reg_repo.listar_para_painel_publico('FIN_LIQUIDADO', [ano])
    reg_aut = reg_repo.listar_para_painel_publico('FIN_ORCAMENTO_ATUALIZADO', [ano])

    val_liq = [r['valor_numerico'] for r in reg_liq if r.get('valor_numerico') is not None]
    val_aut = [r['valor_numerico'] for r in reg_aut if r.get('valor_numerico') is not None]

    total_liquidado = round(sum(val_liq), 2) if val_liq else 0.00
    total_autorizado = round(sum(val_aut), 2) if val_aut else 0.00

    return render_template('public/financas.html',
                           ano=ano,
                           total_liquidado=total_liquidado,
                           n_liquidado=len(val_liq),
                           total_autorizado=total_autorizado,
                           n_autorizado=len(val_aut))

@dimensoes_bp.route('/eficiencia')
def eficiencia():
    reg_repo = RegistroRepository()
    ano = int(request.args.get('ano', 2024))

    reg_liq = reg_repo.listar_para_painel_publico('FIN_LIQUIDADO', [ano])
    reg_aut = reg_repo.listar_para_painel_publico('FIN_ORCAMENTO_ATUALIZADO', [ano])

    mapa_liq = {r['universidade_id']: r['valor_numerico'] for r in reg_liq if r.get('valor_numerico') is not None}
    mapa_aut = {r['universidade_id']: r['valor_numerico'] for r in reg_aut if r.get('valor_numerico') is not None}

    unis_comuns = set(mapa_liq.keys()).intersection(set(mapa_aut.keys()))
    soma_liq = sum(mapa_liq[u] for u in unis_comuns)
    soma_aut = sum(mapa_aut[u] for u in unis_comuns)

    execucao_conjunto = round((soma_liq / soma_aut) * 100.0, 2) if soma_aut > 0 else 0.00

    percentuais_individuais = []
    for u in unis_comuns:
        if mapa_aut[u] > 0:
            percentuais_individuais.append(round((mapa_liq[u] / mapa_aut[u]) * 100.0, 2))

    stats = EstatisticaService.calcular_estatisticas_grupo(percentuais_individuais)

    return render_template('public/eficiencia.html',
                           ano=ano,
                           execucao_conjunto=execucao_conjunto,
                           mediana_execucao=stats.get('mediana'),
                           n_instituicoes=len(unis_comuns))

@dimensoes_bp.route('/custo-aluno')
def custo_aluno():
    reg_repo = RegistroRepository()
    ano = int(request.args.get('ano', 2024))

    reg_der = reg_repo.listar_para_painel_publico('DER_CUSTO_ALUNO', [ano])
    valores = [r['valor_numerico'] for r in reg_der if r.get('valor_numerico') is not None]
    stats = EstatisticaService.calcular_estatisticas_grupo(valores)

    return render_template('public/custo_aluno.html',
                           ano=ano,
                           custo_aluno_medio=stats.get('media'),
                           custo_aluno_mediana=stats.get('mediana'),
                           n_apurados=stats.get('n'))

@dimensoes_bp.route('/convenios')
def convenios():
    conv_repo = ConvenioRepository()
    ano = int(request.args.get('ano', 2024))

    sql = """
        SELECT 
            COALESCE(SUM(valor_global), 0.00) as total_global,
            COALESCE(SUM(valor_liberado), 0.00) as total_liberado,
            COUNT(*) as total_instrumentos
        FROM convenios
        WHERE ano_referencia = %s
    """
    totais = conv_repo.executar_consulta_um(sql, (ano,)) or {}

    return render_template('public/convenios.html',
                           ano=ano,
                           total_global=totais.get('total_global', 0.00),
                           total_liberado=totais.get('total_liberado', 0.00),
                           total_instrumentos=totais.get('total_instrumentos', 0))