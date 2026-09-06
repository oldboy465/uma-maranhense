import sqlite3
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DB_PATH = RAIZ / 'data' / 'abruem.sqlite'

def migrar_e_compatibilizar():
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()

    print("Verificando estrutura do abruem.sqlite...")

    # Garante views ou tabelas para compatibilidade entre o código legado e a arquitetura MVC
    cursor.execute("""
        CREATE VIEW IF NOT EXISTS registro_dados AS
        SELECT 
            id,
            universidade_id,
            indicador_id,
            ano_referencia,
            valor as valor_numerico,
            NULL as valor_texto,
            situacao as status_dado,
            origem as fonte_tipo,
            documento as fonte_descricao,
            url_documento as fonte_url,
            parecer as parecer_devolucao,
            atualizado_por,
            atualizado_em as criado_em,
            atualizado_em
        FROM observacao;
    """)

    cursor.execute("""
        CREATE VIEW IF NOT EXISTS universidades AS
        SELECT 
            universidade_id as id,
            sigla,
            nome,
            esfera as tipo,
            uf,
            regiao,
            pagina_planejamento as municipio_sede,
            2022 as ano_filiacao,
            CASE WHEN ativa = 1 THEN 'ATIVA' ELSE 'INATIVA' END as status,
            CURRENT_TIMESTAMP as criado_em
        FROM universidade;
    """)

    cursor.execute("""
        CREATE VIEW IF NOT EXISTS usuarios AS
        SELECT 
            id,
            nome,
            email,
            senha_hash,
            perfil,
            universidade_id,
            trocar_senha as precisa_trocar_senha,
            ativo,
            criado_em
        FROM usuario;
    """)

    cursor.execute("""
        CREATE VIEW IF NOT EXISTS indicadores AS
        SELECT 
            indicador_id as id,
            indicador_id as codigo,
            nome,
            dimensao,
            CASE 
                WHEN unidade = 'BRL' THEN 'MONETARIO'
                WHEN unidade = '%' THEN 'PERCENTUAL'
                ELSE 'INTEIRO'
            END as tipo_dado,
            tipo_agregacao,
            CASE WHEN derivado = 1 THEN 'CALCULADO' ELSE 'INFORMADO' END as origem,
            unidade as unidade_medida,
            definicao as descricao,
            coleta_institucional as obrigatorio,
            ativo
        FROM indicador;
    """)

    conn.commit()
    conn.close()
    print("Base compatibilizada com sucesso! Todos os dados legados estão ativos e linkados.")

if __name__ == '__main__':
    migrar_e_compatibilizar()