
import requests
from typing import Dict, Any, List

class PokeAPIClient:
    """
    Cliente dedicado para interagir com a PokeAPI.
    Responsável unicamente pela comunicação HTTP e tratamento de dados brutos.
    """
    
    BASE_URL = "https://pokeapi.co/api/v2/"
    
    def __init__(self):
        """Inicializa o cliente com a URL base."""
        print("PokeAPIClient inicializado.") # Para debug inicial
        
    def _fetch_data(self, endpoint: str) -> Dict[str, Any] or None: # type: ignore
        """Método privado para realizar a chamada HTTP e tratar erros."""
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, timeout=10) 
            response.raise_for_status() 
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP ao acessar {url}: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Erro de conexão ao acessar {url}: {e}")
            return None

    def get_pokemon_list(self, limit: int = 151, offset: int = 0) -> List[Dict[str, str]] or None: # type: ignore
        """
        Busca uma lista paginada de nomes e URLs de Pokémon.
        
        Args:
            limit: O número máximo de Pokémon a retornar.
            offset: O ponto de partida da lista.
            
        Returns:
            Uma lista de dicionários com 'name' e 'url', ou None em caso de falha.
        """
        endpoint = f"pokemon?limit={limit}&offset={offset}"
        data = self._fetch_data(endpoint)
        
        if data and 'results' in data:
            return data['results']
        return None

    def get_pokemon_details(self, identifier: str) -> Dict[str, Any] or None: # type: ignore
        """
        Busca detalhes completos de um Pokémon específico (por nome ou ID).
        
        Args:
            identifier: O nome (e.g., 'bulbasaur') ou ID (e.g., '1') do Pokémon.
            
        Returns:
            Um dicionário com todos os detalhes do Pokémon, ou None.
        """
        endpoint = f"pokemon/{identifier}"
        return self._fetch_data(endpoint)

    def get_pokemon_species(self, identifier: str) -> Dict[str, Any] or None: # type: ignore
        """
        Busca dados de espécies de um Pokémon (útil para geração e descrições).
        """
        endpoint = f"pokemon-species/{identifier}"
        return self._fetch_data(endpoint)