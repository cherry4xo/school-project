from typing import Optional, List

from fastapi import HTTPException
#from tortoise.query_utils import Query

from ...base.service_base import Service_base
from .. import models
from ..genre import schemas


class Genre_service(Service_base):
    model = models.Genre
    create_schema = schemas.Genre_create
    update_schema = schemas.Genre_update
    get_schema = schemas.Genre_get_schema


genre_s = Genre_service()