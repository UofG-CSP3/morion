from typing import Callable, TextIO

from ..Experiment import Experiment

_ParsingInputStrategy = Callable[[TextIO], Experiment]
_ParsingOutputStrategy = Callable[[Experiment], TextIO]
