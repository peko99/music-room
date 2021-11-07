# Copyright 2021 Group 21 @ PI (120)


from functools import lru_cache

from config import api, database


@lru_cache()
def get_api_config():
    return api.config


@lru_cache()
def get_database_config():
    return database.config
