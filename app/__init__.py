# this file is necessary for distinguishing the project as 
# a package rather than a module (basically saying this is 
# a whole project)

from flask import Flask
from sqlalchemy import *

app = Flask(__name__)
app.config.from_object('config')

from app import views
