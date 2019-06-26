# BillDueDate

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
import functions # Custom functions.py file

print("\n#################################################################################################")
print("#$%#$%#$%#$%#$%#$%#$%#$%#$%#$%             D    E    V              $%#$%#$%#$%#$%#$%#$%#$%#$%#$%")
print("#################################################################################################\n")

# Setup app and mysql instances
htmlFiles = "public_html"
app = Flask(__name__, template_folder=htmlFiles)
mysql = MySQL()
app.secret_key = 'Bills are due'

# Test user credentials
# U = test@test.com
# P = Test1234!

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'test'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Test1234!'
app.config['MYSQL_DATABASE_DB'] = 'BillDueDate'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initialize mysql app
mysql.init_app(app)

# Create hasBankData class variable to let dashboard know if the user has bank information already
hasBankData = globalVars.cl_HasBankInformation(False)

# Create payDayAmountInput class variable to obtain the inputted pay day amount
payDayAmountInput = globalVars.cl_calculatePayDayAmount(0.00)

# Create runningTotal value of the the currentBankAmount minus each bill amount plus payDays
runningTotal = globalVars.cl_calculateRunningTotal(0.00)

# Create runningTotaldate so we can calculate when bills ARE
runningDate = globalVars.cl_calculateRunningDate(datetime.datetime(1970, 1, 1))

