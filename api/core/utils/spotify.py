# Copyright 2021 Group 21 @ PI (120)


from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import timedelta, timezone, datetime
import requests
from api.config.configs import get_spotify_config

from api.core.crud import crud_spotify
from api.core.schemas import SpotifyUpdate, SpotifyCreate
from api.dependencies import get_db


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token, db: Session = Depends(get_db)):
    tokens = crud_spotify.get_user_tokens(user_id=session_id, db=db)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        token_in = SpotifyUpdate(
            id=tokens.id,
            user=session_id,
            token_type=token_type,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in
        )
        crud_spotify.update(db_obj=tokens, obj_in=token_in, db=db)
    else:
        tokens_in = SpotifyCreate(
            user=session_id,
            created_at=datetime.utcnow(),
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type=token_type
        )
        crud_spotify.create(obj_in=tokens_in, db=db)


def refresh_spotify_token(session_id, db: Session = Depends(get_db)):
    spotify_config = get_spotify_config()
    refresh_token = crud_spotify.get_user_tokens(user_id=session_id, db=db)

    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': spotify_config.client_id,
        'client_secret': spotify_config.client_secret,
    })

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token, db)
