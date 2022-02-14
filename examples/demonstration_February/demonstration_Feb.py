from backend.ivdatahandler.config import database
from backend.ivdatahandler import upload_directory


def clear_database():
    database().drop_collection('IV')
    database().drop_collection('Die')
    database().drop_collection('Wafer')


def upload_all():
    upload_directory('wafers', upsert=True)
    upload_directory('dies', upsert=True)
    upload_directory('ivs', upsert=True)

