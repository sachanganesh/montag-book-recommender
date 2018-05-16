import sqlalchemy as sa
import pandas as pd

con = sa.create_engine('postgresql://localhost/montag')
chunks = pd.read_csv('ratings.csv', chunksize=100000)

for chunk in chunks:
	chunk.to_sql(name='table', if_exist='append', con=con)
