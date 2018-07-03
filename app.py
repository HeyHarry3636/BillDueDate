# App.py (testing bucket list tutorial)

from flask import Flask, render_template, json, session, redirect, url_for, flash, logging, request
from flaskext.mysql import MySQL
#from wtforms import Form, validators, PasswordField, StringField, BooleanField, SelectField, DateField
#from wtforms.fields.html5 import EmailField, DecimalField, DateField
from functools import wraps #Used for 'is_logged_in' var for dashboard
import bcrypt

import forms # Custom forms.py file
import addEditBills # Custom addEditBills.py

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

# Create runningTotal value of the the currentBankAmount minus each bill amount plus payDays
runningTotal = 0.00
# Create variable to let dashboard know if the user has bank information already
hasBankData = True

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = forms.RegisterForm(request.form)

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
			flash("You've done something wrong", 'danger')
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
					session['user_id'] = data[0][0]
					session['user_email'] = data[0][1]
					return redirect(url_for('dashboard'))
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

# Check if user is logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Unauthorized, Please login', 'danger')
			return redirect(url_for('login'))
	return wrap

@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('You have logged out', 'success')
	return redirect(url_for('index'))

###############################################################################################

@app.route('/dashboard')
@is_logged_in
def dashboard():
	try:
		_user_id = session.get('user_id')

		conn = mysql.connect()
		cursor = conn.cursor()

		# Get each bill for the user
		cursor.callproc('sp_getBillByUser', (_user_id,))
		billData = cursor.fetchall()

		# Parse data and convert to dictionary to return easily as JSON
		bill_dict_notSorted = []
		for bill in billData:
			bill_item = {
				'bill_id': bill[0],
				'user_id': bill[1],
				'bill_name': bill[2],
				'bill_description': bill[3],
				# 'bill_amount': decimal.Decimal('12.3'),
				'bill_amount': str(bill[4]),
				'bill_autoWithdrawal': bill[5],
				'bill_date': bill[6],
				'recur_id': bill[7],
				'bill_createdDate': bill[8],
				'bill_paid': bill[9]
			}
			bill_dict_notSorted.append(bill_item)

		# bill_dict is a list of dictionaries
		# This function will sort the list by bill_date
		bill_dict = sorted(bill_dict_notSorted, key=lambda k: k['bill_date'])

		# Get bank details for the user,
		# if bankInfo does not exist, show 'addBank' button on dashboard
		cursor.callproc('sp_getBankByUser', (_user_id,))
		bankData = cursor.fetchall()


		if not all(bankData):
			app.logger.info("if not all(bankData): false")
		else:
			app.logger.info("if not all(bankData): true")

		if bankData is not None:
			app.logger.info("if bankData is not None: false")
		else:
			app.logger.info("if bankData is not None: true")


		# Pythonic way to check if a list is empty
		if not bankData:
			app.logger.info("if not bankData: false")
			#List is empty
			hasBankData = False
			return render_template('dashboard.html', bill_dict=bill_dict, hasBankData=hasBankData)
		else:
			app.logger.info("if not bankData: true")
			#List has data
			hasBankData = True

			# Parse data and convert to dictionary to return easily as JSON
			bank_dict = []
			for bank in bankData:
				bank_item = {
					'bank_id': bank[0],
					'user_id': bank[1],
					'bank_currentAmount': str(bank[2]),
					'bank_payDayAmount': str(bank[3]),
					'bank_nextPayDate': bank[4],
					'recur_id': bank[5],
					'bank_createdDate': bank[6]
				}
				bank_dict.append(bank_item)

			return render_template('dashboard.html', bill_dict=bill_dict, bank_dict=bank_dict, hasBankData=hasBankData)

	except Exception as e:
		return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

###############################################################################################

