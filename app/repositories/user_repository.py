
from app import db
from app.models.user_model import UsuarioModel

class UserRepository:
    """
    Classe responsável pela interação direta com a tabela 'Usuario' no banco de dados.
    Implementa o padrão Repository para abstrair a camada de persistência (SQLAlchemy).
    """

    @staticmethod
    def save(user: UsuarioModel) -> UsuarioModel:
        """Salva um novo objeto UsuarioModel no banco de dados."""
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def find_by_login(login: str) -> UsuarioModel or None: # type: ignore
        """Busca um usuário pelo campo de login (VARCHAR)[cite: 64]."""
        return UsuarioModel.query.filter_by(login=login).first()

    @staticmethod
    def find_by_email(email: str) -> UsuarioModel or None: # type: ignore
        """Busca um usuário pelo campo de email (VARCHAR)[cite: 65]."""
        return UsuarioModel.query.filter_by(email=email).first()

   