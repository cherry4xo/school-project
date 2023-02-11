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

Library_get_schema = pydantic_model_creator(models.Library)


class Library_base(BaseModel):
    user_id: int

    class Config:
        orm_mode=True


class Library_create(Library_base):
    class Config:
        orm_mode=True


class Library_delete(Library_base):
    id: int


class Library(BaseModel):
    id: int

    class Config:
        orm_mode=True


class Library_get_creation(BaseModel):
    class User(BaseModel):
        id: int
    library: Library
    user: User


class Library_get(Library_get_creation):
    class Track(BaseModel):
        id: int
    class Artist(BaseModel):
        id: int
    class Album(BaseModel):
        id: int
    class Genre(BaseModel):
        id: int
    class Playlist(BaseModel):
        id: int
    tracks: List[Track] = []
    artists: List[Artist] = []
    albums: List[Album] = []
    genres: List[Genre] = []
    playlists: List[Playlist] = []

    class Config:
        orm_mode=True


class Create(Library_base):
    class Config:
        orm_mode=True


class Status(BaseModel):
    message: str