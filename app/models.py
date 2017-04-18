from sqlalchemy import *
from app.database import Base
from config import WHOOSH_BASE
from whooshalchemy import IndexService
from database import db

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(8), index=True)
	password = Column(String(8))
	def __repr__(self):
		return '<User %r>'%(self.username)

class Patient(Base):
	__tablename__ = 'patients'
	__searchable__ = ['name']
	id = Column(Integer, primary_key=True)
	name = Column(String, index=True)
	DOB = Column(String, index=True)
	hx = Column(String, index=True)

	def __repr__(self):
		return '<Patient %r %r %r>'%(self.name, self.DOB, self.hx)

from app import app

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = True
    import whooshalchemy

config = {"WHOOSH_BASE": WHOOSH_BASE}

index_service = IndexService(config=config, session = db)
index_service.register_class(Patient)


# class Post(db.Model):
#     __searchable__ = ['body']

#     id = Column(Integer, primary_key=True)
#     body = Column(String(140))
#     timestamp = Column(DateTime)
#     user_id = Column(Integer, ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post %r>' % (self.body)

# if enable_search:
#     whooshalchemy.whoosh_index(app, Patient)