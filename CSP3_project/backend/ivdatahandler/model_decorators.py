from functools import wraps
from typing import Callable, Type

from pymongo.database import Database

from .mongomodel import MongoModel


def forward_link_one(model_get: Callable[[], Type[MongoModel]]):
    # TODO: Give the inner functions more meaningful names and potentially more explanation as to how they work.
    def decorator(func: Callable[[MongoModel], dict]):
        @wraps(func)
        def wrap(self, db: Database):
            return model_get().find_one(db, query=func(self))

        return wrap

    return decorator


def link_one(model: Type[MongoModel]):
    return forward_link_one(lambda: model)


def forward_link_many(model_get: Callable[[], Type[MongoModel]]):
    def decorator(func: Callable[[MongoModel], dict]):
        @wraps(func)
        def wrap(self, db: Database):
            return model_get().find(db, query=func(self))

        return wrap

    return decorator


def link_many(model: Type[MongoModel]):
    return forward_link_many(lambda: model)
