from typing import Optional, List

#from tortoise.query_utils import Q
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_model_creator
from .. import models


getTrack = pydantic_model_creator(models.Track, exclude=('albums',))
getArtist = pydantic_model_creator(models.Artist, exclude=('albums', ))
getLibrary = pydantic_model_creator(models.Library, exclude=('albums', ))
getGenre = pydantic_model_creator(models.Genre, exclude=('albums', ))
getAlbum = pydantic_model_creator(models.Album, exclude=('album', ))

Album_get_schema = pydantic_model_creator(models.Album)


class Album_base(PydanticModel):
    name: str
    description: str
    release_date: str
    picture_file_path: str

    class Config:
        orm_mode=True


class Album(Album_base):
    id: int

    class Config:
        orm_mode=True


class Album_get(BaseModel):
    class Track(BaseModel):
        id: int
    class Artist(BaseModel):
        id: int
    class Genre(BaseModel):
        id: int
    album: Album
    tracks: List[Track]
    artists: List[Artist]
    genres: List[Genre]

    class Config:
        orm_mode=True


class Album_create(Album_base):
    '''tracks: List[getTrack] = []
    artists: List[getArtist] = []
    genre: Optional[int] = None'''

    class Config:
        orm_mode=True


class Album_update(Album_base):
    class Config:
        orm_mode=True


class Album_delete(PydanticModel):
    id: int

    class Config:
        orm_mode=True


class Album_adds(Album_base):
    tracks: List[getTrack] = []
    artists: List[getArtist] = []
    libraries: List[getLibrary] = []

    class Config:
        orm_mode=True


class Create(Album_base):
    '''tracks: List[getTrack] = []
    artists: List[getArtist] = []

    class Config:
        orm_mode=True'''

    pass


class Status(Album_base):
    message: str