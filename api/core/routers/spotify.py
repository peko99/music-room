# Copyright 2021 Group 21 @ PI (120)


import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.config.configs import get_spotify_config
from api.dependencies import get_db
from api.core.crud import crud_room
from api.core.schemas import RoomUpdate


router = APIRouter(
    prefix='/spotify',
    tags=['spotify'],
    dependencies=[Depends(get_db)]
)


def get_spotify_auth():
    spotify_config = get_spotify_config()
    scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=scope,
        client_id=spotify_config.client_id,
        client_secret=spotify_config.client_secret,
        redirect_uri=spotify_config.redirect_uri
    ))
    return sp


@router.get('/current-song')
async def get_current_song():
    sp = get_spotify_auth()
    return sp.current_user_playing_track()


@router.post('/skip')
async def skip_song():
    sp = get_spotify_auth()
    sp.next_track()
# async def skip_song(room_code: str, song_id: str, db: Session = Depends(get_db)):
#     room = crud_room.get_by_code(code=room_code, db=db)
#     if room.song_id != song_id:
#         room_in = RoomUpdate
#         room_in.song_id = song_id
#         room_in.current_votes = 1
#         crud_room.update(db_obj=room, obj_in=room_in, db=db)
#         return 1
#     else:
#         if (room.current_votes + 1) == room.number_of_votes:
#             sp = get_spotify_auth()
#             sp.next_track()
#             room_in = RoomUpdate
#             room_in.current_votes = 0
#             crud_room.update(db_obj=room, obj_in=room_in, db=db)
#             return 0
#         else:
#             room_in = RoomUpdate
#             room_in.current_votes = room.current_votes + 1
#             crud_room.update(db_obj=room, obj_in=room_in, db=db)
#             return room.current_votes + 1
        

@router.put('/play')
async def play_song():
    sp = get_spotify_auth()
    return sp.start_playback()


@router.put('/pause')
async def pause_song():
    sp = get_spotify_auth()
    return sp.pause_playback()
