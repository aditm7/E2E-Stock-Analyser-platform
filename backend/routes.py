from flask import Blueprint
from backend.controllers.auth_controller import auth
from backend.controllers.stock_controller import stock

# main blueprint to be registered with application
api = Blueprint('/api', __name__)

api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(stock, url_prefix="/stock")