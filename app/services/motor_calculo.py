from app.repositories.regra_repository import RegraRepository
from app.repositories.registro_repository import RegistroRepository
from app.models.registro_dado import RegistroDado
from app.services.avaliador_formula import AvaliadorFormula

class MotorCalculo:
    def __init__(self):
        self.regra_repo = RegraRepository()
        self.registro_repo = RegistroRepository()

    def calcular_indicadores_derivados(self, universidade_id, ano_referencia, usuario_id=None):
        """
        Executa as regras de calculo cadastradas em ordem de execucao,
        atualizando os valores dos indicadores derivados para a instituicao no ano.
        """
        regras = self.regra_repo.listar_ordenadas()
        if not regras:
            return 0

        # Carrega todos os registros atuais da universidade naquele ano
        registros = self.registro_repo.listar_por_universidade_e_ano(universidade_id, ano_referencia)
        mapa_valores = {}
        for r in registros:
            if r.get('valor_numerico') is not None:
                mapa_valores[r['indicador_id']] = float(r['valor_numerico'])
                mapa_valores[r['indicador_codigo']] = float(r['valor_numerico'])

        calculados = 0
        for regra in regras:
            resultado = AvaliadorFormula.avaliar(regra.formula, mapa_valores)
            
            if resultado is not None:
                resultado = round(resultado, 2)
                mapa_valores[regra.indicador_destino_id] = resultado
                
                # Persiste ou atualiza o indicador derivado no banco
                novo_registro = RegistroDado(
                    universidade_id=universidade_id,
                    indicador_id=regra.indicador_destino_id,
                    ano_referencia=ano_referencia,
                    valor_numerico=resultado,
                    status_dado='VALIDADO',
                    fonte_tipo='CALCULADO_SISTEMA',
                    fonte_descricao=f'Calculado automaticamente: {regra.formula}',
                    atualizado_por=usuario_id
                )
                self.registro_repo.salvar(novo_registro)
                calculados += 1

        return calculados