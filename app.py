# App.py (testing bucket list tutorial)

from flask import Flask, render_template, json, session, redirect, url_for, flash, logging, request
from flaskext.mysql import MySQL
from data import Bills
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField
import bcrypt

# Setup app and mysql instances
app = Flask(__name__)
mysql = MySQL()
app.secret_key = 'Bills are due'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'test'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Test1234!'
app.config['MYSQL_DATABASE_DB'] = 'BillDueDate'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initialize mysql app
mysql.init_app(app)

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
		validators.DataRequired()
	])
	confirm = PasswordField('Confirm Password', [
		validators.DataRequired(),
		validators.EqualTo('password', message='Passwords do not match')
	])

@app.route('/register', methods=['GET', 'POST'])
def register():
	# try:
	form = RegisterForm(request.form)
	print(request.method)
	print(request.form)
	print(form.validate())
	
	if request.method == 'POST' and form.validate():

		_email = form.email.data
		_password = form.password.data

		# Hash password with bcrypt
		_e_password = _password.encode("utf-8")
		_hs_password = bcrypt.hashpw(_e_password, bcrypt.gensalt())

		# Create mysql connection, create cursor, call procedure, fetch results
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_createUser', (_email, _hs_password))
		data = cursor.fetchall()

		# Return successful or error message to see if called_proc worked
		if len(data) is 0:
			conn.commit()
			flash('You have signed up!', 'success')
			return redirect(url_for('login'))
		else:
			return render_template('error.html', error = str(data[0]))
	# else:
	# 	return render_template('error.html', error = "Enter the required fields!")

	# except Exception as e:
	# 	return render_template('error.html', error = str(e))
	#
	# finally:
	# 	if 'cursor' in locals():
	# 		cursor.close()
	# 	if 'conn' in locals():
	# 		conn.close()

@app.route('/login')
def login():
	return render_template('login.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
