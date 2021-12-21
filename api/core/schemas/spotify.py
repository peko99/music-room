# Copyright 2021 Group 21 @ PI (120)


from typing import Optional
from pydantic import BaseModel


class SpotifyBase(BaseModel):
    user: Optional[str]
    created_at: Optional[str]
    refresh_token: Optional[str]
    access_token: Optional[str]
    expires_in: Optional[str]
    token_type: Optional[str]


class SpotifyCreate(SpotifyBase):
    id: Optional[int]
    user: str
    created_at: str
    refresh_token: str
    access_token: str
    expires_in: str
    token_type: str


class SpotifyUpdate(SpotifyBase):
    pass


class Spotify(SpotifyBase):
    id: int

    class Config:
        orm_mode = True
