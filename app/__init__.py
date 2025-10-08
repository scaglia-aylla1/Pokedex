
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config
from flask_cors import CORS

# Inicializa as extensões sem a aplicação Flask (adiamento da inicialização)
# Isso permite configurar o Flask e as extensões em diferentes momentos,
# facilitando a organização em projetos maiores.
db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_object=Config):
    """Cria e configura a aplicação Flask."""
    # Dentro da sua função create_app(config_object):
    
    app = Flask(__name__)
    app.config.from_object(config_object)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

    # Inicializa as extensões com a aplicação Flask
    db.init_app(app)
    jwt.init_app(app)

    # Registro dos Modelos
    # Importamos os modelos para que o SQLAlchemy saiba quais tabelas criar
    with app.app_context():
        from .models import user_model
        from .models import tipo_pokemon_model
        from .models import pokemon_usuario_model
        db.create_all()

    # Registro das Rotas (APIs)
    # Importamos o blueprint de autenticação
    from .api.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    # Registro da nova rota de Pokémon
    from .api.pokemon_routes import pokemon_bp
    app.register_blueprint(pokemon_bp, url_prefix='/api/v1/pokemon')
    
    return app