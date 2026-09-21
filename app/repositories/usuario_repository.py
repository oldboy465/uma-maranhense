from app.repositories.base_repository import BaseRepository
from app.models.usuario import Usuario

class UsuarioRepository(BaseRepository):
    def buscar_por_id(self, usuario_id):
        sql = "SELECT * FROM usuarios WHERE id = %s LIMIT 1"
        res = self.executar_consulta_um(sql, (usuario_id,))
        return Usuario.from_dict(res) if res else None

    def buscar_por_email(self, email):
        sql = "SELECT * FROM usuarios WHERE LOWER(email) = LOWER(%s) LIMIT 1"
        res = self.executar_consulta_um(sql, (email,))
        return Usuario.from_dict(res) if res else None

    def buscar_por_universidade_id(self, universidade_id):
        sql = "SELECT * FROM usuarios WHERE universidade_id = %s LIMIT 1"
        res = self.executar_consulta_um(sql, (universidade_id,))
        return Usuario.from_dict(res) if res else None

    def buscar_por_identificador(self, termo):
        """
        Permite localizar usuario por:
        1. E-mail cadastrado (ex: admin, uema@abruem.org.br);
        2. Sigla da universidade correspondente (ex: udesc, uema, unicerrado);
        3. E-mail igual a sigla (ex: login direto digitando apenas 'uema').
        """
        termo_limpo = (termo or '').strip().lower()
        sql = """
            SELECT u.* 
            FROM usuarios u
            LEFT JOIN universidades uni ON u.universidade_id = uni.id
            WHERE LOWER(u.email) = %s 
               OR LOWER(COALESCE(uni.sigla, '')) = %s
            LIMIT 1
        """
        res = self.executar_consulta_um(sql, (termo_limpo, termo_limpo))
        return Usuario.from_dict(res) if res else None

    def listar_todos(self):
        sql = """
            SELECT u.*, un.sigla as universidade_sigla, un.nome as universidade_nome 
            FROM usuarios u
            LEFT JOIN universidades un ON u.universidade_id = un.id
            ORDER BY 
                CASE WHEN u.perfil = 'ADMIN_CAMARA' THEN 0 ELSE 1 END ASC,
                un.sigla ASC,
                u.nome ASC
        """
        return self.executar_consulta(sql)

    def criar(self, usuario):
        sql = """
            INSERT INTO usuarios (nome, email, senha_hash, perfil, universidade_id, precisa_trocar_senha, ativo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            usuario.nome, usuario.email, usuario.senha_hash,
            usuario.perfil, usuario.universidade_id,
            1 if usuario.precisa_trocar_senha else 0,
            1 if usuario.ativo else 0
        )
        return self.executar_comando(sql, params)

    def atualizar(self, usuario):
        sql = """
            UPDATE usuarios 
            SET nome = %s, email = %s, senha_hash = %s, perfil = %s, 
                universidade_id = %s, precisa_trocar_senha = %s, ativo = %s
            WHERE id = %s
        """
        params = (
            usuario.nome, usuario.email, usuario.senha_hash,
            usuario.perfil, usuario.universidade_id,
            1 if usuario.precisa_trocar_senha else 0,
            1 if usuario.ativo else 0,
            usuario.id
        )
        return self.executar_comando(sql, params)

    def alterar_senha(self, usuario_id, nova_senha_hash):
        """
        Atualiza a senha do usuario e desmarca a flag de troca forcada.
        """
        sql = """
            UPDATE usuarios 
            SET senha_hash = %s, precisa_trocar_senha = 0 
            WHERE id = %s
        """
        return self.executar_comando(sql, (nova_senha_hash, usuario_id))

    def resetar_senha_para_padrao(self, usuario_id, senha_padrao_hash):
        """
        Funcao restrita de administracao: redefine a senha para 123456
        e forca a redefinicao no primeiro login (precisa_trocar_senha = 1).
        """
        sql = """
            UPDATE usuarios 
            SET senha_hash = %s, precisa_trocar_senha = 1 
            WHERE id = %s
        """
        return self.executar_comando(sql, (senha_padrao_hash, usuario_id))