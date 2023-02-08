from typing import List
from fastapi import APIRouter
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from ... import models
from .. import service


genre_router = APIRouter()


@genre_router.post('/', response_model=schemas.Genre_get_creation)
async def genre_create(
    genre: schemas.Genre_create,
):
    return await service.genre_s.create(genre)

@genre_router.get('/{genre_id}', response_model=schemas.Genre_get)
async def genre_get(
    genre_id: int
):
    return await service.genre_s.get(id=genre_id)

@genre_router.put('/update', response_model=schemas.Genre)
async def genre_update(
    genre_id: int,
    genre: schemas.Genre_update
):
    return await service.genre_s.update(genre, id=genre_id)

@genre_router.delete('', status_code=204)
async def genre_delete(
    genre_id: int
):
    return await service.genre_s.delete(id=genre_id)
