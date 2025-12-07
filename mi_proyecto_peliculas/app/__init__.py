from flask import Flask
from mongoengine import connect 
from os import environ 

def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
    app.config["MONGO_URI"] = environ.get("MONGO_URI")

    connect(host=app.config["MONGO_URI"])
    
    # Registro del Blueprint de Autenticación
    from .auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Registro del Blueprint de Películas
    from .routes import movies_bp
    app.register_blueprint(movies_bp, url_prefix='/movies')

    return app