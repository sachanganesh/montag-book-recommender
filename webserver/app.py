""" Montag Book Recommender """

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_word():
	return "Hello World!"
