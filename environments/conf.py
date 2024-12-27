from dotenv import load_dotenv
from os import getenv


load_dotenv()

class Environments:
    CORS_ALLOWED_ORIGINS: list = getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    ALLOWED_HOSTS: list = getenv('ALLOWED_HOSTS', '').split(',')
    DEBUG: bool = getenv('DEBUG', 'False').lower() == 'true'
    DB_POSTGRES: str = getenv('DB_POSTGRES')
    SECRET_KEY: str = getenv('SECRET_KEY')

environments = Environments
