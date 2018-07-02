from wtforms import Form, validators, PasswordField, StringField, BooleanField, SelectField, DateField
from wtforms.fields.html5 import EmailField, DecimalField, DateField

class RegisterForm(Form):
	email = EmailField('Email', [
		validators.InputRequired(),
		validators.Email(message='Please enter a valid email address')
	])
	password = PasswordField('Password', [
		validators.InputRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')
	])
	confirm = PasswordField('Confirm Password', [
		validators.InputRequired()
	])

class BillForm(Form):
	bill_name = StringField('Name', [
		validators.InputRequired()
	])
	bill_description = StringField('Description')
	bill_amount = DecimalField('Amount', [
		validators.InputRequired()],
		default=0,
		places=2
	)
	bill_autoWithdrawal = BooleanField('Auto Withdrawal', [
		validators.Optional()
	])
	bill_date = DateField('Next Bill Due Date', [
		validators.InputRequired()]
		#format='%m-%d-%Y' This was not working with the format included
	)
	recur_id = SelectField('Recurrence Interval', [
		validators.InputRequired()],
		choices=[
			(3, 'Monthly'),
			(0, 'Annually'),
			(1, 'Bi-Annually'),
			(2, 'Quarterly'),
			(4, 'Bi-Monthly'),
			(5, 'Weekly'),
			(6, 'Custom')],
		coerce=int
	)

class BankForm(Form):
	bank_currentAmount = DecimalField('Current Bank Amount', [
		validators.InputRequired()],
		default=0,
		places=2
	)
	bank_payDayAmount = DecimalField('PayDay Amount', [
		validators.InputRequired()],
		default=0,
		places=2
	)
	recur_id = SelectField('PayDay Frequency', [
		validators.InputRequired()],
		choices=[
			(3, 'Monthly'),
			(0, 'Annually'),
			(1, 'Bi-Annually'),
			(2, 'Quarterly'),
			(4, 'Bi-Monthly'),
			(5, 'Weekly'),
			(6, 'Custom')],
		coerce=int
	)