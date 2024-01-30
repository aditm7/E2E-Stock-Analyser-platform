from app import db,bcrypt

class CompanyData(db.Model):
    __tablename__ = 'company_data'  
    
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(200))
    industry = db.Column(db.String(200))
    symbol = db.Column(db.String(200))
    isin_code = db.Column(db.String(200))
