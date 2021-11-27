from typing import TextIO
from datetime import datetime
import csv
from ..Experiment import Experiment
from .ParsingStrategy import _ParsingInputStrategy
from .parse_config import read_header


def get_delim_strategy(delim: str) -> _ParsingInputStrategy:

    def delim_strategy(data_in: TextIO) -> Experiment:
        reader = csv.reader(data_in, delimiter=delim)
        header = read_header()

        experiment_dict = {}

        for i, heading, in enumerate(header):
            experiment_dict.update(dict(zip(heading, next(reader))))

        experiment_dict['timestamp'] = datetime.strptime(experiment_dict.pop('timestamp'), "%Y-%m-%d_%H:%M")

        fields = {index: field for index, field in enumerate(next(reader))}
        # TODO: Converting all possible readings to floats seems silly. We should come up with a better way.
        readings = [{fields[i]: float(val) for i, val in enumerate(line)} for line in reader]
        experiment_dict['readings'] = readings

        return Experiment(
            devices=[experiment_dict.pop('wafer'), experiment_dict.pop('die')],
            author=experiment_dict.pop('author'),
            timestamp=experiment_dict.pop('timestamp'),
            readings=experiment_dict.pop('readings'),
            meta=experiment_dict,
        )

    return delim_strategy


def tab_strategy(data_in: TextIO) -> Experiment:
    return get_delim_strategy(delim='\t')(data_in)
