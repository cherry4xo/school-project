from typing import List, Optional
from fastapi import APIRouter, HTTPException, Form, File, Depends, UploadFile
from fastapi.responses import FileResponse
from tortoise.contrib.fastapi import HTTPNotFoundError
from .. import schemas
from ... import models
from .. import service


artist_router = APIRouter()


def albums_checker(albums: List[str] = Form(None)):
    if albums == '':
        return None
    if len(albums) == 1:
        albums = [item.strip() for item in albums[0].split(',')]

    return [album for album in albums]

def genres_checker(genres: List[str] = Form(None)):
    if genres == '':
        return None
    if len(genres) == 1:
        genres = [item.strip() for item in genres[0].split(',')]

    return [genre for genre in genres]

def tracks_checker(tracks: List[str] = Form(None)):
    if tracks == '':
        return None
    if len(tracks) == 1:
        tracks = [item.strip() for item in tracks[0].split(',')]
    
    return [track for track in tracks]


@artist_router.post('/', response_model=schemas.Artist_get_creation)
async def artist_create(
    picture_file: UploadFile = File(...),
    artist: schemas.Artist_create = Depends(schemas.Artist_create.as_form),
    genres: List[int] = Depends(genres_checker),
    albums: List[int] = Depends(albums_checker),
    tracks: List[int] = Depends(tracks_checker),
):
    return await service.artist_s.create(artist, genres, albums, tracks, picture_file)

@artist_router.put('/change/data/{artist_id}', response_model=schemas.Artist_change_picture_response)
async def artist_change_picture(
    artist_id: int = Depends(schemas.Artist_change_picture.as_form),
    new_picture_file: UploadFile = File(...)
):
    return await service.artist_s.change_picture(artist_id, new_picture_file)

@artist_router.delete('/change/data/{artist_id}', status_code=204)
async def artist_delete_picture(
    artist_id: int = Depends(schemas.Artist_change_picture.as_form)
):
    return await service.artist_s.delete_picture(artist_id)

@artist_router.get('/get_picture/{artist_id}', response_class=FileResponse)
async def artist_get_picture(
    artist_id: int
):
    return await service.artist_s.get_image(id=artist_id)

@artist_router.get('/{artist_id}', response_model=schemas.Artist_get)
async def artist_get(
    artist_id: int
):
    return await service.artist_s.get(id=artist_id)

@artist_router.put('/update', response_model=schemas.Artist)
async def artist_update(
    artist_id: int,
    artist: schemas.Artist_update
):
    return await service.artist_s.update(artist, id=artist_id)

@artist_router.delete('/delete', status_code=204)
async def artist_delete(
    artist_id: int
):
    return await service.artist_s.delete(id=artist_id)

@artist_router.post('/add_albums', status_code=204)
async def artist_add_albums(
    artist_id: int,
    albums_id: List[int]
):
    return await service.artist_s.add_albums(artist_id, albums_id)

@artist_router.post('/remove_albums', status_code=204)
async def artist_remove_albums(
    artist_id: int,
    albums_id: List[int]
):
    return await service.artist_s.remove_albums(artist_id, albums_id)

@artist_router.post('/add_tracks', status_code=204)
async def artist_add_tracks(
    artist_id: int,
    tracks_id: List[int]
):
    return await service.artist_s.add_albums(artist_id, tracks_id)

@artist_router.post('/remove_tracks', status_code=204)
async def artist_remove_tracks(
    artist_id: int,
    tracks_id: List[int]
):
    return await service.artist_s.remove_albums(artist_id, tracks_id)

@artist_router.post('/add_genres', status_code=204)
async def artist_add_genres(
    artist_id: int,
    genres_id: List[int]
):
    return await service.artist_s.add_albums(artist_id, genres_id)

@artist_router.post('/remove_genres', status_code=204)
async def artist_remove_genres(
    artist_id: int,
    genres_id: List[int]
):
    return await service.artist_s.remove_albums(artist_id, genres_id)