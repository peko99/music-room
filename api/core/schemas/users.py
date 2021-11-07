# Copyright 2021 Group 21 @ PI (120)


from typing import Optional 
from pydantic import BaseModel


class UserBase(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]


class UserCreate(UserBase):
    username: str
    email: str
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