@app.route('/addBill', methods=['GET', 'POST'])
@is_logged_in
def addBill():
	form = forms.BillForm(request.form)

	if request.method == 'GET':
		return render_template('addBill.html', form=form)

	try:
		# When the form data is submitted, a POST request will be made
		if request.method == 'POST' and form.validate():
			# Get form data (using WTForms syntax)
			_user_id = session.get('user_id')
			_bill_name = form.bill_name.data
			_bill_description = form.bill_description.data
			_bill_amount = form.bill_amount.data
			_bill_autoWithdrawal = form.bill_autoWithdrawal.data
			_bill_date = form.bill_date.data
			_recur_id = form.recur_id.data

			# Covert the bill_autoWithdrawal BooleanField to a char True = 1, False == 0
			if _bill_autoWithdrawal:
				_bill_autoWithdrawal_char = 1
			else:
				_bill_autoWithdrawal_char = 0

			# Create mysql connection, create cursor, call procedure, fetch results
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_addBill', (
				_user_id,
				_bill_name,
				_bill_description,
				_bill_amount,
				_bill_autoWithdrawal_char,
				_bill_date,
				_recur_id
			))
			data = cursor.fetchall()

			# Return successful or error message to see if called_proc worked
			if len(data) is 0:
				conn.commit()
				flash('You have added a bill!', 'success')
				return redirect(url_for('dashboard'))
			else:
				return render_template('error.html', error = str(data[0]))
		else:
			flash("Something is wrong", 'danger')
			return render_template('addBill.html', form=form)

	except Exception as e:
		return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

