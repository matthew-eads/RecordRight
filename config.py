# config.py

import os
basedir = os.path.abspath(os.path.dirname(__file__))

BOOTSTRAP_SERVE_LOCAL = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
WHOOSH_BASE = os.path.join(basedir, 'search.db')
SECRET_KEY = 'top secret'
URL = os.getenv("RRHOST", "localhost")
