# Copyright 2021 Group 21 @ PI (120)


from typing import Optional
from pydantic import BaseModel


class RoomBase(BaseModel):
    host_id: Optional[int]
    number_of_votes: Optional[int]
    potential: Optional[str]


class RoomCreate(RoomBase):
    host_id: int
    number_of_votes: int


class RoomUpdate(RoomBase):
    pass


class Room(RoomBase):
    id: int

    class Config:
        orm_mode = True
