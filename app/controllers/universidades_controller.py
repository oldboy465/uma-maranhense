from flask import Blueprint, render_template, abort
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.registro_repository import RegistroRepository
from app.repositories.convenio_repository import ConvenioRepository

universidades_bp = Blueprint('universidades', __name__)

@universidades_bp.route('/')
def lista():
    repo = UniversidadeRepository()
    universidades = repo.listar_todas(apenas_ativas=True)
    return render_template('public/universidades/lista.html', universidades=universidades)

@universidades_bp.route('/<sigla>')
def perfil(sigla):
    uni_repo = UniversidadeRepository()
    reg_repo = RegistroRepository()
    conv_repo = ConvenioRepository()

    uni = uni_repo.buscar_por_sigla(sigla)
    if not uni:
        abort(404)

    responsaveis = uni_repo.listar_responsaveis(uni.id)
    ano_recente = 2024

    registros = reg_repo.listar_por_universidade_e_ano(uni.id, ano_recente, apenas_validados=True)
    mapa_indicadores = {r['indicador_codigo']: r for r in registros}
    totais_convenios = conv_repo.totalizar_por_ano_e_universidade(uni.id, ano_recente)

    return render_template('public/universidades/perfil.html',
                           universidade=uni,
                           responsaveis=responsaveis,
                           ano=ano_recente,
                           indicadores=mapa_indicadores,
                           totais_convenios=totais_convenios)