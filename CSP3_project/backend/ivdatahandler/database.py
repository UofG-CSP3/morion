from pathlib import Path
from typing import Callable, Type, Iterable
from glob import glob

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
    :param upsert: [Optional] Replace existing documents in the database if they have the same id.
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
    :param upsert: [Optional] Replace existing documents in the database if they have the same id.
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

    return successful_uploads


def upload_directory(
        directory: str = './',
        upsert=False,
        ignore_duplicate_error=False,
        recursive=False,
        pattern='*'):
    """
    Upload files in a directory to the database.

    :param directory: [Optional] The root directory to upload. Defaults to the current working directory.
    :param upsert: [Optional] Replace existing documents in the database if they have the same id.
    :param ignore_duplicate_error: [Optional] If True, then the duplicate error that is raised when attempting to
    overwrite a document already in the database will be ignored.
    :param recursive: [Optional] Recurse through the subdirectories when uploading.
    :param pattern: [Optional] Glob pattern of file path.
    :return: The list of documents which were successfully uploaded to the database.
    """
    glob_pattern = (Path(directory) / pattern).as_posix()
    files = [f for f in glob(glob_pattern, recursive=recursive) if Path(f).is_file()]
    return upload_bulk(files, upsert=upsert, ignore_duplicate_error=ignore_duplicate_error)


def download(model_type: Type[MongoModel], filepath: str = '{id}.txt', query: dict = None, **kwargs) -> MongoModel:
    """
    Download a single document into a file from the database.

    Only the first document found that matches the given query would be downloaded.

    :param model_type: The specfic MongoModel type to look for
    :param filepath: [Optional] The path to download the document to. This can include curly braces to allow for formatting.
    If not specified, this will be "<id>.txt" where <id> is the id of the document.
    :param query: [Optional] The MongoDB query to find the document.
    :param kwargs: Key word arguments to use in the query.
    :return: The document that was downloaded.
    """
    model = model_type.find_one(query, **kwargs)

    if model is None:
        raise ValueError('No document with the given query could be found in the Database.')

    formatted_path = filepath.format(**model.__dict__)
    write_file(formatted_path, model)
    return model


def download_many(
        model_type: Type[MongoModel],
        directory: str = './',
        filepath: str = '{id}.txt',
        query: dict = None,
        group: list = None,
        **kwargs):
    """
    Download all documents from the database that match a given query..

    Only the first document found that matches the given query would be downloaded.

    :param model_type: The specfic MongoModel type to look for
    :param filepath: [Optional] The path to download the document to. This can include curly braces to allow for formatting.
    If not specified, this will be "<id>.txt" where <id> is the id of the document.
    :param query: [Optional] The MongoDB query to find the document.
    :param directory: [Optional] The directory to download the documents to.
    :param group: [Optional] Group documents into subdirectories based on their fields.
    :param kwargs: Key word arguments to use in the query.
    :return: List of documents that were downloaded.
    """
    if group is None:
        group = []

    def write_document(doc: MongoModel, write_dir: Path):
        path = str(write_dir / filepath).format(**doc.__dict__)
        write_file(path, doc)

    documents = model_type.find(query, **kwargs)
    document_path_map: dict[MongoModel, Path] = {doc: Path(directory) for doc in documents}

    for group in group:
        for doc in document_path_map:
            document_path_map[doc] = document_path_map[doc] / doc.__dict__[group]

    paths: set[Path] = set(path for path in document_path_map.values())
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)

    for doc, dir_path in document_path_map.items():
        write_document(doc, dir_path)

    return documents
