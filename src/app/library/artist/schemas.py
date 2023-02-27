from typing import Optional, List

#from tortoise.query_utils import Q
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_model_creator
from fastapi import Form, Depends, File, UploadFile
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


class Artist_change_picture(BaseModel):
    id: int

    @classmethod
    def as_form(cls,
                id: int = Form(...)):
        return cls(id=id)

    class Config:
        orm_mode=True


class Artist_change_picture_response(BaseModel):
    picture_file_path: str


class Artist_create(BaseModel):
    name: str
    registration_date: str

    @classmethod
    def as_form(cls,
                name: str = Form(...),
                registraion_date: str = Form(...)):
        return cls(name=name, registration_date=registraion_date)

    class Config:
        orm_mode=True

    
class Artist_delete(Artist_base):
    id: int


class Artist_update(Artist_base):    
    class Config:
        orm_mode=True


class Artist_get_creation(BaseModel):
    class Json_payload(BaseModel):
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

    JSON_Payload: Json_payload
    picture_file_path: str

    class Config:
        orm_mode=True


class Artist_change_picture(BaseModel):
    id: int

    @classmethod
    def as_form(cls, id: int = Form(...)):
        return cls(id=id)

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