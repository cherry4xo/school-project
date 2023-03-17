from typing import List, Optional, TypeVar

from pydantic import BaseModel, BaseConfig, create_model
from pydantic.types import Json
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi.responses import FileResponse
from .user import models as user_models
from .library import models as library_models


BaseConfig.arbitrary_types_allowed = True


class File_response:
    def __init__(self, file: dict):
        self.file = file
    __pydantic_model__ = create_model("File_response_model", file=(dict, ...))

class Library_is_track_added(BaseModel):
    added: bool

class Main_page_get(BaseModel):
    class User(BaseModel):
        id: int
        name: str
        picture_file_path: str
    user: User


class Library_page_get(BaseModel):
    class Track(BaseModel):
        class Artist(BaseModel):
            id: int
            name: str
        class Track_data(BaseModel):
            id: int
            name: str
            picture_file_path: str
            track_file_path: str
            duration_s: int
        track_data: Track_data
        artists: List[Artist]
    class Album(BaseModel):
        class Artist(BaseModel):
            id: int
            name: str
        class Track(BaseModel):
            class Artist(BaseModel):
                id: int
                name: str
            class Track_data(BaseModel):
                id: int
                name: str
                picture_file_path: str
                track_file_path: str
                duration_s: int
            track_data: Track_data
            artists: List[Artist]
        class Album_data(BaseModel):
            id: int
            name: str
            picture_file_path: str
        album_data: Album_data
        artists: List[Artist]
        tracks: List[Track]
    class Playlist(BaseModel):
        class Playlist_data(BaseModel):
            name: str
            picture_file_path: str
            description: str
        class Creator(BaseModel):
            id: int
            name: str
            picture_file_path: str
        class Track(BaseModel):
            class Artist(BaseModel):
                id: int
                name: str
            class Track_data(BaseModel):
                id: int
                name: str
                picture_file_path: str
                track_file_path: str
                duration_s: int
            track_data: Track_data
            artists: List[Artist]
        playlist_data: Playlist_data
        tracks: List[Track]
        creator: Creator
    
    tracks: List[Track]
    albums: List[Album]
    playlists: List[Playlist]

    class Config:
        orm_mode=True


class Search_page_get(BaseModel):
    class Track(BaseModel):
        class Artist(BaseModel):
            id: int
            name: str
        class Track_data(BaseModel):
            id: int
            name: str
            picture_file_path: str
            track_file_path: str
            duration_s: int
        track_data: Track_data
        artists: List[Artist]
    class Album(BaseModel):
        class Album_data(BaseModel):
            id: int
            name: str
            picture_file_path: str
        class Artist(BaseModel):
            id: int
            name: str
        class Track(BaseModel):
            class Artist(BaseModel):
                id: int
                name: str
            class Track_data(BaseModel):
                id: int
                name: str
                picture_file_path: str
                track_file_path: str
                duration_s: int
            track_data: Track_data
            artists: List[Artist]
        album_data: Album_data
        artists: List[Artist]
        tracks: List[Track]
    class Artist(BaseModel):
        class Genre(BaseModel):
            id: int
            name: str
        class Artist_data(BaseModel):
            id: int
            name: str
            picture_file_path: str
        artist_data: Artist_data
        genres: List[Genre]
    
    tracks: List[Track]
    albums: List[Album]
    artists: List[Artist]

    class Config:
        orm_mode=True


class Track_page_get(BaseModel):
    class Artist(BaseModel):
        id: int
        name: str
    class Track_data(BaseModel):
        id: int
        name: str
        picture_file_path: str
        track_file_path: str
        duration_s: int
    track_data: Track_data
    artists: List[Artist]
    added: bool

    class Config:
        orm_mode=True


class Album_page_get(BaseModel):
    class Album_data(BaseModel):
        id: int
        name: str
        picture_file_path: str
    class Artist(BaseModel):
        id: int
        name: str
    class Track(BaseModel):
        class Artist(BaseModel):
            id: int
            name: str
        class Track_data(BaseModel):
            id: int
            name: str
            picture_file_path: str
            track_file_path: str
            duration_s: int
        track_data: Track_data
        artists: List[Artist]
    album_data: Album_data
    artists: List[Artist]
    tracks: List[Track]

    class Config:
        orm_mode=True


class Playlist_page_get(BaseModel):
    class Playlist_data(BaseModel):
        name: str
        picture_file_path: str
        description: str
    class Creator(BaseModel):
        id: int
        name: str
        picture_file_path: str
    class Track(BaseModel):
        class Artist(BaseModel):
            id: int
            name: str
        class Track_data(BaseModel):
            id: int
            name: str
            picture_file_path: str
            track_file_path: str
            duration_s: int
        track_data: Track_data
        artists: List[Artist]
    playlist_data: Playlist_data
    tracks: List[Track]
    creator: Creator

    class Config:
        orm_mode=True


class Artist_page_get(BaseModel):
    class Artist_data(BaseModel):
        id: int
        name: str
        registration_date: str
    class Followers_count(BaseModel):
        count: str
    class Track(BaseModel):
        class Artist(BaseModel):
            id: int
            name: str
        class Track_data(BaseModel):
            id: int
            name: str
            track_file_path: str
            duration_s: int
        track_data: Track_data
        artists: List[Artist]
    class Album(BaseModel):
        class Album_data(BaseModel):
            id: int
            name: str
        class Artist(BaseModel):
            id: int
            name: str
        class Track(BaseModel):
            class Artist(BaseModel):
                id: int
                name: str
            class Track_data(BaseModel):
                id: int
                name: str
                track_file_path: str
                duration_s: int
            track_data: Track_data
            artists: List[Artist]
        album_data: Album_data
        artists: List[Artist]
        tracks: List[Track]

    artist_data: Artist_data
    followers_count: Followers_count
    tracks: List[Track]
    albums: List[Album]

    class Config:
        orm_mode=True
        arbitraty_types_allowed=True


class Status(BaseModel):
    message: str


Genre_pydantic = pydantic_model_creator(library_models.Genre)
Artist_pydantic = pydantic_model_creator(library_models.Artist)
Album_pydantic = pydantic_model_creator(library_models.Album)
Track_pydantic = pydantic_model_creator(library_models.Track)
Playlist_pydantic = pydantic_model_creator(library_models.Playlist)
User_pydantic = pydantic_model_creator(user_models.User)