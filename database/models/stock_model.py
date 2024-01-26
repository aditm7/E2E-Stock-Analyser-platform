from app import db,bcrypt

class StockData(db.Model):
    __tablename__ = 'stock_data'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    ltp = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    value = Column(Float)
    no_of_trades = Column(Integer)
    symbol = Column(String)
