from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Resource,marshal,abort
from api.utils.stocksdto import StocksDto
from api.services.stocks_services import get_all_stock_data,get_stock_data_range,get_statistical_parameters
from datetime import datetime

api = StocksDto.api
_stock = StocksDto.stock
_stats = StocksDto.stats_parameters

@api.route('/market/<stock_id>')
@api.param('stock_id', 'The Stock Unique Code')
class StocksMarketData(Resource):
  @api.doc('The Stock\'s market data stored in the DB')
  @api.doc(params={'from_date': 'Start date (YYYY-MM-DD)', 'to_date': 'End date (YYYY-MM-DD)'})
  @api.marshal_list_with(_stock)
  def get(self,stock_id):
    try:
      if request.args:
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        if from_date and to_date: # Check if the payload is empty or not
          from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
          to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
          return get_stock_data_range(stock_id,from_date,to_date)
      return get_all_stock_data(stock_id)
    except ValueError:
      abort(400, f"Date must be in the following format: YYYY-MM-DD")
    except Exception as e:
      abort(400, f"Server error: {str(e)}")

@api.route('/stats/<stock_id>')
@api.param('stock_id', 'The Stock Unique Code')
class StocksStatsParams(Resource):
  @api.doc('Some statistical properties measured on the selected stock data')
  @api.doc(params={'from_date': 'Start date (YYYY-MM-DD)', 'to_date': 'End date (YYYY-MM-DD)'})
  @api.marshal_list_with(_stats)
  def get(self,stock_id):
    try:
      if request.args:
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        if from_date and to_date: # Check if the payload is empty or not
          from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
          to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
          return get_statistical_parameters(stock_id,from_date,to_date)
      else:
        abort(400, f"Server error: Mention the correct date ranges for parameters to be calculated")
    except ValueError:
      abort(400, f"Date must be in the following format: YYYY-MM-DD")
    except Exception as e:
      abort(400, f"Server error: {str(e)}")