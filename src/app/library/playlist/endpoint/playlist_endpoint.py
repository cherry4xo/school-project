from typing import List
from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from ... import models
from .. import service 


playlist_router = APIRouter()


@playlist_router.post('/', response_model=schemas.Playlist_get)
async def playlist_create(
    playlist: schemas.Playlist_create,
):
    return await service.playlist_s.create(playlist)

@playlist_router.get('/{playlist_id}', response_model=schemas.Playlist_get)
async def playlist_get(
    playlist_id: int 
):
    return await service.playlist_s.get(id=playlist_id)

@playlist_router.put('/update', response_model=schemas.Playlist_get)
async def playlist_update(
    playlist_id: int,
    playlist: schemas.Playlist_update
):
    return await service.playlist_s.update(playlist, id=playlist_id)

@playlist_router.delete('/', response_model=schemas.Playlist_delete)
async def playlist_delete(
    playlist_id: int
):
    return await service.playlist_s.delete(id=playlist_id)

@playlist_router.get('/', response_model=List[schemas.Playlist_get])
async def playlist_filter_by_id(
    playlists_id: List[int] 
):
    return await service.playlist_s.filter(id=playlists_id)

@playlist_router.get('/', response_model=schemas.getPlaylist)
async def playlist_get_obj(
    playlist_id: int
):
    return await service.playlist_s.get_obj(id=playlist_id)