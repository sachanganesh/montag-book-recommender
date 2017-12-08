""" Montag Book Recommender """

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from string import ascii_uppercase
from app import models
from . import home

@home.route("/")
def index():
	return render_template("home/index.html")

@home.route("/book-lookup/<letter>")
@login_required
def book_lookup(letter="a"):
	letter = letter.upper()[0]
	books = models.Book.query.filter(models.Book.title.startswith(letter)).all()
	if books is not None:
		liked_isbns = []
		for rating in current_user.ratings:
			liked_isbns.append(rating.isbn)

		return render_template("home/lookup.html", letter=letter, books=books, liked_isbns=liked_isbns, ascii_upper=list(ascii_uppercase))
	else:
		flash("Please search for a valid book entry.")
		return redirect(url_for("home.book_lookup"))

@home.route("/book/<isbn>")
@login_required
def render_book(isbn):
	book = models.Book.query.filter_by(isbn=isbn).first()

	if book is not None:
		return render_template("home/book.html", book=book)
	else:
		flash("Book does not exist.")
		return redirect(url_for("home.book_lookup"))
