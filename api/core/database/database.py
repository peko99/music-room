# Copyright 2021 Group 21 @ PI (120)


import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from config.configs import get_database_config


def get_database_url() -> str:
    '''Gets database URL based on environmental variables'''
    user = get_database_config().user
    password = get_database_config().password
    host = get_database_config().host
    database = get_database_config().database

    return f'postgresql://{user}:{password}@{host}/{database}'


def initialize_database(db_engine):
    if not database_exists(db_engine.url):
        logging.info('Creating database %s', db_engine.url.database)
        create_database(db_engine.url)
    

engine = create_engine(get_database_url())
initialize_database(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
