import base64
from typing import Optional, List

#from tortoise.query_utils import Q
from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel, PydanticListModel, pydantic_model_creator
from fastapi import Form, File, UploadFile, Depends
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

User_get_schema = pydantic_model_creator(user_models.User, exclude=['picture_file_path'])
Comment_get_schema = pydantic_model_creator(models.Comment)


class User_base(BaseModel):
    login: str

    class Config:
        orm_mode=True


class User(User_base):
    id: int
    name: str
    email: str
    registration_date: str

    class Config:
        orm_mode=True


class User_create(BaseModel):
    login: str
    name: str
    email: str
    registration_date: str

    @classmethod
    def as_form(cls,
                login: str = Form(...),
                name: str = Form(...),
                email: str = Form(...),
                registration_date: str = Form(...)
    ):
        return cls(login=login, name=name, email=email, registration_date=registration_date)

    class Config:
        orm_mode=True


class User_create_request(BaseModel):
    user: User_create
    password: str

    @classmethod
    def as_form(
        cls,
        user: User_create = Depends(User_create.as_form),
        password: str = Form(...),
    ):
        return cls(user=user, password=password)

    class Config:
        orm_mode=True


class User_get(BaseModel):
    class Library(BaseModel):
        id: int
    user: User
    library: Library

    class Config:
        orm_mode=True


class User_get_registration(User_get):
    class Genre(BaseModel):
        id: int
    class Artist(BaseModel):
        id: int
    genres: List[Genre] = []
    artists: List[Artist] = []



class Users_get(User_base):
    id: list[int]


class User_update(User_base):
    name: str
    email: str

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


class Comment(Comment_base):
    id: int
    publishing_date: str


class Comment_id_db(Comment_base):
    id: int
    user: int
    track: int

    class Config:
        orm_mode=True


class Comment_create(Comment_base):
    publishing_date: str
    class Config:
        orm_mode=True


class Comment_update(Comment_base):
    text: str

    class Config:
        orm_mode=True


class Comment_get(BaseModel):
    comment: Comment
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
