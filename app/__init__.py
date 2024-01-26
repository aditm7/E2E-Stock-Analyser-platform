from flask import Flask
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import config,SECRET_KEY

load_dotenv()

app = Flask(__name__,instance_path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../database'))
app.env = config.ENV

app.secret_key = SECRET_KEY
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

db = SQLAlchemy(app)
migrate = Migrate(app, db,directory=os.environ.get("MIGRATION_DIR"))

from app.routes import app_blueprint
from api.routes import api_blueprint
app.register_blueprint(app_blueprint, url_prefix="/")
app.register_blueprint(api_blueprint, url_prefix="/api")

from database.models.user_model import User