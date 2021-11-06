from typing import TextIO
from .ParsingStrategy import _ParsingInputStrategy
from ..Experiment import Experiment


def parse_stream(data_in: TextIO, parsing_fn: _ParsingInputStrategy) -> Experiment:
    experiment = parsing_fn(data_in)
    # TODO: Expand function to check experiment fields for correct type.
    #       Right now, we're just converting all readings to floating points, which may not be ideal.

    return experiment


def parse_file(filepath: str, parsing_fn: _ParsingInputStrategy) -> Experiment:
    with open(filepath, 'r') as f:
        return parse_stream(f, parsing_fn)