# Create projectedMonths class variable to calculate number of months to display
projectMonths = globalVars.cl_projectedMonths(0)


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
			print("data = " + str(data))
			print("type(data) = " + str(type(data)))

			# if list is empty, user does not exist
			if not data:
				return render_template('login.html', error = 'Account does not exist.')
			# data[0][0] = 2  --> user_id
			# data[0][1] = "Test2@Test2.com" --> user_email
			# data[0][2] = "asdf1dsafsd" --> user_password hashed
			else:
				if len(data) > 0:
					if bcrypt.checkpw(_password.encode("utf-8"), data[0][2]):
						app.logger.info('PASSWORD MATCHED') #Logs to app.py console
						session['logged_in'] = True
						session['user_id'] = data[0][0]
						session['user_email'] = data[0][1]
						return redirect(url_for('dashboard'))
					else:
						return render_template('login.html', error = 'Wrong email address or password.')
				else:
					return render_template('login.html', error = 'Wrong email address or password.')

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
@app.route('/dashboard', methods=['GET', 'POST'])
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
			print("payDay = " + str(payDay))
			# print("payDay = " + str(payDay[0].date()))

			# Set initial payday date
			if not payDay:
				print("if not PayDay")
				#List is empty
				hasBankData.setBankInformation(False)
				return render_template('dashboard.html', hasBankData=hasBankData.getBankInformation())

			cursor.execute('SELECT bank_nextPayDate FROM tbl_bank WHERE user_id = %s', (_user_id))
			payDay = cursor.fetchone()
			#print("payDay2 = " + str(payDay))

			runningDate.setInitialDate(payDay[0])
			#print("initial type " + str(type(runningDate.setInitialDate(payDay[0]))))

			# Create a list for future pay days
			payDayList = []
			payDayList.append(runningDate.getRunningDate())

			# Project out the next __ 50 __ paydays for now
			tempPayDay = runningDate.getRunningDate()
			for i in range(50):
				# in this case the next payday is 14 days/2 weeks after the initial payday
				tempPayDay = tempPayDay + datetime.timedelta(days=14)
				payDayList.append(tempPayDay)

			# for i in range(0, len(payDayList)):
			# 	print("payDayList[" + str(i) + "] = " + str(payDayList[i]))

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
			print("type(bill_dict)" + str(type(bill_dict)))

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
						'bank_projectedMonths' : bank[5],
						'recur_id': bank[6],
						'bank_createdDate': bank[7]
					}
					shownMonths = bank[5]
					bank_dict.append(bank_item)

					# Set the runningTotal to the current value of the bank account
					#runningTotal.setInitialAmount(50000)
					runningTotal.setInitialAmount(bank[2])
					payDayAmountInput.setPayDayAmount(bank[3])

				# Duplicate bills that occur on recur_id basis
				# Ex: if you want to show the next three months of bills, duplicate the bill three times for the future months
				print("shownMonths = " + str(shownMonths))

				# Create new list that will only store the bills that the user wants to see (Ex: only want to see next 3 months)
				bill_dict_truncated = []
				counter = 0
				#Set initial date based on the first bill in the sorted bill List
				for li in bill_dict:
					#Set initial date based on the first bill in the sorted bill List
					# print("li = " + str(li))
					if counter == 0:
						initialBillDate = li['bill_date']
						# Set the limit for the number of bills that are viewable
						dateLimit = functions.addMonths(initialBillDate, shownMonths)
						print("dateLimit = " + str(dateLimit))
						print("type(dateLimit) = " + str(type(dateLimit)))

					if li['bill_date'] <= dateLimit:
						bill_dict_truncated.append(li)
						print(bill_dict_truncated)
						counter += 1





				# Create an index to track payDays steps
				payDayListIndex = 0

				# Calculate runningTotal after sorting by DATE
				# Append these results to an item named 'bill_runningTotal' that will be rendered in the dashboard.html
				# For each bill in the bill dictionary, calculate the running total bill amound along with
				# adding appropriate paydays based on the payday list created above
				for li in bill_dict:

					for x in range(0, len(payDayList)):
						print("li['bill_name'] = " + str(li['bill_name']))
						print("li['bill_date'] = " + str(li['bill_date']))

						# print("type(li['bill_date']) = " + str(type(li['bill_date'])))
						# print("type(payDayList[payDayListIndex].date()) = " + str(type(payDayList[payDayListIndex].date())))
						if li['bill_date'] <= datetime.date.today():
							print("BILL DATE COMES BEFORE TODAY/NOW")
						else:
							print("BILL DATE COMES __AFTER__ TODAY/NOW")

						# if bill date is previous OR equal to the first payday (in payday list),
						# then subtract bill amount from running runningTotal
						if li['bill_date'] <= payDayList[payDayListIndex].date():
							# set the new running total, which is based off the current running total minus the bill amount
							runningTotal.setRunningTotal(li['bill_amount'])
							break

						# These bills occur after the current payday (which is the first index in the paydaylist),
						# so increment to the next payDay in the list
						else:
							# The first bill that does not meet the criteria (has a bill after the current payday,
							# which is determined by the payday list created above) will increment the payday
							# index to the next date in the paydaylist list
							if li['bill_date'] <= payDayList[payDayListIndex+1].date():
								runningTotal.setRunningTotalAfterPayDayMultiple(li['bill_amount'], payDayAmountInput.getPayDayAmount(), x+1)
								runningTotal.setRunningTotal(li['bill_amount'])
								payDayListIndex += 1
								break
							else:
								payDayListIndex += 1

					li['bill_runningTotal'] = runningTotal.getRunningTotal()




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

