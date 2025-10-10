

from app.external.poke_api_client import PokeAPIClient
from app.repositories.pokemon_repository import PokemonRepository 
from app.repositories.user_repository import UserRepository 
from app.models.pokemon_usuario_model import PokemonUsuarioModel
from typing import Dict, Any, List


class PokemonService:
    """
    Camada de Serviço para a lógica de negócios de Pokémon.
    Transforma dados brutos da PokeAPI e gerencia o estado do usuário no BD.
    """
    
    def __init__(self):
        """Inicializa o serviço com o cliente da API e o repositório."""
        self.api_client = PokeAPIClient()

        # Inicializa o repositório (dependência de persistência)
        self.pokemon_repo = PokemonRepository() 
    

    def _extract_data_from_details(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai e formata os dados essenciais de um Pokémon a partir da resposta da PokeAPI.
        Isso garante que nossa aplicação só use os dados de que realmente precisa.
        """
        if not raw_data:
            return None
      
        id_pokemon = raw_data.get('id')
        
        return {
            'id_pokemon': id_pokemon,
            'nome': raw_data.get('name').capitalize(),
            'codigo': str(id_pokemon),
            'tipos': [t['type']['name'].capitalize() for t in raw_data.get('types', [])],
            'imagem_uri': raw_data['sprites']['other']['official-artwork']['front_default'],
            # Mapeamento para a listagem (exemplo: HP, Ataque, etc.)
            'stats': {s['stat']['name']: s['base_stat'] for s in raw_data.get('stats', [])}
        }

    def get_pokemons_for_listing(self, user_id: int, limit: int = 20, offset: int = 0, name_filter: str = None, generation_id: int = None) -> List[Dict[str, Any]]:
        """
        Busca a lista da PokeAPI, anexa o status do usuário e aplica filtros.
        """
        pokemon_list_raw = self.api_client.get_pokemon_list(limit=limit, offset=offset)
        
        if not pokemon_list_raw:
            return []
            
        pokemons_processed = []
        
        for item in pokemon_list_raw:
            pokemon_name = item['name']
            
            # Filtro por nome (Requisito Básico)
            # Se o filtro de nome for fornecido e o nome do Pokémon não contiver o filtro (case-insensitive), pula para o próximo.
            if name_filter and name_filter.lower() not in pokemon_name.lower():
                continue
            
            details = self.api_client.get_pokemon_details(pokemon_name)
            
            if details:
                pokemon_data = self._extract_data_from_details(details)
                
                if pokemon_data:
                    # ... (lógica de verificação de estado do usuário)
                    user_pokemon_state = self.pokemon_repo.get_pokemon_by_user_and_code(
                        user_id=user_id, 
                        pokemon_code=pokemon_data['codigo']
                    )
                    
                    pokemon_data['is_favorite'] = user_pokemon_state.favorito if user_pokemon_state else False
                    pokemon_data['in_battle_team'] = user_pokemon_state.grupo_batalha if user_pokemon_state else False
                    
                    pokemons_processed.append(pokemon_data)
                    
        return pokemons_processed

    # Lógica de Marcar/Desmarcar favorito
    def toggle_favorite(self, user_id: int, pokemon_code: str, pokemon_data: Dict[str, Any]=None) -> bool:
        """
        Adiciona ou remove um Pokémon da lista de favoritos do usuário.
        """
        user_pokemon = self.pokemon_repo.get_pokemon_by_user_and_code(user_id, pokemon_code)

        if user_pokemon:
            # Se já existe, apenas inverte o status de favorito
            user_pokemon.favorito = not user_pokemon.favorito
            is_favorite = user_pokemon.favorito

            # Se for desfavoritado e não estiver no time, deleta o registro para limpar o BD
            if not user_pokemon.favorito and not user_pokemon.grupo_batalha:
                self.pokemon_repo.delete(user_pokemon)
                return False # Foi desfavoritado
            
            self.pokemon_repo.save(user_pokemon)
            return is_favorite
        else:
            # Se não existe, cria o registro e marca como favorito
            if not pokemon_data:
                try:
                    # IMPLEMENTAR ESTA CHAMADA NO SEU REPOSITÓRIO
                    pokemon_data = self.pokemon_repo.get_pokemon_details_from_api(pokemon_code)
                except Exception:
                    # Se a busca na PokeAPI ou no cache falhar
                    raise ValueError(f"Não foi possível obter os dados do Pokémon '{pokemon_code}' para criação.")

            # Garante que o TipoPokemon exista e pega seu ID (Foreign Key)
            first_type = pokemon_data['tipos'][0] # Pega o primeiro tipo para o TipoPokemon FK
            tipo_pokemon_model = self.pokemon_repo.find_or_create_type(first_type)

            # Cria o novo objeto no BD
            new_user_pokemon = PokemonUsuarioModel(
                id_usuario=user_id,
                id_tipo_pokemon=tipo_pokemon_model.id_tipo_pokemon,
                codigo=pokemon_code,
                nome=pokemon_data['nome'],
                imagem_uri=pokemon_data['imagem_uri'],
                favorito=True,
                grupo_batalha=False
            )
            self.pokemon_repo.save(new_user_pokemon)
            return True 

    from typing import Dict, Any



    def toggle_battle_team(self, user_id: int, pokemon_code: str, pokemon_data: Dict[str, Any]=None) -> bool:
        """
        Adiciona ou remove um Pokémon da Equipe de Batalha do usuário,
        garantindo o limite máximo de 6 Pokémon.
        """
        user_pokemon = self.pokemon_repo.get_pokemon_by_user_and_code(user_id, pokemon_code)

        if user_pokemon:
            # Caso 1: O Pokémon já está registrado para o usuário (Lógica OK)

            if user_pokemon.grupo_batalha:
                # Se já está no time, vamos removê-lo
                user_pokemon.grupo_batalha = False
                action = False
                
                # Se for removido do time E não for favorito, deletamos o registro
                if not user_pokemon.favorito:
                    self.pokemon_repo.delete(user_pokemon)
                    return False
            else:
                # Se NÃO está no time, vamos adicioná-lo
                
                # VERIFICAÇÃO DO LIMITE DE 6 
                current_count = self.pokemon_repo.get_user_battle_team_count(user_id)
                if current_count >= 6:
                    raise ValueError("A Equipe de Batalha já está completa (máximo de 6 Pokémon).")
                
                # Adiciona ao time
                user_pokemon.grupo_batalha = True
                action = True
            
            self.pokemon_repo.save(user_pokemon)
            return action
            
        else:
            # Caso 2: O Pokémon NÃO está registrado para o usuário (precisa ser criado)
            
            # VERIFICAÇÃO DO LIMITE DE 6 (Aplica-se à criação também)
            current_count = self.pokemon_repo.get_user_battle_team_count(user_id)
            if current_count >= 6:
                raise ValueError("A Equipe de Batalha já está completa (máximo de 6 Pokémon).")
            
            # === CORREÇÃO: Buscando dados do Pokémon se o Front-End não enviou ===
            if not pokemon_data:
                try:
                    # Chama a função do Repositório para buscar na PokeAPI
                    pokemon_data = self.pokemon_repo.get_pokemon_details_from_api(pokemon_code)
                except Exception:
                    # Se falhar ao buscar na API, levanta o erro 400
                    raise ValueError(f"Não foi possível obter os dados do Pokémon '{pokemon_code}' para adicionar ao time.")

            # Cria o TipoPokemon e o registro de PokemonUsuario, marcando GrupoBatalha=True
            first_type = pokemon_data['tipos'][0]
            tipo_pokemon_model = self.pokemon_repo.find_or_create_type(first_type)

            new_user_pokemon = PokemonUsuarioModel(
                id_usuario=user_id,
                id_tipo_pokemon=tipo_pokemon_model.id_tipo_pokemon,
                codigo=pokemon_code,
                nome=pokemon_data['nome'],
                imagem_uri=pokemon_data['imagem_uri'],
                favorito=False, # Não é automaticamente favorito, apenas faz parte do time
                grupo_batalha=True
            )
            self.pokemon_repo.save(new_user_pokemon)
            return True # Foi adicionado
    
    def _format_user_pokemon_list(self, pokemon_list: List[PokemonUsuarioModel]) -> List[Dict[str, Any]]:
        """
        Método auxiliar para formatar objetos PokemonUsuarioModel para JSON de resposta.
        Retorna apenas os dados armazenados localmente.
        """
        formatted_list = []
        for p in pokemon_list:
            formatted_list.append({
                # ID do registro local
                'id_usuario_pokemon': p.id_pokemon_usuario, 
                # Código (ID/Nome) do Pokémon na PokeAPI
                'codigo': p.codigo, 
                'nome': p.nome.capitalize(),
                'imagem_uri': p.imagem_uri,
                'is_favorite': p.favorito,
                'in_battle_team': p.grupo_batalha
            })
        return formatted_list

    def get_user_favorite_list(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Busca a lista de Pokémon favoritos do usuário no BD e formata.
        """
        favorite_pokemons = self.pokemon_repo.get_user_favorite_pokemons(user_id)
        return self._format_user_pokemon_list(favorite_pokemons)

    def get_user_battle_team_list(self, user_id: int) -> List[Dict[str, Any]]:
        """
        Busca a Equipe de Batalha do usuário no BD e formata.
        """
        battle_team = self.pokemon_repo.get_user_battle_team(user_id)
        return self._format_user_pokemon_list(battle_team)