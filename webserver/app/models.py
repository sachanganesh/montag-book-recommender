from app import db
from sqlalchemy.dialects.mysql import INTEGER

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.String(60), index=True, unique=True)
	password = db.Column(db.String(128))
	age = db.Column(db.Integer)
	location = db.Column(db.String(250))

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

	uid = db.Column(db.Integer, primary_key=True)
	isbn = db.Column(db.String(13), primary_key=True)
	rating = db.Column(db.Integer)

	def __repr__(self):
		return "Rating {}".format(self.isbn + ", " + str(self.uid))

	def __str__(self):
		return self.__repr__()
