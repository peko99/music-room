# Copyright 2021 Group 21 @ PI (120)


from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from api.core.database.database import Base


class Spotify(Base):
    __tablename__ = 'spotify'

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, auto_now_add=True)
    refresh_token = Column(String)
    access_token = Column(String)
    expires_in = Column(DateTime)
    token_type = Column(String)
