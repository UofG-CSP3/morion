import pathlib


def filename_startswith(prefix: str):
    def query(filepath: str):
        return pathlib.Path(filepath).name.startswith(prefix)

    return query


def file_extension(extension: str):
    def query(filepath: str):
        return pathlib.Path(filepath).suffix == extension

    return query
