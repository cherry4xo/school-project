from typing import Optional, List

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi import Depends, Form, File, UploadFile
from .. library import models 
from . import models as model_params

Params_get_schema = pydantic_model_creator(model_params.Track_params, exclude=('id', 'track_id'))
Track_get_schema = pydantic_model_creator(models.Track)

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

class Get_all_track_params(BaseModel):
    tracks: List[Track]

    class Config:
        orm_mode=True