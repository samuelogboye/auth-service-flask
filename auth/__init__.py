''' To initialize auth app'''
import os
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger
from auth.utils.logger import log_warning
from .config import DevelopmentConfig, TestingConfig, Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}

swagger_template = {
    "info": {
        "title": "Authentication Service API Documentation",
        "description": "This is a custom API documentation for a \
            simple authentication service with Flask.",
        "version": "1.0.0",
        "termsOfService": "/terms",
        "contact": {
            "email": "ogboyesam@gmail.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    "host": "", # Initially empty
    "basePath": "/",  # Base path for the APIs
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your bearer token in the format **Bearer &lt;token>**"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    "operationId": "get_my_data",
    "produces": [
        "application/json"
    ],
    "consumes": [
        "application/json"
    ],
    "tags": [
        {
            "name": "auth",
            "description": "Authentication related endpoints"
        }
    ]
}

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

    # Update Swagger host dynamically
    with app.test_request_context():
        from auth.utils.logger import log_debug # pylint: disable=import-outside-toplevel

        swagger_template["host"] = os.getenv('SWAGGER_HOST', request.host)
        Swagger(app, config=swagger_config, template=swagger_template)
        log_debug(
            "createapp.update_swagger_host()", f"Swagger host updated- {swagger_template['host']}")

    # create db tables from models if not exists
    with app.app_context():
        try:
            db.create_all()
        except Exception as e: # pylint: disable=broad-exception-caught
            from auth.utils.logger import log_error # pylint: disable=import-outside-toplevel
            log_error("create_app()", f"An error occurred: {e}")

    # General route to get logs
    @app.route('/logs', methods=['GET'])
    def get_logs():
        """Endpoint to retrieve logs"""
        log_file_path = 'logs/app.log'
        try:
            with open(log_file_path, 'r', encoding='utf-8') as file:
                log_content = file.read()
            return Response(log_content, mimetype='text/plain')
        except Exception as e:  # pylint: disable=broad-exception-caught
            return jsonify({"error": str(e)}), 500

    return app
