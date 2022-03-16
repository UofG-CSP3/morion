from dataclasses import dataclass
from typing import Callable

from .mongomodel import MongoModel
from .errors import FunctionErrorPair, ReadError, ReadListError


@dataclass
class FileReader:
    reader: Callable[[str], MongoModel]
    use_when: Callable[[str], bool]
    priority: int


readers: list[FileReader] = []


def register_reader(use_when: Callable[[str], bool], priority: int = 1):
    """
    Function decorator to add a reader function to a known list of readers.

    :param use_when: A function which, given a filepath, returns a boolean stating whether this reader is applicable
    for the given file.
    :param priority: The priority of this reader. A higher priority means the reader takes precedence.
    """

    def register(f: Callable[[str], MongoModel]):
        nonlocal use_when, priority
        readers.append(FileReader(reader=f,
                                  use_when=use_when,
                                  priority=priority))

        return f

    return register


def filter_readers(filepath: str):
    return sorted([r for r in readers if r.use_when(filepath)], key=lambda r: r.priority, reverse=True)


def read_file(filepath: str, reader: Callable[[str], MongoModel] = None) -> MongoModel:
    if reader is not None:
        return reader(filepath)

    if len(readers) == 0:
        raise ReadError("No readers have been registered. Make sure that your readers have been imported.")

    filtered_readers = [fr.reader for fr in filter_readers(filepath)]

    if len(filtered_readers) == 0:
        raise ReadError("None of the registered readers say they can read this file. Make sure that the file path "
                        "given exists and the file is formatted correctly.")

    reader_errors: list[FunctionErrorPair] = []

    for reader in filtered_readers:
        try:
            return reader(filepath)
        except Exception as err:
            reader_errors.append(FunctionErrorPair(reader, err))

    raise ReadListError(reader_errors=reader_errors)
