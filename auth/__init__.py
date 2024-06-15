from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from .config import DevelopmentConfig, TestingConfig, ProductionConfig, Config
import os
from auth.utils.logger import log_warning
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import Table, MetaData


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Load Configuration
    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig
    }

    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config_map.get(env, Config))

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["20 per 5 minutes"]
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Initialize CORS
    allowed_origins = os.getenv('ALLOWED_ORIGINS')
    if allowed_origins is None:
        log_warning("createapp()", "ALLOWED_ORIGINS environment variable not set. Allowing all origins.")
        allowed_origins = '*'
    else:
        allowed_origins = allowed_origins.split(',')
    CORS(app, origins=allowed_origins, supports_credentials=True)

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
