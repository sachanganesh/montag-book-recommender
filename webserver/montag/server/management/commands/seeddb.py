from django.core.management.base import BaseCommand, CommandError
import environ
import sqlalchemy as sa
import pandas as pd

from django.conf import settings

class Command(BaseCommand):
	help = "Seeds the database with processed data for the recommender system"

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		# read the environment variables
		env = environ.Env(DEBUG=(bool, False))
		environ.Env.read_env(settings.BASE_DIR + '/montag/.env')

		# establish database connection
		try:
			con = sa.create_engine('postgresql://' + env('DB_USER') + ':' + env('DB_PASSWORD') + '@' + 'localhost/' + env('DB_NAME'))
		except:
			raise CommandError('Could not connect to database. Check environment vars and database validity')

		self.stdout.write(self.style.SUCCESS('Connected to db'))

		# read and add records from ratings.csv
		chunks = pd.read_csv(settings.BASE_DIR + '/../../model/data/processed/ratings.csv', header=None, skiprows=1, names=['id', 'user_id', 'book_id', 'rating'], chunksize=100000)
		for chunk in chunks:
			try:
				chunk.to_sql(name='server_rating', if_exists='append', con=con, index=False)
			except:
				raise CommandError('Error in processing ratings table')

		self.stdout.write(self.style.SUCCESS('Seeded ratings table'))

		# read and add records from books.csv
		chunks = pd.read_csv(settings.BASE_DIR + '/../../model/data/processed/books.csv', header=None, skiprows=1, names=['null_id', 'id', 'isbn', 'title', 'author', 'pub_year', 'publisher', 'img_s', 'img_m', 'img_l'], usecols=['id', 'isbn', 'title', 'author', 'pub_year', 'publisher', 'img_s', 'img_m', 'img_l'], chunksize=100000)
		for chunk in chunks:
			try:
				chunk.to_sql(name='server_book', if_exists='append', con=con, index=False)
			except:
				raise CommandError('Error in processing books table')

		self.stdout.write(self.style.SUCCESS('Seeded books table'))
