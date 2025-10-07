
from app import db

class TipoPokemonModel(db.Model):
    """
    Define o modelo de dados para a tabela 'TipoPokemon'.
    Usado para categorizar os tipos de Pokémon (Fogo, Água, etc.). [cite: 79]
    """
    __tablename__ = 'TipoPokemon'

    # IDTipoPokemon INT PrimaryKey 
    id_tipo_pokemon = db.Column('IDTipoPokemon', db.Integer, primary_key=True)
    
    # Descricao VARCHAR 
    descricao = db.Column('Descricao', db.String(50), nullable=False, unique=True)
    
    # Relacionamento 1...N com PokemonUsuarioModel 
    pokemon_usuario = db.relationship('PokemonUsuarioModel', backref='tipo_pokemon', lazy='dynamic')

    def __repr__(self):
        return f"<TipoPokemonModel ID: {self.id_tipo_pokemon}, Descricao: {self.descricao}>"