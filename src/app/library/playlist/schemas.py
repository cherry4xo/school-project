from typing import Optional, List

#from tortoise.query_utils import Q
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_model_creator
from .. import models


getTrack = pydantic_model_creator(models.Track, exclude_readonly=True, exclude=('playlists',))
getArtist = pydantic_model_creator(models.Artist, exclude_readonly=True, exclude=('playlists', ))
getLibrary = pydantic_model_creator(models.Library, exclude_readonly=True, exclude=('playlists', ))
getAlbum = pydantic_model_creator(models.Album, exclude_readonly=True, exclude=('playlists', ))
getGenre = pydantic_model_creator(models.Genre, exclude_readonly=True, exclude=('playlists', ))
getPlaylist = pydantic_model_creator(models.Playlist)


class Playlist_base(PydanticModel):
    creator: int

    class Config:
        orm_mode=True


class Playlist_in_db(Playlist_base):
    id: int
    name: str
    description: str

    class Config:
        orm_mode=True


class Playlist_create(Playlist_base):
    name: str
    description: str
    release_date: str
    tracks: List[getTrack] = []

    class Config:
        orm_mode=True


class Create(Playlist_base):
    name: str
    description: str
    release_date: str
    tracks: List[getTrack] = []

    class Config:
        orm_mode=True


class Playlist_update(Playlist_base):
    name: str
    description: str
    picture_file_path: str

    class Config:
        orm_mode=True


class Playlist_get(Playlist_base):
    id: int
    name: str
    description: str
    release_date: str
    picture_file_path: str
    tracks: List[getTrack] = []
    libraries: List[getLibrary] = []
    genres: List[getGenre] = []

    class Config:
        orm_mode=True


class Playlist_adds(Playlist_base):
    tracks: List[getTrack] = []
    libraries: List[getLibrary] = []
    genre: List[getGenre] = []

    class Config: 
        orm_mode=True


class Playlist(Playlist_base):
    id: int
    name: str
    description: str
    release_date: str
    tracks: List[getTrack] = []
    genre: List[getGenre] = []
    libraries: List[getLibrary] = []

    class Config:
        orm_mode=True


class Playlist_delete(Playlist_base):
    id: int

    class Config:
        orm_mode=True


class Status(Playlist_base):
    message: str