
from dataclasses import dataclass
from typing import Callable, Type

from .mongomodel import MongoModel


@dataclass
class FileWriter:
    # A instance of writer present in list to be used later, takes in filepath of
    writer: Callable[[str], bool]
    # A instance of knowing what type of database entry to download
    use_when: Callable[[str], bool]
    # A field for the model to which we would use the writer for
    model: Type[MongoModel]
    priority: int


writers: list[FileWriter] = []


def register_writer(model: Type[MongoModel], use_when: Callable[[str], bool], priority: int = 1):
    def register(w: Callable[[str], bool]):
        nonlocal model, use_when, priority
        writers.append(FileWriter(writer=w,
                                  model=model,
                                  use_when=use_when,
                                  priority=priority))

        return w

    return register


def filter_writers(filepath: str, model: MongoModel):
    return sorted([r for r in writers if r.use_when(filepath) and isinstance(model, r.model)],
                  key=lambda r: r.priority, reverse=True)


def write_file(filepath: str, model: MongoModel, writer: Callable[[str], bool] = None) -> bool:
    if writer is not None:
        return writer(filepath, model)

    filtered_writers = [fr.writer for fr in filter_writers(filepath, model)]


    for writer in filtered_writers:
        try:
            return writer(filepath, model)
        # TODO: The below except is FAR too broad.
        except Exception as err:
            # TODO: Maybe change this to log something instead of just silently ignoring it?
            pass

    raise ValueError("No writer could write this file.")
