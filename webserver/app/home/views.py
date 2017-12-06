""" Montag Book Recommender """

from flask import Flask, render_template
from app import models
from werkzeug import generate_password_hash, check_password_hash

from . import home

@home.route("/")
def main():
	return render_template("home/index.html")

@home.route("/showSignUp")
def showSignUp():
    return render_template("home/signup.html")

@home.route('/signUp',methods=['POST'])
def signUp(): 
        # read the posted values from the UI
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        # validate the received values
        if _name and _email and _password:
		_hashed_password = generate_password_hash(_password)
		    
@home.route('/showSignin')
def showSignin():
#       if session.get('user'):
#               return render_template('userHome.html')
#       else:
        return render_template('home/signin.html')

@home.route("/users")
def show_users():
	res = ""
	for user in models.User.query.limit(5).all():
		res += "<p>" + str(user) + ", " + user.location + "</p>"

	return res
