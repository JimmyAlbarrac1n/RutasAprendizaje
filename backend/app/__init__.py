from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import os
from dotenv import load_dotenv

mongo = PyMongo()

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, supports_credentials=True)  # Habilitar credenciales para CORS
    
    # Configuración de la sesión
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-key-123")
    app.config["SESSION_COOKIE_SECURE"] = False  # Cambiar a True en producción
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    app.config["MONGO_URI"] = os.getenv("MONGO_URI")

    mongo.init_app(app)

    # Register Blueprints (views)
    from .views.user_routes import user_bp
    from .views.auth_routes import auth_bp
    from .views.tag_routes import tag_bp
    from .views.material_routes import material_bp
    from .views.route_routes import route_bp

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tag_bp, url_prefix='/tags')
    app.register_blueprint(material_bp, url_prefix='/materials')
    app.register_blueprint(route_bp, url_prefix='/routes')

    return app
