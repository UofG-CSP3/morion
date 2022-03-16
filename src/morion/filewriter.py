from dataclasses import dataclass
from typing import Callable, Type

from .errors import WriteError, FunctionErrorPair, WriteListError
from .mongomodel import MongoModel


@dataclass
class FileWriter:
    writer: Callable[[str], bool]
    use_when: Callable[[str], bool]
    model: Type[MongoModel]
    priority: int


writers: list[FileWriter] = []


def register_writer(model: Type[MongoModel], use_when: Callable[[str], bool], priority: int = 1):
    """
    Function decorator to add a writer function to a known list of writers.

    :param model: The type of MongoModel this writer is applicable to.
    :param use_when: A function which, given a filepath, returns a boolean stating whether this writer is applicable
    for the given file.
    :param priority: The priority of this writer. A higher priority means the writer takes precedence.
    """

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


def write_file(filepath: str, model: MongoModel, writer: Callable[[str, MongoModel], bool] = None) -> bool:
    if writer is not None:
        return writer(filepath, model)

    if len(writers) == 0:
        raise WriteError("No readers have been registered. Make sure that your readers have been imported.")

    filtered_writers = [fr.writer for fr in filter_writers(filepath, model)]

    if len(filtered_writers) == 0:
        raise WriteError("None of the registered writers say they can create a file for this model.")

    writer_errors: list[FunctionErrorPair] = []

    for writer in filtered_writers:
        try:
            return writer(filepath, model)
        except Exception as err:
            writer_errors.append(FunctionErrorPair(writer, err))

    raise WriteListError(writer_errors)
