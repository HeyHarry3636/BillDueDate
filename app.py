# App.py (testing bucket list tutorial)

from flask import Flask, render_template, request, json, session, redirect
from flaskext.mysql import MySQL
import bcrypt

app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')
	
@app.route("/showSignUp")
def showSignUp():
	return render_template('signUp.html')
	
@app.route("/signUp", methods=["POST"])
def signUp():
	_email = request.form['inputName']
	_password = request.form['inputPassword']
	
	if _email and _password:
		return json.dumps({'html':'<span>All fields good!</span>'})
	else:
		return json.dumps({'html':'<span>Enter the required fields!</span>'})

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)












































