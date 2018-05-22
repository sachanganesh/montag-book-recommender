from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import environ
import sqlalchemy as sa
import pandas as pd

class Command(BaseCommand):
	help = "Seeds the database with processed data for the recommender system"

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		# read the environment variables
		env = environ.Env(DEBUG=(bool, False))
		environ.Env.read_env(settings.BASE_DIR + '/montag/.env')

		con = self.connect_db(env)

		self.seed_books(settings.BASE_DIR + '/../../model/data/processed/books.csv', con)

		self.seed_ratings(settings.BASE_DIR + '/../../model/data/processed/ratings.csv', con)

		self.seed_recommender(con)

	# establish database connection
	def connect_db(self, env):
		try:
			con = sa.create_engine('postgresql://' + env('DB_USER') + ':' + env('DB_PASSWORD') + '@' + 'localhost/' + env('DB_NAME'))
		except:
			raise CommandError('Could not connect to database. Check environment vars and database validity')

		self.stdout.write(self.style.SUCCESS('Connected to db'))
		return con

	# read and add records from ratings.csv
	def seed_ratings(self, path, con):
		chunk_dfs = pd.read_csv(path, header=None, skiprows=1, names=['id', 'user_id', 'book_id', 'rating'], chunksize=100000)
		for df in chunk_dfs:
			try:
				df.to_sql(name='server_rating', if_exists='append', con=con, index=False)
			except:
				raise CommandError('Error in processing ratings table')

		self.stdout.write(self.style.SUCCESS('Seeded ratings table'))

	# read and add records from books.csv
	def seed_books(self, path, con):
		chunk_dfs = pd.read_csv(path, header=None, skiprows=1, names=['null_id', 'id', 'isbn', 'title', 'author', 'pub_year', 'publisher', 'img_s', 'img_m', 'img_l'], usecols=['id', 'isbn', 'title', 'author', 'pub_year', 'publisher', 'img_s', 'img_m', 'img_l'], chunksize=100000)
		for df in chunk_dfs:
			try:
				df.to_sql(name='server_book', if_exists='append', con=con, index=False)
			except:
				raise CommandError('Error in processing books table')

		self.stdout.write(self.style.SUCCESS('Seeded books table'))

	# save pickled model to model table
	def seed_recommender(self, con):
		call_command('trainrecommender')
		self.stdout.write(self.style.SUCCESS('Seeded recommenders table'))
