from flask import Blueprint, render_template
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.registro_repository import RegistroRepository

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    uni_repo = UniversidadeRepository()
    reg_repo = RegistroRepository()

    total_universidades = len(uni_repo.listar_todas(apenas_ativas=True))
    ano_destaque = 2024

    # Codigos reais existentes no banco legado (catalogo-estrutural.json)
    indicadores_chave = {
        'estudantes': 'ACA_GRAD_TOTAL',
        'orcamento': 'FIN_LIQUIDADO',
        'docentes': 'PES_DOCENTES_TOTAL',
        'cursos': 'ACA_CURSOS_GRAD'
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