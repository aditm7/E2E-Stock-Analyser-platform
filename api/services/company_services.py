from database.models.company_model import CompanyData

def get_all_companies():
  return CompanyData.query.all()

def get_company(id):
  return CompanyData.query.filter_by(symbol=id).first()