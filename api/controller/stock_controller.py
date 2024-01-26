from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource
from api.utils.stocksdto import StocksDto
from api.services.stocks_services import get_a_stock

api = StocksDto.api
_stock = StocksDto.stock

@api.route('/')
class StocksList(Resource):
  @api.doc('list of all stocks')
  @api.marshal_with(_stock, envelope='data')
  def get(self):
    return get_a_stock(1)