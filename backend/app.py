from flask import Flask
from config import DevelopmentConfig, TestingConfig
from extensions import db, login_manager
from models.user import User
from routes import auth, data, errors

def create_app(config_name='development'):
    app = Flask(__name__)
    
    if config_name == 'development':
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        app.config.from_object(TestingConfig)

    # Initialize database and authentication
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()

    # Register blueprints for routes
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(data.data_bp)
    app.register_blueprint(errors.errors_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app