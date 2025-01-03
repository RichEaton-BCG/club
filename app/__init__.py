from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import User

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.debug = True

    db.init_app(app)
    login_manager.init_app(app)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints registration
    from .routes import public, members, store
    app.register_blueprint(public.bp)
    app.register_blueprint(members.bp)
    app.register_blueprint(store.bp)

    return app
