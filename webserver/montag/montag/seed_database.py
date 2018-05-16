import sqlalchemy as sa
import pandas as pd
import environ
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

con = sa.create_engine('postgresql://' + env('DB_USER') + ':' + env('DB_PASSWORD') + '@' + 'localhost/' + env('DB_NAME'))


chunks = pd.read_csv('../../model/data/processed/ratings.csv', chunksize=100000)
for chunk in chunks:
	chunk.to_sql(name='server_rating', if_exists='append', con=con)

chunks = pd.read_csv('../../model/data/processed/books.csv', chunksize=100000)
for chunk in chunks:
	chunk.to_sql(name='server_book', if_exists='append', con=con)
