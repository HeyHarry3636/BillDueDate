# App.py (testing bucket list tutorial)
<<<<<<< HEAD

### TESTING TESTBRANCH FOR GIT ###
### MORE TEST CHANGES MADE ON SERVER ###

=======
# changes to master
# changes to master#2
>>>>>>> master
from flask import Flask, render_template, json, session, redirect, url_for, flash, logging, request
from flaskext.mysql import MySQL
#from wtforms import Form, validators, PasswordField, StringField, BooleanField, SelectField, DateField
#from wtforms.fields.html5 import EmailField, DecimalField, DateField
from functools import wraps #Used for 'is_logged_in' var for dashboard
import bcrypt
import decimal
import datetime

import forms # Custom forms.py file
import globalVars  # Custom globalVars.py file

print("\n#################################################################################################")
print("#$%#$%#$%#$%#$%#$%#$%#$%#$%#$%             D    E    V              $%#$%#$%#$%#$%#$%#$%#$%#$%#$%")
print("#################################################################################################\n")

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
#runningTotal = 0.00
runningTotal = globalVars.cl_calculateRunningTotal(0.00)
# Create hasBankData class variable to let dashboard know if the user has bank information already
hasBankData = globalVars.cl_HasBankInformation(False)
# Create runningTotaldate so we can calculate when bills ARE
runningDate = globalVars.cl_calculateRunningDate(datetime.datetime(1970, 1, 1))
print("type(runningDate1) = " + str(type(runningDate)))
# runningDate.convertDatetimeToDate(runningDate)
# print("type(runningDate2) = " + str(type(runningDate)))


###############################################################################################
# Login/Registration methods
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
# Main dashboard method
@app.route('/dashboard')
@is_logged_in
def dashboard():

	try:
		if request.method == 'GET':
			_user_id = session.get('user_id')

			conn = mysql.connect()
			cursor = conn.cursor()

			# Check to see if there is already a bank account in the database
			cursor.execute('SELECT bank_nextPayDate FROM tbl_bank WHERE user_id = %s', (_user_id))
			payDay = cursor.fetchone()
			app.logger.info("payDay = " + str(payDay[0].date()))

			# Set initial payday date
			runningDate.setInitialDate(payDay[0])
			print("initial type " + str(type(runningDate.setInitialDate(payDay[0]))))

			# Create a list for future pay days
			payDayList = []
			payDayList.append(runningDate.getRunningDate())

			# Project out the next __ 20 __ paydays for now
			tempPayDay = runningDate.getRunningDate()
			for i in range(20):
				# in this case the next payday is 14 days/2 weeks after the initial payday
				tempPayDay = tempPayDay + datetime.timedelta(days=14)
				payDayList.append(tempPayDay)

			for i in range(0, len(payDayList)):
				app.logger.info("payDayList[" + str(i) + "] = " + str(payDayList[i]))


			# Get each bill for the user
			cursor.callproc('sp_getBillByUser', (_user_id,))
			billData = cursor.fetchall()

			# Parse data and convert to dictionary to return easily as JSON
			bill_dict_notSorted = []

			# billData is a list of tuples billData = ( (), (), () )
			for bill in billData:
				bill_item = {
					'bill_id': bill[0],
					'user_id': bill[1],
					'bill_name': bill[2],
					'bill_description': bill[3],
					# Set the bill amount to decimal.Decimal which is what the
					# running total class type is
					'bill_amount': decimal.Decimal(bill[4]),
					'bill_autoWithdrawal': bill[5],
					'bill_date': bill[6],
					'recur_id': bill[7],
					'bill_createdDate': bill[8],
					'bill_paid': bill[9]#,
				}
				bill_dict_notSorted.append(bill_item)

			# bill_dict is a list of dictionaries billData = ( { : }, { : }, { : } )
			# This function will sort the list by bill_date
			bill_dict = sorted(bill_dict_notSorted, key=lambda k: k['bill_date'])
			# Get bank details for the user,
			# if bankInfo does not exist, show 'addBank' button on dashboard
			cursor.callproc('sp_getBankByUser', (_user_id,))
			bankData = cursor.fetchall()

			# Pythonic way to check if a list is empty
			if not bankData:
				#List is empty
				hasBankData.setBankInformation(False)
				return render_template('dashboard.html', bill_dict=bill_dict, hasBankData=hasBankData.getBankInformation())
			else:
				#List has data
				hasBankData.setBankInformation(True)

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

					# Set the runningTotal to the current value of the bank account
					#runningTotal.setInitialAmount(50000)
					runningTotal.setInitialAmount(bank[2])

				# Calculate runningTotal after sorting by DATE
				# Append these results to an item named 'bill_runningTotal' that will be rendered in the dashboard.html
				#for li in bill_dict:
					#runningTotal.setRunningTotal(li['bill_amount'])
					#li['bill_runningTotal'] = runningTotal.getRunningTotal()
					#print("The bill running total is = " + str(runningTotal.getRunningTotal()))


				# Functional loop above

				# Create an index to track payDays steps
				payDayListIndex = 0

				for li in bill_dict:
					# if bill date is previous OR equal to the first payday (in payday list),
					# then subtract bill amount from running runningTotal
					print("li[bill_name] = " + str(li['bill_name']))
					#print("type(li['bill_date']) = " + str(type(li['bill_date'])))
					#print("type(payDayList[payDayListIndex]) = " + str(type(payDayList[payDayListIndex])))

					if li['bill_date'] <= payDayList[payDayListIndex].date():
						print("if loop")
						print("li['bill_date'] = " + str(li['bill_date']))
						print("payDayList[payDayListIndex] = " + str((payDayList[payDayListIndex]).date()))
						runningTotal.setRunningTotal(li['bill_amount'])

					#print("li = " + str(li))
					runningTotal.setRunningTotal(li['bill_amount'])
					li['bill_runningTotal'] = runningTotal.getRunningTotal()
					print("The bill running total is = " + str(runningTotal.getRunningTotal()))
					print("The running date is = " + str(runningDate.getRunningDate()))





				return render_template('dashboard.html', bill_dict=bill_dict, bank_dict=bank_dict, hasBankData=hasBankData.getBankInformation())

	# except Exception as e:
	# 	return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

