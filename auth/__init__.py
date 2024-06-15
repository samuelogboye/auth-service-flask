''' To initialize auth app'''
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from auth.utils.logger import log_warning
from .config import DevelopmentConfig, TestingConfig, Config



db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    ''' Create app'''
    app = Flask(__name__)

    # Load Configuration
    config_map = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        # 'production': ProductionConfig
    }

    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object(config_map.get(env, Config))

    limiter = Limiter( # pylint: disable=unused-variable
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
        log_warning(
            "createapp()", 
            "ALLOWED_ORIGINS environment variable not set. Allowing all origins."
        )
        allowed_origins = '*'
    else:
        allowed_origins = allowed_origins.split(',')
    CORS(app, origins=allowed_origins, supports_credentials=True)

    from .routes.auth import auth_bp # pylint: disable=import-outside-toplevel
    from .errors.handlers import error # pylint: disable=import-outside-toplevel

    app.register_blueprint(error)
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    # create db tables from models if not exists
    with app.app_context():
        try:
            db.create_all()
        except Exception as e: # pylint: disable=broad-exception-caught
            print(f"An error occurred: {e}")

    return app
