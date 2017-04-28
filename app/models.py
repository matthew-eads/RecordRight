from sqlalchemy import *
from app.database import Base
from config import WHOOSH_BASE
from whooshalchemy import IndexService
from database import session
from sqlalchemy.ext.mutable import MutableDict
import whooshalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text, DateTime
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker


class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(8), index=True)
	password = Column(String(8))
	def __repr__(self):
		return '<User %r>'%(self.username)

class Patient(Base):
	__tablename__ = 'patients'
	__searchable__ = ['name', 'DOB', 'hx', 'phone_number', 'address', 'past_visit_notes']
	id = Column(Integer, primary_key=True)
	name = Column(String, index=True)
	DOB = Column(String, index=True)
	hx = Column(String, index=True)
	phone_number = Column(String, index=True)
        address = Column(String, index=True)
        past_visit_notes = Column(MutableDict.as_mutable(PickleType))

	def __repr__(self):
		return '<Patient %r %r %r>'%(self.name, self.DOB, self.hx)


config = {"WHOOSH_BASE": WHOOSH_BASE}

index_service = IndexService(config=config, session = session)
index_service.register_class(Patient)
