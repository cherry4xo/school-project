from typing import List, Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from .user import models as user_models
from .library import models as library_models


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
        genre: Genre
    
    tracks: List[Track]
    albums: List[Album]
    artists: List[Artist]

    class Config:
        orm_mode=True


class Status(BaseModel):
    message: str


Genre_pydantic = pydantic_model_creator(library_models.Genre)
Artist_pydantic = pydantic_model_creator(library_models.Artist)
Album_pydantic = pydantic_model_creator(library_models.Album)
Track_pydantic = pydantic_model_creator(library_models.Track)
Playlist_pydantic = pydantic_model_creator(library_models.Playlist)
User_pydantic = pydantic_model_creator(user_models.User)