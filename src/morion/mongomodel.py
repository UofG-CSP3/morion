"""
This module contains the class MongoModel,
that serves as the base model for all object types stored in the database.
"""
from __future__ import annotations
from typing import Any

from pydantic import Field, BaseModel as PydanticBaseModel, Extra
from pymongo.collection import Collection

from .config import database


def query_merge(query: dict, **kwargs: dict) -> dict:
    """
    Merge a dictionary and key word arguments into a single dictionary.

    Used to merge a MongoDB query and key word arguments into a single query.

    :param query: The dictionary to merge.
    :param kwargs: The key word arguments to merge.
    :return: A dictionary merging query and kwargs.
    """
    if query is None:
        return kwargs
    else:
        return {**query, **kwargs}


class BaseModel(PydanticBaseModel):
    """Base model allows for the use of field name when constructing."""

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True


class MongoModel(BaseModel):
    """
    Mongo model serves as the base model for all object types stored in the database.
    It implements common functionality for database inspection and modification.
    """
    # id by default is None, so that it would be set by the MongoDB database.
    id: Any = Field(default=None, title='The MongoDB primary key', alias='_id')

    class Config:
        extra = Extra.allow

    def __hash__(self):
        return hash(id)

    @classmethod
    def collection(cls) -> Collection:
        """Get the MongoDB Collection representing this model."""
        collection_name = cls.schema()['title']
        return database().get_collection(collection_name)

    @classmethod
    def find_one(cls, query: dict = None, with_validation: bool = True, **kwargs):
        """
        Get a single instance of this model from the MongoDB database that matches a given query.

        :param query: The MongoDB query.
        :param kwargs: Python key-word arguments to combine with the MongoDB query.
        :param with_validation: If True, will check whether the data matches the pydantic model.
        :return: A single instance of this model that matches the query. If there are no matches, then returns None.
        """
        model_dict = cls.collection().find_one(query_merge(query, **kwargs))
        if model_dict is not None:
            return cls.get_instance(model_dict, with_validation)

    @classmethod
    def find(cls, query: dict = None, with_validation: bool = True, **kwargs):
        """
        Get all instances of this model from the MongoDB database that match a given query.

        :param query: The MongoDB query.
        :param kwargs: Python key-word arguments to combine with the MongoDB query.
        :param with_validation: If True, will check whether the data matches the pydantic model.
        :return: A tuple containing all the instances of this model that match the query.
        """
        model_dicts = cls.collection().find(query_merge(query, **kwargs))
        return tuple(cls.get_instance(d, with_validation) for d in model_dicts)

    @classmethod
    def delete_one(cls, query: dict = None, **kwargs):
        """
        Delete a single instance of this model from the MongoDB database that matches a given a query.

        :param query: The MongoDB query.
        :param kwargs: Python key-word arguments to combine with the MongoDB query.
        """
        return cls.collection().delete_one(query_merge(query, **kwargs)).acknowledged

    @classmethod
    def delete_many(cls, query: dict = None, **kwargs):
        """
        Delete all instances of this model from the MongoDB database that match a given a query.

        :param query: The MongoDB query.
        :param kwargs: Python key-word arguments to combine with the MongoDB query.
        """
        return cls.collection().delete_many(query_merge(query, **kwargs)).acknowledged

    @classmethod
    def find_one_and_delete(cls, query: dict = None, with_validation: bool = True, **kwargs):
        """
        Find and delete one instance of this model in the MongoDB Database.

        :param query: The MongoDB query.
        :param kwargs: Python key-word arguments to combine with the MongoDB query.
        :param with_validation: If True, will check whether the data matches the pydantic model.
        """
        result = cls.collection().find_one_and_delete(query_merge(query, **kwargs))
        if result is not None:
            return cls.get_instance(result, with_validation)

    def insert(self):
        """Insert into the database."""

        inserted = self.collection().insert_one(to_mongo_dict(self))
        self.id = inserted.inserted_id
        return inserted.acknowledged

    def update(self):
        """Update this object in the database."""
        return self.collection().replace_one({'_id': self.id}, to_mongo_dict(self)).acknowledged

    def insert_or_update(self):
        """Either update this object or insert for the first time in the database."""
        if self.id is not None:
            replaced = self.collection().replace_one({'_id': self.id}, to_mongo_dict(self), upsert=True)
            return replaced.acknowledged
        else:
            return self.insert()

    def find_and_replace(self, query: dict = None, with_validation: bool = True, **kwargs):
        """
        Replace an instance in the database with this object. Return the replaced instance,

        :param query: The MongoDB query.
        :param kwargs: Python key-word arguments to combine with the MongoDB query.
        :param with_validation: If True, will check whether the data matches the pydantic model.
        :return: The model object that was replaced.
        """
        self.id = None
        replaced = self.collection().find_one_and_replace(query_merge(query, **kwargs), to_mongo_dict(self))
        if replaced:
            return type(self).get_instance(replaced, with_validation)

    def delete(self):
        """Delete this object from the database."""
        self.delete_one(_id=self.id)

    @classmethod
    def get_instance(cls, d: dict, with_validation: bool) -> MongoModel:
        """ Construct a model from a dictionary with or  without validation. """
        if with_validation:
            return cls(**d)
        else:
            d['id'] = d.pop('_id')
            return cls.construct(**d)


def to_mongo_dict(model: MongoModel) -> dict:
    """Convert a MongoModel to a dict that is ready to be inserted into a MongoDB database"""
    d = model.dict()
    object_id = d.pop('id')
    if object_id is not None:
        d['_id'] = object_id
    return d
