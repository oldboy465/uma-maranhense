import sys
import os

# Define a pasta raiz do projeto no path do interpretador
CAMINHO_RAIZ = os.path.dirname(os.path.abspath(__file__))
if CAMINHO_RAIZ not in sys.path:
    sys.path.insert(0, CAMINHO_RAIZ)

from app import create_app

# Objeto WSGI executado pelo cPanel (Passenger/HostGator) ou PythonAnywhere
application = create_app()