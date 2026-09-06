import ast
import operator

class AvaliadorFormula:
    """
    Avaliador aritmetico seguro baseado em AST (Abstract Syntax Tree).
    Impede qualquer execucao arbitraria de codigo (sem eval).
    Suporta as operacoes basicas: +, -, *, / com protecao contra divisao por zero.
    """
    OPERADORES = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    @classmethod
    def avaliar(cls, expressao, variaveis):
        """
        expressao: string no formato "IND01 / IND02"
        variaveis: dict {'IND01': 100.0, 'IND02': 50.0}
        Retorna float arredondado em 2 casas decimais ou None se inviavel/divisao por zero.
        """
        try:
            arvore = ast.parse(expressao.strip(), mode='eval')
            resultado = cls._avaliar_no(arvore.body, variaveis)
            if resultado is None:
                return None
            return round(float(resultado), 2)
        except Exception:
            return None

    @classmethod
    def _avaliar_no(cls, no, variaveis):
        if isinstance(no, ast.Constant):
            if isinstance(no.value, (int, float)):
                return float(no.value)
            return None

        elif isinstance(no, ast.Name):
            nome_var = no.id
            if nome_var not in variaveis or variaveis[nome_var] is None:
                return None
            return float(variaveis[nome_var])

        elif isinstance(no, ast.UnaryOp):
            operador = cls.OPERADORES.get(type(no.op))
            if not operador:
                return None
            operando = cls._avaliar_no(no.operand, variaveis)
            if operando is None:
                return None
            return operador(operando)

        elif isinstance(no, ast.BinOp):
            operador = cls.OPERADORES.get(type(no.op))
            if not operador:
                return None

            esquerdo = cls._avaliar_no(no.left, variaveis)
            direito = cls._avaliar_no(no.right, variaveis)

            if esquerdo is None or direito is None:
                return None

            # Protecao metodologica: denominador zero anula o indicador derivado
            if isinstance(no.op, ast.Div):
                if round(direito, 6) == 0.0:
                    return None

            return operador(esquerdo, direito)

        return None