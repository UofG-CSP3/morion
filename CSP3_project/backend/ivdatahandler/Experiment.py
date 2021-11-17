from dataclasses import dataclass
from datetime import datetime
from .Device import Device


@dataclass
class Experiment:
    _id: int
    devices: list[Device]
    author: str
    timestamp: datetime
    meta: dict[str, any]
    readings: list[dict[str, any]]
            
