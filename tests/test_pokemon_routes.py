
import json
from unittest.mock import patch, MagicMock

# Dados de um Pokémon para usar no POST
POKEMON_DATA = {
    "nome": "Bulbasaur",
    "imagem_uri": "img_uri_bulba",
    "tipos": ["Grass", "Poison"]
}


# Mock para API externa(PokeAPIClient)
# Para garantir que os testes sejam UNITÁRIOS e não dependam da PokeAPI.
# Mock de um item de lista (GET /pokemon/)
MOCK_POKEMON_LIST_ITEM = [
    {"name": "bulbasaur", "url": "url_bulba"},
    {"name": "ivysaur", "url": "url_ivy"}
]

# Mock dos detalhes de um Pokémon (GET /pokemon/ e POST /favorite)
MOCK_POKEMON_DETAILS = {
    "id": 1,
    "name": "bulbasaur",
    "sprites": {"other": {"official-artwork": {"front_default": POKEMON_DATA["imagem_uri"]}}},
    "types": [{"type": {"name": "grass"}}, {"type": {"name": "poison"}}],
    "stats": [{"stat": {"name": "hp"}, "base_stat": 45}]
}

@patch('app.external.poke_api_client.PokeAPIClient.get_pokemon_details', return_value=MOCK_POKEMON_DETAILS)
@patch('app.external.poke_api_client.PokeAPIClient.get_pokemon_list', return_value=MOCK_POKEMON_LIST_ITEM)
def test_list_pokemons_success(mock_list, mock_details, client, auth_headers):
    """
    Testa se a listagem de Pokémon funciona (código 200) e retorna o formato esperado
    ao ser chamado com um JWT válido.
    """
    response = client.get('/api/v1/pokemon/', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert 'data' in data
    assert len(data['data']) > 0
    assert data['data'][0]['nome'] == 'Bulbasaur'
    # Verifica se os status iniciais são False (pois não favoritamos nada ainda)
    assert data['data'][0]['is_favorite'] == False
    assert data['data'][0]['in_battle_team'] == False

def test_list_pokemons_unauthorized(client):
    """Testa se a rota de listagem é protegida e retorna 401/422 sem JWT."""
    response = client.get('/api/v1/pokemon/')
    # O Flask-JWT-Extended retorna 401 ou 422
    assert response.status_code in [401, 422] 

# Testes de lógica de negócio (favoritar, time de batalha, etc.)
@patch('app.external.poke_api_client.PokeAPIClient.get_pokemon_details', return_value=MOCK_POKEMON_DETAILS)
def test_toggle_favorite_lifecycle(mock_details, client, auth_headers):
    """
    Testa o ciclo de vida: 
    1. Favoritar (Cria registro)
    2. Desfavoritar (Remove registro, pois não está no time)
    3. Tenta favoritar novamente.
    """
    # FAVORITAR (Cria o registro no BD, favorito = True)
    response = client.post('/api/v1/pokemon/1/favorite', headers=auth_headers, data=json.dumps(POKEMON_DATA))
    assert response.status_code == 200
    assert response.get_json()['is_favorite'] == True
    
    # DESFAVORITAR (Remove o registro do BD)
    response = client.post('/api/v1/pokemon/1/favorite', headers=auth_headers, data=json.dumps(POKEMON_DATA))
    assert response.status_code == 200
    assert response.get_json()['is_favorite'] == False # Deve ser False agora
    
    # TENTA FAVORITAR NOVAMENTE (Garante que o registro foi recriado)
    response = client.post('/api/v1/pokemon/1/favorite', headers=auth_headers, data=json.dumps(POKEMON_DATA))
    assert response.status_code == 200
    assert response.get_json()['is_favorite'] == True
    
@patch('app.external.poke_api_client.PokeAPIClient.get_pokemon_details', return_value=MOCK_POKEMON_DETAILS)
def test_toggle_battle_team_limit(mock_details, client, auth_headers):
    """
    Testa a regra de negócio do limite máximo de 6 Pokémon no time.
    """
    # Dados de Pokémon para o loop
    team_pokemons = [
        {"codigo": str(i), "nome": f"Poke{i}", "imagem_uri": "uri", "tipos": ["Normal"]}
        for i in range(1, 8)
    ]
    
    # Adiciona 6 Pokémon (Limiar)
    for i in range(6):
        data = team_pokemons[i]
        response = client.post(f'/api/v1/pokemon/{data["codigo"]}/team', 
                               headers=auth_headers, 
                               data=json.dumps(data))
        assert response.status_code == 200
        assert response.get_json()['in_battle_team'] == True

    # Tenta adicionar o 7º (Deve falhar com erro 400)
    data_7 = team_pokemons[6]
    response = client.post(f'/api/v1/pokemon/{data_7["codigo"]}/team', 
                           headers=auth_headers, 
                           data=json.dumps(data_7))
    
    assert response.status_code == 400
    assert "Equipe de Batalha já está completa" in response.get_json()['msg']

@patch('app.external.poke_api_client.PokeAPIClient.get_pokemon_details', return_value=MOCK_POKEMON_DETAILS)
def test_list_favorites_and_team(mock_details, client, auth_headers):
    """Testa se as listagens de favoritos e time funcionam."""
    
    # Adiciona um Pokémon como favorito (Poké 1)
    client.post('/api/v1/pokemon/1/favorite', headers=auth_headers, data=json.dumps(POKEMON_DATA))

    # Adiciona um Pokémon ao time (Poké 2)
    poke_2_data = {"nome": "Ivysaur", "imagem_uri": "uri_2", "tipos": ["Grass"]}
    client.post('/api/v1/pokemon/2/team', headers=auth_headers, data=json.dumps(poke_2_data))

    # Teste de Favoritos
    response_fav = client.get('/api/v1/pokemon/favorites', headers=auth_headers)
    assert response_fav.status_code == 200
    data_fav = response_fav.get_json()['data']
    assert len(data_fav) == 1
    assert data_fav[0]['codigo'] == '1'
    
    # Teste de Equipe
    response_team = client.get('/api/v1/pokemon/team', headers=auth_headers)
    assert response_team.status_code == 200
    data_team = response_team.get_json()['data']
    assert len(data_team) == 1
    assert data_team[0]['codigo'] == '2'