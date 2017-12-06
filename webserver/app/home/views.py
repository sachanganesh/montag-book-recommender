""" Montag Book Recommender """

from flask import Flask, render_template

from . import home

@home.route("/")
def main():
	return render_template("home/index.html")

@home.route("/showSignUp")
def showSignUp():
    return render_template("home/signup.html")
