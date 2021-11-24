from dataclasses import dataclass, field, asdict

from ..Experiment import Experiment
from ..Device import Device

import pymongo


def _get_experiment_from_db_json(experiment_dict: dict) -> Experiment:
    return Experiment(**experiment_dict)


def _get_device_from_db_json(device_dict: dict) -> Device:
    return Device(**device_dict)


@dataclass
class Database:
    client: pymongo.MongoClient
    dbname: str
    db: pymongo.database.Database = field(init=False)
    experiment_collection: pymongo.collection.Collection = field(init=False)
    device_collection: pymongo.collection.Collection = field(init=False)

    def __post_init__(self):
        self.db = self.client[self.dbname]
        self.experiment_collection = self.db['experiments']
        self.device_collection = self.db['devices']

    def add_experiment(self, experiment: Experiment):
        self.experiment_collection.insert_one(asdict(experiment))

    def find_experiments(self, *args, **kwargs) -> tuple[Experiment]:
        experiments = self.experiment_collection.find(*args, **kwargs)
        return tuple(_get_experiment_from_db_json(e) for e in experiments)

    def find_experiment(self, *args, **kwargs):
        experiment = self.experiment_collection.find_one(*args, **kwargs)
        if experiment is not None:
            return _get_experiment_from_db_json(experiment)

    def add_device(self, device: Device):
        self.device_collection.insert_one(asdict(device))

    def find_device(self, *args, **kwargs):
        device = self.device_collection.find_one(*args, **kwargs)
        if device is not None:
            return _get_device_from_db_json(device)

    def find_devices(self, *args, **kwargs) -> tuple[Device]:
        devices = self.device_collection.find(*args, **kwargs)
        return tuple(_get_device_from_db_json(d) for d in devices)

    def disconnect(self):
        self.client.close()


def connect(db: str, *args, **kwargs):
    return Database(client=pymongo.MongoClient(*args, **kwargs), dbname=db)
