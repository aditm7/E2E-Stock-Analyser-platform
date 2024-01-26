import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database/database.db')

Session = sessionmaker(bind=engine)
session = Session()

# Delete existing data if any
session.execute(text("DELETE FROM stock_data"))
session.commit()

#Insert the new stocks data
csv_files = [f for f in os.listdir('database/data') if f.endswith('.csv')]
for csv_file in csv_files:
  df = pd.read_csv(f'database/data/{csv_file}')
  df.to_sql('stock_data', con=engine, if_exists='append', index=False)

# commit the session
session.commit()