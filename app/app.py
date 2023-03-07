from flask import Flask
from flask_jwt_extended import JWTManager
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.blueprints.main import bp_main
    app.register_blueprint(bp_main)

    from app.blueprints.auth import bp_auth
    app.register_blueprint(bp_auth)

    from app.blueprints.user import bp_users
    app.register_blueprint(bp_users)

    from app.db import db
    db.init_app(app)

    with app.app_context():
        db.create_all()

    JWTManager(app)

    return app
