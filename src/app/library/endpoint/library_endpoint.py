from typing import List, Union
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from .. import models
from .. import service


library_router = APIRouter()


@library_router.get('/{library_id}', response_model=schemas.Library_get)
async def library_get(
    library_id: int,
):
    return await service.library_s.get(id=library_id)

@library_router.delete('/', status_code=204)
async def library_delete(
    library_id: int
):
    return await service.library_s.delete(id=library_id)