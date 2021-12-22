# Copyright 2021 Group 21 @ PI (120)


import random
import string
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.core.crud import crud_room
from api.dependencies import get_db
from api.core.schemas import Room, RoomCreate, RoomUpdate


router = APIRouter(
    prefix='/room',
    tags=['room'],
    dependencies=[Depends(get_db)]
)


@router.post('', response_model=Room)
async def create_room(
    room_in: RoomCreate,
    db: Session = Depends(get_db)
) -> Any:
    if not room_in.code:
        room_in.code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    try:
        created_room = crud_room.create(obj_in=room_in, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return created_room


@router.get('', response_model=List[Room])
async def get_all_rooms(db: Session = Depends(get_db)) -> Any:
    return crud_room.get_all(db=db)


@router.get('/code/{code}', response_model=Room)
async def get_room_by_code(
    code: str,
    db: Session = Depends(get_db)
) -> Any:
    room = crud_room.get_by_code(code=code, db=db)
    if not room:
        raise HTTPException(
            status_code=404,
            detail='Room not found!'
        )
    
    return room


@router.get('/host-id/{host_id}', response_model=Room)
async def get_room_by_host_id(
    host_id: int,
    db: Session = Depends(get_db)
) -> Any:
    room = crud_room.get_by_host_id(host_id=host_id, db=db)
    if not room:
        raise HTTPException(
            status_code=404,
            detail='Room not found!'
        )
    
    return room


@router.put('/{code}', response_model=Room)
async def update_room(
    code: str,
    room_in: RoomUpdate,
    db: Session = Depends(get_db)
) -> Any:
    room = crud_room.get_by_code(code=code, db=db)
    if not room:
        raise HTTPException(
            status_code=404,
            detail='Room not found!'
        )
    
    try:
        updated_room = crud_room.update(db_obj=room, obj_in=room_in, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return updated_room


@router.delete('/{code}', response_model=Room)
async def delete_room(
    code: str,
    db: Session = Depends(get_db)
) -> Any:
    room = crud_room.get_by_code(code=code, db=db)
    if not room:
        raise HTTPException(
            status_code=404,
            detail='Room not found!'
        )
    
    return crud_room.delete(id_=room.code, db=db)
