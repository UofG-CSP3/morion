from dataclasses import dataclass


@dataclass
class Experiment:
    wafer: str
    die: str
    author: str
    readings: list[dict[str, any]]
