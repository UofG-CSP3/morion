from dataclasses import dataclass
from datetime import datetime


@dataclass
class Experiment:
    _next_id = 0

    _id: int
    devices: list[str] # str is the type of Device._id
    author: str
    timestamp: datetime
    meta: dict[str, any]
    readings: list[dict[str, any]]

    def __post_init__(self):
        self._id = Experiment._next_id
        Experiment._next_id += 1

        