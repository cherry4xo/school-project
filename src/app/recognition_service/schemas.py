from typing import Optional, List

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi import Depends, Form, File, UploadFile
from .. library import models 
from . import models as model_spectro

Get_track_spectrogram = pydantic_model_creator(model_spectro.Track_spectorgram)
Track_pydantic = pydantic_model_creator(models.Track)

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