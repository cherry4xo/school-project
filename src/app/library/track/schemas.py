from typing import Optional, List

#from tortoise.query_utils import Query
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_model_creator
from .. import models


getArtist = pydantic_model_creator(models.Artist, exclude_readonly=True, exclude=('tracks', ))
getLibrary = pydantic_model_creator(models.Library, exclude_readonly=True, exclude=('tracks', ))
getAlbum = pydantic_model_creator(models.Album, exclude_readonly=True, exclude=('tracks', ))
getGenre = pydantic_model_creator(models.Genre, exclude_readonly=True, exclude=('tracks', ))
getPlaylist = pydantic_model_creator(models.Playlist, exclude_readonly=True, exclude=('tracks'))
getTrack = pydantic_model_creator(models.Track)

Track_get_schema = pydantic_model_creator(models.Track)


class Track_base(PydanticModel):
    name: str

    class Config:
        orm_mode=True

class Track_in_db(Track_base):
    id: int
    duration_s: int
    track_file_path: str

    class Config:
        orm_mode=True


class Track_create(Track_base):
    track_file_path: str
    picture_file_path: Optional[str] = None

    class Config:
        orm_mode=True


class Track_delete(Track_base):
    id: int


class Create(Track_base):
    track_path: str
    picture_file_path: str
    duartion_s: str
    album: Optional[getAlbum] = None
    genre: Optional[getGenre] = None

    class Config:
        orm_mode=True


class Track_update(Track_base):
    id: int
    track_path: str
    picture_file_path: str
    duration_s: str

    class Config:
        orm_mode=True


class Track_get(Track_base):
    id: int
    duration_s: str
    track_file_path: str
    picture_file_path: str
    libraries: List[getLibrary] = []
    artists: List[getArtist] = []
    playlists: List[getPlaylist] = []
    #album: Optional[int] = None
    #genre: Optional[int] = None

    class Config:
        orm_mode=True


class Track_adds(Track_base):
    libraries: List[getLibrary] = []
    artists: List[getArtist] = []
    playlists: List[getPlaylist] = []
    album: Optional[getAlbum] = []
    genre: Optional[getGenre] = []


class Track_change_genre(Track_base):
    id: int
    genre: int

    class Config:
        orm_mode=True


class Track(Track_base):
    id: int
    duration_s: int
    picture_path: str
    artists: List[getArtist] = []
    libraries: List[getLibrary] = []
    playlists: List[getPlaylist] = []
    album: Optional[getAlbum] = None
    genre: Optional[getGenre] = None

    class Config:
        orm_mode=True


class Status(Track_base):
    message: str
