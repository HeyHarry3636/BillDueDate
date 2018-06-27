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
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password', [
		validators.DataRequired()
	])

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm(request.form)

	# When the request method is 'GET', this statement will pull the register.html Form
	# and display it, use other 'POST' method above to process form data
	if request.method == 'GET':
		return render_template('register.html', form=form)

	try:
		# When the form data is submitted, a POST request will be made
		if request.method == 'POST' and form.validate():
			# Get form data (using WTForms syntax)
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
		else:
			flash("You've done something wrong', 'error'")
			return render_template('register.html', form=form)

	except Exception as e:
		return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():

	# When the request method is 'GET', this statement will pull the login.html Form
	# and display it, use other 'POST' method above to process form data
	if request.method == 'GET':
		return render_template('login.html')

	try:
		if request.method == 'POST':
			# Get forms from request (not using WTForms)
			_email = request.form['email']
			_password = request.form['password']

			# Create mysql connection, create cursor, call procedure, fetch results
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_validateLogin', (_email,))
			data = cursor.fetchall()

			# data[0][0] = 2  --> user_id
			# data[0][1] = "Test2@Test2.com" --> user_email
			# data[0][2] = "asdf1dsafsd" --> user_password hashed

			if len(data) > 0:
				if bcrypt.checkpw(_password.encode("utf-8"), data[0][2]):
					app.logger.info('PASSWORD MATCHED') #Logs to app.py console
					session['logged_in'] = True
					session['user'] = data[0][0]
					flash('You are now logged in', 'sucess')
					return redirect(url_for('userHome'))
				else:
					return render_template('login.html', error = 'Wrong email address or password.1')
			else:
				return render_template('login.html', error = 'Wrong email address or password.2')

	except Exception as e:
		return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

@app.route('/userHome')
def userHome():
	return render_template('userHome.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
