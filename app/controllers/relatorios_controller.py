from flask import Blueprint, render_template, request, Response, redirect, url_for
from app.services.auth_service import AuthService
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.services.exportacao_service import ExportacaoService

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/pendencias')
def pendencias():
    if not AuthService.esta_autenticado():
        return redirect(url_for('auth.login'))

    uni_repo = UniversidadeRepository()
    ind_repo = IndicadorRepository()
    reg_repo = RegistroRepository()

    ano = int(request.args.get('ano', 2024))
    formato = request.args.get('formato')

    universidades = uni_repo.listar_todas(apenas_ativas=True)
    indicadores_obrigatorios = [i for i in ind_repo.listar_todos(apenas_ativos=True) if i.obrigatorio and not i.is_calculado()]

    relatorio = []
    for uni in universidades:
        registros = reg_repo.listar_por_universidade_e_ano(uni.id, ano)
        preenchidos_ids = {r['indicador_id'] for r in registros if r.get('status_dado') == 'VALIDADO'}

        pendentes = [ind for ind in indicadores_obrigatorios if ind.id not in preenchidos_ids]
        responsaveis = uni_repo.listar_responsaveis(uni.id)

        relatorio.append({
            'universidade': uni,
            'total_pendencias': len(pendentes),
            'indicadores_pendentes': pendentes,
            'responsaveis': responsaveis
        })

    # Exportação em CSV
    if formato == 'csv':
        colunas = ['Universidade Sigla', 'Universidade Nome', 'UF', 'Ano', 'Indicador Pendente', 'Dimensão', 'Responsável']
        linhas = []
        for item in relatorio:
            resp_str = item['responsaveis'][0]['nome'] if item['responsaveis'] else 'Não informado'
            for ind in item['indicadores_pendentes']:
                linhas.append([
                    item['universidade'].sigla,
                    item['universidade'].nome,
                    item['universidade'].uf,
                    ano,
                    ind.nome,
                    ind.dimensao,
                    resp_str
                ])
        csv_bytes = ExportacaoService.gerar_csv(colunas, linhas)
        return Response(
            csv_bytes,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename=pendencias_abruem_{ano}.csv'}
        )

    # Visualização de Impressão / Salvar como PDF
    if formato == 'impressao':
        return render_template('admin/relatorio_pendencias_impressao.html', relatorio=relatorio, ano=ano)

    return render_template('admin/relatorio_pendencias.html', relatorio=relatorio, ano=ano)