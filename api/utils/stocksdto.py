from flask_restx import Namespace, fields

class StocksDto:
  api = Namespace('stocks', description='stocks related operations')
  stock = api.model('stocks', {
    'low': fields.String(required=True, description='desc 1'),
    'high': fields.String(description='desc 2')
  })