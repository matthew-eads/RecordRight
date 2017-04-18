from sqlalchemy import *
from app.database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	username = Column(String(8), index=True)
	password = Column(String(8))

class Patient(Base):
	__tablename__ = 'patients'
	id = Column(Integer, primary_key=True)
	name = Column(String, index=True)
	DOB = Column(String, index=True)
	hx = Column(String, index=True)

