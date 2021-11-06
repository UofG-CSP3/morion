from dataclasses import dataclass
from datetime import datetime


@dataclass
class Experiment:
    wafer: str
    die: str
    author: str
    timestamp: datetime
    meta: dict[str, any]
    readings: list[dict[str, any]]