@app.route('/editBill/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def editBill(id):
	try:
		_bill_id = id

		# Create connection, create cursor, call procedure, fetch results
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_getBillByBillID', (_bill_id,))
		data = cursor.fetchall()

		cursor.close()
		form = forms.BillForm(request.form)

		# app.logger.info("data[0][0] = " + str(data[0][0])) # bill_id
		# app.logger.info("data[0][1] = " + str(data[0][1])) # user_id
		# app.logger.info("data[0][2] = " + str(data[0][2])) # bill_name
		# app.logger.info("data[0][3] = " + str(data[0][3])) # bill_description
		# app.logger.info("data[0][4] = " + str(data[0][4])) # bill_amount
		# app.logger.info("data[0][5] = " + str(data[0][5])) # bill_autoWithdrawal
		# app.logger.info("data[0][6] = " + str(data[0][6])) # bill_date
		# app.logger.info("data[0][7] = " + str(data[0][7])) # recur_id
		# app.logger.info("data[0][8] = " + str(data[0][8])) # bill_createdDate
		# app.logger.info("data[0][9] = " + str(data[0][9])) # bill_paid

		# Populate bill form fields
		form.bill_name.data = data[0][2]
		form.bill_description.data = data[0][3]
		form.bill_amount.data = data[0][4]
		form.bill_autoWithdrawal.data = data[0][5]
		form.bill_date.data = data[0][6]
		form.recur_id.data = data[0][7]

	except Exception as e:
		return render_template('error.html', error = str(e))

	try:
		# When the form data is submitted, a POST request will be made
		if request.method == 'POST' and form.validate():
			try:
				# Get form data (using WTForms syntax)
				_user_id = session.get('user_id')
				_bill_name = request.form['bill_name']
				_bill_description = request.form['bill_description']
				_bill_amount = request.form['bill_amount']
				_bill_autoWithdrawal = request.form['bill_autoWithdrawal']
				_bill_date = request.form['bill_date']
				_recur_id = request.form['recur_id']

				# Covert the bill_autoWithdrawal BooleanField to a char True = 1, False == 0
				if _bill_autoWithdrawal:
					_bill_autoWithdrawal_char = 1
				else:
					_bill_autoWithdrawal_char = 0

				# Create cursor, call procedure, fetch results
				cursor = conn.cursor()
				cursor.callproc('sp_editBill', (
					_bill_id,
					_user_id,
					_bill_name,
					_bill_description,
					_bill_amount,
					_bill_autoWithdrawal_char,
					_bill_date,
					_recur_id
				))
				data = cursor.fetchall()

				# Return successful or error message to see if called_proc worked
				if len(data) is 0:
					conn.commit()
					flash('You have edited this bill!', 'success')
					return redirect(url_for('dashboard'))
				else:
					return render_template('error.html', error = str(data[0]))

			except Exception as e:
				return render_template('error.html', error = str(e))

			finally:
				if 'cursor' in locals():
					cursor.close()
				if 'conn' in locals():
					conn.close()

	except Exception as e:
		return render_template('error.html', error = str(e))

	return render_template('editBill.html', form=form)

@app.route('/deleteBill/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def deleteBill(id):
	try:
		_bill_id = id
		# Create connection, create cursor, call procedure, fetch results
		conn = mysql.connect()
		cursor = conn.cursor()
		# SQL DELETE FROM tbl_bill WHERE bill_id = _bill_id
		cursor.callproc('sp_deleteBillByBillID', (_bill_id,))
		data = cursor.fetchall()

		# Return successful or error message to see if called_proc worked
		if len(data) is 0:
			conn.commit()
			flash('You have deleted this bill!', 'success')
			return redirect(url_for('dashboard'))
		else:
			return render_template('error.html', error = str(data[0]))

	except Exception as e:
		return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

###############################################################################################

@app.route('/addBank', methods=['GET', 'POST'])
@is_logged_in
def addBank():

	form = forms.BankForm(request.form)

	if request.method == 'GET':
		if hasBankData == False:
			app.logger.info("if"+hasBankData)
			return render_template('addBank.html', form=form)
		else:
			flash('You already have bank information entered', 'danger')
			app.logger.info("else"+hasBankData)
			return redirect(url_for('dashboard', form=form, hasBankData=hasBankData))

	# try:
	# 	if request.method == 'POST' and form.validate():
	# 		# Change hasBankData to true
	# 		hasBankData = True

	# try:
	# 	if request.method == 'POST' and form.validate():
	# 		# Get form data (using WTForms syntax)
	# 		_user_id = session.get('user_id')
	# 		_bank_currentAmount = form.bank_currentAmount.data
	# 		_bank_payDayAmount = form.bank_payDayAmount.data
	# 		_recur_id = form.recur_id.data
	#
	# 		# Create mysql connection, create cursor, call procedure, fetch results
	# 		conn = mysql.connect()
	# 		cursor = conn.cursor()
	#
	# 		# Check to see if there is already a bank account in the database
	# 		bankInfoExists = cursor.execute('SELECT * FROM tbl_bank WHERE user_id = %s', (_user_id))
	#
	# 		# Only allowed to have one bank account in the system
	# 		if bankInfoExists < 1:
	# 			app.logger.info('YOU ARE ALLOWED TO ADD A BANK')
	# 			cursor.callproc('sp_addBank', (
	# 				_user_id,
	# 				_bill_currentAmount,
	# 				_bill_payDayAmount,
	# 				_recur_id
	# 			))
	# 			data = cursor.fetchall()
	#
	# 			# Return successful or error message to see if called_proc worked
	# 			if len(data) is 0:
	# 				conn.commit()
	# 				flash('You have added the bank information!', 'success')
	# 				return redirect(url_for('dashboard', hasBankData=hasBankData))
	# 			else:
	# 				return render_template('error.html', error = str(data[0]))
	# 		else:
	# 			app.logger.info('You already have bank information in the database')
	# 			return redirect(url_for('dashboard'))
	# 	else:
	# 		flash("Something is wrong", 'danger')
	# 		return render_template('dashboard.html', form=form)
	#
	# except Exception as e:
	# 	return render_template('error.html', error = str(e))
	#
	# finally:
	# 	if 'cursor' in locals():
	# 		cursor.close()
	# 	if 'conn' in locals():
	# 		conn.close()

	# return render_template('dashboard.html', form=form)

@app.route('/updateBankInfo', methods=['GET', 'POST'])
def updateBankInfo():

	#FUNCTIONAL!
	_user_id = session.get('user_id')
	_bank_currentAmount = request.form['bank_currentAmount']
	_bank_payDayAmount = request.form['bank_payDayAmount']
	_bank_nextPayDate = request.form['bank_nextPayDate']
	#_recur_id = request.form['recur_id']

	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM tbl_bank WHERE user_id = %s', (_user_id))
	_bank_id = cursor.fetchone()
	cursor.execute('UPDATE tbl_bank SET bank_currentAmount = %s, bank_payDayAmount = %s, bank_nextPayDate = %s WHERE bank_id = %s', (_bank_currentAmount, _bank_payDayAmount, _bank_nextPayDate, _bank_id[0]))
	bankInfo = cursor.fetchall()


	conn.commit()
	return json.dumps({'result' : 'success', 'bank_currentAmount' : _bank_currentAmount, 'bank_payDayAmount' : _bank_payDayAmount, 'bank_nextPayDate' : _bank_nextPayDate})

###############################################################################################






if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
