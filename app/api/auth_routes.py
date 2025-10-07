
from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

# Cria um Blueprint (módulo de rotas) para as rotas de autenticação
auth_bp = Blueprint('auth', __name__)
user_service = UserService() # Instância do nosso Serviço

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint para registrar um novo usuário no sistema.
    URL: POST /api/v1/auth/register
    """
    data = request.get_json()
    
    # Validação básica de campos obrigatórios
    if not data or not all(k in data for k in ('nome', 'login', 'email', 'senha')):
        return jsonify({"msg": "Dados incompletos. Requer: nome, login, email, senha."}), 400

    try:
        # Usa o UserService para a lógica de negócio e persistência
        new_user = user_service.register_user(data)
        
        # Retorna o sucesso.
        return jsonify({
            "msg": "Usuário registrado com sucesso!",
            "id_usuario": new_user.id_usuario,
            "login": new_user.login
        }), 201
        
    except ValueError as e:
        # Erro de negócio (login/email já em uso)
        return jsonify({"msg": str(e)}), 409
    except Exception:
        # Erro genérico do servidor
        return jsonify({"msg": "Erro interno ao registrar usuário."}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Endpoint para realizar o login e obter o Token JWT[cite: 86].
    URL: POST /api/v1/auth/login
    """
    data = request.get_json()
    
    if not data or not all(k in data for k in ('login', 'senha')):
        return jsonify({"msg": "Dados incompletos. Requer: login e senha."}), 400

    try:
        # Usa o UserService para autenticar e gerar o Token
        access_token = user_service.login_user(data['login'], data['senha'])
        
        # Retorna o Token JWT que será usado pelo Front-End 
        return jsonify({"access_token": access_token}), 200
        
    except ValueError as e:
        # Erro de negócio (credenciais inválidas)
        return jsonify({"msg": str(e)}), 401 
    except Exception:
        return jsonify({"msg": "Erro interno ao realizar login."}), 500