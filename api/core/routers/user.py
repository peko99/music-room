# Copyright 2021 Group 21 @ PI (120)


from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.core.crud import crud_user, crud_room
from api.dependencies import get_db
from api.core.schemas import User, UserCreate, UserUpdate


router = APIRouter(
    prefix='/user',
    tags=['user'],
    dependencies=[Depends(get_db)]
)


@router.post('', response_model=User)
async def create_user(user_in: UserCreate, db: Session = Depends(get_db)) -> Any:
    try:
        created_user = crud_user.create(obj_in=user_in, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return created_user


@router.get('', response_model=List[User])
async def get_users(db: Session = Depends(get_db)) -> Any:
    return crud_user.get_all(db=db)


@router.get('/id', response_model=User)
async def get_user_by_id(
    id_: int,
    db: Session = Depends(get_db)
) -> Any:
    user = crud_user.get(id_=id_, db=db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found!'
        )

    return user


@router.put('/', response_model=User)
async def edit_user(
    user_in: UserUpdate,
    id_: int,
    db: Session = Depends(get_db)
) -> Any:
    user = crud_user.get(id_=id_, db=db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found!'
        )

    try:
        updated_user = crud_user.update(db_obj=user, obj_in=user_in, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return updated_user


@router.delete('/', response_model=User)
async def delete_user(id_: int, db: Session = Depends(get_db)) -> Any:
    user = crud_user.get(id_=id_, db=db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found!'
        )
    
    return crud_user.delete(id_=id_, db=db)


@router.put('/room-code/{code}', response_model=User)
async def join_room(
    code: str,
    id_: int,
    db: Session = Depends(get_db)
) -> Any:
    user = crud_user.get(id_=id_, db=db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found!'
        )

    room = crud_room.get_by_code(code=code, db=db)
    if not room:
        raise HTTPException(
            status_code=404,
            detail='Room not found!'
        )
    
    try:
        joined_user = crud_user.join_room(user_in=user, room_code=code, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return joined_user


@router.put('/leave-room', response_model=User)
async def leave_room(id_: int, db: Session = Depends(get_db)) -> Any:
    user = crud_user.get(id_=id_, db=db)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found!'
        )

    room = crud_room.get_by_code(code=user.room_code, db=db)
    if not room:
        raise HTTPException(
            status_code=404,
            detail='Room not found!'
        )
    
    try:
        updated_user = crud_user.leave_room(user_in=user, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return updated_user
    