from flask import Blueprint, render_template, request
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.registro_repository import RegistroRepository
from app.services.estatistica_service import EstatisticaService

regioes_bp = Blueprint('regioes', __name__)

@regioes_bp.route('/')
def index():
    uni_repo = UniversidadeRepository()
    reg_repo = RegistroRepository()

    regiao_selecionada = request.args.get('regiao', 'NORDESTE').upper()
    ano = int(request.args.get('ano', 2024))

    regioes_validas = ['NORTE', 'NORDESTE', 'CENTRO-OESTE', 'SUDESTE', 'SUL']
    if regiao_selecionada not in regioes_validas:
        regiao_selecionada = 'NORDESTE'

    universidades_regiao = uni_repo.listar_por_regiao(regiao_selecionada)
    
    # Orçamento executado e Matrículas por universidade da região
    dados_tabela = []
    valores_orcamento = []
    valores_matriculas = []

    for uni in universidades_regiao:
        dado_orc = reg_repo.buscar_por_chave(uni.id, 'IND_ORC_EXECUTADO', ano)
        dado_mat = reg_repo.buscar_por_chave(uni.id, 'IND_MATRICULAS_GRAD', ano)

        v_orc = round(dado_orc.valor_numerico, 2) if (dado_orc and dado_orc.valor_numerico is not None) else None
        v_mat = round(dado_mat.valor_numerico, 0) if (dado_mat and dado_mat.valor_numerico is not None) else None

        if v_orc is not None:
            valores_orcamento.append(v_orc)
        if v_mat is not None:
            valores_matriculas.append(v_mat)

        dados_tabela.append({
            'universidade': uni,
            'orcamento': v_orc,
            'matriculas': int(v_mat) if v_mat is not None else None
        })

    stats_orc = EstatisticaService.calcular_estatisticas_grupo(valores_orcamento)
    stats_mat = EstatisticaService.calcular_estatisticas_grupo(valores_matriculas)

    return render_template('public/regioes.html',
                           regioes=regioes_validas,
                           regiao_selecionada=regiao_selecionada,
                           ano=ano,
                           dados_tabela=dados_tabela,
                           stats_orc=stats_orc,
                           stats_mat=stats_mat)