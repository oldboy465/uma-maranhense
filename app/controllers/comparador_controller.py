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

    universidades = uni_repo.listar_todas(apenas_ativas=True)
    indicadores = ind_repo.listar_todos(apenas_ativos=True)

    uni1_id = request.args.get('uni1')
    uni2_id = request.args.get('uni2')
    ano = int(request.args.get('ano', 2024))

    u1 = uni_repo.buscar_por_id(uni1_id) if uni1_id else None
    u2 = uni_repo.buscar_por_id(uni2_id) if uni2_id else None

    comparativo = []
    if u1 and u2:
        for ind in indicadores:
            r1 = reg_repo.buscar_por_chave(u1.id, ind.id, ano)
            r2 = reg_repo.buscar_por_chave(u2.id, ind.id, ano)

            v1 = round(r1.valor_numerico, 2) if (r1 and r1.valor_numerico is not None) else None
            v2 = round(r2.valor_numerico, 2) if (r2 and r2.valor_numerico is not None) else None

            # Cálculo de referência metodológica de rede (todos do ano)
            todos_ano = reg_repo.listar_para_painel_publico(ind.id, [ano])
            valores_rede = [r['valor_numerico'] for r in todos_ano if r.get('valor_numerico') is not None]
            stats = EstatisticaService.calcular_estatisticas_grupo(valores_rede)

            comparativo.append({
                'indicador': ind,
                'v1': v1,
                'v2': v2,
                'mediana_rede': stats.get('mediana'),
                'media_rede': stats.get('media')
            })

    return render_template('public/comparador.html',
                           universidades=universidades,
                           u1=u1,
                           u2=u2,
                           ano=ano,
                           comparativo=comparativo)