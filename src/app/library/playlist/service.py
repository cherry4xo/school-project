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
    get_schema = schemas.Playlist_get_schema
    create_m2m_schema = schemas.Playlist_adds

    async def create(self, schema, tracks: List[int] = [], genres: List[int] = [], creator: int = None, **kwargs) -> Optional[schemas.Create]:
        _creator = await models.User.get_or_none(id=creator)
        if not _creator:
            raise HTTPException(status=404, detail=f'Creator {creator} does not exist')
        obj = await self.model.create(**schema.dict(exclude_unset=True), creator=_creator, **kwargs)
        await obj.save()
        _tracks = await models.Track.filter(id__in=tracks)
        if _tracks:
            await obj.tracks.add(*_tracks)
        _genres = await models.Genre.filter(id__in=genres)
        if _genres:
            await obj.genres.add(*_genres)
        return await self.get_schema.from_tortoise_orm(obj)


playlist_s = Playlist_service()