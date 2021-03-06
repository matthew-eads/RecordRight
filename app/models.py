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
    is_admin = Column(Boolean, default=False)
    def __repr__(self):
        return '<User %r>'%(self.username)

class Patient(Base):
    __tablename__ = 'patients'
    __searchable__ = ['name']
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    DOB = Column(String, index=True)
    hx = Column(String, index=True)
    phone_number = Column(String, index=True)
    address = Column(String, index=True)
    past_visit_notes = Column(MutableDict.as_mutable(PickleType))
    patient_note=Column(String, index=True)
    def __repr__(self):
        return '<Patient %r %r %r %r %r %r>'%(self.name, self.DOB, self.hx, self.phone_number, self.address, self.past_visit_notes)

class Announcement(Base):
    __tablename__ = 'announcements'
    id = Column(Integer, primary_key = True)
    date = Column(String, index=True)
    name = Column(String, index=True)
    announcement = Column(String, index=True)
    severity = Column(String, index=True)
    user_id = Column(Integer)

    def __repr__(self):
        return '<Announcement %r %r %r>'%(self.name, self.announcement, self.severity)
class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key = True) 
    # 1 for single reminder, 2 for recurring reminder
    reminder_type = Column(Integer)
    patient_id = Column(Integer)
    message = Column(String)
    schedule = Column(String)
    end_on = Column(String)
    end_after = Column(Integer)
    cron_command = Column(String)
    at_id = Column(Integer)
    extra_at_id = Column(Integer) # sorry
    sched_file_prefix = Column(String) # ugh

config = {"WHOOSH_BASE": WHOOSH_BASE}

index_service = IndexService(config=config, session = session)
index_service.register_class(Patient)
