import sqlalchemy as sa
import pandas as pd
import numpy as np
import environ
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env()

con = sa.create_engine('postgresql://' + env('DB_USER') + ':' + env('DB_PASSWORD') + '@' + 'localhost/' + env('DB_NAME'))


# chunks = pd.read_csv('../../model/data/processed/ratings.csv', names=['id', 'user_id', 'book_id', 'rating'], chunksize=100000)
# for chunk in chunks:
# 	chunk.to_sql(name='server_rating', if_exists='replace', con=con, index=False)

chunks = pd.read_csv('../../model/data/processed/books.csv', header=None, skiprows=1, names=['null_id', 'id', 'isbn', 'title', 'author', 'pub_year', 'publisher', 'img_s', 'img_m', 'img_l'], usecols=['id', 'isbn', 'title', 'author', 'pub_year', 'publisher', 'img_s', 'img_m', 'img_l'], chunksize=100000)
for chunk in chunks:
	print(chunk[chunk['pub_year'].astype(str) == 'DK Publishing Inc']['title'].values)
	# chunk['pub_year'] = pd.to_numeric(chunk['pub_year'])

	# print(chunk['pub_year'].isnull().values.any())
	# print(chunk['pub_year'].dtype)
	# if False in chunk['pub_year'].apply(np.isreal).unique():
	# 	for yr in chunk['pub_year']:
	# 		if np.isreal(yr) == False:
	# 			print(yr, type(yr))

	# chunk.to_sql(name='server_book', if_exists='replace', con=con, index=False)
