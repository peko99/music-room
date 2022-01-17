# Copyright 2021 Group 21 @ PI (120)


from typing import Optional 
from pydantic import BaseModel


class UserBase(BaseModel):
    id: Optional[int]
    room_code: Optional[str]


class UserCreate(UserBase):
    id: int


class UserUpdate(UserBase):
    pass


class User(UserBase):

    class Config:
        orm_mode = True
