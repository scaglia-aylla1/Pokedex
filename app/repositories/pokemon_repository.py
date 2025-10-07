
from app import db
from app.models.pokemon_usuario_model import PokemonUsuarioModel
from app.models.tipo_pokemon_model import TipoPokemonModel
from typing import List

class PokemonRepository:
    """
    Repositório para gerenciar a persistência de dados de Pokémon associados
    ao usuário (Favoritos e Grupo de Batalha).
    Responsabilidade: Comunicação direta com o banco de dados.
    """

    @staticmethod
    def get_pokemon_by_user_and_code(user_id: int, pokemon_code: str) -> PokemonUsuarioModel or None: # type: ignore
        """Busca um registro de Pokémon de um usuário específico pelo seu código/ID."""
        return PokemonUsuarioModel.query.filter_by(
            id_usuario=user_id,
            codigo=pokemon_code
        ).first()

    @staticmethod
    def get_user_battle_team_count(user_id: int) -> int:
        """Conta quantos Pokémon um usuário tem no Grupo de Batalha (GrupoBatalha = True)."""
        return PokemonUsuarioModel.query.filter_by(
            id_usuario=user_id,
            grupo_batalha=True
        ).count()

    @staticmethod
    def save(pokemon_usuario: PokemonUsuarioModel) -> PokemonUsuarioModel:
        """Salva ou atualiza um registro de PokemonUsuario no banco de dados."""
        db.session.add(pokemon_usuario)
        db.session.commit()
        return pokemon_usuario

    @staticmethod
    def delete(pokemon_usuario: PokemonUsuarioModel):
        """Remove um registro de PokemonUsuario do banco de dados."""
        db.session.delete(pokemon_usuario)
        db.session.commit()

    # Funções para Tipos de Pokémon 

    @staticmethod
    def find_or_create_type(description: str) -> TipoPokemonModel:
        """Busca um tipo de Pokémon pela descrição ou o cria se não existir."""
        tipo = TipoPokemonModel.query.filter_by(descricao=description).first()
        if not tipo:
            # Cria um novo tipo se não for encontrado
            tipo = TipoPokemonModel(descricao=description)
            db.session.add(tipo)
            db.session.commit()
        return tipo

    @staticmethod
    def get_user_favorite_pokemons(user_id: int) -> List[PokemonUsuarioModel]:
        """Busca todos os Pokémon que o usuário marcou como favorito."""
        return PokemonUsuarioModel.query.filter_by(
            id_usuario=user_id,
            favorito=True
        ).all()

    @staticmethod
    def get_user_battle_team(user_id: int) -> List[PokemonUsuarioModel]:
        """Busca a equipe de batalha do usuário."""
        return PokemonUsuarioModel.query.filter_by(
            id_usuario=user_id,
            grupo_batalha=True
        ).all()