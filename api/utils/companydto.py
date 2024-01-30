from flask_restx import Namespace, fields

class CompanyDto:
  """ Data transfer object for Stocks. """
  api = Namespace('Companies', description='Companies related operations')

  company = api.model('stocks', {
    'company': fields.String(description='Name of the company'),
    'industry': fields.String(description='Type of Industry to which company belongs'),
    'symbol': fields.String(description='Company\'s stock symbol on the NSE'),
    'isin_code': fields.String(description='Company\'s ISIN code'),
  })