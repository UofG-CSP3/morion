from pathlib import Path
from typing import Callable

from pymongo.database import Database

from .mongomodel import MongoModel, BaseModel
from .filereader import read_file
from .config import setup_mongodb_from_file


def upload_file(filename: str, reader: Callable[[str], MongoModel] = None, upsert=False):
    mongo_model = read_file(filename, reader)
    if upsert:
        mongo_model.insert_or_replace()
    else:
        mongo_model.insert()

    return mongo_model


setup_mongodb_from_file(str(Path(__file__).with_name('config.ini')))
