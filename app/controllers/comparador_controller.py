from flask import Blueprint, render_template, request
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.services.estatistica_service import EstatisticaService

comparador_bp = Blueprint('comparador', __name__)

@comparador_bp.route('/')
def index():
    uni_repo = UniversidadeRepository()
    ind_repo = IndicadorRepository()
    reg_repo = RegistroRepository()

    # Filtros recebidos
    ano = int(request.args.get('ano', 2023))
    filtro_autonomia = request.args.get('autonomia', 'TODAS').upper()  # SIM, NAO, TODAS
    indicador_id = request.args.get('i', 'ACA_ALUNOS_TOTAL').strip()

    # Mapeamento de autonomia para repositório
    autonomia_param = None
    if filtro_autonomia == 'SIM':
        autonomia_param = 1
    elif filtro_autonomia == 'NAO':
        autonomia_param = 0

    universidades_disponiveis = uni_repo.listar_todas(apenas_ativas=True, autonomia=autonomia_param)
    todos_indicadores = ind_repo.listar_todos(apenas_ativos=True)
    indicador_selecionado = ind_repo.buscar_por_id(indicador_id) or ind_repo.buscar_por_id('ACA_ALUNOS_TOTAL')

    # Universidades selecionadas (suporte de 2 a 5 universidades)
    selecionadas_siglas = request.args.getlist('u')
    if not selecionadas_siglas:
        # Default de demonstração idêntico ao PDF
        selecionadas_siglas = ['UEL', 'UNEMAT', 'UNIMONTES']

    # Recupera instâncias das selecionadas
    universidades_selecionadas = []
    for sigla in selecionadas_siglas:
        u = uni_repo.buscar_por_sigla(sigla)
        if u and (autonomia_param is None or u.autonomia_financeira == autonomia_param):
            universidades_selecionadas.append(u)

    ids_selecionados = [u.id for u in universidades_selecionadas]

    # 1. Gráfico de Barras: apenas universidades com dados no indicador selecionado e ano
    barras_comparativo = []
    max_barra = 1.0
    for u in universidades_selecionadas:
        reg = reg_repo.buscar_por_chave(u.id, indicador_selecionado.id, ano)
        if reg and reg.valor_numerico is not None and reg.status_dado == 'VALIDADO':
            barras_comparativo.append({
                'universidade': u,
                'valor': reg.valor_numerico
            })
            if reg.valor_numerico > max_barra:
                max_barra = reg.valor_numerico

    # Ordena decrescente pela magnitude
    barras_comparativo.sort(key=lambda x: x['valor'], reverse=True)

    # 2. Gráfico de Linhas de Evolução Comparada (2022 a 2025)
    # Regra estrita: a universidade só aparece no gráfico se tiver dados sincronizados; sem dados, omite-se apenas ela
    series_linhas = reg_repo.listar_series_comparador(ids_selecionados, indicador_selecionado.id, [2022, 2023, 2024, 2025])

    # 3. Quadro Comparativo (Valores, variação vs ano anterior e mediana)
    quadro_comparativo = []
    todos_ano_rede = reg_repo.listar_para_painel_publico(indicador_selecionado.id, [ano])
    valores_rede = [r['valor_numerico'] for r in todos_ano_rede if r.get('valor_numerico') is not None]
    stats_rede = EstatisticaService.calcular_estatisticas_grupo(valores_rede)
    mediana_rede = stats_rede.get('mediana')

    for item in barras_comparativo:
        u = item['universidade']
        v_atual = item['valor']
        # Busca ano anterior para cálculo de variação
        reg_ant = reg_repo.buscar_por_chave(u.id, indicador_selecionado.id, ano - 1)
        v_ant = reg_ant.valor_numerico if (reg_ant and reg_ant.status_dado == 'VALIDADO') else None

        var_perc = None
        if v_ant and v_ant > 0:
            var_perc = round(((v_atual - v_ant) / v_ant) * 100.0, 1)

        quadro_comparativo.append({
            'universidade': u,
            'valor': v_atual,
            'var_perc': var_perc,
            'ano_anterior': ano - 1
        })

    # 4. Perfil Comparado (Matriz com todos os indicadores chave das universidades selecionadas)
    indicadores_perfil = [
        {'id': 'ACA_ALUNOS_TOTAL', 'nome': 'Estudantes'},
        {'id': 'ACA_GRAD_TOTAL', 'nome': 'Graduação'},
        {'id': 'ACA_POS_TOTAL', 'nome': 'Pós-graduação'},
        {'id': 'ACA_CURSOS_GRAD', 'nome': 'Cursos de graduação'},
        {'id': 'PES_DOCENTES_TOTAL', 'nome': 'Docentes'},
        {'id': 'PES_TECNICOS_TOTAL', 'nome': 'Técnicos'},
        {'id': 'FIN_ORCAMENTO_ATUALIZADO', 'nome': 'Orçamento autorizado'},
        {'id': 'FIN_EMPENHADO', 'nome': 'Empenhado'},
        {'id': 'FIN_LIQUIDADO', 'nome': 'Liquidado'},
        {'id': 'DER_EXECUCAO_PERC', 'nome': '% execução'},
        {'id': 'DER_CUSTO_ALUNO', 'nome': 'Custo-aluno'},
        {'id': 'DER_ALUNOS_DOCENTE', 'nome': 'Estudantes/docente'}
    ]

    matriz_perfil = []
    for ind in indicadores_perfil:
        linha = {'nome': ind['nome'], 'valores': []}
        for u in universidades_selecionadas:
            r = reg_repo.buscar_por_chave(u.id, ind['id'], ano)
            val = r.valor_numerico if (r and r.status_dado == 'VALIDADO') else None
            linha['valores'].append(val)
        matriz_perfil.append(linha)

    return render_template('public/comparador.html',
                           ano=ano,
                           anos_disponiveis=[2022, 2023, 2024, 2025],
                           filtro_autonomia=filtro_autonomia,
                           indicador_selecionado=indicador_selecionado,
                           todos_indicadores=todos_indicadores,
                           universidades_disponiveis=universidades_disponiveis,
                           universidades_selecionadas=universidades_selecionadas,
                           selecionadas_siglas=selecionadas_siglas,
                           barras_comparativo=barras_comparativo,
                           max_barra=max_barra,
                           series_linhas=series_linhas,
                           quadro_comparativo=quadro_comparativo,
                           mediana_rede=mediana_rede,
                           matriz_perfil=matriz_perfil)