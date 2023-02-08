from typing import Optional, List

#from tortoise.query_utils import Q
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_model_creator
from .. import models


getTrack = pydantic_model_creator(models.Track, exclude_readonly=True, exclude=('genres',))
getArtist = pydantic_model_creator(models.Artist, exclude_readonly=True, exclude=('genres', ))
getLibrary = pydantic_model_creator(models.Library, exclude_readonly=True, exclude=('genres', ))
getAlbum = pydantic_model_creator(models.Album, exclude_readonly=True, exclude=('genres', ))
getPlaylist = pydantic_model_creator(models.Playlist, exclude_readonly=True, exclude=('genres', ))

Genre_get_schema = pydantic_model_creator(models.Genre)


class Genre_base(PydanticModel):
    name: str
    alt_name: Optional[str] = None

    class Config:
        orm_mode=True


class Genre(Genre_base):
    description: str

    class Config:
        orm_mode=True


class Genre_in_db(Genre_base):
    id: int

    class Config:
        orm_mode=True


class Genre_create(Genre_base):
    description: str

    class Config:
        orm_mode=True


class Genre_update(Genre_base):
    description: str


class Genre_get_creation(BaseModel):
    genre: Genre

    class Config:
        orm_mode=True


class Genre_get(Genre_get_creation):
    class Library(BaseModel):
        id: int
    class Artist(BaseModel):
        id: int
    class Album(BaseModel):
        id: int
    class Playlist(BaseModel):
        id: int
    class Track(BaseModel):
        id: int
    libraries: List[Library] = []
    artists: List[Artist] = []
    albums: List[Album] = []
    playlists: List[Playlist] = []
    tracks: List[Track] = []

    class Config:
        orm_mode=True


class Genre_delete(Genre_base):
    id: int

    class Config:
        orm_mode=True


class Status(Genre_base):
    message: str