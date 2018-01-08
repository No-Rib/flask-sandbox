from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SECRET_KEY"] = "supersecret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/database.db"

app.config["REDIS_URL"] = "redis://localhost:6379"

Bootstrap(app)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

redis = FlaskRedis(app)

from app import views # noqa: ignore=E402,F401
from app import models # noqa: ignore=E402,F401
from app import utils # noqa: ignore=E402,F401

app.jinja_env.globals.update(format_datetime=utils.format_datetime)
