from typing import Optional, List

#from tortoise.query_utils import Q
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_model_creator
from .. import models


getTrack = pydantic_model_creator(models.Track, exclude_readonly=True, exclude=('artists',))
getLibrary = pydantic_model_creator(models.Library, exclude_readonly=True, exclude=('artists', ))
getGenre = pydantic_model_creator(models.Genre, exclude_readonly=True, exclude=('artists', ))
getAlbum = pydantic_model_creator(models.Album, exclude_readonly=True, exclude=('artists', ))
getArtist = pydantic_model_creator(models.Artist)

Artist_get_schema = pydantic_model_creator(models.Artist)

class Artist_base(PydanticModel):
    name: str
    registration_date: str

    class Config:
        orm_mode=True


class Artist(Artist_base):
    id: int
    picture_file_path: str

    class Config:
        orm_mode=True


class Artist_create(Artist_base):
    picture_file_path: str

    class Config:
        orm_mode=True

    
class Artist_delete(Artist_base):
    id: int


class Artist_update(Artist_base):
    picture_file_path: str
    
    class Config:
        orm_mode=True


class Artist_get_creation(BaseModel):
    class Genre(BaseModel):
        id: int
    class Album(BaseModel):
        id: int
    class Track(BaseModel):
        id: int
    artist: Artist
    genres: List[Genre] = []
    albums: List[Album] = []
    tracks: List[Track] = []

    class Config:
        orm_mode=True


class Artist_get(Artist_get_creation):
    class Library(BaseModel):
        id: int
    
    libraries: List[Library] = []

    class Config:
        orm_mode=True


class Artist_adds(Artist_base):
    libraries: List[getLibrary] = []
    genres: List[getGenre] = []
    albums: List[getAlbum] = []
    tracks: List[getTrack] = []

    class Config:
        orm_mode=True


class Status(Artist_base):
    message: str