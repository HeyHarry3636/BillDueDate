# App.py (testing bucket list tutorial)

from flask import Flask, render_template, request, json, session, redirect
from flaskext.mysql import MySQL
import bcrypt

mysql = MySQL()
app = Flask(__name__)
# app.secret_key = 'Bills are due'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'test'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Test1234!'
app.config['MYSQL_DATABASE_DB'] = 'BillDueDate'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# Initialize mysql app
mysql.init_app(app)

@app.route("/")
def main():
	return render_template('index.html')
	
@app.route("/showSignUp")
def showSignUp():
	return render_template('signUp.html')
	
@app.route("/signUp", methods=["POST"])
def signUp():
	try:
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		
		if _email and _password:
		
			# Hash password using bcrypt
			_e_password = _password.encode("utf-8")
			_hashsalt_password = bcrypt.hashpw(_e_password, bcrypt.gensalt())
			
			# Create mysql connection, create cursor, call procedure, fetch results
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_createUser', (_email, _hashsalt_password))
			data = cursor.fetchall()
		
			# Return successful or error message to see if called_proc worked
			if len(data) is 0:
				conn.commit()
				return render_template('error.html', error = 'User created successfully!')
			else:
				return render_template('error.html', error = str(data[0]))

		else:
			return render_template('error.html', error = 'Enter the required fields!')

	except Exception as e:
		return json.dumps({'error':str(e)})
	
	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

@app.route("/showLogIn")
def showLogIn():
	return render_template('logIn.html')

@app.route("/logIn", methods=["POST"])
def logIn():
	try:
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']

		# Create mysql connection, create cursor, call procedure, fetch results
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_validateLogin', (_email,))
		data = cursor.fetchall()
		
		# data[0][0] = 2  --> user_id
		# data[0][1] = "Test2@Test2.com" --> user_email
		# data[0][2] = "asdf1dsafsd" --> user_password hashed
		
		return json.dumps({'error':str(data[0][0])})

		if len(data) > 0:
			if bcrypt.checkpw(_password.encode("utf-8"), data[0][2]):
				session['user'] = data[0][0]
				return redirect('/')
			else:
				return render_template('error.html', error = 'Wrong email address or password.')
		else:
			return render_template('error.html', error = 'Wrong email address or password.')
	
	except Exception as e:
		return json.dumps({'error':str(e)})
	
	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

			

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)












































