# Copyright 2021 Group 21 @ PI (120)


from typing import Any, Optional, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.crud import crud_user
from dependencies import get_db
from core.schemas import User, UserCreate, UserUpdate


router = APIRouter(
    prefix='/user',
    tags=['user'],
    dependencies=[Depends(get_db)]
)


@router.post('', response_model=User)
async def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    try:
        created_user = crud_user.create(obj_in=user_in, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return created_user


@router.get('', response_model=List[User])
async def get_users(
    db: Session = Depends(get_db)
) -> Any:
    return crud_user.get_all(db=db)


@router.delete('/{id_}', response_model=User)
async def delete_user(
    id_: int,
    db: Session = Depends(get_db)
) -> Any:
    user = crud_user.get(id_=id_, db=db)
    if not user:
        raise Exception('User not found!')
    
    return crud_user.delete(id_=id_, db=db)
