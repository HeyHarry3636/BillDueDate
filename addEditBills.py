from flask import Flask, render_template, json, session, redirect, url_for, flash, logging, request
from flaskext.mysql import MySQL

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
