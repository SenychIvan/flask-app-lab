import os
from dotenv import load_dotenv

load_dotenv()

# абсолютний шлях до поточної папки
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    # абсолютний шлях до instance/data.sqlite
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(BASE_DIR), 'instance', 'data.sqlite')}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.path.dirname(BASE_DIR), 'instance', 'prod.sqlite')}"
