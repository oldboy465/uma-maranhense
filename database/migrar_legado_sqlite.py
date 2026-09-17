import sqlite3
import sys
from pathlib import Path

# Adiciona raiz ao path de importação
RAIZ = Path(__file__).resolve().parent.parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from config.settings import Config

def migrar():
    """
    Aplica a migração para adicionar a coluna 'autonomia_financeira'
    à tabela 'universidades' no SQLite caso ela ainda não exista.
    Garante integridade e evita duplicação de schema.
    """
    db_path = Path(Config.DB_PATH)
    if not db_path.exists():
        print(f"[ERRO] Banco de dados não localizado em: {db_path}")
        return

    print(f"Executando migração no banco: {db_path}")
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        # Verifica se a coluna já existe no pragma
        cursor.execute("PRAGMA table_info(universidades);")
        colunas = [coluna[1] for coluna in cursor.fetchall()]

        if 'autonomia_financeira' not in colunas:
            print("Adicionando coluna 'autonomia_financeira' (INTEGER DEFAULT 0)...")
            cursor.execute("""
                ALTER TABLE universidades 
                ADD COLUMN autonomia_financeira INTEGER DEFAULT 0;
            """)
            conn.commit()
            print("[SUCESSO] Coluna 'autonomia_financeira' criada com sucesso!")
        else:
            print("[INFO] Coluna 'autonomia_financeira' já existe no banco.")

    except Exception as e:
        conn.rollback()
        print(f"[ERRO] Falha ao aplicar migração: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    migrar()