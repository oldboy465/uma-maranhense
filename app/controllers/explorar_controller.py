from flask import Blueprint, render_template, request, Response
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.services.exportacao_service import ExportacaoService

explorar_bp = Blueprint('explorar', __name__)

@explorar_bp.route('/')
def index():
    uni_repo = UniversidadeRepository()
    ind_repo = IndicadorRepository()
    reg_repo = RegistroRepository()

    universidades = uni_repo.listar_todas(apenas_ativas=True)
    indicadores = ind_repo.listar_todos(apenas_ativos=True)

    uni_id = request.args.get('universidade')
    ind_id = request.args.get('indicador')
    ano = request.args.get('ano')
    formato = request.args.get('formato')

    filtros_ativos = bool(uni_id or ind_id or ano)
    resultado = []

    if filtros_ativos:
        anos = [int(ano)] if ano else [2022, 2023, 2024]
        if ind_id:
            dados = reg_repo.listar_para_painel_publico(ind_id, anos)
            if uni_id:
                dados = [d for d in dados if d['universidade_id'] == uni_id]
            resultado = dados

    # Exportação direta em CSV formatado para padrão BR
    if formato == 'csv' and resultado:
        colunas = ['Universidade Sigla', 'Região', 'UF', 'Ano Referência', 'Valor']
        linhas = [
            [r['sigla'], r['regiao'], r['uf'], r['ano_referencia'], r['valor_numerico']]
            for r in resultado
        ]
        csv_bytes = ExportacaoService.gerar_csv(colunas, linhas)
        return Response(
            csv_bytes,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=abruem_dados_explorados.csv'}
        )

    return render_template('public/explorar.html',
                           universidades=universidades,
                           indicadores=indicadores,
                           uni_id=uni_id,
                           ind_id=ind_id,
                           ano=int(ano) if ano else None,
                           resultado=resultado)