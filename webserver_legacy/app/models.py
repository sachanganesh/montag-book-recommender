from app import db
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import func, desc, select
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(60), index=True, unique=True)
	password = db.Column(db.String(128))
	age = db.Column(db.Integer)
	location = db.Column(db.String(250))
	authenticated = db.Column(db.Boolean, default=False)

	ratings = db.relationship("Rating")

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	@property
	def is_authenticated(self):
		"""Return True if the user is authenticated."""
		return self.authenticated

	@property
	def is_active(self):
		"""Always True, as all users are active."""
		return True

	@property
	def is_anonymous(self):
		"""Always False, as anonymous users aren't supported."""
		return False

	def get_id(self):
		"""Return the email address to satisfy Flask-Login's requirements."""
		return str(self.id)

	def __repr__(self):
		return "User {}".format(self.id)

	def __str__(self):
		return self.__repr__()

class Book(db.Model):
	__tablename__ = "books"

	isbn = db.Column(db.String(13), primary_key=True)
	title = db.Column(db.String(255))
	author = db.Column(db.String(255))
	year_of_pub = db.Column(INTEGER(unsigned=True))
	publisher = db.Column(db.String(255))
	img_url_s = db.Column(db.String(255))
	img_url_m = db.Column(db.String(255))
	img_url_l = db.Column(db.String(255))

	def __repr__(self):
		return "Book {}".format(self.isbn)

	def __str__(self):
		return self.__repr__()

class Rating(db.Model):
	__tablename__ = "ratings"

	uid = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
	isbn = db.Column(db.String(13), db.ForeignKey("books.isbn"), primary_key=True)
	rating = db.Column(db.Integer)

	def __repr__(self):
		return "Rating {}".format(self.isbn + ", " + str(self.uid))

	def __str__(self):
		return self.__repr__()

class Recommender(object):
	# def __init__(self):
	# 	with open("recsys/explicit_rec.pkl", "rb") as fid:
	# 		self.model = pickle.load(fid)

	def most_rated(self, n=3):
		queried_books = db.session.query(Rating.isbn, func.count(Rating.rating).label('qty')).group_by(Rating.isbn).order_by(desc('qty')).limit(n).all()
		books = []
		for book in queried_books:
			books.append(Book.query.get(book[0]))

		return books

	def top_average_rated(self, n=3):
		queried_books = db.session.query(Rating.isbn,
				func.count(Rating.rating).label('qty'),
				func.avg(Rating.rating).label('avg_rating')
				).group_by(Rating.isbn).order_by(desc('avg_rating'), desc('qty')).limit(n).all()

		books = []
		for book in queried_books:
			books.append(Book.query.get(book[0]))

		return books

	def top_rated(self, n=3):
		queried_books = db.session.query(Rating.isbn, Rating.rating.label('rating')).order_by(desc('rating')).limit(n).all()

		books = []
		for book in queried_books:
			books.append(Book.query.get(book[0]))

		return books

	def top_rated_isbns(self, n=3):
		queried_books = db.session.query(Rating.isbn, Rating.rating.label('rating')).order_by(desc('rating')).limit(n).all()

		books = []
		for book in queried_books:
			books.append(book[0])

		return books

	def recommend(self, n=3):
		queried_books = [b.isbn for b in db.session.query(Book.isbn)]
		queried_books = np.random.choice(queried_books, n, replace=False)

		books = []
		for isbn in queried_books:
			books.append(Book.query.get(isbn))

		return books
