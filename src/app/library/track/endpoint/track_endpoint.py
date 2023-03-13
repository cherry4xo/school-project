from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from tortoise.contrib.fastapi import HTTPNotFoundError
from ..schemas import *
from .. import schemas
from .. import service
from ... import models


track_router = APIRouter()


def artists_checker(artists: List[str] = Form(...)):
    if len(artists) == 1:
        artists = [item.strip() for item in artists[0].split(',')]

    return [artist for artist in artists]

@track_router.post('/', response_model=schemas.Track_get_creation)
async def track_create(
    track: schemas.Track = Depends(schemas.Track_create.as_form),
    track_params: schemas.Track_params = Depends(schemas.Track_params.as_form),
    artists: List[int] = Depends(artists_checker),
    album: int = Form(None),
    genre: int = Form(None),
    picture_file: UploadFile = File(None),
    track_file: UploadFile = File(None)
):
    return await service.track_s.create(schema=track, 
                                        track_params=track_params, 
                                        artists=artists, 
                                        album=album, 
                                        genre=genre, 
                                        picture_file=picture_file, 
                                        track_file=track_file, 
                                        duration_s=123)

@track_router.post('/update/track_params', status_code=204)
async def track_update_params(
    track_id: int,
    params: schemas.Track_params
):
    return await service.track_s.update_track_params(track_id=track_id, params=params)

@track_router.get('/track_params', response_model=schemas.Track_params)
async def track_get_params(
    track_id: int
):
    return await service.track_s.get_track_params(track_id=track_id)

@track_router.put('/update/data/picture/{track_id}')
async def track_change_picture(
    track_id: int = Depends(schemas.Track_change_picture.as_form),
    new_picture_file: UploadFile = File(...)
):
    return await service.track_s.change_picture(track_id, new_picture_file)

@track_router.delete('/delete/data/picture/{track_id}', status_code=204)
async def track_delete_picture(
    track_id: schemas.Track_change_picture = Depends(schemas.Track_change_picture.as_form)
):
    return await service.track_s.delete_picture(track_id)

@track_router.get('/get_picture/{track_id}', response_class=FileResponse, status_code=204)
async def track_get_picture(
    track_id: int
):
    return await service.track_s.get_image(id=track_id)

@track_router.get('/get_track_file/{track_id}', response_class=FileResponse, status_code=204)
async def track_get_file(
    track_id: int
):
    return await service.track_s.get_track_file(id=track_id)

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
