import sys
from pathlib import Path

# Adiciona a raiz do projeto no path de importacao
RAIZ_PROJETO = Path(__file__).resolve().parent.parent.parent
if str(RAIZ_PROJETO) not in sys.path:
    sys.path.insert(0, str(RAIZ_PROJETO))

from werkzeug.security import generate_password_hash
from database.connection import get_db_connection

# As 31 instituicoes oficiais da Rede ABRUEM
SIGLAS_UNIVERSIDADES = [
    'udesc', 'uea', 'uece', 'uefs', 'ueg', 'uel', 'uem', 'uema', 'uemasul',
    'uemg', 'uems', 'uenp', 'uepa', 'uepb', 'uergs', 'uerj', 'uern', 'uespi',
    'uncisal', 'uneal', 'uneb', 'unemat', 'unesp', 'unicentro', 'unifae',
    'unimontes', 'unioeste', 'unitins', 'upe', 'unifacef', 'unicerrado'
]

def popular_usuarios_universidades():
    """
    Cadastra ou atualiza os usuarios institucionais para as 31 universidades.
    - Login: sigla em letras minusculas (ex: uema, udesc);
    - Senha padrao inicial: 123456;
    - Redefinicao forcada: precisa_trocar_senha = 1;
    - Perfil: GESTOR_INSTITUCIONAL.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        senha_padrao_hash = generate_password_hash("123456")

        criados = 0
        atualizados = 0
        nao_encontradas = []

        print("Iniciando configuracao dos logins institucionais...")

        for sigla in SIGLAS_UNIVERSIDADES:
            sigla_upper = sigla.upper()

            # Localiza a instituicao pelo campo sigla
            cursor.execute(
                "SELECT id, nome FROM universidades WHERE UPPER(sigla) = ? LIMIT 1",
                (sigla_upper,)
            )
            uni = cursor.fetchone()

            # Tratamento de variacao de grafia para Uni-FACEF e UniCerrado
            if not uni:
                if sigla == 'unifacef':
                    cursor.execute("SELECT id, nome FROM universidades WHERE UPPER(sigla) LIKE '%FACEF%' LIMIT 1")
                    uni = cursor.fetchone()
                elif sigla == 'unicerrado':
                    cursor.execute("SELECT id, nome FROM universidades WHERE UPPER(sigla) LIKE '%CERRADO%' LIMIT 1")
                    uni = cursor.fetchone()

            if not uni:
                nao_encontradas.append(sigla_upper)
                continue

            uni_id = uni['id']
            nome_gestor = f"Gestão Institucional {uni['nome']}"
            login_email = sigla.lower()

            # Verifica se ja existe usuario para esta universidade ou com este login
            cursor.execute(
                "SELECT id FROM usuarios WHERE universidade_id = ? OR LOWER(email) = ? LIMIT 1",
                (uni_id, login_email)
            )
            usuario_existente = cursor.fetchone()

            if usuario_existente:
                # Atualiza mantendo a credencial padronizada e forca a redefinicao
                sql_update = """
                    UPDATE usuarios 
                    SET nome = ?, email = ?, senha_hash = ?, perfil = 'GESTOR_INSTITUCIONAL', 
                        universidade_id = ?, precisa_trocar_senha = 1, ativo = 1
                    WHERE id = ?
                """
                cursor.execute(sql_update, (nome_gestor, login_email, senha_padrao_hash, uni_id, usuario_existente['id']))
                atualizados += 1
            else:
                # Cria o novo usuario institucional
                sql_insert = """
                    INSERT INTO usuarios (nome, email, senha_hash, perfil, universidade_id, precisa_trocar_senha, ativo)
                    VALUES (?, ?, ?, 'GESTOR_INSTITUCIONAL', ?, 1, 1)
                """
                cursor.execute(sql_insert, (nome_gestor, login_email, senha_padrao_hash, uni_id))
                criados += 1

        conn.commit()

        print("\nResultado da execucao:")
        print(f" -> Usuarios criados: {criados}")
        print(f" -> Usuarios atualizados para o padrao: {atualizados}")

        if nao_encontradas:
            print(f" [!] Siglas nao encontradas na tabela 'universidades': {', '.join(nao_encontradas)}")
        else:
            print(" -> Todas as 31 universidades foram vinculadas com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"Erro ao processar criacao dos usuarios: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    popular_usuarios_universidades()