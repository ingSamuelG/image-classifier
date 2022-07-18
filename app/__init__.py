from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_migrate import Migrate
from decimal import Decimal, localcontext, ROUND_05UP
from config import config
# import flask_excel as excel
from flask_mail import Mail
from flask_login import LoginManager

meta = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })

bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
db = SQLAlchemy(metadata = meta, session_options = {"autoflush": False} )
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    # excel.init_excel(app)
    login_manager.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .classifier import classifier as classifier_blueprint
    app.register_blueprint(classifier_blueprint, url_prefix='/classifier')

    from .examples import examples as examples_blueprint
    app.register_blueprint(examples_blueprint, url_prefix='/examples')

    return app