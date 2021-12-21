# Copyright 2021 Group 21 @ PI (120)


from pydantic import BaseSettings


class SpotifyConfig(BaseSettings):
    client_id: str = ''
    client_secret: str = ''
    redirect_uri: str = ''

    class Config:
        env_prefix = 'spotify_'
        env_file = '.env'
    
config = SpotifyConfig()
