# Copyright 2021 Group 21 @ PI (120)


from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship

from api.core.database.database import Base


class Room(Base):
    __tablename__ = 'rooms'

    code = Column(String, primary_key=True)
    host_id = Column(Integer, ForeignKey('users.id'))
    number_of_votes = Column(Integer)
    guests_can_pause = Column(Boolean)

    users = relationship('User', back_populates='room')
