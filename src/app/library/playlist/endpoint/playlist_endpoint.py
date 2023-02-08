from typing import List
from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from ... import models
from .. import service 


playlist_router = APIRouter()


@playlist_router.post('/', response_model=schemas.Playlist_get_creation)
async def playlist_create(
    playlist: schemas.Playlist_create,
    tracks: List[int] = [],
    genres: List[int] = [],
    creator: int = None
):
    return await service.playlist_s.create(playlist, tracks, genres, creator)

@playlist_router.get('/{playlist_id}', response_model=schemas.Playlist_get)
async def playlist_get(
    playlist_id: int
):
    return await service.playlist_s.get(id=playlist_id)

@playlist_router.put('/update', response_model=schemas.Playlist)
async def playlist_update(
    playlist_id: int,
    playlist: schemas.Playlist_update
):
    return await service.playlist_s.update(playlist, id=playlist_id)

@playlist_router.delete('/', status_code=204)
async def playlist_delete(
    playlist_id: int
):
    return await service.playlist_s.delete(id=playlist_id)