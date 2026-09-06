import sqlite3
import sys
from pathlib import Path

# Caminho do banco novo (onde o Flask roda)
RAIZ_NOVA = Path(__file__).resolve().parent.parent
DB_DESTINO = RAIZ_NOVA / 'data' / 'abruem.sqlite'

# Caminho do banco antigo do seu amigo
DB_ORIGEM = Path(r"C:\Users\Cliente\Projeto Uma Maranhense\OUTRAS INFORMAÇÕES\UMA MARANHENSE - VERSÃO ORIGINAL\data\abruem.sqlite")

def migrar_banco():
    if not DB_ORIGEM.exists():
        print(f"ERRO: Banco original não encontrado em: {DB_ORIGEM}")
        return

    print(f"Origem : {DB_ORIGEM}")
    print(f"Destino: {DB_DESTINO}")

    conn = sqlite3.connect(str(DB_DESTINO))
    cur = conn.cursor()

    try:
        # Conecta no banco do seu amigo como 'banco_origem'
        cur.execute(f"ATTACH DATABASE '{str(DB_ORIGEM)}' AS banco_origem;")

        # 1. Copia Universidades
        print("Copiando universidades...")
        cur.execute("""
            INSERT OR REPLACE INTO main.universidades (id, sigla, nome, tipo, uf, regiao, municipio_sede, status)
            SELECT 
                universidade_id,
                sigla,
                nome,
                COALESCE(esfera, 'ESTADUAL'),
                uf,
                regiao,
                pagina_planejamento,
                CASE WHEN ativa = 1 THEN 'ATIVA' ELSE 'INATIVA' END
            FROM banco_origem.universidade;
        """)

        # 2. Copia Indicadores
        print("Copiando dicionário de indicadores...")
        cur.execute("""
            INSERT OR REPLACE INTO main.indicadores (id, codigo, nome, dimensao, tipo_dado, tipo_agregacao, origem, unidade_medida, descricao, obrigatorio, ativo)
            SELECT 
                indicador_id,
                indicador_id,
                nome,
                dimensao,
                CASE 
                    WHEN unidade = 'BRL' THEN 'MONETARIO'
                    WHEN unidade = '%' THEN 'PERCENTUAL'
                    ELSE 'INTEIRO'
                END,
                tipo_agregacao,
                CASE WHEN derivado = 1 THEN 'CALCULADO' ELSE 'INFORMADO' END,
                unidade,
                definicao,
                coleta_institucional,
                ativo
            FROM banco_origem.indicador;
        """)

        # 3. Copia Registros de Dados (Tabela observacao -> registro_dados)
        print("Copiando registros de dados históricos...")
        cur.execute("""
            INSERT OR REPLACE INTO main.registro_dados (
                id, universidade_id, indicador_id, ano_referencia, valor_numerico, 
                status_dado, fonte_tipo, fonte_descricao, fonte_url, parecer_devolucao,
                criado_em, atualizado_em
            )
            SELECT 
                id,
                universidade_id,
                indicador_id,
                ano_referencia,
                valor,
                COALESCE(situacao, 'VALIDADO'),
                origem,
                documento,
                url_documento,
                parecer,
                atualizado_em,
                atualizado_em
            FROM banco_origem.observacao
            WHERE ativo = 1;
        """)

        # 4. Copia Regras de Cálculo
        print("Copiando regras de cálculo...")
        cur.execute("""
            INSERT OR REPLACE INTO main.regras_calculo (id, indicador_destino_id, formula, descricao, ordem_execucao)
            SELECT 
                id,
                indicador_id,
                expressao,
                justificativa,
                id
            FROM banco_origem.regra_calculo
            WHERE ativa = 1;
        """)

        conn.commit()

        # Auditoria rápida
        cur.execute("SELECT COUNT(*) FROM main.universidades")
        total_u = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM main.registro_dados")
        total_r = cur.fetchone()[0]

        print(f"\nSucesso absoluto! {total_u} universidades e {total_r} registros históricos migrados.")

    except Exception as e:
        conn.rollback()
        print(f"Erro durante a migração: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    migrar_banco()