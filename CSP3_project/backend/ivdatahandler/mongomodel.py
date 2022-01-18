from typing import Any

from pydantic import Field, BaseModel as PydanticBaseModel, Extra
from pymongo.collection import Collection
from pymongo.database import Database


def query_merge(query: dict, **kwargs: dict) -> dict:
    if query is None:
        return kwargs
    else:
        return {**query, **kwargs}


class BaseModel(PydanticBaseModel):
    class Config:
        allow_population_by_field_name = True


class MongoModel(BaseModel):
    # id by default is None, so that it would be set by the MongoDB database.
    id: Any = Field(default=None, title='The MongoDB primary key', alias='_id')

    class Config:
        extra = Extra.allow

    @classmethod
    def collection(cls, db: Database) -> Collection:
        collection_name = cls.schema()['title']
        return db[collection_name]

    @classmethod
    def find_one(cls, db: Database, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.find_one`"""
        model_dict = cls.collection(db).find_one(query_merge(query, **kwargs))
        if model_dict is not None:
            return cls(**model_dict)

    @classmethod
    def find(cls, db: Database, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.find`"""
        model_dicts = cls.collection(db).find(query_merge(query, **kwargs))
        return tuple(cls(**d) for d in model_dicts)

    @classmethod
    def delete_one(cls, db: Database, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.delete_one`"""
        return cls.collection(db).delete_one(query_merge(query, **kwargs))

    @classmethod
    def delete_many(cls, db: Database, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.delete_many`"""
        return cls.collection(db).delete_many(query_merge(query, **kwargs))

    @classmethod
    def find_one_and_delete(cls, db: Database, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.find_one_and_delete`"""
        result = cls.collection(db).find_one_and_delete(query_merge(query, **kwargs))
        if result is not None:
            return cls(**result)

    def insert(self, db: Database):
        self.id = self.collection(db).insert_one(to_mongo_dict(self)).inserted_id

    def update(self, db: Database):
        self.collection(db).replace_one({'_id': self.id}, to_mongo_dict(self))

    def insert_or_replace(self, db: Database):
        if self.id is not None:
            self.id = self.collection(db).replace_one({'_id': self.id}, to_mongo_dict(self), upsert=True).upserted_id
        else:
            self.insert(db)

    def find_and_replace(self, db: Database, query: dict = None, **kwargs):
        replaced = self.collection(db).find_one_and_replace(query_merge(query, **kwargs), to_mongo_dict(self))
        if replaced:
            return type(self)(**replaced)

    def delete(self, db: Database):
        self.delete_one(db, _id=self.id)


def to_mongo_dict(model: MongoModel) -> dict:
    """Convert a MongoModel to a dict that is ready to be inserted into a MongoDB database"""
    d = model.dict()
    object_id = d.pop('id')
    if object_id is not None:
        d['_id'] = object_id
    return d
