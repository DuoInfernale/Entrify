import os
import random
import string

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')  
    
    # Set up the App SECRET_KEY
    SECRET_KEY = os.getenv('SECRET_KEY', ''.join(random.choices(string.ascii_letters + string.digits, k=32)))

    # Social AUTH context
    SOCIAL_AUTH_ENTRA = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLAlchemy engine options
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,  # Recycle connections after 300 seconds
        'pool_size': 10,      # Number of connections to keep open
        'max_overflow': 20    # Number of extra connections allowed
    }

    # Database Configuration
    DB_ENGINE = os.getenv('DB_ENGINE', '')
    DB_USERNAME = os.getenv('DB_USERNAME', '')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_HOST = os.getenv('DB_HOST', '')
    DB_PORT = os.getenv('DB_PORT', '')
    DB_NAME = os.getenv('DB_NAME', '')

    USE_SQLITE = False 

    # Set up the SQLALCHEMY_DATABASE_URI if database info is provided
    if DB_ENGINE and DB_NAME and DB_USERNAME:
        SQLALCHEMY_DATABASE_URI = f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        try:
            # Placeholder for potentially validating the DB connection string
            pass
        except Exception as e:
            print(f'> Error: DBMS Exception: {e}')
            print('> Fallback to SQLite.')
    else:
        SQLALCHEMY_DATABASE_URI = None

class ProductionConfig(Config):
    DEBUG = False

    # Security settings
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600  # Cookie duration in seconds

class DebugConfig(Config):
    DEBUG = True

# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}