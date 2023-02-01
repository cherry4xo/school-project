from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from .. import models
from .. import service


library_router = APIRouter()


@library_router.post('/', response_model=schemas.Library_get)
async def library_create(
    library: schemas.Library_create
):
    return await service.Library_s.create(library)

@library_router.get('/{library_id}', response_model=schemas.Library_get)
async def library_get(
    library_id: int,
):
    return await service.library_s.get(id=library_id)

@library_router.delete('/', response_model=schemas.Library_delete)
async def library_delete(
    library_id: int
):
    return await service.library_s.delete(id=library_id)

@library_router.get('/filter', response_model=List[schemas.Library_get])
async def library_filter_by_id(
    libraries_id: List[int]
):
    return await service.library_s.filter(id=libraries_id)

@library_router.get('/get_obj', response_model=schemas.Library_get)
async def library_get_obj(
    library_id: int
):
    return await service.library_s.get_obj(id=library_id)