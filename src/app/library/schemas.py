from typing import Optional, List

#from tortoise.query_utils import Query
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from . import models


getArtist = pydantic_model_creator(models.Artist, exclude_readonly=True, exclude=('libraries', ))
getAlbum = pydantic_model_creator(models.Album, exclude_readonly=True, exclude=('libraries', ))
getPlaylist = pydantic_model_creator(models.Playlist, exclude_readonly=True, exclude=('libraries', ))
getGenre = pydantic_model_creator(models.Genre, exclude_readonly=True, exclude=('libraries', ))
getTrack = pydantic_model_creator(models.Track, exclude_readonly=True, exclude=('libraries', ))

class Library_base(BaseModel):
    user_id: int

    class Config:
        orm_mode=True


class Library_in_db(Library_base):
    id: int

    class Config:
        orm_mode=True


class Library_create(Library_base):
    class Config:
        orm_mode=True


class Library_delete(Library_base):
    id: int


class Library_get(Library_base):
    tracks: List[getTrack] = []
    artists: List[getArtist] = []
    albums: List[getAlbum] = []
    genres: List[getGenre] = []
    playlists: List[getPlaylist] = []


class Create(Library_base):
    class Config:
        orm_mode=True


class Library_get(Library_base):
    id: int

    class Config:
        orm_mode=True


class Library_adds(Library_base):
    tracks: List[getTrack] = []
    artists: List[getArtist] = []
    albums: List[getAlbum] = []
    genres: List[getGenre] = []
    playlists: List[getPlaylist] = []

    class Config:
        orm_mode=True


class Status(BaseModel):
    message: str