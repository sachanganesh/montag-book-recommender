from app import db

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True, unique=True)
	# email = db.Column(db.String(60), index=True, unique=True)
	# password_hash = db.Column(db.String(128))
	age = db.Column(db.Integer)
	location = db.Column(db.String(250))

	def __repr__(self):
		return "User {}".format(self.id)

	def __str__(self):
		return self.__repr__()


class Book(db.Model)
