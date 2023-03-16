from typing import Optional, List

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi import Depends, Form, File, UploadFile
from .. library import models 
from . import models as model_params

Params_get_schema = pydantic_model_creator(model_params.Track_params, exclude=('id', 'track_id'))
Track_get_schema = pydantic_model_creator(models.Track, exclude=('picture_file_path', 'track_file_path'))

class Track(BaseModel):
    valence: Optional[float] = None
    acousticness: Optional[float] = None
    danceability: Optional[float] = None
    energy: Optional[float] = None
    explicit: Optional[bool] = None
    instrumentalness: Optional[float] = None
    liveness: Optional[float] = None
    loudness: Optional[float] = None
    speechiness: Optional[float] = None
    tempo: Optional[float] = None

    class Config:
        orm_mode=True

class Track_page_get(BaseModel):
    class Artist(BaseModel):
        id: int
        name: str
    class Track_data(BaseModel):
        id: int
        name: str
        duration_s: int
    track_data: Track_data
    artists: List[Artist]

    class Config:
        orm_mode=True

class Get_all_track_params(BaseModel):
    tracks: List[Track]

    class Config:
        orm_mode=True