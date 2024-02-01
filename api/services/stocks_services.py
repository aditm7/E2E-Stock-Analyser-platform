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

def get_statistical_parameters(id,start_date,end_date):
  data = StockData.query.filter(
    and_(
      StockData.symbol == id,
      StockData.date.between(start_date, end_date)
    )
  ).order_by(StockData.date).all()

  out = {"symbol":f"{id}","ngr":""}
  if data:
    cagr = (data[-1].close-data[0].close)*100/(data[0].close)
    out["ngr"] = round(cagr,2)
  return out