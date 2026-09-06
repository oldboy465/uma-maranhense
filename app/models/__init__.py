"""
Pacote de Modelos de Dominio da aplicacao MVC Flask.
Representa as entidades essenciais de negocios do banco de dados.
"""
from app.models.usuario import Usuario
from app.models.universidade import Universidade
from app.models.indicador import Indicador
from app.models.registro_dado import RegistroDado
from app.models.regra_calculo import RegraCalculo
from app.models.campanha import Campanha
from app.models.convenio import Convenio
from app.models.auditoria import Auditoria

__all__ = [
    'Usuario',
    'Universidade',
    'Indicador',
    'RegistroDado',
    'RegraCalculo',
    'Campanha',
    'Convenio',
    'Auditoria'
]