# Copyright 2021 Group 21 @ PI (120)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api.core.routers import user, room, spotify

api = FastAPI()

api.include_router(user.router)
api.include_router(room.router)
api.include_router(spotify.router)

origins = ['*']

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)
api.add_middleware(SessionMiddleware, secret_key="token")

@api.get('/')
async def root ():
    return { 'status' : 'working' }
