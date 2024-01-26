from flask import Blueprint,url_for,redirect
from app.controllers.auth_controller import auth
from app.controllers.stock_controller import stock

# main blueprint to be registered with application
app_blueprint = Blueprint('/', __name__)
app_blueprint.register_blueprint(auth, url_prefix="/auth")
app_blueprint.register_blueprint(stock, url_prefix="/stock")

@app_blueprint.route('/')
def index():
  return redirect(url_for("/.auth.index"))