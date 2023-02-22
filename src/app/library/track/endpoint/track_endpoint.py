from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from ..schemas import *
from .. import schemas
from .. import service
from ... import models


track_router = APIRouter()


@track_router.post('/', response_model=schemas.Track_get_creation)
async def track_create(
    track: schemas.Track = Depends(schemas.Track_create.as_form),
    artists: List[int] = Form(...),
    album: int = Form(None),
    genre: int = Form(None),
    picture_file: UploadFile = File(None),
    track_file: UploadFile = File(None)
):
    return await service.track_s.create(schema=track, artists=artists, album=album, genre=genre, picture_file=picture_file, track_file=track_file, duration_s=123)

@track_router.get('/{track_id}', response_model=schemas.Track_get)
async def track_get(
    track_id: int
):
    return await service.track_s.get(id=track_id)

@track_router.put('/', response_model=schemas.Track_update_get)
async def track_update(
    track_id: int,
    track: schemas.Track_update
):
    return await service.track_s.update(track, id=track_id)

@track_router.delete('/', status_code=204)
async def track_delete(
    track_id: int
):
    return await service.track_s.delete(id=track_id)
