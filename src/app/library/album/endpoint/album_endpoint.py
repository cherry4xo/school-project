from typing import List
from fastapi import APIRouter, HTTPException, Form, Depends, UploadFile, File
from fastapi.responses import FileResponse
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from ...models import *
from .. import service


album_router = APIRouter()


def genres_checker(genres: List[str] = Form(None)):
    if len(genres) == 1:
        genres = [item.strip() for item in genres[0].split(',')]

    return [genre for genre in genres]

def artists_checker(artists: List[str] = Form(None)):
    if len(artists) == 1:
        artists = [item.strip() for item in artists[0].split(',')]

    return [artist for artist in artists]

def tracks_checker(tracks: List[str] = Form(None)):
    if len(tracks) == 1:
        tracks = [item.strip() for item in tracks[0].split(',')]

    return [track for track in tracks]


@album_router.post('/', response_model=schemas.Album_get)
async def album_create(
    picture_file: UploadFile = File(...),
    album: schemas.Album_create = Depends(schemas.Album_create.as_form),
    tracks: List[int] = Depends(tracks_checker),
    artists: List[int] = Depends(artists_checker),
    genres: List[int] = Depends(genres_checker),
):
    return await service.album_s.create(album, artists, tracks, genres, picture_file)

@album_router.put('/update/data/{album_id}', response_model=schemas.Album_change_picture_response)
async def album_change_picture(
    picture_file: UploadFile = File(...),
    album_id: int = Depends(schemas.Album_change_picture.as_form),
):
    return await service.album_s.change_picture(album_id, picture_file)

@album_router.delete('/delete/data/{album_id}', status_code=204)
async def album_delete_picture(
    album_id: int = Depends(schemas.Album_change_picture.as_form)
):  
    return await service.album_s.delete_picture(album_id)

@album_router.get('/get_picture/{album_id}', response_class=FileResponse)
async def album_get_picture(
    album_id: int
):
    return await service.album_s.get_image(id=album_id)

@album_router.get('/{album_id}', response_model=schemas.Album_get)
async def album_get(
    album_id: int
):
    return await service.album_s.get(id=album_id)

@album_router.put('/{album_id}', response_model=schemas.Album)
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

@album_router.post('/add_tracks', status_code=204)
async def album_add_tracks(
    album_id: int, 
    tracks_id: List[int]
):
    return await service.album_s.add_tracks(album_id, tracks_id)

@album_router.post('/remove_tracks', status_code=204)
async def album_remove_tracks(
    album_id: int, 
    tracks_id: List[int]
):
    return await service.album_s.remove_tracks(album_id, tracks_id)

@album_router.post('/add_genres', status_code=204)
async def album_add_genres(
    album_id: int,
    genres_id: List[int]
):
    return await service.album_s.add_genres(album_id, genres_id)

@album_router.post('/remove_genres', status_code=204)
async def remove_add_genres(
    album_id: int,
    genres_id: List[int]
):
    return await service.album_s.remove_genres(album_id, genres_id)

