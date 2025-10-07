
from app import db
from datetime import datetime

class UsuarioModel(db.Model):
    """
    Define o modelo de dados para a tabela 'Usuario' no banco de dados.
    Esta classe mapeia as colunas definidas no requisito do projeto.
    """
    # Define o nome da tabela no banco de dados
    __tablename__ = 'Usuario'

    id_usuario = db.Column('IDUsuario', db.Integer, primary_key=True)
    nome = db.Column('Nome', db.String(100), nullable=False)
    login = db.Column('Login', db.String(50), unique=True, nullable=False)
    email = db.Column('Email', db.String(100), unique=True, nullable=False)
    senha = db.Column('Senha', db.String(255), nullable=False)
    dt_inclusao = db.Column('DtInclusao', db.DateTime, default=datetime.utcnow, nullable=False)
    dt_alteracao = db.Column('DtAlteracao', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relacionamento: Um usuário pode ter muitos Pokémon (favoritos ou em grupo)
    # Lazy='dynamic' permite consultas mais eficientes
    pokemon_usuario = db.relationship('PokemonUsuarioModel', backref='usuario', lazy='dynamic')


    def __repr__(self):
        """Representação da instância do objeto para debugging."""
        return f"<UsuarioModel ID: {self.id_usuario}, Login: {self.login}>"