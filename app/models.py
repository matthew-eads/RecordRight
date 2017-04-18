from sqlalchemy import *
from app.database import Base

class User(Base):
	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	DOB = Column(String(8), index=True)
