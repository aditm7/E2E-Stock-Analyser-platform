from database.models.stock_model import StockData
from sqlalchemy import and_

def get_all_stock_data(id):
  return StockData.query.filter_by(symbol=id).all()

def get_stock_data_range(id, start_date, end_date):
  return StockData.query.filter(
    and_(
      StockData.symbol == id,
      StockData.date.between(start_date, end_date)
    )
  ).all()