from sqlalchemy import *
from config import SQLALCHEMY_DATABASE_URI
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db.query_property()

def init_db():
	import app.models
	Base.metadata.create_all(bind=engine)