
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    """Configurações de base para o Flask."""
    
    # Configuração do Banco de Dados
    # O caminho 'sqlite:///pokedex.db' cria o arquivo no diretório raiz do projeto
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Chave Secreta para o Flask e JWT 
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key_nao_segura')
    JWT_SECRET_KEY = SECRET_KEY  