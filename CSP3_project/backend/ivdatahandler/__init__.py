from pathlib import Path
from typing import Callable

from pymongo.database import Database

from .mongomodel import MongoModel, BaseModel
from .filereader import read_file
from .config import setup_mongodb_from_file
from .database import (
    upload_file, upload_bulk, upload_directory,
    download_one, download_many)

setup_mongodb_from_file(str(Path(__file__).with_name('config.ini')))
