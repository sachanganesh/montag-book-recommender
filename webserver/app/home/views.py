""" Montag Book Recommender """

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from string import ascii_uppercase
from app import models
from . import home

@home.route("/")
def index():
	return render_template("home/index.html")

@home.route("/protected")
@login_required
def protect():
	return "hey it's a secret!"

@home.route("/book-lookup/<letter>")
# @login_required
def book_lookup(letter):
	letter = letter.upper()[0]
	books = models.Book.query.filter(models.Book.title.startswith(letter)).all()
	return render_template("home/lookup.html", letter=letter, books=books, ascii_upper=list(ascii_uppercase))
