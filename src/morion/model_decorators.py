"""
This module contains decorators that can be used in model implementation to relate them to each other.
For example, getting dies from a wafer.
"""
from functools import wraps
from typing import Callable, Type

from .mongomodel import MongoModel


def forward_link_one(model_get: Callable[[], Type[MongoModel]]):
    """
    Links to a single instance of another model type that is defined in the code after this model
    :param model_get: Method that returns the model name of the model that is not yet defined
    :return: Decorator that links to a single instance of another model type
    """
    def decorator(func: Callable[[MongoModel], dict]):
        @wraps(func)
        def wrap(self):
            return model_get().find_one(query=func(self))

        return wrap

    return decorator


def link_one(model: Type[MongoModel]):
    """
    Links to a single instance of another model type
    :param model: The model type to link to
    :return: Decorator that links to a single instance of another model type
    """
    return forward_link_one(lambda: model)


def forward_link_many(model_get: Callable[[], Type[MongoModel]]):
    """
    Links to multiple instances of another model type that is defined in the code after this model
    :param model_get: Method that returns the model name of the model that is not yet defined
    :return: Decorator that links to multiple instances of another model type
    """
    def decorator(func: Callable[[MongoModel], dict]):
        @wraps(func)
        def wrap(self):
            return model_get().find(query=func(self))

        return wrap

    return decorator


def link_many(model: Type[MongoModel]):
    """
    Links to multiple instances of another model type
    :param model: The model type to link to
    :return: Decorator that links to multiple instances of another model type
    """
    return forward_link_many(lambda: model)
