from flask import Flask
from .filter_api.routes import filter_bp
from .photos_api.routes import photos_bp
from .patients_api.routes import patients_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(filter_bp, url_prefix='/filter')
    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(photos_bp, url_prefix='/photos')
    return app
