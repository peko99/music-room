# Copyright 2021 Group 21 @ PI (120)


import spotipy
from spotipy.oauth2 import SpotifyOAuth
from fastapi import APIRouter

from api.config.configs import get_spotify_config


router = APIRouter(
    prefix='/spotify',
    tags=['spotify']
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
    return sp.current_playback()


@router.post('/skip')
async def skip_song():
    sp = get_spotify_auth()
    return sp.next_track()


@router.put('/play')
async def play_song():
    sp = get_spotify_auth()
    return sp.start_playback()


@router.put('/pause')
async def pause_song():
    sp = get_spotify_auth()
    return sp.pause_playback()
