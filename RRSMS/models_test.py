from sqlalchemy import Column, Integer, String
from database_test import Base

class Patient(Base):
    __tablename__ = 'patients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(Integer)
    birth_month = Column(Integer)
    birth_day = Column(Integer)
    phone_number = Column(String)
    def __init__(self, name=None, birth_year=None, birth_month=None, birth_day=None, phone_number=None):
        self.name = name
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.phone_number = phone_number
    
    def __repr__(self):
        return "{}, {}/{}/{}, #: {}".format(self.name, self.birth_month, self.birth_day, self.birth_year, self.phone_number)
