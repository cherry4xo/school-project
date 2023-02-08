from typing import Optional, List

#from tortoise.query_utils import Q
from pydantic import BaseModel, create_model
from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator
from .. import models


getTrack = pydantic_model_creator(models.Track, exclude_readonly=True, exclude=('playlists',))
getArtist = pydantic_model_creator(models.Artist, exclude_readonly=True, exclude=('playlists', ))
getLibrary = pydantic_model_creator(models.Library, exclude_readonly=True, exclude=('playlists', ))
getAlbum = pydantic_model_creator(models.Album, exclude_readonly=True, exclude=('playlists', ))
getGenre = pydantic_model_creator(models.Genre, exclude_readonly=True, exclude=('playlists', ))

Playlist_get_schema = pydantic_model_creator(models.Playlist)


class Playlist_base(PydanticModel):
    picture_file_path: str
    class Config:
        orm_mode=True


class Playlist(BaseModel):
    id: int
    name: str
    picture_file_path: str
    description: str
    release_date: str

    class Config:
        orm_mode=True


class Playlist_create(Playlist_base):
    name: str
    description: str
    release_date: str

    class Config:
        orm_mode=True


class Playlist_update(Playlist_base):
    name: str
    description: str
    picture_file_path: str

    class Config:
        orm_mode=True


class Playlist_get_creation(BaseModel):
    class Track(BaseModel):
        id: int
    class Genre(BaseModel):
        id: int
    class Creator(BaseModel):
        id: int
    playlist: Playlist_get_schema
    creator: Creator
    tracks: List[Track]
    genres: List[Genre] = []

    class Config:
        orm_mode=True


class Playlist_get(Playlist_get_creation):
    class Library(BaseModel):
        id: int
    libraries: List[Library] = []

    class Config:
        orm_mode=True


class Playlist_adds(Playlist_base):
    tracks: List[getTrack] = []
    libraries: List[getLibrary] = []
    genre: List[getGenre] = []

    class Config: 
        orm_mode=True


class Playlist_delete(Playlist_base):
    id: int

    class Config:
        orm_mode=True


class Status(Playlist_base):
    message: str