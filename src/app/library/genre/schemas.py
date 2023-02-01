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


class Genre_get(Genre_base):
    id: int
    description: str
    librarises: List[getLibrary] = []


class Genre(Genre_base):
    id: int
    description: str
    libraries: List[getLibrary] = []
    artists: List[getArtist] = []
    albums: List[getAlbum] = []
    playlists: List[getPlaylist] = []

    class Config:
        orm_mode=True


class Genre_delete(Genre_base):
    id: int

    class Config:
        orm_mode=True


class Status(Genre_base):
    message: str