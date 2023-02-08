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

    async def create(self, schema, genres, albums, tracks, **kwargs) -> Optional[schemas.Artist_get_creation]:
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
        return {'artist': await self.get_schema.from_tortoise_orm(obj),
                'genres': _genres,
                'albums': _albums,
                'tracks': _tracks}

    async def get(self, **kwargs) -> Optional[schemas.Artist_get]:
        obj = await self.model.get(**kwargs)
        _genres = await models.Genre.filter(artists=obj.id)
        _albums = await models.Album.filter(artists=obj.id)
        _tracks = await models.Track.filter(artists=obj.id)
        _libraries = await models.Library.filter(artists=obj.id)
        return {'artist': await self.get_schema.from_tortoise_orm(obj),
                'genres': _genres,
                'albums': _albums,
                'tracks': _tracks,
                'libraries': _libraries}


artist_s = Artist_service()