from typing import Optional, List

#from tortoise.query_utils import Q
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_model_creator
from . import models as user_models
from ..library import models 


getTrack = pydantic_model_creator(models.Track, exclude=('users',))
getArtist = pydantic_model_creator(models.Artist, exclude=('users', ))
getLibrary = pydantic_model_creator(models.Library, exclude=('users', ))
getGenre = pydantic_model_creator(models.Genre, exclude=('users', ))
getAlbum = pydantic_model_creator(models.Album, exclude=('users', ))
getPlaylist = pydantic_model_creator(models.Playlist, exclude=('users', ))
getUser = pydantic_model_creator(user_models.User)
getComment = pydantic_model_creator(models.Comment)

User_get_schema = pydantic_model_creator(models.User)


class User_base(BaseModel):
    login: str
    picture_file_path: str

    class Config:
        orm_mode=True


class User_in_db(User_base):
    id: int
    name: str
    email: str
    library_id: int

    class Config:
        orm_mode=True


class User_create(User_base):
    name: str
    email: str
    hashed_password: str
    registration_date: str

    class Config:
        orm_mode=True


class User_get(User_base):
    id: int
    name: str
    email: str
    registration_date: str

    class Config:
        orm_mode=True


class Users_get(User_base):
    id: list[int]


class User_update(User_base):
    name: str
    email: str
    picture_file_path: str


    class Config:
        orm_mode=True


class User_delete(BaseModel):
    id: int


class Create(User_base):
    pass


class User_change_password(User_base):
    hashed_password: str    

    class Config:
        orm_mode=True


class Comment_base(PydanticModel):
    text: str

    class Config:
        orm_mode=True


class Comment_id_db(Comment_base):
    id: int
    user: int
    track: int

    class Config:
        orm_mode=True


class Comment_create(Comment_base):
    user: int
    track: int

    class Config:
        orm_mode=True


class Comment_update(Comment_base):
    text: str

    class Config:
        orm_mode=True


class Comment_get(Comment_base):
    id: int
    text: str
    user: int
    track: int

    class Config:
        orm_mode=True


class Comment_delete(Comment_base):
    id: int

    class Config:
        orm_mode=True


class Status(BaseModel):
    message: str

    class Config:
        allow_none=True
