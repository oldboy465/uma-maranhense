from flask import Blueprint, render_template, request
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.services.estatistica_service import EstatisticaService

regioes_bp = Blueprint('regioes', __name__)

@regioes_bp.route('/')
def index():
    uni_repo = UniversidadeRepository()
    ind_repo = IndicadorRepository()
    reg_repo = RegistroRepository()

    ano_selecionado = int(request.args.get('ano', 2025))
    indicador_id = request.args.get('i', 'ACA_ALUNOS_TOTAL').strip()

    indicadores_disponiveis = [
        {'id': 'ACA_ALUNOS_TOTAL', 'nome': 'Total de estudantes matriculados ativos'},
        {'id': 'ACA_GRAD_TOTAL', 'nome': 'Matrículas na graduação'},
        {'id': 'ACA_POS_TOTAL', 'nome': 'Matrículas na pós-graduação'},
        {'id': 'PES_DOCENTES_TOTAL', 'nome': 'Docentes (total)'},
        {'id': 'PES_TECNICOS_TOTAL', 'nome': 'Técnicos administrativos (total)'},
        {'id': 'PES_SERVIDORES_TOTAL', 'nome': 'Total de servidores'},
        {'id': 'FIN_ORCAMENTO_ATUALIZADO', 'nome': 'Orçamento autorizado ou atualizado'},
        {'id': 'FIN_LIQUIDADO', 'nome': 'Despesa liquidada'},
        {'id': 'DER_ALUNOS_DOCENTE', 'nome': 'Estudantes por docente'},
        {'id': 'DER_CUSTO_ALUNO', 'nome': 'Custo-aluno'}
    ]

    indicador_atual = ind_repo.buscar_por_id(indicador_id) or ind_repo.buscar_por_id('ACA_ALUNOS_TOTAL')

    # Todas as universidades cadastradas no recorte (31)
    todas_universidades = uni_repo.listar_todas(apenas_ativas=True)
    total_filiadas_recorte = len(todas_universidades)

    # Registros do indicador e ano
    registros_ano = reg_repo.listar_para_painel_publico(indicador_atual.id, [ano_selecionado])
    mapa_valores = {r['universidade_id']: r['valor_numerico'] for r in registros_ano if r.get('valor_numerico') is not None}
    unis_com_dado = [u for u in todas_universidades if u.id in mapa_valores]

    # Total conhecido do recorte
    valores_numericos = list(mapa_valores.values())
    total_conhecido = sum(valores_numericos) if valores_numericos else 0.0

    # Composição por Região (Tabela e Gráfico)
    regioes_lista = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    composicao_regional = []

    for reg in regioes_lista:
        unis_reg = [u for u in todas_universidades if u.regiao.lower() == reg.lower()]
        unis_reg_com_dado = [u for u in unis_reg if u.id in mapa_valores]
        vals_reg = [mapa_valores[u.id] for u in unis_reg_com_dado]

        total_reg = sum(vals_reg) if vals_reg else None
        participacao = round((total_reg / total_conhecido * 100.0), 1) if (total_conhecido > 0 and total_reg is not None) else None

        stats_reg = EstatisticaService.calcular_estatisticas_grupo(vals_reg)

        composicao_regional.append({
            'regiao': reg,
            'total_filiadas': len(unis_reg),
            'filiadas_com_dado': len(unis_reg_com_dado),
            'total_conhecido': total_reg,
            'participacao': participacao,
            'mediana': stats_reg.get('mediana'),
            'ufs': sorted(list({u.uf for u in unis_reg}))
        })

    # Cobertura territorial geral da base
    cobertura_base = []
    for reg in regioes_lista:
        unis_reg = [u for u in todas_universidades if u.regiao.lower() == reg.lower()]
        total_reg_dados = sum(1 for u in unis_reg if len(reg_repo.listar_por_universidade_e_ano(u.id, ano_selecionado, apenas_validados=True)) > 0)
        
        cobertura_base.append({
            'regiao': reg,
            'ufs': ' '.join(sorted(list({u.uf for u in unis_reg}))),
            'filiadas': len(unis_reg),
            'com_dados': total_reg_dados,
            'status': f"{total_reg_dados} parcial" if total_reg_dados > 0 else "0 parcial"
        })

    # Série Histórica de Evolução (2022-2025) da Coorte
    anos_serie = [2022, 2023, 2024, 2025]
    serie_coorte = []
    for a in anos_serie:
        regs = reg_repo.listar_para_painel_publico(indicador_atual.id, [a])
        # Pega a instituição mais representativa ou a soma das instituições presentes
        val_ano = sum(r['valor_numerico'] for r in regs if r.get('valor_numerico') is not None)
        serie_coorte.append({'ano': a, 'valor': round(val_ano, 0)})

    return render_template('public/regioes.html',
                           ano_selecionado=ano_selecionado,
                           anos_disponiveis=[2022, 2023, 2024, 2025],
                           indicadores=indicadores_disponiveis,
                           indicador_atual=indicador_atual,
                           todas_universidades=todas_universidades,
                           total_filiadas_recorte=total_filiadas_recorte,
                           unis_com_dado=unis_com_dado,
                           total_conhecido=total_conhecido,
                           composicao_regional=composicao_regional,
                           cobertura_base=cobertura_base,
                           serie_coorte=serie_coorte)