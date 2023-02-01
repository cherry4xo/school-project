from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from ...models import *
from .. import service


album_router = APIRouter()


@album_router.post('/', response_model=schemas.Album_get)
async def album_create(
    album: schemas.Album_create,
    tracks: List[int],
    artists: List[int],
):
    return await service.album_s.create(album, artists, tracks)

@album_router.get('/{album_id}', response_model=schemas.Album_get)
async def album_get(
    album_id: int
):
    return await service.album_s.get(id=album_id)

@album_router.put('/{album_id}', response_model=schemas.Album_get)
async def album_update(
    album_id: int,
    album: schemas.Album_update
):
    return await service.album_s.update(album, id=album_id)

@album_router.delete('/{album_id}', status_code=204)
async def album_delete(
    album_id: int
):
    return await service.album_s.delete(id=album_id)

