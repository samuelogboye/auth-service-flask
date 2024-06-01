from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import DevelopmentConfig, TestingConfig, ProductionConfig, Config
import os
from auth.utils.logger import log_warning


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }

    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config_map.get(env, Config))

    # Initialize CORS
    # Retrieve allowed origins from environment variable
    allowed_origins = os.getenv('ALLOWED_ORIGINS')

    if allowed_origins is None:
        log_warning("createapp()", "ALLOWED_ORIGINS environment variable not set. Allowing all origins.")
        allowed_origins = '*'
    else:
        allowed_origins = allowed_origins.split(',')

    # Configure CORS with the allowed origins
    CORS(app, origins=allowed_origins, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    from .errors.handlers import error

    app.register_blueprint(error)
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    # create db tables from models if not exists
    with app.app_context():
        try:
             db.create_all()
        except Exception as e:
             print(f"An error occurred: {e}")

    return app
