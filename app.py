# App.py (testing bucket list tutorial)

from flask import Flask, render_template, json, session, redirect, url_for, flash, logging, request
from flaskext.mysql import MySQL
from data import Bills
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField
import bcrypt

app = Flask(__name__)

# Grab temp test data from data.py file
bill_dict = Bills()

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/mainBills')
def mainBills():
	return render_template('mainBills.html')

@app.route('/tempData')
def tempData():
	return render_template('tempData.html', bills = bill_dict)

@app.route('/bill/<string:id>/')
def bill(id):
	return render_template('bill.html', id=id)

class RegisterForm(Form):
	email = EmailField('Email', [
		validators.DataRequired(),
		validators.Email(message='Please enter a valid email address')
	])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password',[
		valdiators.DataRequired()
	])

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate:
		return render_template('register.html', form=form)
	return render_template('register.html', form=form)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