###############################################################################################
# Bill Methods
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
# Bank Methods
@app.route('/addBank', methods=['GET', 'POST'])
@is_logged_in
def addBank():

	hasBank = hasBankData.getBankInformation()
	form = forms.BankForm(request.form)

	if request.method == 'GET':
		if hasBank == False:
			return render_template('addBank.html', form=form)
		elif hasBank == True:
			flash('You already have bank information entered', 'danger')
			app.logger.info("else"+str(hasBankData))
			return redirect(url_for('dashboard', form=form, hasBankData=hasBankData))
		else:
			flash('Error', 'danger')
			app.logger.info("else"+str(hasBankData))
			return redirect(url_for('dashboard', form=form, hasBankData=hasBankData))

	# return render_template('dashboard.html', form=form)

	try:
		if request.method == 'POST' and form.validate():
			# Get form data (using WTForms syntax)
			_user_id = session.get('user_id')
			_bank_currentAmount = form.bank_currentAmount.data
			_bank_payDayAmount = form.bank_payDayAmount.data
			_bank_nextPayDate = form.bank_nextPayDate.data
			_recur_id = form.recur_id.data

			# Create mysql connection, create cursor, call procedure, fetch results
			conn = mysql.connect()
			cursor = conn.cursor()

			# Check to see if there is already a bank account in the database
			bankInfoExists = cursor.execute('SELECT * FROM tbl_bank WHERE user_id = %s', (_user_id))

			# Only allowed to have one bank account in the system
			if bankInfoExists < 1:
				app.logger.info('YOU ARE ALLOWED TO ADD A BANK')
				cursor.callproc('sp_addBank', (
					_user_id,
					_bank_currentAmount,
					_bank_payDayAmount,
					_bank_nextPayDate,
					_recur_id
				))
				data = cursor.fetchall()

				# Return successful or error message to see if called_proc worked
				if len(data) is 0:
					conn.commit()
					flash('You have added the bank information!', 'success')
					return redirect(url_for('dashboard'))
				else:
					return render_template('error.html', error = str(data[0]))
			else:
				app.logger.info('You already have bank information in the database')
				return redirect(url_for('dashboard'))
		else:
			flash("Something is wrong", 'danger')
			return render_template('dashboard.html', form=form)

	except Exception as e:
		return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

