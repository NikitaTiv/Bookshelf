from flask import Flask
from flask_login import LoginManager, FlaskLoginClient
from flask_migrate import Migrate

from settings_box.config import get_config
from webapp.admin.views import blueprint as admin_blueprint
from webapp.db import db
from webapp.page.views import blueprint as pages_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__)
    app.config.update(get_config())
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(pages_blueprint)
    app.register_blueprint(user_blueprint)
    app.test_client_class = FlaskLoginClient

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
