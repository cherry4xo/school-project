from typing import Optional, List

from fastapi import HTTPException
#from tortoise.query_utils import Query

from ...base.service_base import Service_base
from .. import models
from ..playlist import schemas


class Playlist_service(Service_base):
    model = models.Playlist
    create_schema = schemas.Playlist_create
    update_schema = schemas.Playlist_update
    get_schema = schemas.Playlist_get
    create_m2m_schema = schemas.Playlist_adds

    async def create(self, schema, **kwargs) -> Optional[schemas.Create]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        _tracks = await models.Track.filter(id=schema.tracks.id)
        await obj.tracks.add(*_tracks)
        return await self.get_schema.from_tortoise_orm(obj)


playlist_s = Playlist_service()