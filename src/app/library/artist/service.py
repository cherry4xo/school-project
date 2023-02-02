from typing import Optional, List, Union

from fastapi import HTTPException
#from tortoise.query_utils import Query

from ...base.service_base import Service_base, Get_schema_type
from .. import models
from ..artist import schemas


class Artist_service(Service_base):
    model = models.Artist
    create_schema = schemas.Artist_create
    update_schema = schemas.Artist_update
    get_schema = schemas.Artist_get_schema
    create_m2m_schema = schemas.Artist_adds

    async def create(self, schema, genres, albums, tracks, **kwargs) -> Optional[schemas.Create]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        await obj.save()
        _genres = await models.Genre.filter(id__in=genres)
        if _genres:
            await obj.genres.add(*_genres)
        _albums = await models.Album.filter(id__in=albums)
        if _albums:
            await obj.albums.add(*_albums)
        _tracks = await models.Track.filter(id__in=tracks)
        if _tracks:
            await obj.tracks.add(*_tracks)
        return await self.get_schema.from_tortoise_orm(obj)


artist_s = Artist_service()