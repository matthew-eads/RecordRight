from sqlalchemy import Column, Integer, String
from Server import app, db

class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    birth_year = db.Column(db.Integer)
    birth_month = db.Column(db.Integer)
    birth_day = db.Column(db.Integer)
    phone_number = db.Column(db.String)
    def __init__(self, name=None, birth_year=None, birth_month=None, birth_day=None, phone_number=None):
        self.name = name
        self.birth_year = birth_year
        self.birth_month = birth_month
        self.birth_day = birth_day
        self.phone_number = phone_number
    
    def __repr__(self):
        return "{}, {}/{}/{}, #: {}".format(self.name, self.birth_month, self.birth_day, self.birth_year, self.phone_number)