from dataclasses import dataclass, field
from datetime import datetime


@dataclass(init=False)
class Experiment:
    _next_id = 0

    _id: int
    devices: list[str] # str is the type of Device._id
    author: str
    timestamp: datetime
    meta: dict[str, any]
    readings: list[dict[str, any]]

    def __init__(self, devices, author, timestamp, meta, readings, _id=None):
        if _id is None:
            self._id = Experiment._next_id
            Experiment._next_id += 1
        else:
            self._id = _id

        self.devices = devices
        self.author = author
        self.timestamp = timestamp
        self.meta = meta
        self.readings = readings

        