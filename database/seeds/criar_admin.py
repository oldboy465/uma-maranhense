import sys
from pathlib import Path

RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

from werkzeug.security import generate_password_hash
from database.connection import get_db_connection

def criar_administrador():
    conn = get_db_connection()
    try:
        nome = "Administrador da Câmara"
        email = "admin"
        senha_hash = generate_password_hash("admin")
        perfil = "ADMIN_CAMARA"

        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()

        if usuario:
            sql = """
                UPDATE usuarios 
                SET nome = ?, senha_hash = ?, perfil = ?, precisa_trocar_senha = 0, ativo = 1
                WHERE email = ?
            """
            cursor.execute(sql, (nome, senha_hash, perfil, email))
            print("Administrador existente atualizado com sucesso (admin / admin).")
        else:
            sql = """
                INSERT INTO usuarios (nome, email, senha_hash, perfil, universidade_id, precisa_trocar_senha, ativo)
                VALUES (?, ?, ?, ?, NULL, 0, 1)
            """
            cursor.execute(sql, (nome, email, senha_hash, perfil))
            print("Administrador criado com sucesso (admin / admin).")

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir administrador no SQLite: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    criar_administrador()