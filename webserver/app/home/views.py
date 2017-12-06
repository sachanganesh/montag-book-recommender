""" Montag Book Recommender """

from flask import Flask, render_template
from app import models

from . import home

@home.route("/")
def main():
	return render_template("home/index.html")

@home.route("/showSignUp")
def showSignUp():
    return render_template("home/signup.html")

@home.route("/users")
def show_users():
	res = ""
	for user in models.User.query.limit(5).all():
		res += "<p>" + str(user) + ", " + user.location + "</p>"

	return res

@home.route("/books")
def show_books():
	res = ""
	for book in models.Book.query.limit(5).all():
		res += "<p>" + str(book) + ", " + book.title + "</p>"

	return res

@home.route("/ratings")
def show_ratings():
	joined = models.Rating.query.join(models.Book, models.Rating.uid == models.Book.isbn)
	print(joined)

	res = ""
	for rating in joined.limit(5).all():
		res += "<p>" + rating.title + ", " + str(rating.rating) + "</p>"

	return res
