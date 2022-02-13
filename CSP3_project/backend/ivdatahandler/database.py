from typing import Callable, Type, Iterable

import pymongo.errors as errors

from .mongomodel import MongoModel
from .filereader import read_file
from .filewriter import write_file


def upload_file(filepath: str, reader: Callable[[str], MongoModel] = None, upsert=False):
    """
    Upload a file containing a model document to the database.

    If the reader is not specified, it will be automatically deduced.

    :param filepath: The path to the file to upload.
    :param reader: [Optional] The reader to use to read the file. If not specified, it will be automatically deduced.
    :param upsert: If upsert is True, and a document with the same id already exists in the database,
    the file in this document will replace it.
    :return: The document that was uploaded to the database.
    """
    mongo_model = read_file(filepath, reader)
    if upsert:
        mongo_model.insert_or_replace()
    else:
        mongo_model.insert()

    return mongo_model


def upload_bulk(
        filepaths: Iterable[str],
        reader: Callable[[str], MongoModel] = None,
        upsert=False,
        ignore_duplicate_error=False):
    """
    Upload a list of files to the database.

    :param filepaths: List of files to upload.
    :param reader:  [Optional] The reader to use to read the files. If not specified, it will be automatically deduced.
    :param upsert: [Optional] If upsert is True, and a document with the same id already exists in the database,
    the file in this document will replace it.
    :param ignore_duplicate_error: [Optional] If True, then the duplicate error that is raised when attempting to
    overwrite a document already in the database will be ignored.
    :return: The list of documents which were successfully uploaded to the database.
    """
    successful_uploads = []
    for file in filepaths:
        try:
            document = upload_file(file, reader=reader, upsert=upsert)
            successful_uploads.append(document)
        except errors.DuplicateKeyError as err:
            if not ignore_duplicate_error:
                raise err


def download(model_type: Type[MongoModel], filepath: str, query: dict = None, **kwargs) -> MongoModel:
    """
    Download a single document into a file from the database.

    Only the first document found that matches the given query would be downloaded.

    :param model_type: The specfic MongoModel type to look for
    :param filepath: The path to download the document to.
    :param query: The MongoDB query to find the document.
    :param kwargs: Key word arguments to use in the query.
    :return: The model instance that was downloaded.
    """
    model = model_type.find_one(query, **kwargs)

    if model is None:
        raise ValueError('No document with the given query could be found in the Database.')

    write_file(filepath, model)
    return model
