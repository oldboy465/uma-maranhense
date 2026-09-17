from flask import Blueprint, render_template, request
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.registro_repository import RegistroRepository
from app.services.estatistica_service import EstatisticaService

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    uni_repo = UniversidadeRepository()
    reg_repo = RegistroRepository()

    ano_selecionado = int(request.args.get('ano', 2023))
    total_universidades = len(uni_repo.listar_todas(apenas_ativas=True))

    # 1. Cards Principais da Rede no Ano[cite: 2]
    indicadores_chave = {
        'estudantes': 'ACA_ALUNOS_TOTAL',
        'cursos': 'ACA_CURSOS_GRAD',
        'docentes': 'PES_DOCENTES_TOTAL',
        'tecnicos': 'PES_TECNICOS_TOTAL',
        'orcamento_autorizado': 'FIN_ORCAMENTO_ATUALIZADO',
        'despesa_liquidada': 'FIN_LIQUIDADO',
        'campi': 'PER_CAMPI_TOTAL'
    }

    totais = {}
    for chave, id_ind in indicadores_chave.items():
        registros = reg_repo.listar_para_painel_publico(id_ind, [ano_selecionado])
        valores = [r['valor_numerico'] for r in registros if r.get('valor_numerico') is not None]
        totais[chave] = {
            'valor': round(sum(valores), 2) if valores else 0.0,
            'n': len(valores)
        }

    # 2. Presença Regional e Distribuição de Filiadas[cite: 2]
    regioes_ordem = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']
    distribuicao_regional = {}
    ufs_distintas = set()

    for reg in regioes_ordem:
        unis_regiao = uni_repo.listar_por_regiao(reg)
        for u in unis_regiao:
            ufs_distintas.add(u.uf)
        distribuicao_regional[reg] = {
            'total_filiadas': len(unis_regiao)
        }

    total_ufs = len(ufs_distintas)

    # 3. Gráfico de Estudantes por Região[cite: 2]
    reg_estudantes = reg_repo.listar_para_painel_publico('ACA_ALUNOS_TOTAL', [ano_selecionado])
    estudantes_por_regiao = {r: {'valor': 0, 'n': 0} for r in regioes_ordem}
    max_estudantes_regiao = 1

    for item in reg_estudantes:
        reg = item['regiao'].title() if item.get('regiao') else ''
        reg_formatada = next((r for r in regioes_ordem if r.lower() == reg.lower()), None)
        if reg_formatada and item.get('valor_numerico'):
            estudantes_por_regiao[reg_formatada]['valor'] += int(item['valor_numerico'])
            estudantes_por_regiao[reg_formatada]['n'] += 1

    for reg, dados in estudantes_por_regiao.items():
        if dados['valor'] > max_estudantes_regiao:
            max_estudantes_regiao = dados['valor']

    # 4. Quadro de Pessoal por Região (Docentes x Técnicos lado a lado)[cite: 2]
    reg_doc = reg_repo.listar_para_painel_publico('PES_DOCENTES_TOTAL', [ano_selecionado])
    reg_tec = reg_repo.listar_para_painel_publico('PES_TECNICOS_TOTAL', [ano_selecionado])

    pessoal_regional = {r: {'docentes': 0, 'tecnicos': 0, 'n': 0} for r in regioes_ordem}
    max_pessoal_regiao = 1

    for item in reg_doc:
        reg = next((r for r in regioes_ordem if r.lower() == (item.get('regiao') or '').lower()), None)
        if reg and item.get('valor_numerico'):
            pessoal_regional[reg]['docentes'] += int(item['valor_numerico'])
            pessoal_regional[reg]['n'] += 1

    for item in reg_tec:
        reg = next((r for r in regioes_ordem if r.lower() == (item.get('regiao') or '').lower()), None)
        if reg and item.get('valor_numerico'):
            pessoal_regional[reg]['tecnicos'] += int(item['valor_numerico'])

    for reg, dados in pessoal_regional.items():
        pico = max(dados['docentes'], dados['tecnicos'])
        if pico > max_pessoal_regiao:
            max_pessoal_regiao = pico

    # 5. Orçamento e Execução por Região[cite: 2]
    reg_aut = reg_repo.listar_para_painel_publico('FIN_ORCAMENTO_ATUALIZADO', [ano_selecionado])
    reg_liq = reg_repo.listar_para_painel_publico('FIN_LIQUIDADO', [ano_selecionado])

    orcamento_regional = {r: {'autorizado': 0.0, 'liquidado': 0.0, 'n': 0} for r in regioes_ordem}
    max_orcamento_regiao = 1.0

    for item in reg_aut:
        reg = next((r for r in regioes_ordem if r.lower() == (item.get('regiao') or '').lower()), None)
        if reg and item.get('valor_numerico'):
            orcamento_regional[reg]['autorizado'] += float(item['valor_numerico'])
            orcamento_regional[reg]['n'] += 1

    for item in reg_liq:
        reg = next((r for r in regioes_ordem if r.lower() == (item.get('regiao') or '').lower()), None)
        if reg and item.get('valor_numerico'):
            orcamento_regional[reg]['liquidado'] += float(item['valor_numerico'])

    for reg, dados in orcamento_regional.items():
        pico_orc = max(dados['autorizado'], dados['liquidado'])
        if pico_orc > max_orcamento_regiao:
            max_orcamento_regiao = pico_orc

    # Execução global da rede[cite: 2]
    soma_liq_rede = sum(d['liquidado'] for d in orcamento_regional.values() if d['autorizado'] > 0)
    soma_aut_rede = sum(d['autorizado'] for d in orcamento_regional.values() if d['autorizado'] > 0)
    execucao_rede_perc = round((soma_liq_rede / soma_aut_rede) * 100.0, 1) if soma_aut_rede > 0 else 0.0

    # 6. Série Histórica de Evolução da Matrícula (2022-2025)[cite: 2]
    anos_serie = [2022, 2023, 2024, 2025]
    todos_matriculas = {a: reg_repo.listar_para_painel_publico('ACA_ALUNOS_TOTAL', [a]) for a in anos_serie}

    # Identifica coorte de universidades presentes em todos os exercícios da série[cite: 8]
    sets_unis = [{r['universidade_id'] for r in lista} for lista in todos_matriculas.values()]
    coorte_unis = set.intersection(*sets_unis) if sets_unis and all(len(s) > 0 for s in sets_unis) else set()

    pontos_evolucao = []
    for a in anos_serie:
        regs = todos_matriculas[a]
        if coorte_unis:
            val = sum(r['valor_numerico'] for r in regs if r['universidade_id'] in coorte_unis and r.get('valor_numerico'))
        else:
            val = sum(r['valor_numerico'] for r in regs if r.get('valor_numerico'))
        pontos_evolucao.append({'ano': a, 'valor': round(val, 0)})

    # Variação global da série[cite: 2]
    var_perc = 0.0
    if len(pontos_evolucao) >= 2 and pontos_evolucao[0]['valor'] > 0:
        v_ini = pontos_evolucao[0]['valor']
        v_fim = pontos_evolucao[-1]['valor']
        var_perc = round(((v_fim - v_ini) / v_ini) * 100.0, 1)

    return render_template('public/index.html',
                           ano_selecionado=ano_selecionado,
                           anos_disponiveis=[2022, 2023, 2024, 2025],
                           total_universidades=total_universidades,
                           total_ufs=total_ufs,
                           totais=totais,
                           distribuicao_regional=distribuicao_regional,
                           estudantes_por_regiao=estudantes_por_regiao,
                           max_estudantes_regiao=max_estudantes_regiao,
                           pessoal_regional=pessoal_regional,
                           max_pessoal_regiao=max_pessoal_regiao,
                           orcamento_regional=orcamento_regional,
                           max_orcamento_regiao=max_orcamento_regiao,
                           execucao_rede_perc=execucao_rede_perc,
                           pontos_evolucao=pontos_evolucao,
                           var_perc=var_perc,
                           coorte_filiadas=list(coorte_unis))