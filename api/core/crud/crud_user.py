# Copyright 2021 Group 21 @ PI (120)


from sqlalchemy.orm import Session

from api.core.crud.crud_base import CRUDBase
from api.core.database.models.users import User
from api.core.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_username(self, *, username: str, db: Session) -> User:
        return db.query(self.model).filter(self.model.username == username).first()

    def join_room(self, *, user_in: User, room_code: str, db: Session) -> User:
        user_in.room_code = room_code
        db.commit()
        return user_in
    
    def leave_room(self, *, user_in: User, db: Session) -> User:
        user_in.room_code = None
        db.commit()
        return user_in

crud_user = CRUDUser(User)
