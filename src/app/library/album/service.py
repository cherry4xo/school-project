from typing import Optional, List

from fastapi import HTTPException
#rom tortoise.query_utils import Q

from ...base.service_base import Service_base
from .. import models
from ..album import schemas


class Album_service(Service_base):
    model = models.Album
    create_schema = schemas.Album_create
    update_schema = schemas.Album_update
    get_schema = schemas.Album_get_schema
    create_m2m_schema = schemas.Album_adds

    async def create(self, schema, artists: List[int], tracks:List[int], genre: int = None, **kwargs) -> Optional[schemas.Create]:
        _genre = await models.Genre.get_or_none(id=genre)
        obj = await self.model.create(**schema.dict(exclude_unset=True), genre=_genre, **kwargs)
        await obj.save()
        _artists = await models.Artist.get_or_none(id__in=artists)
        _tracks = await models.Track.get_or_none(id__in=tracks)
        print(_tracks)
        if _artists:
            await obj.artists.add(*_artists)
        if _tracks:
            await _tracks.update(album=obj.id)
        return await self.get_schema.from_tortoise_orm(obj)


album_s = Album_service()