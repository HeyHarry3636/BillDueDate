# App.py (testing bucket list tutorial)

from flask import Flask, render_template, request, json, session, redirect, url_for, flash, logging
from flaskext.mysql import MySQL
from data import Bills
import bcrypt

app = Flask(__name__)

# Grab temp test data from data.py file
bill_dict = Bills()

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/tempData')
def tempData():
	return render_template('tempData.html', bills = bill_dict)

@app.route('/bills/<string:id>/')
def bills(id):
	return render_template('bills.html', id=id)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
