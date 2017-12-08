""" Montag Book Recommender """

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from . import home

@home.route("/")
def index():
	return render_template("home/index.html")

@home.route("/protected")
@login_required
def protect():
	return "hey it's a secret!"