@app.route('/billsPaidCheckboxes', methods=['GET', 'POST'])
@is_logged_in
def billsPaidCheckboxes():
	try:
		# _user_id = session.get('user_id')
		# _bank_currentAmount = request.form['bank_currentAmount']
		# _bank_payDayAmount = request.form['bank_payDayAmount']
		# _bank_nextPayDate = request.form['bank_nextPayDate']
		_user_id = session.get('user_id')

		_bill_id = request.form['bill_billId']
		_hasTheBillBeenPaid = request.form['bill_billPaid']

		print("\n")
		print("_bill_id = " + _bill_id)
		print("JS _hasTheBillBeenPaid = " + _hasTheBillBeenPaid)
		# print("type JS _hasTheBillBeenPaid = " + str(type(_hasTheBillBeenPaid)))

		conn = mysql.connect()
		cursor = conn.cursor()

		cursor.execute('SELECT * FROM tbl_bill WHERE user_id = %s AND bill_id = %s', (_user_id, _bill_id))
		_currentBill = cursor.fetchone()

		# conn = mysql.connect()
		# cursor = conn.cursor()
		# cursor.execute('SELECT * FROM tbl_bank WHERE user_id = %s', (_user_id))
		# _bank_id = cursor.fetchone()

		# Get current due date of active bill
		# bill_date at index[6] of _currentBill tuple
		print("bill_id _currentBill[0] = " + str(_currentBill[0]))
		print("user_id _currentBill[1] = " + str(_currentBill[1]))
		print("bill_name _currentBill[2] = " + str(_currentBill[2]))
		print("bill_description _currentBill[3] = " + str(_currentBill[3]))
		print("bill_amount _currentBill[4] = " + str(_currentBill[4]))
		print("bill_autoWithdrawal _currentBill[5] = " + str(_currentBill[5]))
		print("bill_date _currentBill[6] = " + str(_currentBill[6]))
		print("recur_id _currentBill[7] = " + str(_currentBill[7]))
		print("bill_createdDate _currentBill[8] = " + str(_currentBill[8]))
		print("bill_paid _currentBill[9] = " + str(_currentBill[9]))

		# if the checkbox has been selected for the 'bill_paid'
		# update the bill date to the next interval in the recurrence schedule
		if _hasTheBillBeenPaid == "true":
			print("hasTheBillBeenPaid bill_date _currentBill[6] = " + str(_currentBill[6]))
			#cursor.execute('UPDATE tbl_bill SET bill_date = %s WHERE bill_id = %s', ("2019-02-02", _bill_id))
			#newBillData = cursor.fetchone()

			#cursor.execute('SELECT * FROM tbl_bill WHERE user_id = %s AND bill_id = %s', (_user_id, _bill_id))
			#selectNewBillDate = cursor.fetchone()
			#print("NEW hasTheBillBeenPaid bill_date _currentBill[6] = " + str(selectNewBillDate[6]))

			# if month has a 'monthly' recurrence interval, then increment the bill_date by one month
			# _currentBill[7] = recur_id
			# recur_id (3) is the values for the monthly recurrence
			if _currentBill[7] == 3:
				newDateForBill = functions.addMonths(_currentBill[6], 1)

				print("newDateForBill = " + str(newDateForBill))
				cursor.execute('UPDATE tbl_bill SET bill_date = %s WHERE bill_id = %s', (newDateForBill, _bill_id))

		else:
			print("ERROR SETTING _hasTheBillBeenPaid to True/False")

		cursor.execute('SELECT * FROM tbl_bill WHERE user_id = %s AND bill_id = %s', (_user_id, _bill_id))
		_currentBillUpdated = cursor.fetchone()

		print("_currentBillUpdated[6] = " + str(_currentBillUpdated[6]))

		# cursor.execute('UPDATE tbl_bank SET bank_currentAmount = %s,
		# 										bank_payDayAmount = %s,
		#										bank_nextPayDate = %s
		# 								WHERE bank_id = %s', (
		# 										_bank_currentAmount,
		# 										_bank_payDayAmount,
		# 										_bank_nextPayDate,
		# 										_bank_id[0]))
		#
		# bankInfo = cursor.fetchall()
		#
		conn.commit()
		# return json.dumps({'result' : 'success',
		# 					'bank_currentAmount' : _bank_currentAmount,
		# 					'bank_payDayAmount' : _bank_payDayAmount,
		# 					'bank_nextPayDate' : _bank_nextPayDate})

		return json.dumps({'result' : 'success', "hasTheBillBeenPaid" : _hasTheBillBeenPaid })

	# except Exception as e:
	# 	return render_template('error.html', error = str(e))

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
		_bank_projectedMonths = request.form['bank_projectedMonths']
		#_recur_id = request.form['recur_id']

		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute('SELECT * FROM tbl_bank WHERE user_id = %s', (_user_id))
		_bank_id = cursor.fetchone()
		cursor.execute('UPDATE tbl_bank SET bank_currentAmount = %s, bank_payDayAmount = %s, bank_nextPayDate = %s, bank_projectedMonths = %s WHERE bank_id = %s', (
			_bank_currentAmount, _bank_payDayAmount, _bank_nextPayDate, _bank_projectedMonths, _bank_id[0]))
		bankInfo = cursor.fetchall()


		conn.commit()
		print(json.dumps({'result' : 'success', 'bank_currentAmount' : _bank_currentAmount, 'bank_payDayAmount' : _bank_payDayAmount, 'bank_nextPayDate' : _bank_nextPayDate, 'bank_projectedMonths' : _bank_projectedMonths}))
		return json.dumps({'result' : 'success', 'bank_currentAmount' : _bank_currentAmount, 'bank_payDayAmount' : _bank_payDayAmount, 'bank_nextPayDate' : _bank_nextPayDate, 'bank_projectedMonths' : _bank_projectedMonths})

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
# CONTACT
@app.route('/contact')
def contact():
	return render_template('contact.html')

