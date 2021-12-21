# Copyright 2021 Group 21 @ PI (120)


from typing import Optional
from pydantic import BaseModel


class RoomBase(BaseModel):
    host_id: Optional[int]
    code: Optional[str]
    number_of_votes: Optional[int]
    guests_can_pause: Optional[bool]


class RoomCreate(RoomBase):
    number_of_votes: int


class RoomUpdate(RoomBase):
    pass


class Room(RoomBase):

    class Config:
        orm_mode = True
