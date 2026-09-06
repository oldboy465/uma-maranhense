-- Semente Estrutural da Rede ABRUEM — Plataforma Maria Firmina
-- Gerado a partir de scripts/semente/catalogo-estrutural.json

SET FOREIGN_KEY_CHECKS = 0;

-- 1. Universidades Filiadas (31 Instituições)
INSERT INTO universidades (id, sigla, nome, tipo, uf, regiao, status) VALUES
('U01', 'UENP', 'Universidade Estadual do Norte do Paraná', 'ESTADUAL', 'PR', 'SUL', 'ATIVA'),
('U02', 'UPE', 'Universidade de Pernambuco', 'ESTADUAL', 'PE', 'NORDESTE', 'ATIVA'),
('U03', 'UNEMAT', 'Universidade do Estado de Mato Grosso', 'ESTADUAL', 'MT', 'CENTRO-OESTE', 'ATIVA'),
('U04', 'UNESP', 'Universidade Estadual Paulista', 'ESTADUAL', 'SP', 'SUDESTE', 'ATIVA'),
('U05', 'Uni-FACEF', 'Centro Universitário de Franca', 'MUNICIPAL', 'SP', 'SUDESTE', 'ATIVA'),
('U06', 'UNICENTRO', 'Universidade Estadual do Centro-Oeste', 'ESTADUAL', 'PR', 'SUL', 'ATIVA'),
('U07', 'UNIFAE', 'Centro Universitário das Faculdades Associadas de Ensino', 'MUNICIPAL', 'SP', 'SUDESTE', 'ATIVA'),
('U08', 'UniCerrado', 'Centro Universitário de Goiás', 'MUNICIPAL', 'GO', 'CENTRO-OESTE', 'ATIVA'),
('U09', 'UEMG', 'Universidade do Estado de Minas Gerais', 'ESTADUAL', 'MG', 'SUDESTE', 'ATIVA'),
('U10', 'UNITINS', 'Universidade Estadual do Tocantins', 'ESTADUAL', 'TO', 'NORTE', 'ATIVA'),
('U11', 'UECE', 'Universidade Estadual do Ceará', 'ESTADUAL', 'CE', 'NORDESTE', 'ATIVA'),
('U12', 'UEPB', 'Universidade Estadual da Paraíba', 'ESTADUAL', 'PB', 'NORDESTE', 'ATIVA'),
('U13', 'UEPA', 'Universidade do Estado do Pará', 'ESTADUAL', 'PA', 'NORTE', 'ATIVA'),
('U14', 'UERJ', 'Universidade do Estado do Rio de Janeiro', 'ESTADUAL', 'RJ', 'SUDESTE', 'ATIVA'),
('U15', 'UEL', 'Universidade Estadual de Londrina', 'ESTADUAL', 'PR', 'SUL', 'ATIVA'),
('U16', 'UEM', 'Universidade Estadual de Maringá', 'ESTADUAL', 'PR', 'SUL', 'ATIVA'),
('U17', 'UNCISAL', 'Universidade Estadual de Ciências da Saúde de Alagoas', 'ESTADUAL', 'AL', 'NORDESTE', 'ATIVA'),
('U18', 'UESPI', 'Universidade Estadual do Piauí', 'ESTADUAL', 'PI', 'NORDESTE', 'ATIVA'),
('U19', 'UNIOESTE', 'Universidade Estadual do Oeste do Paraná', 'ESTADUAL', 'PR', 'SUL', 'ATIVA'),
('U20', 'UNIMONTES', 'Universidade Estadual de Montes Claros', 'ESTADUAL', 'MG', 'SUDESTE', 'ATIVA'),
('U21', 'UERN', 'Universidade do Estado do Rio Grande do Norte', 'ESTADUAL', 'RN', 'NORDESTE', 'ATIVA'),
('U22', 'UEFS', 'Universidade Estadual de Feira de Santana', 'ESTADUAL', 'BA', 'NORDESTE', 'ATIVA'),
('U23', 'UEG', 'Universidade Estadual de Goiás', 'ESTADUAL', 'GO', 'CENTRO-OESTE', 'ATIVA'),
('U24', 'UEMS', 'Universidade Estadual de Mato Grosso do Sul', 'ESTADUAL', 'MS', 'CENTRO-OESTE', 'ATIVA'),
('U25', 'UEA', 'Universidade do Estado do Amazonas', 'ESTADUAL', 'AM', 'NORTE', 'ATIVA'),
('U26', 'UNEB', 'Universidade do Estado da Bahia', 'ESTADUAL', 'BA', 'NORDESTE', 'ATIVA'),
('U27', 'UERGS', 'Universidade Estadual do Rio Grande do Sul', 'ESTADUAL', 'RS', 'SUL', 'ATIVA'),
('U28', 'UDESC', 'Universidade do Estado de Santa Catarina', 'ESTADUAL', 'SC', 'SUL', 'ATIVA'),
('U29', 'UNEAL', 'Universidade Estadual de Alagoas', 'ESTADUAL', 'AL', 'NORDESTE', 'ATIVA'),
('U30', 'UEMASUL', 'Universidade Estadual da Região Tocantina do Maranhão', 'ESTADUAL', 'MA', 'NORDESTE', 'ATIVA'),
('U31', 'UEMA', 'Universidade Estadual do Maranhão', 'ESTADUAL', 'MA', 'NORDESTE', 'ATIVA')
ON DUPLICATE KEY UPDATE nome = VALUES(nome), uf = VALUES(uf), regiao = VALUES(regiao);

