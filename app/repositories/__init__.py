"""
Pacote de Repositorios para persistencia e consultas diretas no MySQL.
"""
from app.repositories.base_repository import BaseRepository
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.universidade_repository import UniversidadeRepository
from app.repositories.indicador_repository import IndicadorRepository
from app.repositories.registro_repository import RegistroRepository
from app.repositories.regra_repository import RegraRepository
from app.repositories.convenio_repository import ConvenioRepository
from app.repositories.auditoria_repository import AuditoriaRepository

__all__ = [
    'BaseRepository',
    'UsuarioRepository',
    'UniversidadeRepository',
    'IndicadorRepository',
    'RegistroRepository',
    'RegraRepository',
    'ConvenioRepository',
    'AuditoriaRepository'
]