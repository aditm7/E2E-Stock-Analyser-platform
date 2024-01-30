from app import db,bcrypt

class StockData(db.Model):
    __tablename__ = 'market_data'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    ltp = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.Integer)
    value = db.Column(db.Float)
    no_of_trades = db.Column(db.Integer)
    symbol = db.Column(db.String(200))
