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
'''Artist_genres_get_schema = pydantic_model_creator(models.Artist.genres)
Artist_albums_get_schema = pydantic_model_creator(models.Artist.albums)
Artist_tracks_get_schema = pydantic_model_creator(models.Artist.tracks)
'''

class Artist_base(PydanticModel):
    name: str
    registration_date: str

    class Config:
        orm_mode=True


class Artist_in_db(Artist_base):
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


class Create(Artist_base):
    picture_file_path: str
    genres: List[getGenre] = []
    albums: List[getAlbum] = []
    tracks: List[getTrack] = []

    class Config:
        orm_mode=True


class Artist_update(Artist_base):
    picture_file_path: str
    
    class Config:
        orm_mode=True


class Artist_get(Artist_base):
    picture_file_path: str
    '''libraries: List[int] = []
    genres: List[int]
    albums: List[int]
    tracks: List[int]'''

    class Config:
        orm_mode=True


class Artist_adds(Artist_base):
    libraries: List[getLibrary] = []
    genres: List[getGenre] = []
    albums: List[getAlbum] = []
    tracks: List[getTrack] = []

    class Config:
        orm_mode=True


class Artist(Artist_base):
    id: int
    users: List[getLibrary] = []
    tracks: List[getTrack] = []
    genres: List[getGenre] = []
    albums: List[getAlbum] = []

    class Config:
        orm_mode=True


class Status(Artist_base):
    message: str