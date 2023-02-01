from typing import Optional, List

from fastapi import HTTPException
#from tortoise.query_utils import Query

from ...base.service_base import Service_base
from .. import models
from ..artist import schemas


class Artist_service(Service_base):
    model = models.Artist
    create_schema = schemas.Artist_create
    update_schema = schemas.Artist_update
    get_schema = schemas.Artist_get
    create_m2m_schema = schemas.Artist_adds

    async def create(self, schema, genres, albums, tracks, **kwargs) -> Optional[schemas.Create]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        await self.get_schema.from_tortoise_orm(obj)


artist_s = Artist_service()