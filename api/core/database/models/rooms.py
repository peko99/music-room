# Copyright 2021 Group 21 @ PI (120)


from sqlalchemy import Column, Integer, String

from api.core.database.database import Base


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, unique=True)
    number_of_votes = Column(Integer)
    potential = Column(String)