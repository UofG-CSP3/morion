from typing import TextIO
from datetime import datetime
import csv
from ..Experiment import Experiment
from .ParsingStrategy import _ParsingInputStrategy


def get_delim_strategy(delim: str) -> _ParsingInputStrategy:
    # TODO: This strategy is based on the example files that Dima gave, there are almost certainly some mistakes.
    #       We should do a code review to iron them out.

    def delim_strategy(data_in: TextIO) -> Experiment:
        reader = csv.reader(data_in, delimiter=delim)

        wafer, die, experiment_type = next(reader)
        comments = next(reader)

        institution, author, timestamp_str = next(reader)
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H:%M")  # For example: 2021-03-29_13:07

        # TODO: I'm not really sure what this line is supposed to be, we should ask Dima for more info.
        additional = [float(val) for val in next(reader)]

        fields = {index: field for index, field in enumerate(next(reader))}
        # TODO: Converting all possible readings to floats seems silly. We should come up with a better way.
        readings = [{fields[i]: float(val) for i, val in enumerate(line)} for line in reader]

        return Experiment(
            wafer=wafer,
            die=die,
            author=author,
            timestamp=timestamp,
            meta={'comments': comments, 'additional': additional, 'type': experiment_type},
            readings=readings
        )

    return delim_strategy


def tab_strategy(data_in: TextIO) -> Experiment:
    return get_delim_strategy(delim='\t')(data_in)
