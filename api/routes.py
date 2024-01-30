from flask import Blueprint,url_for,redirect
from flask_restx import Api
from api.controller.stock_controller import api as stocks_ns
from api.controller.company_controller import api as company_ns

api_blueprint = Blueprint('/api', __name__)

api = Api(api_blueprint,
          title='TradeCorp API',
          version='1.0',
          description='Built with Flask'
          )

api.add_namespace(stocks_ns,path='/stocks')
api.add_namespace(company_ns,path='/company')