-- 2. Dicionário de Indicadores (49 Indicadores)
INSERT INTO indicadores (id, codigo, nome, dimensao, tipo_dado, tipo_agregacao, origem, unidade_medida, descricao, obrigatorio, ativo) VALUES
('PER_CAMPI_TOTAL', 'PER_CAMPI_TOTAL', 'Número de campi', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Quantidade de campi da instituição conforme nomenclatura oficial', 1, 1),
('PER_UNIDADES_ACAD', 'PER_UNIDADES_ACAD', 'Unidades acadêmicas', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Quantidade de unidades acadêmicas (centros, departamentos, faculdades)', 0, 1),
('PER_MUNICIPIOS', 'PER_MUNICIPIOS', 'Municípios de atuação', 'ACADEMICO', 'INTEIRO', 'NAO_ADITIVO', 'INFORMADO', 'número', 'Quantidade de municípios em que a instituição possui atuação', 1, 1),
('ACA_ALUNOS_TOTAL', 'ACA_ALUNOS_TOTAL', 'Total de estudantes matriculados ativos', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'CALCULADO', 'número', 'Total institucional de estudantes matriculados ativos no ano de referência', 1, 1),
('ACA_GRAD_TOTAL', 'ACA_GRAD_TOTAL', 'Matrículas na graduação', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Total de matrículas em cursos de graduação', 1, 1),
('ACA_GRAD_PRESENCIAL', 'ACA_GRAD_PRESENCIAL', 'Matrículas na graduação presencial', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Matrículas em cursos de graduação presenciais', 0, 1),
('ACA_GRAD_EAD', 'ACA_GRAD_EAD', 'Matrículas na graduação EaD', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Matrículas em cursos de graduação a distância', 0, 1),
('ACA_POS_TOTAL', 'ACA_POS_TOTAL', 'Matrículas na pós-graduação', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Total de matrículas em cursos de pós-graduação', 1, 1),
('ACA_POS_STRICTO', 'ACA_POS_STRICTO', 'Matrículas na pós-graduação stricto sensu', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Matrículas em mestrado e doutorado', 0, 1),
('ACA_POS_LATO', 'ACA_POS_LATO', 'Matrículas na pós-graduação lato sensu', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Matrículas em especialização e residências', 0, 1),
('ACA_INGRESSANTES', 'ACA_INGRESSANTES', 'Ingressantes', 'ACADEMICO', 'INTEIRO', 'FLUXO', 'INFORMADO', 'número', 'Estudantes ingressantes no ano de referência', 0, 1),
('ACA_CONCLUINTES', 'ACA_CONCLUINTES', 'Concluintes', 'ACADEMICO', 'INTEIRO', 'FLUXO', 'INFORMADO', 'número', 'Estudantes concluintes no ano de referência', 0, 1),
('ACA_CONCLUINTES_POS', 'ACA_CONCLUINTES_POS', 'Concluintes da pós-graduação', 'ACADEMICO', 'INTEIRO', 'FLUXO', 'INFORMADO', 'número', 'Concluintes de cursos de pós-graduação no ano de referência', 0, 1),
('ACA_CURSOS_TOTAL', 'ACA_CURSOS_TOTAL', 'Total de cursos', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'CALCULADO', 'número', 'Total de cursos ofertados pela instituição', 1, 1),
('ACA_CURSOS_GRAD', 'ACA_CURSOS_GRAD', 'Cursos de graduação', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Quantidade de cursos de graduação', 1, 1),
('ACA_CURSOS_GRAD_PRESENCIAL', 'ACA_CURSOS_GRAD_PRESENCIAL', 'Cursos de graduação presenciais', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Quantidade de cursos de graduação presenciais', 0, 1),
('ACA_CURSOS_GRAD_EAD', 'ACA_CURSOS_GRAD_EAD', 'Cursos de graduação EaD', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Quantidade de cursos de graduação a distância', 0, 1),
('ACA_CURSOS_POS', 'ACA_CURSOS_POS', 'Cursos de pós-graduação', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Quantidade de cursos de pós-graduação', 1, 1),
('ACA_CURSOS_POS_STRICTO', 'ACA_CURSOS_POS_STRICTO', 'Cursos de pós-graduação stricto sensu', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Quantidade de programas de mestrado e doutorado', 0, 1),
('ACA_CURSOS_POS_LATO', 'ACA_CURSOS_POS_LATO', 'Cursos de pós-graduação lato sensu', 'ACADEMICO', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Quantidade de cursos de especialização', 0, 1),
('PES_DOCENTES_TOTAL', 'PES_DOCENTES_TOTAL', 'Docentes (total)', 'PESSOAS', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Total de docentes da instituição no ano de referência', 1, 1),
('PES_DOCENTES_EFETIVOS', 'PES_DOCENTES_EFETIVOS', 'Docentes efetivos', 'PESSOAS', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Docentes do quadro efetivo ou permanente', 0, 1),
('PES_DOCENTES_TEMPORARIOS', 'PES_DOCENTES_TEMPORARIOS', 'Docentes temporários ou substitutos', 'PESSOAS', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Docentes com vínculo temporário ou substituto', 0, 1),
('PES_TECNICOS_TOTAL', 'PES_TECNICOS_TOTAL', 'Técnicos administrativos (total)', 'PESSOAS', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Total de servidores técnico-administrativos', 1, 1),
('PES_TECNICOS_EFETIVOS', 'PES_TECNICOS_EFETIVOS', 'Técnicos administrativos efetivos', 'PESSOAS', 'INTEIRO', 'ESTOQUE', 'INFORMADO', 'número', 'Técnico-administrativos do quadro efetivo', 0, 1),
('PES_SERVIDORES_TOTAL', 'PES_SERVIDORES_TOTAL', 'Total de servidores', 'PESSOAS', 'INTEIRO', 'ESTOQUE', 'CALCULADO', 'número', 'Soma total de docentes e técnicos administrativos', 1, 1),
('FIN_ORCAMENTO_INICIAL', 'FIN_ORCAMENTO_INICIAL', 'Dotação inicial', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Dotação orçamentária inicial (LOA) do exercício', 0, 1),
('FIN_ORCAMENTO_ATUALIZADO', 'FIN_ORCAMENTO_ATUALIZADO', 'Orçamento autorizado ou atualizado', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Dotação atualizada do exercício após créditos adicionais', 1, 1),
('FIN_ORC_PESSOAL', 'FIN_ORC_PESSOAL', 'Dotação atualizada — pessoal e encargos', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Dotação atualizada do grupo pessoal e encargos sociais', 0, 1),
('FIN_ORC_CUSTEIO', 'FIN_ORC_CUSTEIO', 'Dotação atualizada — outras despesas correntes', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Dotação atualizada do grupo outras despesas correntes', 0, 1),
('FIN_ORC_INVESTIMENTO', 'FIN_ORC_INVESTIMENTO', 'Dotação atualizada — investimentos', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Dotação atualizada do grupo investimentos', 0, 1),
('FIN_EMPENHADO', 'FIN_EMPENHADO', 'Despesa empenhada', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Valor total empenhado no exercício', 1, 1),
('FIN_LIQUIDADO', 'FIN_LIQUIDADO', 'Despesa liquidada', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Valor total liquidado no exercício (execução efetiva)', 1, 1),
('FIN_PAGO', 'FIN_PAGO', 'Despesa paga', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Valor total pago no exercício', 1, 1),
('FIN_PESSOAL', 'FIN_PESSOAL', 'Despesa com pessoal e encargos', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Despesa do grupo pessoal e encargos sociais', 0, 1),
('FIN_CUSTEIO', 'FIN_CUSTEIO', 'Outras despesas correntes (custeio)', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Despesa do grupo outras despesas correntes', 0, 1),
('FIN_INVESTIMENTO', 'FIN_INVESTIMENTO', 'Investimentos', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Despesa do grupo ou elemento investimentos', 0, 1),
('FIN_CAPITAL', 'FIN_CAPITAL', 'Despesas de capital', 'FINANCAS', 'MONETARIO', 'FLUXO', 'INFORMADO', 'BRL', 'Despesa do grupo capital', 0, 1),
('CNV_QUANTIDADE', 'CNV_QUANTIDADE', 'Quantidade de convênios', 'CONVENIOS', 'INTEIRO', 'FLUXO', 'CALCULADO', 'número', 'Número total de convênios vigentes', 0, 1),
('CNV_VALOR_PACTUADO', 'CNV_VALOR_PACTUADO', 'Valor pactuado em convênios', 'CONVENIOS', 'MONETARIO', 'FLUXO', 'CALCULADO', 'BRL', 'Valor total pactuado nos convênios', 0, 1),
('CNV_VALOR_RECEBIDO', 'CNV_VALOR_RECEBIDO', 'Valor recebido de convênios', 'CONVENIOS', 'MONETARIO', 'FLUXO', 'CALCULADO', 'BRL', 'Valor efetivamente recebido de convênios', 0, 1),
('CNV_VALOR_EXECUTADO', 'CNV_VALOR_EXECUTADO', 'Valor executado de convênios', 'CONVENIOS', 'MONETARIO', 'FLUXO', 'CALCULADO', 'BRL', 'Valor executado dos convênios', 0, 1),
('DER_ALUNOS_DOCENTE', 'DER_ALUNOS_DOCENTE', 'Estudantes por docente', 'EFICIENCIA', 'DECIMAL', 'RAZAO', 'CALCULADO', 'razão', 'Razão entre estudantes ativos e docentes no mesmo ano', 1, 1),
('DER_ALUNOS_TECNICO', 'DER_ALUNOS_TECNICO', 'Estudantes por técnico', 'EFICIENCIA', 'DECIMAL', 'RAZAO', 'CALCULADO', 'razão', 'Razão entre estudantes ativos e técnicos administrativos', 1, 1),
('DER_ALUNOS_SERVIDOR', 'DER_ALUNOS_SERVIDOR', 'Estudantes por servidor', 'EFICIENCIA', 'DECIMAL', 'RAZAO', 'CALCULADO', 'razão', 'Razão entre estudantes ativos e total de servidores', 0, 1),
('DER_EXECUCAO_PERC', 'DER_EXECUCAO_PERC', 'Percentual de execução orçamentária', 'EFICIENCIA', 'PERCENTUAL', 'RAZAO', 'CALCULADO', '%', 'Proporção do orçamento autorizado liquidado', 1, 1),
('DER_CUSTO_ALUNO', 'DER_CUSTO_ALUNO', 'Custo-aluno', 'CUSTO_ALUNO', 'MONETARIO', 'RAZAO', 'CALCULADO', 'BRL', 'Despesa liquidada dividida por estudantes matriculados ativos', 1, 1)
ON DUPLICATE KEY UPDATE nome = VALUES(nome), dimensao = VALUES(dimensao);

-- 3. Regras de Cálculo Automatizadas (Fórmulas Oficiais)
INSERT INTO regras_calculo (id, indicador_destino_id, formula, descricao, ordem_execucao) VALUES
(1, 'ACA_ALUNOS_TOTAL', 'ACA_GRAD_TOTAL + ACA_POS_TOTAL', 'Soma de estudantes de graduação e pós-graduação', 1),
(2, 'ACA_CURSOS_TOTAL', 'ACA_CURSOS_GRAD + ACA_CURSOS_POS', 'Soma de cursos de graduação e pós-graduação', 1),
(3, 'PES_SERVIDORES_TOTAL', 'PES_DOCENTES_TOTAL + PES_TECNICOS_TOTAL', 'Soma de docentes e técnicos administrativos', 1),
(4, 'DER_ALUNOS_DOCENTE', 'ACA_ALUNOS_TOTAL / PES_DOCENTES_TOTAL', 'Relação estudantes por docente', 2),
(5, 'DER_ALUNOS_TECNICO', 'ACA_ALUNOS_TOTAL / PES_TECNICOS_TOTAL', 'Relação estudantes por técnico', 2),
(6, 'DER_ALUNOS_SERVIDOR', 'ACA_ALUNOS_TOTAL / PES_SERVIDORES_TOTAL', 'Relação estudantes por servidor', 2),
(7, 'DER_EXECUCAO_PERC', 'FIN_LIQUIDADO / FIN_ORCAMENTO_ATUALIZADO * 100', 'Percentual de execução orçamentária', 2),
(8, 'DER_CUSTO_ALUNO', 'FIN_LIQUIDADO / ACA_ALUNOS_TOTAL', 'Custo por estudante ativo', 2)
ON DUPLICATE KEY UPDATE formula = VALUES(formula), ordem_execucao = VALUES(ordem_execucao);

-- 4. Campanhas de Coleta
INSERT INTO campanhas (id, nome, ano_referencia, data_inicio, data_fim, status) VALUES
(1, 'Campanha 2026 — Núcleo Essencial', 2025, '2026-01-01', '2026-12-31', 'ABERTA')
ON DUPLICATE KEY UPDATE nome = VALUES(nome), status = VALUES(status);

-- 5. Responsáveis Institucionais
INSERT INTO universidades_responsaveis (id, universidade_id, nome, cargo, tipo, email) VALUES
(1, 'U28', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@udesc.br'),
(2, 'U11', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@uece.br'),
(3, 'U23', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@ueg.br'),
(4, 'U15', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@uel.br'),
(5, 'U31', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@uema.br'),
(6, 'U12', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@uepb.br'),
(7, 'U14', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@uerj.br'),
(8, 'U21', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@uern.br'),
(9, 'U26', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@uneb.br'),
(10, 'U03', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@unemat.br'),
(11, 'U20', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@unimontes.br'),
(12, 'U10', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@unitins.br'),
(13, 'U02', 'A designar', 'Pró-Reitoria de Planejamento', 'RESPONSAVEL_TECNICO', 'planejamento@upe.br')
ON DUPLICATE KEY UPDATE cargo = VALUES(cargo), email = VALUES(email);

SET FOREIGN_KEY_CHECKS = 1;