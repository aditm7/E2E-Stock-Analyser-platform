from flask import Flask
import os
from backend.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# for password hashing
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)
config = Config()
app.env = config.ENV

app.secret_key = os.environ.get("SECRET_KEY")
bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

# sql alchemy instance
db = SQLAlchemy(app)

# Flask Migrate instance to handle migrations
migrate = Migrate(app, db)

# import api blueprint to register it with app
from backend.routes import api
app.register_blueprint(api, url_prefix="/api")

# import models to let the migrate tool know
from backend.models.user_model import User