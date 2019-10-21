from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from FlaskAPP.config import Config
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from FlaskAPP.models.users import load_user
    login_manager.init_app(app)
    login_manager.user_loader(load_user)

    from FlaskAPP.endpoints.Settings.routes import settings
    from FlaskAPP.endpoints.Index.routes import main
    from FlaskAPP.endpoints.Patient.routes import patients
    from FlaskAPP.endpoints.About.routes import about
    from FlaskAPP.endpoints.Login.routes import login
    from FlaskAPP.endpoints.Data.routes import data

    app.register_blueprint(main)
    app.register_blueprint(settings)
    app.register_blueprint(patients)
    app.register_blueprint(about)
    app.register_blueprint(login)
    app.register_blueprint(data)

    return app
