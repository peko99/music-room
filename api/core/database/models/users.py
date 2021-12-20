# Copyright 2021 Group 21 @ PI (120)


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.core.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    room_code = Column(String, ForeignKey('rooms.code'))

    room = relationship('Room', back_populates='users')
