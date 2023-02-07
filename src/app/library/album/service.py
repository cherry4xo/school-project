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

    async def create(self, schema, artists: List[int], tracks:List[int], genres: List[int] = None, **kwargs) -> Optional[schemas.Create]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        await obj.save()
        _genres = await models.Genre.filter(id__in=genres)
        _artists = await models.Artist.filter(id__in=artists)
        await models.Track.filter(id__in=tracks).update(album=obj)
        _tracks = await models.Track.filter(id__in=tracks)
        if _artists:
            await obj.artists.add(*_artists)
        if _genres:
            await obj.genres.add(*_genres)
        return {'album': await self.get_schema.from_tortoise_orm(obj),
                'tracks': _tracks,
                'artists': _artists,
                'genres': _genres}

    async def get(self, **kwargs):
        obj = await self.model.get(**kwargs)
        _genres = await models.Genre.filter(albums=obj.id)
        _artists = await models.Artist.filter(albums=obj.id)
        _tracks = await models.Track.filter(album=obj)
        return {'album': await self.get_schema.from_tortoise_orm(obj),
                'tracks': _tracks,
                'artists': _artists,
                'genres': _genres}


album_s = Album_service()