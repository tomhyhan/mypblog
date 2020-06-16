from flask import Flask
from myblog.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from myblog.config_test import Config_test


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_myblog(use_config=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from myblog.main.routes import main
    from myblog.users.routes import users
    from myblog.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)
    return app


def testing_myblog(use_config_test=Config_test):
    app = Flask(__name__)
    app.config.from_object(Config_test)
    app.config['TESTING'] = True
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from myblog.main.routes import main
    from myblog.users.routes import users
    from myblog.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(errors)
    return app
