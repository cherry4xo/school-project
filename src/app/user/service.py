from typing import Optional, List
from hashlib import pbkdf2_hmac
from random import randint

from fastapi import HTTPException
from tortoise.expressions import Q

from ..base.service_base import Service_base
from ..library import models
from ..user import schemas
from ...config import config


class User_service(Service_base):
    model = models.User
    create_schema = schemas.User_create
    update_schema = schemas.User_update
    get_schema = schemas.User_get_schema

    def _get_password_hash_hex(self, password: str) -> Optional[str]:
        _salt = config.SALT[randint(0, len(config.SALT) - 1)]
        _digest = pbkdf2_hmac('sha256', password.encode(), _salt, 10000)
        hex_hash = _digest.hex()

        return hex_hash

    def _check_password_valid(self, password: str, password_hash: str) -> Optional[bool]:
        for i in config.SALT:
            _salt = i
            _digest = pbkdf2_hmac('sha256', password.encode(), _salt, 10000)
            _hex_hash = _digest.hex()
            if _hex_hash == password_hash:
                return True
        return False

    async def create(self, schema, password: str, genres: List[int], artists: List[int], **kwargs) -> Optional[schemas.Create]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), hashed_password=self._get_password_hash_hex(password), **kwargs)
        await obj.save()
        _lib = await models.Library.create(user_id=obj.id)
        _artists = await models.Artist.filter(id__in=artists)
        _genres = await models.Genre.filter(id__in=genres)
        
        await _lib.artists.add(*_artists)
        await _lib.genres.add(*_genres)
        return {'user': await self.get_schema.from_tortoise_orm(obj),
                'genres': _genres,
                'artists': _artists,
                'library': _lib}

    async def change_password(self, old_password: str, new_password: str, **kwargs) -> Optional[schemas.User_change_password]:
        _old_password_model_get = await self.model.filter(**kwargs).values('hashed_password')
        if self._check_password_valid(old_password, _old_password_model_get):
            await self.model.filter(**kwargs).update(hashed_password=self._get_password_hash_hex(new_password))
            return await self.get_schema.from_queryset_single(self.model.get(**kwargs))
        else: return HTTPException(status_code=400, detail=f'Old password is not valid')

    async def get_library(self, schema, **kwargs):
        obj = await self.model.get(**schema.dict(exclude_unset=True), **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)

    async def get(self, **kwargs):
        obj = await self.model.get(**kwargs)
        _lib = await models.Library.filter(user_id=obj.id).first()
        return {'user': await self.get_schema.from_tortoise_orm(obj),
                'library': _lib}



class Comment_service(Service_base):
    model = models.Comment
    create_schema = schemas.Comment_create
    update_schema = schemas.Comment_update
    get_schema = schemas.Comment_get_schema

    async def get_user(self, id: int) -> Optional[models.User]:
        return await models.User.get(id=id)

    async def get_track(self, id: int) -> Optional[models.Track]:
        return await models.Track.get(id=id)
    
    async def create(self, schema, track, user, **kwargs):
        _track = await self.get_track(track)
        _user = await self.get_user(user)
        _comment = await self.model.create(**schema.dict(exclude_unset=True), track=_track, user=_user, **kwargs)
        comment_response = await self.get_schema.from_tortoise_orm(_comment)
        return {'comment': comment_response,
                'user': _user.id,
                'track': _track.id}

    async def get(self, id):
        _comment = await self.model.get(id=id)
        _track = await self.get_track(id=_comment.track_id)
        _user = await self.get_user(id=_comment.user_id)
        comment_response = await self.get_schema.from_tortoise_orm(_comment)
        return {'comment': comment_response,
                'track': _track.id,
                'user': _user.id}


user_s = User_service()
comment_s = Comment_service()

