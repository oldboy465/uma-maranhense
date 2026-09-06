from flask import Blueprint, render_template
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.services.estatistica_service import EstatisticaService

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    uni_repo = UniversidadeRepository()
    ind_repo = IndicadorRepository()
    reg_repo = RegistroRepository()

    total_universidades = len(uni_repo.listar_todas(apenas_ativas=True))
    
    # Ano de referência mais recente disponível na base consolidada
    ano_destaque = 2024

    # Busca valores validados dos 4 indicadores-chave do painel 'Força da Rede'
    indicadores_chave = {
        'estudantes': 'IND_MATRICULAS_GRAD',
        'orcamento': 'IND_ORC_EXECUTADO',
        'docentes': 'IND_DOCENTES_TOTAL',
        'cursos': 'IND_CURSOS_GRAD'
    }

    totais = {}
    for chave, id_ind in indicadores_chave.items():
        registros = reg_repo.listar_para_painel_publico(id_ind, [ano_destaque])
        valores = [r['valor_numerico'] for r in registros if r.get('valor_numerico') is not None]
        soma = round(sum(valores), 2) if valores else 0.00
        totais[chave] = {
            'valor': soma,
            'n': len(valores)
        }

    return render_template('public/index.html',
                           total_universidades=total_universidades,
                           ano_destaque=ano_destaque,
                           totais=totais)