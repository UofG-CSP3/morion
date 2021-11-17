from dataclasses import dataclass
from .Experiment import Experiment


@dataclass
class Device:
    _id: str
    type: str
    properties: dict[str, any]
    experiments: list[Experiment]
