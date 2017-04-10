# this file is necessary for distinguishing the project as 
# a package rather than a module (basically saying this is 
# a whole project)

from flask import Flask

app = Flask(__name__)
from app import views

