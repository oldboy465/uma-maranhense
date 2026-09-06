import sys
import os

# Adiciona a raiz ao path para importar as configuracoes
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from werkzeug.security import generate_password_hash
from database.connection import get_db_connection

def criar_administrador():
    conn = get_db_connection()
    try:
        nome = "Administrador da Câmara"
        email = "admin"
        senha_pura = "admin"
        senha_hash = generate_password_hash(senha_pura)
        perfil = "ADMIN_CAMARA"
        precisa_trocar_senha = 0
        ativo = 1

        sql = """
            INSERT INTO usuarios (nome, email, senha_hash, perfil, universidade_id, precisa_trocar_senha, ativo)
            VALUES (%s, %s, %s, %s, NULL, %s, %s)
            ON DUPLICATE KEY UPDATE
                nome = VALUES(nome),
                senha_hash = VALUES(senha_hash),
                perfil = VALUES(perfil),
                precisa_trocar_senha = VALUES(precisa_trocar_senha),
                ativo = VALUES(ativo);
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, (nome, email, senha_hash, perfil, precisa_trocar_senha, ativo))
        conn.commit()
        print("Administrador inserido/atualizado com sucesso no banco MySQL.")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir administrador: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    criar_administrador()