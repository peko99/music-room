# Copyright 2021 Group 21 @ PI (120)


import pytest
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from typing import Generator

from api.core.database import get_database_url
from api import dependencies
from api.core.database.database import initialize_database, Base
from api.core import api


@pytest.fixture(scope='session')
def engine():
    engine = create_engine(get_database_url())
    initialize_database(engine)
    return engine


@pytest.fixture(scope='session')
def tables(engine) -> Generator:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db(engine, tables) -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db) -> Generator:
    with TestClient(api) as test_client:
        api.dependency_overrides[dependencies.get_db] = lambda: db
        yield test_client