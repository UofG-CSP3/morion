from typing import Any

from pydantic import Field, BaseModel as PydanticBaseModel, Extra
from pymongo.collection import Collection

from .config import database


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

    def __hash__(self):
        return hash(id)

    @classmethod
    def collection(cls) -> Collection:
        collection_name = cls.schema()['title']
        return database().get_collection(collection_name)

    @classmethod
    def find_one(cls, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.find_one`"""
        model_dict = cls.collection().find_one(query_merge(query, **kwargs))
        if model_dict is not None:
            return cls(**model_dict)

    @classmethod
    def find(cls, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.find`"""
        model_dicts = cls.collection().find(query_merge(query, **kwargs))
        return tuple(cls(**d) for d in model_dicts)

    @classmethod
    def delete_one(cls, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.delete_one`"""
        return cls.collection().delete_one(query_merge(query, **kwargs))

    @classmethod
    def delete_many(cls, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.delete_many`"""
        return cls.collection().delete_many(query_merge(query, **kwargs))

    @classmethod
    def find_one_and_delete(cls, query: dict = None, **kwargs):
        """Wrapper around :func:`pymongo.collection.Collection.find_one_and_delete`"""
        result = cls.collection().find_one_and_delete(query_merge(query, **kwargs))
        if result is not None:
            return cls(**result)

    def insert(self):
        self.id = self.collection().insert_one(to_mongo_dict(self)).inserted_id

    def update(self):
        self.collection().replace_one({'_id': self.id}, to_mongo_dict(self))

    def insert_or_replace(self):
        if self.id is not None:
            self.id = self.collection().replace_one({'_id': self.id}, to_mongo_dict(self), upsert=True).upserted_id
        else:
            self.insert()

    def find_and_replace(self, query: dict = None, **kwargs):
        replaced = self.collection().find_one_and_replace(query_merge(query, **kwargs), to_mongo_dict(self))
        if replaced:
            return type(self)(**replaced)

    def delete(self):
        self.delete_one(_id=self.id)


def to_mongo_dict(model: MongoModel) -> dict:
    """Convert a MongoModel to a dict that is ready to be inserted into a MongoDB database"""
    d = model.dict()
    object_id = d.pop('id')
    if object_id is not None:
        d['_id'] = object_id
    return d
