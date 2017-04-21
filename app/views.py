from __future__ import print_function
from app import app
from flask import render_template, redirect, request, flash
from .forms import *
from wtforms import Form, validators
from app.models import Patient
from database import session
import database
import logging


import sys


@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
	patients = Patient.query.all()
	form = SearchForm(request.form)
	if form.validate() and request.method == 'POST':
		results = Patient.search_query(form.keyword.data).
		return redirect(url_for('results', results=))
	return render_template('index.html', patients=patients, form = form)

@app.route('/patient_data/<path:id>')
def patient_data(id):
	# this converts the patient variable, which is a string, into a dict
	patient = session.query(Patient).filter(Patient.id == id).all()
	return render_template('patient_data.html', patient=patient)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	sys.stderr.write("FORM IS validated? %s \n" % form.validate())
	if form.validate() and request.method == 'POST':
		# flash('Login requested for patient=%s, is_remembered=%s' % (form.username.data, str(form.is_remembered.data)))
		return redirect('/index')
	return render_template('login.html', title="SignIn", form=form)

@app.route('/new_patient', methods=['GET', 'POST'])
def create_patient():
	form = NewPatientForm(request.form)
	if form.validate() and request.method == 'POST':
		new_patient = Patient(name = form.name.data, DOB = form.DOB.data, hx = form.hx.data)
		database.session.add(new_patient)
		database.session.commit()
		return redirect('/index')
	return render_template('new_patient.html', title="CreatePatient", form=form)

@app.route('/results', methods =['GET', 'POST'])
def show_results():
	return render_template('results.html', results=results)




