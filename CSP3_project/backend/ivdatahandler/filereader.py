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
    def register(f: Callable[[str], MongoModel]):
        nonlocal use_when, priority
        readers.append(FileReader(reader=f,
                                  use_when=use_when,
                                  priority=priority))

        return f

    return register


def filter_readers(filename: str):
    return sorted([r for r in readers if r.use_when(filename)], key=lambda r: r.priority, reverse=True)


def read_file(filename: str, reader: Callable[[str], MongoModel] = None) -> MongoModel:
    if reader is not None:
        return reader(filename)

    filtered_readers = [fr.reader for fr in filter_readers(filename)]

    for reader in filtered_readers:
        try:
            return reader(filename)
        # TODO: The below except is FAR too broad.
        except Exception as err:
            # TODO: Maybe change this to log something instead of just silently ignoring it?
            pass

    raise ValueError("No reader could read this file.")
