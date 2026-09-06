-- Esquema de Banco MySQL (Maria Firmina - Rede ABRUEM)
-- Adaptado para MySQL 5.7+ / 8.0+ compatível com Hostgator / cPanel

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS auditoria;
DROP TABLE IF EXISTS relatorio_pendencias;
DROP TABLE IF EXISTS convenios;
DROP TABLE IF EXISTS registro_dados;
DROP TABLE IF EXISTS regras_calculo;
DROP TABLE IF EXISTS indicadores;
DROP TABLE IF EXISTS campanhas;
DROP TABLE IF EXISTS usuarios;
DROP TABLE IF EXISTS universidades_responsaveis;
DROP TABLE IF EXISTS universidades;

SET FOREIGN_KEY_CHECKS = 1;

-- 1. Universidades Filiadas
CREATE TABLE universidades (
    id VARCHAR(10) PRIMARY KEY,
    sigla VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    tipo ENUM('ESTADUAL', 'MUNICIPAL') NOT NULL,
    uf VARCHAR(2) NOT NULL,
    regiao ENUM('NORTE', 'NORDESTE', 'CENTRO-OESTE', 'SUDESTE', 'SUL') NOT NULL,
    municipio_sede VARCHAR(150),
    ano_filiacao INT,
    status ENUM('ATIVA', 'INATIVA') DEFAULT 'ATIVA',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Responsaveis Institucionais
CREATE TABLE universidades_responsaveis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    universidade_id VARCHAR(10) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    cargo VARCHAR(150) NOT NULL,
    tipo ENUM('REITOR', 'PRO_REITOR', 'REPRESENTANTE_CAMARA', 'RESPONSAVEL_TECNICO') NOT NULL,
    email VARCHAR(191),
    telefone VARCHAR(50),
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Usuarios do Sistema
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(191) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    perfil ENUM('ADMIN_CAMARA', 'GESTOR_INSTITUCIONAL') NOT NULL,
    universidade_id VARCHAR(10) NULL,
    precisa_trocar_senha TINYINT(1) DEFAULT 1,
    ativo TINYINT(1) DEFAULT 1,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Campanhas de Coleta
CREATE TABLE campanhas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    ano_referencia INT NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    status ENUM('ABERTA', 'ENCERRADA') DEFAULT 'ABERTA',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Dicionario de Indicadores
CREATE TABLE indicadores (
    id VARCHAR(50) PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nome VARCHAR(255) NOT NULL,
    dimensao ENUM('ACADEMICO', 'PESSOAS', 'FINANCAS', 'EFICIENCIA', 'CUSTO_ALUNO', 'CONVENIOS') NOT NULL,
    tipo_dado ENUM('INTEIRO', 'MONETARIO', 'PERCENTUAL', 'DECIMAL', 'TEXTO') NOT NULL,
    tipo_agregacao ENUM('ESTOQUE', 'FLUXO', 'RAZAO', 'NAO_ADITIVO') NOT NULL,
    origem ENUM('INFORMADO', 'CALCULADO') NOT NULL DEFAULT 'INFORMADO',
    unidade_medida VARCHAR(50),
    descricao TEXT,
    obrigatorio TINYINT(1) DEFAULT 1,
    ativo TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Regras de Calculo de Indicadores Derivados
CREATE TABLE regras_calculo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    indicador_destino_id VARCHAR(50) NOT NULL,
    formula VARCHAR(500) NOT NULL,
    descricao VARCHAR(255),
    ordem_execucao INT DEFAULT 1,
    FOREIGN KEY (indicador_destino_id) REFERENCES indicadores(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Registro de Dados (Central de Atualizacao / Fatos)
CREATE TABLE registro_dados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    universidade_id VARCHAR(10) NOT NULL,
    indicador_id VARCHAR(50) NOT NULL,
    ano_referencia INT NOT NULL,
    valor_numerico DECIMAL(18, 4) NULL,
    valor_texto TEXT NULL,
    status_dado ENUM('RASCUNHO', 'ENVIADO', 'VALIDADO', 'DEVOLVIDO') NOT NULL DEFAULT 'RASCUNHO',
    fonte_tipo VARCHAR(100),
    fonte_descricao VARCHAR(255),
    fonte_url VARCHAR(500),
    parecer_devolucao TEXT,
    atualizado_por INT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_uni_ind_ano (universidade_id, indicador_id, ano_referencia),
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE CASCADE,
    FOREIGN KEY (indicador_id) REFERENCES indicadores(id) ON DELETE CASCADE,
    FOREIGN KEY (atualizado_por) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Captacao e Convenios
CREATE TABLE convenios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    universidade_id VARCHAR(10) NOT NULL,
    ano_referencia INT NOT NULL,
    orgao_concedente VARCHAR(255) NOT NULL,
    numero_instrumento VARCHAR(100),
    objeto TEXT,
    valor_global DECIMAL(18, 2) NOT NULL,
    valor_liberado DECIMAL(18, 2) DEFAULT 0.00,
    data_inicio DATE,
    data_fim DATE,
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Auditoria de Acoes
CREATE TABLE auditoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL,
    universidade_id VARCHAR(10) NULL,
    tabela_afetada VARCHAR(100) NOT NULL,
    acao ENUM('INSERT', 'UPDATE', 'DELETE', 'LOGIN', 'VALIDACAO') NOT NULL,
    dados_antigos JSON NULL,
    dados_novos JSON NULL,
    ip_origem VARCHAR(45),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;