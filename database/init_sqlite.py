import sqlite3
import sys
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parent.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

from config.settings import Config

SCHEMA_SQLITE = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS universidades (
    id TEXT PRIMARY KEY,
    sigla TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    uf TEXT NOT NULL,
    regiao TEXT NOT NULL,
    municipio_sede TEXT,
    ano_filiacao INTEGER,
    status TEXT DEFAULT 'ATIVA',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS universidades_responsaveis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    universidade_id TEXT NOT NULL,
    nome TEXT NOT NULL,
    cargo TEXT NOT NULL,
    tipo TEXT NOT NULL,
    email TEXT,
    telefone TEXT,
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL,
    universidade_id TEXT,
    precisa_trocar_senha INTEGER DEFAULT 0,
    ativo INTEGER DEFAULT 1,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS campanhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    ano_referencia INTEGER NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    status TEXT DEFAULT 'ABERTA',
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS indicadores (
    id TEXT PRIMARY KEY,
    codigo TEXT NOT NULL UNIQUE,
    nome TEXT NOT NULL,
    dimensao TEXT NOT NULL,
    tipo_dado TEXT NOT NULL,
    tipo_agregacao TEXT NOT NULL,
    origem TEXT NOT NULL DEFAULT 'INFORMADO',
    unidade_medida TEXT,
    descricao TEXT,
    obrigatorio INTEGER DEFAULT 1,
    ativo INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS regras_calculo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicador_destino_id TEXT NOT NULL,
    formula TEXT NOT NULL,
    descricao TEXT,
    ordem_execucao INTEGER DEFAULT 1,
    FOREIGN KEY (indicador_destino_id) REFERENCES indicadores(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS registro_dados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    universidade_id TEXT NOT NULL,
    indicador_id TEXT NOT NULL,
    ano_referencia INTEGER NOT NULL,
    valor_numerico REAL,
    valor_texto TEXT,
    status_dado TEXT NOT NULL DEFAULT 'RASCUNHO',
    fonte_tipo TEXT,
    fonte_descricao TEXT,
    fonte_url TEXT,
    parecer_devolucao TEXT,
    atualizado_por INTEGER,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    atualizado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (universidade_id, indicador_id, ano_referencia),
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE CASCADE,
    FOREIGN KEY (indicador_id) REFERENCES indicadores(id) ON DELETE CASCADE,
    FOREIGN KEY (atualizado_por) REFERENCES usuarios(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS convenios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    universidade_id TEXT NOT NULL,
    ano_referencia INTEGER NOT NULL,
    orgao_concedente TEXT NOT NULL,
    numero_instrumento TEXT,
    objeto TEXT,
    valor_global REAL NOT NULL DEFAULT 0.0,
    valor_liberado REAL DEFAULT 0.0,
    data_inicio DATE,
    data_fim DATE,
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    universidade_id TEXT,
    tabela_afetada TEXT NOT NULL,
    acao TEXT NOT NULL,
    dados_antigos TEXT,
    dados_novos TEXT,
    ip_origem TEXT,
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL,
    FOREIGN KEY (universidade_id) REFERENCES universidades(id) ON DELETE SET NULL
);
"""

def inicializar():
    caminho_db = Path(Config.DB_PATH)
    caminho_db.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(str(caminho_db))
    try:
        cursor = conn.cursor()
        cursor.executescript(SCHEMA_SQLITE)
        conn.commit()
        print("Tabelas SQLite criadas/verificadas com sucesso em:", caminho_db)
    finally:
        conn.close()

if __name__ == '__main__':
    inicializar()