from app import database
from app import models
import sys

reminder_id = sys.argv[1]
database.session.query(models.Reminder).filter(models.Reminder.id == reminder_id).delete()
database.session.commit()