@app.route('/updateBankInfo', methods=['GET', 'POST'])
@is_logged_in
def updateBankInfo():
	try:
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
		cursor.execute('UPDATE tbl_bank SET bank_currentAmount = %s, bank_payDayAmount = %s, bank_nextPayDate = %s WHERE bank_id = %s', (
			_bank_currentAmount, _bank_payDayAmount, _bank_nextPayDate, _bank_id[0]))
		bankInfo = cursor.fetchall()


		conn.commit()
		return json.dumps({'result' : 'success', 'bank_currentAmount' : _bank_currentAmount, 'bank_payDayAmount' : _bank_payDayAmount, 'bank_nextPayDate' : _bank_nextPayDate})

	except Exception as e:
		return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

@app.route('/updateBillAmounts', methods=['GET', 'POST'])
@is_logged_in
def updateBillAmounts():

	try:
		_user_id = session.get('user_id')

		conn = mysql.connect()
		cursor = conn.cursor()

		# Get each bill for the user
		cursor.callproc('sp_getBillByUser', (_user_id,))
		billData = cursor.fetchall()

		# Parse data and convert to dictionary to return easily as JSON
		bill_dict_notSorted = []

		# billData is a list of tuples billData = ( (), (), () )
		for bill in billData:
			bill_item = {
				'bill_id': bill[0],
				'user_id': bill[1],
				'bill_name': bill[2],
				'bill_description': bill[3],
				# Set the bill amount to decimal.Decimal which is what the
				# running total class type is
				'bill_amount': decimal.Decimal(bill[4]),
				'bill_autoWithdrawal': bill[5],
				'bill_date': bill[6],
				'recur_id': bill[7],
				'bill_createdDate': bill[8],
				'bill_paid': bill[9]#,
			}
			bill_dict_notSorted.append(bill_item)

		# bill_dict is a list of dictionaries billData = ( { : }, { : }, { : } )
		# This function will sort the list by bill_date
		bill_dict = sorted(bill_dict_notSorted, key=lambda k: k['bill_date'])

		for li in bill_dict:
			runningTotal.setRunningTotal(li['bill_amount'])
			li['bill_runningTotal'] = runningTotal.getRunningTotal()
			print("The bill running total is = " + str(runningTotal.getRunningTotal()))

		conn.commit()
		return json.dumps({'result' : 'success', 'billAmountList' : _billAmountList})

	#***************************** LOOK INTO JQUERY to updated

	except Exception as e:
		return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

###############################################################################################
# # PayDay Methods
# @app.route('/createPayDayList')
# @is_logged_in
# def createPayDayList():
# 	_user_id = session.get('user_id')
#
# 	# Create mysql connection, create cursor, call procedure, fetch results
# 	conn = mysql.connect()
# 	cursor = conn.cursor()
#
# 	# Check to see if there is already a bank account in the database
# 	cursor.execute('SELECT bank_nextPayDate FROM tbl_bank WHERE user_id = %s', (_user_id))
# 	payDay = cursor.fetchone()
#
# 	app.logger.info("payDay = " + str(payDay))
# 	# Returns: payDay = (datetime.datetime(2018, 12, 21, 0, 0),)
# 	app.logger.info("type(payDay) = " + str(type(payDay)))
# 	# Returns: payDay Type = <class 'tuple'>
#
# 	payDayStuff = payDay[0]
# 	app.logger.info("payDayStuff = " + str(payDayStuff))
# 	app.logger.info("type(payDayStuff) = " + str(type(payDayStuff)))
#
# 	payDay14 = payDayStuff + datetime.timedelta(days=14)
# 	app.logger.info("payDay14 = " + str(payDay14))
# 	app.logger.info("type(payDay14) = " + str(type(payDay14)))
#
# 	# Create a list for future pay days
# 	payDayList = []
# 	tempPayDay = payDayStuff
# 	payDayList.append(tempPayDay)
#
# 	for i in range(20):
# 		tempPayDay = tempPayDay + datetime.timedelta(days=14)
# 		payDayList.append(tempPayDay)
# 		print(tempPayDay)
#
# 	for i in range(0, len(payDayList)):
# 		app.logger.info("payDayList[" + str(i) + "] = " + str(payDayList[i]))
#
#
#
#
# 	return render_template('createPayDayList.html')


###############################################################################################



if __name__ == '__main__':
	# For running on server
	app.run(host='0.0.0.0', port=5000, debug=True)
