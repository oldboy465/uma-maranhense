from flask import Flask
from config.settings import Config

def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_class)

    # Filtros Globais Jinja para padrao monetario e numerico brasileiro
    @app.template_filter('moeda_br')
    def moeda_br_filter(valor):
        """
        Formata valores monetarios no padrao brasileiro (R$ 1.234.567,89).
        Trata dizimas arredondando rigorosamente para 2 casas decimais.
        """
        if valor is None or valor == '':
            return "R$ 0,00"
        try:
            val_float = round(float(valor), 2)
            formatado = f"{val_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            return f"R$ {formatado}"
        except (ValueError, TypeError):
            return "R$ 0,00"

    @app.template_filter('numero_br')
    def numero_br_filter(valor, casas=2):
        """
        Formata numeros e percentuais com separador de milhar (.) e decimal (,).
        """
        if valor is None or valor == '':
            return "0,00"
        try:
            val_float = round(float(valor), casas)
            if casas == 0:
                formatado = f"{int(val_float):,}".replace(',', '.')
            else:
                formatado = f"{val_float:,.{casas}f}".replace(',', 'X').replace('.', ',').replace('X', '.')
            return formatado
        except (ValueError, TypeError):
            return "0,00"

    # Registro de Blueprints (Controllers)
    from app.controllers.home_controller import home_bp
    from app.controllers.auth_controller import auth_bp
    from app.controllers.regioes_controller import regioes_bp
    from app.controllers.universidades_controller import universidades_bp
    from app.controllers.comparador_controller import comparador_bp
    from app.controllers.explorar_controller import explorar_bp
    from app.controllers.metodologia_controller import metodologia_bp
    from app.controllers.minha_universidade_controller import minha_universidade_bp
    from app.controllers.relatorios_controller import relatorios_bp
    from app.controllers.admin_controller import admin_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(regioes_bp, url_prefix='/regioes')
    app.register_blueprint(universidades_bp, url_prefix='/universidades')
    app.register_blueprint(comparador_bp, url_prefix='/comparador')
    app.register_blueprint(explorar_bp, url_prefix='/explorar')
    app.register_blueprint(metodologia_bp, url_prefix='/metodologia')
    app.register_blueprint(minha_universidade_bp, url_prefix='/minha-universidade')
    app.register_blueprint(relatorios_bp, url_prefix='/relatorios')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app