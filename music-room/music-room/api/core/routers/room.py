# Copyright 2021 Group 21 @ PI (120)


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
    try:
        created_room = crud_room.create(obj_in=room_in, db=db)
    except IntegrityError as error:
        db.rollback()
        raise Exception(error)
    else:
        return created_room


@router.get('', response_model=List[Room])
async def get_rooms(db: Session = Depends(get_db)) -> Any:
    return crud_room.get_all(db=db)


@router.get('/id/{id_}', response_model=Room)
async def get_room_by_id(
    id_: int,
    db: Session = Depends(get_db)
) -> Any:
    room = crud_room.get(id_=id_, db=db)
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


@router.put('/{id_}', response_model=Room)
async def update_room(
    id_: int,
    room_in: RoomUpdate,
    db: Session = Depends(get_db)
) -> Any:
    room = crud_room.get(id_=id_, db=db)
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


@router.delete('/{id_}', response_model=Room)
async def delete_room(
    id_: int,
    db: Session = Depends(get_db)
) -> Any:
    room = crud_room.get(id_=id_, db=db)
    if not room:
        raise HTTPException(
            status_code=404,
            detail='Room not found!'
        )
    
    return crud_room.delete(id_=id_, db=db)
