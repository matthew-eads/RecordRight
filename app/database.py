from sqlalchemy import *
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

import sys

engine = create_engine(SQLALCHEMY_DATABASE_URI)
# original way:
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Session = sessionmaker(bind=engine)
# session = Session()

Base = declarative_base()
# original way:
Base.query = session.query_property()

def init_db():
	import app.models
	sys.stderr.write('INTIALIZING session \n \n \n')
	# actually creates the session -- should only run this once
	Base.metadata.create_all(bind=engine)
	# Base.metadata.create_all(engine)