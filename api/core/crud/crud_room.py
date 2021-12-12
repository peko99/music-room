# Copyright 2021 Group 21 @ PI (120)


from sqlalchemy.orm import Session

from api.core.crud.crud_base import CRUDBase
from api.core.database.models.rooms import Room
from api.core.schemas.rooms import RoomCreate, RoomUpdate


class CRUDRoom(CRUDBase[Room, RoomCreate, RoomUpdate]):

    def get_by_host_id(self, *, host_id: int, db: Session) -> Room:
        return db.query(self.model).filter(self.model.host_id == host_id).first()


crud_room = CRUDRoom(Room)
