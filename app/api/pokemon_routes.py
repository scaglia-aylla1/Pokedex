
from flask import Blueprint, request, jsonify
from app.services.pokemon_service import PokemonService
from flask_jwt_extended import jwt_required, get_jwt_identity

# Cria o Blueprint para as rotas de Pokémon
pokemon_bp = Blueprint('pokemon', __name__)
pokemon_service = PokemonService()

@pokemon_bp.route('/', methods=['GET'])
@jwt_required() # Requisito: Acesso a esta rota requer um JWT válido
def list_pokemons():
    """
    Endpoint para listar Pokémon com paginação e FILTROS (Requisito 2).
    URL: GET /api/v1/pokemon/?limit=...&offset=...&name=<filtro>&generation=<id>
    """
    limit = request.args.get('limit', default=20, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    # NOVOS FILTROS
    name_filter = request.args.get('name', default=None, type=str)

    id_usuario = int(get_jwt_identity()) # Convertemos para int aqui
    
    try:
        pokemons = pokemon_service.get_pokemons_for_listing(
            user_id=id_usuario, 
            limit=limit, 
            offset=offset,
            name_filter=name_filter
        )
        
        return jsonify({
            "msg": "Lista de Pokémon obtida com sucesso.",
            "data": pokemons,
            "total_retornado": len(pokemons)
        }), 200
        
    except Exception as e:
        print(f"Erro ao listar Pokémon: {e}")
        return jsonify({"msg": "Erro interno ao buscar lista de Pokémon."}), 500

    
@pokemon_bp.route('/<string:pokemon_code>/favorite', methods=['POST'])
@jwt_required()
def toggle_favorite(pokemon_code):
    """
    Endpoint para marcar/desmarcar um Pokémon como favorito.
    URL: POST /api/v1/pokemon/<codigo_pokemon>/favorite
    """
    id_usuario = get_jwt_identity()
    

    try:
        is_now_favorite = pokemon_service.toggle_favorite(
            user_id=id_usuario,
            pokemon_code=pokemon_code
        )

        action = "favoritado" if is_now_favorite else "removido dos favoritos"
        return jsonify({
            "msg": f"Pokémon {pokemon_code} {action} com sucesso.",
            "is_favorite": is_now_favorite
        }), 200
        
    except ValueError as e:
        return jsonify({"msg": str(e)}), 400
    except Exception:
        return jsonify({"msg": "Erro interno ao processar favorito."}), 500
    
@pokemon_bp.route('/<string:pokemon_code>/team', methods=['POST'])
@jwt_required()
def toggle_battle_team(pokemon_code):
    """
    Endpoint para adicionar/remover um Pokémon do Grupo de Batalha, com limite de 6.
    URL: POST /api/v1/pokemon/<codigo_pokemon>/team
    """
    id_usuario = get_jwt_identity()
    
    # 1. Tenta obter o JSON de forma silenciosa.
    # Se o corpo for vazio ou houver erro de parsing, data = None.
    data = request.get_json(silent=True)
    
    # 2. Garante que o service receba 'None' se não for um dicionário válido
    pokemon_data = data if isinstance(data, dict) else None

    try:
        pokemon_code_slug = pokemon_code.lower() 

        # 3. Chama o Service. O Service lidará com 'pokemon_data = None'
        is_now_in_team = pokemon_service.toggle_battle_team(
            user_id=id_usuario,
            pokemon_code=pokemon_code_slug,
            pokemon_data=pokemon_data
        )

        action = "adicionado ao time" if is_now_in_team else "removido do time"
        return jsonify({
            "msg": f"Pokémon {pokemon_code_slug} {action} com sucesso.",
            "in_battle_team": is_now_in_team
        }), 200
        
    except ValueError as e:
        # Captura erros de limite ou falha na API (400)
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        # Captura 500. É bom imprimir o erro no console do Flask para debug.
        print(f"Erro interno no toggle_battle_team: {e}")
        return jsonify({"msg": "Erro interno ao processar Grupo de Batalha."}), 500

@pokemon_bp.route('/favorites', methods=['GET'])
@jwt_required()
def list_favorites():
    """
    Endpoint para listar todos os Pokémon favoritos do usuário (Requisito 3).
    URL: GET /api/v1/pokemon/favorites
    """
    # Lembre-se: id_usuario é string, o serviço espera um int.
    id_usuario = int(get_jwt_identity())
    
    try:
        favorites = pokemon_service.get_user_favorite_list(id_usuario)
        
        return jsonify({
            "msg": "Lista de favoritos obtida com sucesso.",
            "data": favorites
        }), 200
    except Exception as e:
        print(f"Erro ao listar favoritos: {e}")
        return jsonify({"msg": "Erro interno ao buscar lista de favoritos."}), 500

@pokemon_bp.route('/team', methods=['GET'])
@jwt_required()
def get_battle_team():
    """
    Endpoint para exibir a Equipe de Batalha do usuário (Requisito 4).
    URL: GET /api/v1/pokemon/team
    """
    id_usuario = int(get_jwt_identity())
    
    try:
        team = pokemon_service.get_user_battle_team_list(id_usuario)
        
        return jsonify({
            "msg": "Equipe de Batalha obtida com sucesso.",
            "data": team,
            "count": len(team)
        }), 200
    except Exception as e:
        print(f"Erro ao obter equipe de batalha: {e}")
        return jsonify({"msg": "Erro interno ao buscar Equipe de Batalha."}), 500