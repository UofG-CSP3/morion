from dataclasses import dataclass, field, asdict

import pymongo

from ..Experiment import Experiment


def _get_experiment_from_db_json(experiment_dict: dict) -> Experiment:
    del experiment_dict['_id']
    return Experiment(**experiment_dict)


@dataclass
class Database:
    client: pymongo.MongoClient
    dbname: str
    collection_name: str
    db: pymongo.database.Database = field(init=False)
    collection: pymongo.collection.Collection = field(init=False)

    def __post_init__(self):
        self.db = self.client[self.dbname]
        self.collection = self.db[self.collection_name]

    def add_experiment(self, experiment: Experiment):
        self.collection.insert_one(asdict(experiment))

    def find_experiments(self, query: dict) -> tuple[Experiment]:
        experiments = self.collection.find(query)
        return tuple(_get_experiment_from_db_json(e) for e in experiments)

    def find_experiment(self, query):
        experiment = self.collection.find_one(query)
        if experiment is not None:
            return _get_experiment_from_db_json(experiment)


def connect(db: str, collection: str, *args, **kwargs):
    return Database(client=pymongo.MongoClient(*args, **kwargs), dbname=db, collection_name=collection)
