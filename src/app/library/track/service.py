from typing import Optional, List

from fastapi import HTTPException
#from tortoise.query_utils import Query

from ...base.service_base import Service_base
from .. import models
from ..track import schemas


class Track_service(Service_base):
    model = models.Track
    create_schema = schemas.Track_create
    update_schema = schemas.Track_update
    get_schema = schemas.Track_get_schema
    create_m2m_schema = schemas.Track_adds

    async def create(self, schema, artists: List[int] = None, album: List[int] = None, genre: List[int] = None, **kwargs) -> Optional[schemas.Create]:
        _album = await models.Album.get_or_none(id=album)
        _genre = await models.Genre.get_or_none(id=genre)
        if not(_genre):
            raise HTTPException(status_code=404, detail=f'Genre {genre} does not exist')
        if not(_album):
            raise HTTPException(status_code=404, detail=f'Album {album} does not exist')
        obj = await self.model.create(**schema.dict(exclude_unset=True), album=_album, genre=_genre, **kwargs)
        await obj.save()
        _artists = await models.Artist.filter(id__in=artists)
        if _artists:
            await obj.artists.add(*_artists)
        return await self.get_schema.from_tortoise_orm(obj)

    async def change_genre(self, schema, genre, **kwargs) -> Optional[schemas.Track_change_genre]:
        _genre = await models.get(id=genre)
        obj = await self.model.update(schema.dict(exclude_unset=True), genre=_genre, **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)


track_s = Track_service()
    
