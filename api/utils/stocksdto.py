from flask_restx import Namespace, fields

class StocksDto:
  """ Data transfer object for Stocks. """
  api = Namespace('stocks', description='Stocks related operations')

  stock = api.model('stocks', {
    'date':fields.Date(description="Date in YYYY-MM-DD String format"),
    'open': fields.Float(description='opening price of the stock on the day'),
    'close': fields.Float(description='closing price of the stock on the day'),
    'high': fields.Float(description='highest price of the stock on the day'),
    'low': fields.Float(description='lowest price of the stock on the day'),
  })

  payload = api.model('Payload', {
    'from_date': fields.String(description='Start date of the range'),
    'to_date': fields.String(description='End date of the range')
  })