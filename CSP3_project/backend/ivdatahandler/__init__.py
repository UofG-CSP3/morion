from typing import Callable

from pymongo.database import Database

from .mongomodel import MongoModel, BaseModel
from .filereader import read_file


def upload_file(db: Database, filename: str, reader: Callable[[str], MongoModel] = None, upsert=False):
    mongo_model = read_file(filename, reader)
    if upsert:
        mongo_model.insert_or_replace(db)
    else:
        mongo_model.insert(db)

    return mongo_model
