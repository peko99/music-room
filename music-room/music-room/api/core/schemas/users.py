# Copyright 2021 Group 21 @ PI (120)


import re
from typing import Optional 
from pydantic import BaseModel, validator


class UserBase(BaseModel):
    username: Optional[str]

    @validator('username')
    def username_form(cls, value_in):
        if not re.match(f'^[a-zA-Z0-9-_]+$', value_in):
            raise ValueError('Username has to use only alphanumeric symbols, hyphen and dash!')
        return value_in


class UserCreate(UserBase):
    username: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
