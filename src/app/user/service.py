from typing import Optional, List

from fastapi import HTTPException
from tortoise.expressions import Q

from ..base.service_base import Service_base
from ..library import models
from ..user import schemas


class User_service(Service_base):
    model = models.User
    create_schema = schemas.User_create
    update_schema = schemas.User_update
    get_schema = schemas.User_get_schema

    async def create(self, schema, genres: List[int], artists: List[int], **kwargs) -> Optional[schemas.Create]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        await obj.save()
        _lib = await models.Library.create(user_id=obj.id)
        _artists = await models.Artist.filter(id__in=artists)
        _genres = await models.Genre.filter(id__in=genres)
        await _lib.artists.add(*_artists)
        await _lib.genres.add(*_genres)
        return await self.get_schema.from_tortoise_orm(obj)

    async def change_password(self, schema, **kwargs) -> Optional[schemas.User_change_password]:
        #TODO password validation
        obj = await self.model.get(**schema.dict(exclude_unset=True), **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)

    async def get_library(self, schema, **kwargs):
        obj = await self.model.get(**schema.dict(exclude_unset=True), **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)


class Comment_service(Service_base):
    model = models.Comment
    create_schema = schemas.Comment_create
    update_schema = schemas.Comment_update
    get_schema = schemas.Comment_get
    
    async def create(self, schema, track, user, **kwargs):
        comment = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        _track = await models.Track.filter(id=track)
        _user = await models.User.filter(id=user)
        await comment.tracks.add(*_track)
        await comment.user.add(*_user)
        return await self.get_schema.from_tortoise_orm(comment)


user_s = User_service()
comment_s = Comment_service()

