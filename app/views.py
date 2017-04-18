from __future__ import print_function
from app import app
from flask import render_template, redirect
from .forms import LoginForm
from wtforms import Form, validators
import logging


import sys


@app.route('/')
@app.route('/index')
def index():
	users = [ 
		{ 'name' : 'Matt Eads', 'DOB' : '04/38/27', 'hx' : 'History of great cardigans.'}, 
		{ 'name' : 'Robert Downey Jr', 'DOB' : '11/27/69', 'hx' : 'History of hyperextensible knees.'},
		{ 'name' : 'Sir Biddly-Bop III', 'DOB' : '3/3/33', 'hx' : 'History of fibromyalgia, smoking, GERD.'},
		]
	# print("Can I see this?", file=sys.stderr)
	return render_template('index.html', users=users)

@app.route('/patientdata/<path:user>')
def patient_data(user):
	sys.stderr.write("Can is SEE?")
	# this converts the user variable, which is a string, into a dict
	user = eval(user)
	return render_template('patient_data.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	sys.stderr.write("FORM IS %s \n" % form.is_remembered)
	sys.stderr.write("\n")
	if form.validate() and request.method == 'POST':
		flash('Login requested for User=%s, is_remembered=%s' % form.username.data, str(form.is_remembered.data))
		sys.stderr.write("AFTER FLASH \n")
		return redirect('/index')
	return render_template('login.html', title="SignIn", form=form)

