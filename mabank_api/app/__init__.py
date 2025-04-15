from flask import Flask
from database import db
from flask_migrate import Migrate
from config import Config   
from app.routes.user_route import user_bp
from app.routes.account_routes import account_bp
from app.routes.transaction_route import transaction_bp

# from app.routes.transaction_route import transaction_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Konfigurasi database
    app.config.from_object(Config)

     # Inisialisasi db dengan aplikasi
    db.init_app(app)
    
    migrate.init_app(app, db)
    # Register Blueprints for each route
    app.register_blueprint(user_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(transaction_bp)

    # app.register_blueprint(transaction_bp)
    
    return app
