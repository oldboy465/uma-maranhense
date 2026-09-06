from flask import Blueprint, render_template
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.regra_repository import RegraRepository

metodologia_bp = Blueprint('metodologia', __name__)

@metodologia_bp.route('/')
def index():
    ind_repo = IndicadorRepository()
    regra_repo = RegraRepository()

    indicadores = ind_repo.listar_todos(apenas_ativos=True)
    regras = regra_repo.listar_ordenadas()
    mapa_regras = {r.indicador_destino_id: r for r in regras}

    # Agrupamento por dimensão analítica oficial
    dimensoes = {}
    for ind in indicadores:
        dim = ind.dimensao
        if dim not in dimensoes:
            dimensoes[dim] = []
        dimensoes[dim].append({
            'indicador': ind,
            'regra': mapa_regras.get(ind.id)
        })

    return render_template('public/metodologia.html', dimensoes=dimensoes)