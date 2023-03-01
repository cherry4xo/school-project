from typing import List
from fastapi import APIRouter, Form, Depends, File, UploadFile
from fastapi.responses import FileResponse
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from ... import models
from .. import service 


playlist_router = APIRouter()


def tracks_checker(tracks: List[str] = Form(None)):
    if len(tracks) == 1:
        tracks = [item.strip() for item in tracks[0].split(',')]

    return [track for track in tracks]

def genres_checker(genres: List[str] = Form(None)):
    if len(genres) == 1:
        genres = [item.strip() for item in genres[0].split(',')]

    return [genre for genre in genres]


@playlist_router.post('/', response_model=schemas.Playlist_get_creation)
async def playlist_create(
    picture_file: UploadFile = File(...),
    playlist: schemas.Playlist_create = Depends(schemas.Playlist_create.as_form),
    tracks: List[int] = Depends(tracks_checker),
    genres: List[int] = Depends(genres_checker),
    creator: int = Form(...)
):
    return await service.playlist_s.create(picture_file, playlist, tracks, genres, creator)

@playlist_router.put('/update/data/{playlist_id}', response_model=schemas.Playlist_change_picture_response)
async def playlist_change_picture(
    picture_file: UploadFile = File(...),
    playlist_id: int = Depends(schemas.Playlist_change_picture.as_form)
):
    return await service.playlist_s.change_picture(playlist_id, picture_file)

@playlist_router.delete('/delete/data/{playlist_id}', status_code=204)
async def playlist_delete_picture(
    playlist_id: int = Depends(schemas.Playlist_change_picture.as_form)
):
    return await service.playlist_s.delete_picture(playlist_id)

@playlist_router.get('/get_picture/{playlist_id}', response_class=FileResponse)
async def playlist_get_picture(
    playlist_id: int
):
    return await service.playlist_s.get_image(id=playlist_id)

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

@playlist_router.post('/add_tracks', status_code=204)
async def playlist_add_tracks(
    playlist_id: int,
    tracks_id: List[int]
):
    return await service.playlist_s.add_tracks(playlist_id, tracks_id)

@playlist_router.post('/remove_tracks', status_code=204)
async def playlist_remove_tracks(
    playlist_id: int,
    tracks_id: List[int]
):
    return await service.playlist_s.remove_tracks(playlist_id, tracks_id)

@playlist_router.post('/add_genres', status_code=204)
async def playlist_add_genres(
    playlist_id: int,
    genres_id: List[int]
):
    return await service.playlist_s.add_tracks(playlist_id, genres_id)

@playlist_router.post('/remove_genres', status_code=204)
async def playlist_remove_genres(
    playlist_id: int,
    genres_id: List[int]
):
    return await service.playlist_s.remove_tracks(playlist_id, genres_id)