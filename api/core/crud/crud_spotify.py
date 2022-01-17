# Copyright 2021 Group 21 @ PI (120)


from sqlalchemy.orm import Session

from api.core.crud.crud_base import CRUDBase
from api.core.database.models.spotify import Spotify
from api.core.schemas.spotify import SpotifyCreate, SpotifyUpdate


class CRUDSpotify(CRUDBase[Spotify, SpotifyCreate, SpotifyUpdate]):

    def get_user_tokens(self, *, user_id: str, db: Session) -> Spotify:
        return db.query(self.model).filter(user=user_id).first()
    

crud_spotify = CRUDSpotify(Spotify)
