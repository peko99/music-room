# Copyright 2021 Group 21 @ PI (120)


from sqlalchemy.orm import Session

from api.core.crud.crud_base import CRUDBase
from api.core.database.models.users import User
from api.core.schemas.users import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_username(self, *, username: str, db: Session) -> User:
        return db.query(self.model).filter(self.model.username == username).first()


crud_user = CRUDUser(User)
