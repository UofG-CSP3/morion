"""
This module can be used to get methods to query files
"""
import pathlib


def filename_startswith(prefix: str):
    """
    Get a method to find files whose name start with a certain string
    :param prefix: The string that the filename has to start with
    :return: Method to find files whose name start with a certain string
    """
    def query(filepath: str):
        return pathlib.Path(filepath).name.startswith(prefix)

    return query


def file_extension(extension: str):
    """
    Get a method to find files with a specific extension
    :param extension: The string that the extension of the file will be
    :return: Method to find files with a specific extension
    """
    def query(filepath: str):
        return pathlib.Path(filepath).suffix == extension

    return query