###############################################################################################
# TESTING
@app.route('/testDynamicTable')
def testDynamicTable():
	return render_template('testDynamicTable.html')

# Set selectfield options of city based on the state
@app.route('/testSelectField', methods=['GET', 'POST'])
def testSelectField():
	try:
		formTest = forms.testForm()

		conn = mysql.connect()
		cursor = conn.cursor()

		cursor.execute('SELECT * FROM city WHERE state = "CA"')
		testReturn = cursor.fetchall()
		conn.commit()

		print(testReturn)

		# testReturn.city.choices = [(city.id, city.name) for city in City.query.filter_by(state='CA').all()]
		print("len(testReturn) = " + str(len(testReturn)))

		cityList = []

		for x in range(0, len(testReturn)):
			print("testReturn[" + str(x) + "][0] = " + str(testReturn[x][0]))
			print("testReturn[" + str(x) + "][1] = " + str(testReturn[x][1]))
			print("testReturn[" + str(x) + "][2] = " + str(testReturn[x][2]))

			cityList.append((testReturn[x][0], testReturn[x][2]))

		print("cityList = " + str(cityList))


		# formTest.city.choices = [(testReturn[0][0], testReturn[0][2]), (testReturn[1][0], testReturn[1][2])]
		formTest.city.choices = cityList


		if request.method == 'POST':
			cursor.execute('SELECT * FROM city WHERE id = %s', (formTest.city.data))
			city = cursor.fetchone()
			print("city = " + str(city))
			conn.commit()
			return '<h1>State: {}, City: {}</h1>'.format(formTest.state.data, formTest.city.data)


		return render_template('testSelectField.html', form=formTest)

	except Exception as e:
		return render_template('error.html', error = str(e))

	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

#Query database for all cities available for the state that is passed in
# then pass the cities back to whatever is calling this function
@app.route('/city/<state>')
def city(state):

	conn = mysql.connect()
	cursor = conn.cursor()

	cursor.execute('SELECT * FROM city WHERE state = %s', (state))
	cities = cursor.fetchall()
	conn.commit()

	print("citiesReturn = " + str(cities))

	cityArray = []

	for city in cities:
		#create new city object for each city (dictionary)
		print("cityInForLoop = " + str(city))
		print("cityType = " + str(type(city)))
		cityObj = {}
		cityObj['id'] = city[0]
		cityObj['name'] = city[2]
		cityArray.append(cityObj)

	# print(json.dumps({'cities' : cityArray}))
	return json.dumps({'cities' : cityArray})

###############################################################################################

# Main
if __name__ == '__main__':
	# For running on server
	#context = ('/etc/letsencrypt/live/billduedate.com/cert.pem', '/etc/letsencrypt/live/billduedate.com/privkey.pem')
	#app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=context)
	app.run(host='0.0.0.0', port=5000, debug=True)
