from flask import Flask
from .filter_api.routes import filter_bp
from .images_api.routes import images_bp
from .patients_api.routes import patients_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(filter_bp, url_prefix='/filter')
    app.register_blueprint(patients_bp, url_prefix='/patients')
    app.register_blueprint(images_bp, url_prefix='/images')
    return app
