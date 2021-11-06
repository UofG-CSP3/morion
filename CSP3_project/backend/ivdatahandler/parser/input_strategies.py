from typing import TextIO
from ..Experiment import Experiment
from datetime import datetime


def tab_strategy(data_in: TextIO) -> Experiment:
    # TODO: This is the strategy for the example files that Dima gave, there are almost certainly some mistakes.
    #       We should do a code review to iron them out.

    # TODO: Use a library to deal with tab delimited files. That should save us the bother of having to use
    #  .strip().split('\t') everywhere.

    wafer, die = data_in.readline().split('\t')[:2]
    comments = data_in.readline().strip()

    institution, author, timestamp_str = data_in.readline().strip().split('\t')
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H:%M")  # For example: 2021-03-29_13:07

    # TODO: I'm not really sure what this line in the experiment is supposed to be, we should ask Dima for more info.
    additional = [float(val) for val in data_in.readline().strip().split('\t')]

    fields = {index: field for index, field in enumerate(data_in.readline().strip().split('\t'))}
    # TODO: Converting all possible readings to floats seems silly. We should come up with a better way.
    readings = [{fields[i]: float(val) for i, val in enumerate(line.strip().split('\t'))} for line in data_in]

    return Experiment(
        wafer=wafer,
        die=die,
        author=author,
        timestamp=timestamp,
        meta={'comments': comments, 'additional': additional},
        readings=readings
    )
