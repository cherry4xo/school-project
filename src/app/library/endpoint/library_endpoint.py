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

@library_router.post('/add_tracks', status_code=204)
async def library_add_tracks(
    library_id: int,
    tracks_id: List[int]
):
    return await service.library_s.add_tracks(library_id, tracks_id)

@library_router.delete('/delete_tracks', status_code=204)
async def library_delete_tracks(
    library_id: int,
    tracks_id: List[int]
):
    return await service.library_s.delete_tracks(library_id, tracks_id)

@library_router.post('/add_artists', status_code=204)
async def library_add_artists(
    library_id: int,
    artists_id: List[int]
):
    return await service.library_s.add_artists(library_id, artists_id)

@library_router.delete('/delete_artists', status_code=204)
async def library_delete_artists(
    library_id: int,
    artists_id: List[int]
):
    return await service.library_s.delete_artists(library_id, artists_id)

@library_router.post('/add_playlists', status_code=204)
async def library_add_playlists(
    library_id: int,
    playlists_id: List[int]
):
    return await service.library_s.add_playlists(library_id, playlists_id)

@library_router.delete('/delete_artists', status_code=204)
async def library_delete_playlists(
    library_id: int,
    playlists_id: List[int]
):
    return await service.library_s.delete_playlists(library_id, playlists_id)

@library_router.post('/add_albums', status_code=204)
async def library_add_albums(
    library_id: int,
    albums_id: List[int]
):
    return await service.library_s.add_albums(library_id, albums_id)

@library_router.delete('/delete_albums', status_code=204)
async def library_delete_albums(
    library_id: int,
    albums_id: List[int]
):
    return await service.library_s.delete_albums(library_id, albums_id)

@library_router.post('/add_genres', status_code=204)
async def library_add_genres(
    library_id: int,
    genres_id: List[int]
):
    return await service.library_s.add_genres(library_id, genres_id)

@library_router.delete('/delete_genres', status_code=204)
async def library_delete_genres(
    library_id: int,
    genres_id: List[int]
):
    return await service.library_s.delete_genres(library_id, genres_id)
