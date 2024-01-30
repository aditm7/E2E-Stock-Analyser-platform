from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource,marshal,abort
from api.utils.companydto import CompanyDto
from api.services.company_services import get_all_companies,get_company

api = CompanyDto.api
_company = CompanyDto.company

@api.route('/all')
class CompaniesList(Resource):
  @api.doc('All data of all the Companies stored in the DB')
  @api.marshal_list_with(_company)
  def get(self):
    try:
      return get_all_companies()
    except Exception as e:
      abort(400, f"Server error: {str(e)}")

@api.route('/<stock_id>')
@api.param('stock_id', 'The Stock Unique Code')
class StocksMarketData(Resource):
  @api.doc('Company\'s data in the DB, identified by the StockCode')
  @api.marshal_with(_company)
  def get(self,stock_id):
    try:
      return get_company(stock_id)
    except Exception as e:
      abort(400, f"Server error: {str(e)}")