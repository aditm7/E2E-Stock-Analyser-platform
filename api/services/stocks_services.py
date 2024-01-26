from database.models.stock_model import StockData

def get_a_stock(id):
  return StockData.query.filter_by(id=id).first()