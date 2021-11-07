# Copyright 2021 Group 21 @ PI (120)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.routers import user

api = FastAPI()

api.include_router(user.router)

origins = ['*']

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)

@api.get('/')
async def root ():
    return { 'status' : 'working' }
