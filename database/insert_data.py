import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

market_table_name="market_data"
company_table_name="company_data"

engine = create_engine('sqlite:///database/database.db')
Session = sessionmaker(bind=engine)
session = Session()

session.execute(text(f"DELETE FROM {market_table_name}"))
session.execute(text(f"DELETE FROM {company_table_name}"))
session.commit()

csv_files = [f for f in os.listdir('database/market_data') if f.endswith('.csv')]
for csv_file in csv_files:
  df = pd.read_csv(f'database/market_data/{csv_file}')
  df.to_sql(f'{market_table_name}', con=engine, if_exists='append', index=False)

df = pd.read_csv(f'database/company_data/ind_nifty50list.csv',usecols=['company','industry','symbol','isin_code'])
df.to_sql(f'{company_table_name}', con=engine, if_exists='append', index=False)

session.commit()