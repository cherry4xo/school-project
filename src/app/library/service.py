from typing import Optional, List

from fastapi import HTTPException
#from tortoise.query_utils import Query

from ..base.service_base import Service_base
from ..library import models
from ..library import schemas


class Library_service(Service_base):
    model = models.Library
    create_schema = schemas.Library_create
    get_schema = schemas.Library_get_schema

    async def create(self, user_id, **kwargs) -> Optional[schemas.Library_get_creation]:
        _user = await models.User.get_or_none(id=user_id)
        if not _user:
            raise HTTPException(status_code=404, detail=f'User {user_id} does not exist')
        obj = await self.model.create(user_id=_user.id, **kwargs)
        return {'library': await self.get_schema.from_tortoise_orm(obj),
                'user': {'id': obj.user}}

    async def get_user_id(self, id, **kwargs) -> Optional[int]:
        _library = await self.model.get_or_none(id=id)
        if not _library:
            raise HTTPException(status_code=404, detail=f'Library {id} does not exist')
        user_id = await models.User.filter(id=_library.user).first().values('id')
        return user_id

    async def get(self, id, **kwargs) -> Optional[schemas.Library_get]:
        obj = await self.model.get_or_none(id=id)
        if not obj:
            raise HTTPException(status_code=404, detail=f'Library {id} does not exist')
        _tracks = await models.Track.filter(libraries=obj.id)
        _artists = await models.Artist.filter(libraries=obj.id)
        _albums = await models.Album.filter(libraries=obj.id)
        _genres = await models.Genre.filter(libraries=obj.id)
        _playlists = await models.Playlist.filter(libraries=obj.id)
        return {'library': await self.get_schema.from_tortoise_orm(obj),
                'user': {'id': obj.user_id},
                'tracks': _tracks,
                'artists': _artists,
                'albums': _albums,
                'genres': _genres,
                'playlists': _playlists}


library_s = Library_service()
