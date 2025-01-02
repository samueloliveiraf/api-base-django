from dotenv import load_dotenv
from os import getenv


load_dotenv()

class Environments:
    CORS_ALLOWED_ORIGINS: list = getenv('CORS_ALLOWED_ORIGINS', '').split(',')
    ALLOWED_HOSTS: list = getenv('ALLOWED_HOSTS', '').split(',')
    DEBUG: bool = getenv('DEBUG', 'False').lower() == 'true'
    DB_POSTGRES: str = getenv('DB_POSTGRES')
    SECRET_KEY: str = getenv('SECRET_KEY')
    EMAIL_HOST_USER: str = getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD: str = getenv('EMAIL_HOST_PASSWORD')
    EMAIL_HOST: str = getenv('EMAIL_HOST')
    EMAIL_PORT: int = getenv('EMAIL_PORT')

environments = Environments
