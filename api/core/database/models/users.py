# Copyright 2021 Group 21 @ PI (120)


from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from api.core.database.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    room_code = Column(String, unique=True)

    room = relationship('Room', back_populates='users')
