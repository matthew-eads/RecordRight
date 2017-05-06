from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
reminders = Table('reminders', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('reminder_type', Integer),
    Column('patient_id', Integer),
    Column('message', String),
    Column('schedule', String),
    Column('end_on', String),
    Column('end_after', Integer),
    Column('cron_command', String),
    Column('at_id', Integer),
    Column('extra_at_id', Integer),
    Column('sched_file_prefix', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['reminders'].columns['extra_at_id'].create()
    post_meta.tables['reminders'].columns['sched_file_prefix'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['reminders'].columns['extra_at_id'].drop()
    post_meta.tables['reminders'].columns['sched_file_prefix'].drop()
