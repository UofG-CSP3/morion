from dataclasses import dataclass, field
from datetime import datetime
from bson.objectid import ObjectId


@dataclass
class Experiment:

    devices: list[str] # str is the type of Device._id
    author: str
    timestamp: datetime
    meta: dict[str, any]
    readings: list[dict[str, any]]
    _id: ObjectId = None

        