
from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository
from app.models.user_model import UsuarioModel
from flask_jwt_extended import create_access_token
from typing import Dict, Any

class UserService:
    """
    Classe de Serviço (Business Logic) para operações relacionadas ao Usuário.
    Usa o Repository para a persistência de dados.
    """
    
    def __init__(self):
        """Inicializa o serviço com o Repositório de Usuários."""
        self.repository = UserRepository
        
    def register_user(self, data: Dict[str, str]) -> UsuarioModel:
        """
        Cria e registra um novo usuário no sistema.
        
        Args:
            data: Dicionário contendo nome, login, email e senha.
            
        Returns:
            O objeto UsuarioModel criado.
            
        Raises:
            ValueError: Se o login ou email já estiverem em uso.
        """
        # Validação de Unicidade
        if self.repository.find_by_login(data['login']):
            raise ValueError("O login fornecido já está em uso.")
        if self.repository.find_by_email(data['email']):
            raise ValueError("O email fornecido já está em uso.")
            
        # Hashing da Senha (Segurança)
        # O generate_password_hash aplica um algoritmo seguro de hash 
        hashed_password = generate_password_hash(data['senha'])
        
        # Criação do Objeto
        new_user = UsuarioModel(
            nome=data['nome'],
            login=data['login'],
            email=data['email'],
            senha=hashed_password # Salva o hash, e não a senha em texto puro
        )
        
        # Persistência (Usa a camada de Repositório)
        return self.repository.save(new_user)

    def login_user(self, login: str, senha: str) -> str:
        """
        Autentica um usuário e gera um Token JWT[cite: 86].
        
        Args:
            login: Login do usuário.
            senha: Senha em texto puro fornecida pelo usuário.
            
        Returns:
            Um access_token JWT.
            
        Raises:
            ValueError: Se as credenciais estiverem inválidas.
        """
        user = self.repository.find_by_login(login)
        
        # Verifica se o usuário existe e se a senha está correta
        if user and check_password_hash(user.senha, senha):
            # Converter o ID do usuário para string 
            user_identity = str(user.id_usuario)

            # Gera o Token JWT
            access_token = create_access_token(identity=user_identity)
            return access_token
        
        raise ValueError("Login ou senha inválidos.")