from dataclasses import dataclass
from typing import Callable

from .mongomodel import MongoModel


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

    filtered_readers = [fr.reader for fr in filter_readers(filepath)]

    for reader in filtered_readers:
        try:
            return reader(filepath)
        # TODO: The below except is FAR too broad.
        except Exception as err:
            # TODO: Maybe change this to log something instead of just silently ignoring it?
            pass

    raise ValueError("No reader could read this file.")
