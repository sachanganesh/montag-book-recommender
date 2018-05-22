from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import environ
import random
import sqlalchemy as sa

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from lightfm import LightFM
import pickle

class Command(BaseCommand):
	help = 'Mine data and update the recommender model'

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		random.seed(17)

		# read the environment variables
		env = environ.Env(DEBUG=(bool, False))
		environ.Env.read_env(settings.BASE_DIR + '/montag/.env')

		con = self.connect_db(env)

		model_id, model = self.load_model(con)
		self.stdout.write(self.style.SUCCESS('Loaded model version {}'.format(str(model_id))))

		self.batch_train_model(model, con)

		model_id += 1
		self.save_model(model_id, model, con)
		self.stdout.write(self.style.SUCCESS('Stored model version {}'.format(str(model_id))))

	# establish database connection
	def connect_db(self, env):
		try:
			con = sa.create_engine('postgresql://' + env('DB_USER') + ':' + env('DB_PASSWORD') + '@' + 'localhost/' + env('DB_NAME'))
		except:
			raise CommandError('Could not connect to database. Check environment vars and database validity')

		self.stdout.write(self.style.SUCCESS('Connected to db'))
		return con

	def batch_train_model(self, model, con):
		max_user_id = -1
		max_book_id = -1

		batch_dfs = pd.read_sql(sql='server_rating', con=con, chunksize=100000)
		for df in batch_dfs:
			max_tmp_u = max(df['user_id'])
			max_tmp_b = max(df['book_id'])

			if max_tmp_u > max_user_id:
				max_user_id = max_tmp_u
			if max_tmp_b > max_book_id:
				max_book_id = max_tmp_b

		batch_dfs = pd.read_sql(sql='server_rating', con=con, chunksize=50000)
		for df in batch_dfs:
			sparse_matrix = coo_matrix((df['rating'], (df['user_id'], df['book_id'])), shape=(max_user_id + 1, max_book_id + 1), dtype=np.float32)

			try:
				model.fit_partial(sparse_matrix, epochs=5)
			except:
				raise CommandError('Error in batch-training recommender model')

		self.stdout.write(self.style.SUCCESS('Trained the recommender model'))

	def load_model(self, con):
		df = pd.read_sql(sql='SELECT * FROM server_recommender ORDER BY version DESC LIMIT 1', con=con)

		if df.shape[0] == 0:
			return -1, LightFM(loss='warp')

		return df['version'].values[0], pickle.loads(df['model'].values[0])

	def save_model(self, model_id, model, con):
		data = {
			'version': [model_id],
			'model': [pickle.dumps(model)]
		}

		df = pd.DataFrame(data=data)
		df.to_sql(name='server_recommender', if_exists='append', con=con, index=False)
