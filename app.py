# App.py (testing bucket list tutorial)

from flask import Flask, render_template, request, json, session, redirect
from flaskext.mysql import MySQL
import bcrypt

app = Flask(__name__)

@app.route("/")
def main():
	return render_template('index.html')
	
@app.route("showSignUp")
def showSignUp():
	return render_template('signUp.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)












































