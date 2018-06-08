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
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	
	try:
		if _email and _password:
			# Create mysql connection, create cursor, call procedure, fetch results
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_createUser', (_email, _password))
			data = cursor.fetchall()
		
			# Return successful or error message to see if called_proc worked
			if len(data) is 0:
				conn.commit()
				return json.dumps({'message':'User created successfully!'})
			else:
				return json.dumps({'error':str(data[0])})
		else:
			return json.dumps({'html':'<span>Enter the required fields!</span>'})
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		if 'cursor' in locals():
			cursor.close()
		if 'conn' in locals():
			conn.close()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)












































