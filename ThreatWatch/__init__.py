# Import necessary modules and classes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from sqlalchemy import create_engine
from .enums import AccountStatus, Role
from ThreatWatch.config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

# Application factory function
def create_app(config_class=Config):
    # Create Flask application instance
    app = Flask(__name__)
    # Load configuration from Config class
    app.config.from_object(Config)

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Add custom Jinja environment globals for enums
    app.jinja_env.globals.update(AccountStatus=AccountStatus)
    app.jinja_env.globals.update(Role=Role)

    # Import blueprints and register them with the app
    from ThreatWatch.users.routes import users
    from ThreatWatch.incidents.routes import incidents
    from ThreatWatch.main.routes import main
    from ThreatWatch.errors.handlers import errors

    from .audit import db_after_flush, db_before_flush

    app.register_blueprint(users)
    app.register_blueprint(incidents)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
