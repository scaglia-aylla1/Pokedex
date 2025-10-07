
from app import db

class PokemonUsuarioModel(db.Model):
    """
    Define o modelo de dados para a tabela 'PokemonUsuario'.
    Rastreia os Pokémon que um usuário marcou como favorito ou membro do Grupo de Batalha. [cite: 75]
    """
    __tablename__ = 'PokemonUsuario'

    # IDPokemonUsuario INT PrimaryKey 
    id_pokemon_usuario = db.Column('IDPokemonUsuario', db.Integer, primary_key=True)
    
    # Chave estrangeira que referencia a tabela 'Usuario'
    id_usuario = db.Column('IDUsuario', db.Integer, db.ForeignKey('Usuario.IDUsuario'), nullable=False)
    
    # Chave estrangeira que referencia o tipo de Pokémon 
    id_tipo_pokemon = db.Column('IDTipoPokemon', db.Integer, db.ForeignKey('TipoPokemon.IDTipoPokemon'), nullable=False)
    
    # Codigo VARCHAR (o ID ou nome do Pokémon na PokeAPI) 
    codigo = db.Column('Codigo', db.String(50), nullable=False)
    
    # ImagemUrI VARCHAR 
    imagem_uri = db.Column('ImagemUrI', db.String(255), nullable=False)
    
    # Nome VARCHAR 
    nome = db.Column('Nome', db.String(100), nullable=False)
    
    
    # Indica se o Pokémon faz parte da Equipe de Batalha (máx. 6) 
    grupo_batalha = db.Column('GrupoBatalha', db.Boolean, default=False, nullable=False)
    
    # Indica se o Pokémon está na lista de Favoritos 
    favorito = db.Column('Favorito', db.Boolean, default=False, nullable=False)

    # Restrição de Unicidade: Um usuário só pode ter um registro para um Pokémon específico
    __table_args__ = (
        db.UniqueConstraint('IDUsuario', 'Codigo', name='_usuario_pokemon_uc'),
    )

    def __repr__(self):
        return f"<PokemonUsuarioModel ID: {self.id_pokemon_usuario}, Usuário: {self.id_usuario}, Pokémon: {self.nome}>"