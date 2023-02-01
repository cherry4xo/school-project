from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from ... import models
from .. import service


artist_router = APIRouter()


@artist_router.post('/', response_model=schemas.Artist_get)
async def artist_create(
    artist: schemas.Artist_create,
    genres: List[int],
    albums: List[int],
    tracks: List[int]
):
    return await service.artist_s.create(artist, genres, albums, tracks)

@artist_router.get('/{artist_id}', response_model=schemas.Artist_get)
async def artist_get(
    artist_id: int
):
    return await service.artist_s.get(id=artist_id)

@artist_router.put('/update')
async def artist_update(
    artist_id: int,
    artist: schemas.Artist_update
):
    return await service.artist_s.update(artist, id=artist_id)

@artist_router.delete('/delete', response_model=schemas.Artist_delete)
async def artist_delete(
    artist_id: int
):
    return await service.artist_s.delete(id=artist_id)

@artist_router.get('/filter', response_model=List[schemas.Artist_get])
async def artist_filter_by_id(
    artists_id: List[int]
):
    return await service.artist_s.filter(id=artists_id)

@artist_router.get('/get_obj', response_model=schemas.getArtist)
async def artist_get_obj(
    artist_id: int
):
    return await service.artist_s.get_obj(id=artist_id)

