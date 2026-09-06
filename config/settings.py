import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'b8f3c7a109e4d582f6a9c1e30d7b2a548e6c9f1a2b3c4d5e6f7a8b9c0d1e2f3a')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Banco SQLite embarcado (data/abruem.sqlite)
    DB_PATH = os.getenv('DB_PATH', str(BASE_DIR / 'data' / 'abruem.sqlite'))
    
    # Sessoes seguras
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400