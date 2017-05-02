# this file is necessary for distinguishing the project as 
# a package rather than a module (basically saying this is 
# a whole project)

from flask import Flask
from flask_bootstrap import Bootstrap
from sqlalchemy import *
#import whooshalchemy
#from app.models import Patient


app = Flask(__name__)

#whooshalchemy.whoosh_index(app, Patient)
# contains some paths necessary for db
app.config.from_object('config')
Bootstrap(app)

from app import views
