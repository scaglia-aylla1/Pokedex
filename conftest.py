
import pytest
from app import create_app, db
from app.config import TestingConfig
import json

from app.models.user_model import UsuarioModel 
from werkzeug.security import generate_password_hash 

# Dados de um usuário padrão para autenticação nos testes
TEST_USER = {
    "nome": "Teste User",
    "login": "testuser",
    "email": "test@pokedex.com",
    "senha": "password123"
}

@pytest.fixture(scope='function')
def app():
    """Fixture para criar a instância da aplicação Flask com a config de teste."""
    app = create_app(config_object=TestingConfig)
    
    with app.app_context():
        # Cria as tabelas no BD em memória antes de rodar os testes
        db.create_all()
        yield app
        # Remove as tabelas após os testes
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Fixture para obter o cliente de teste do Flask."""
    return app.test_client()

@pytest.fixture(scope='function')
def auth_headers(client, app): # <--- Adicione 'app' como argumento
    """
    Fixture que garante a existência de um usuário e retorna o cabeçalho
    de autorização com o Token JWT.
    """
    with app.app_context():
        # 1. Busca ou cria o usuário diretamente no BD em memória
        user = UsuarioModel.query.filter_by(login=TEST_USER['login']).first()
        
        if not user:
            # Se o usuário não existe (primeira vez no teste)
            user = UsuarioModel(
                nome=TEST_USER['nome'],
                login=TEST_USER['login'],
                email=TEST_USER['email'],
                senha=generate_password_hash(TEST_USER['senha']) 
            )
            db.session.add(user)
            db.session.commit()
            
        # 2. Faz Login pela rota, garantindo que o ID do token é o ID do BD
        login_response = client.post('/api/v1/auth/login', 
                                     data=json.dumps(TEST_USER), 
                                     content_type='application/json')
        
        # 3. Extrair o token e montar o cabeçalho
        access_token = login_response.get_json()['access_token']
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # O ID do usuário logado (retornado do JWT) é uma STRING
        return headers