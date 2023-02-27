from typing import Optional, List

#from tortoise.query_utils import Query
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_model_creator
from fastapi import Depends, Form, File, UploadFile
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

    class Config:
        orm_mode=True


class Track_delete(Track_base):
    id: int


class Track_update(Track_base):
    id: int
    duration_s: str

    class Config:
        orm_mode=True


class Track_change_picture(BaseModel):
    id: int

    @classmethod
    def as_form(cls, 
                id: int = Form(...)):
        return cls(id=id)

    class Config:
        orm_mode=True


class Track_change_picture_response(BaseModel):
    picture_file_path: str

    @classmethod
    def as_form(cls, picture_file_path: str = Form(...)):
        return cls(picture_file_path=picture_file_path)


class Track_create(BaseModel):
    name: str

    @classmethod
    def as_form(cls, 
                name: str = Form(...),
    ):
        return cls(name=name)   

    class Config:
        orm_mode=True


class Track(BaseModel):
    id: int
    name: str
    duration_s: int
    track_file_path: str
    picture_file_path: str

    @classmethod
    def as_form(cls, 
                id: int = Form(...), 
                name: str = Form(...),
                duration_s: int = Form(...),
                track_file_path: str = Form(...), 
                picture_file_path: str = Form(...)
    ):
        return cls(id=id, name=name, duration_s=duration_s, track_file_path=track_file_path, picture_file_path=picture_file_path)   

    class Config:
        orm_mode=True


class Track_update_get(Track_base):
    id: int
    duration_s: int
    track_file_path: str
    picture_file_path: str

    class Config:
        orm_mode=True


class Track_get_creation(BaseModel):
    class Artist(BaseModel):
        id: int
        @classmethod
        def as_form(cls, id: int = Form(...)): return cls(id=id)
    class Genre(BaseModel):
        id: int
        @classmethod
        def as_form(cls, id: int = Form(...)): return cls(id=id)
    class Album(BaseModel):
        id: int
        @classmethod
        def as_form(cls, id: int = Form(...)): return cls(id=id)
    track: Track
    artists: List[Artist]
    genre: Genre
    album: Optional[Album] = None

    @classmethod
    def as_form(cls, 
                track: Track = Depends(Track.as_form),
                artists: List[Artist] = Depends(Form(List[Artist])),
                genre: Genre = Depends(Genre.as_form),
                album: Album = Depends(Album.as_form)):
        return cls(track=track, artists=artists, genre=genre, album=album)

    class Config:
        orm_mode=True


class Track_get(Track_get_creation):
    class Playlist(BaseModel):
        id: int
    class Library(BaseModel):
        id: int
    libraries: List[Library] = []
    playlists: List[Playlist] = []

    class Config:
        orm_mode=True


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


class Track_adds(BaseModel):
    class Artist(BaseModel):
        id: int
    class Library(BaseModel):
        id: int
    class Playlist(BaseModel):
        id: int
    class Album(BaseModel):
        id: int
    class Genre(BaseModel):
        id: int
    artists: List[Artist] = []
    libraries: List[Library] = []
    playlists: List[Playlist] = []
    album: Optional[Album] = []
    genre: Genre


class Status(Track_base):
    message: str
