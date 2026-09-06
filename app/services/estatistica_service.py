import numpy as np

class EstatisticaService:
    @staticmethod
    def calcular_estatisticas_grupo(valores):
        """
        Calcula média, mediana, quartis e extremos metodológicos.
        Trata dizimas limitando rigorosamente a duas casas decimais.
        """
        validos = [float(v) for v in valores if v is not None]
        n = len(validos)
        
        if n == 0:
            return {
                'n': 0, 'media': None, 'mediana': None, 
                'q1': None, 'q3': None, 'min': None, 'max': None
            }

        validos.sort()

        media = round(float(np.mean(validos)), 2)
        mediana = round(float(np.median(validos)), 2) if n >= 3 else None
        
        q1 = round(float(np.percentile(validos, 25)), 2) if n >= 4 else None
        q3 = round(float(np.percentile(validos, 75)), 2) if n >= 4 else None
        
        v_min = round(validos[0], 2)
        v_max = round(validos[-1], 2)

        return {
            'n': n,
            'media': media,
            'mediana': mediana,
            'q1': q1,
            'q3': q3,
            'min': v_min,
            'max': v_max
        }

    @staticmethod
    def calcular_execucao_grupo(soma_liquidado, soma_orcamento):
        """
        Calcula percentual de execucao do grupo = (soma liquidado / soma orcamento) * 100.
        """
        if not soma_orcamento or round(soma_orcamento, 2) == 0.0:
            return 0.00
        return round((float(soma_liquidado) / float(soma_orcamento)) * 100.0, 2)