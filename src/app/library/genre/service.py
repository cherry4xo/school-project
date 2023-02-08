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

    async def create(self, schema, **kwargs) -> Optional[schemas.Genre_get_creation]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        await obj.save()
        return {'genre': await self.get_schema.from_tortoise_orm(obj)}

    async def get(self, **kwargs) -> Optional[schemas.Genre_get]:
        obj = await self.model.get(**kwargs)
        _libraries = await models.Library.filter(genres=obj.id)
        _artists = await models.Artist.filter(genres=obj.id)
        _albums = await models.Album.filter(genres=obj.id)
        _playlists = await models.Playlist.filter(genres=obj.id)
        _tracks = await models.Track.filter(genre=obj.id)
        return {'genre': await self.get_schema.from_tortoise_orm(obj),
                'libraries': _libraries,
                'artists': _artists,
                'albums': _albums,
                'playlists': _playlists,
                'tracks': _tracks}


genre_s = Genre_service()