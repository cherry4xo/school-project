import shutil
import os
import uuid

from typing import Optional, List
from hashlib import pbkdf2_hmac
from random import randint

from fastapi import HTTPException, File, UploadFile, Depends, Form
from fastapi.responses import FileResponse
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from tortoise.expressions import Q
from fastapi.concurrency import run_in_threadpool

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

    async def create(self, 
                    schema: schemas.User_create_request = Depends(), 
                    artists: List[int] = Form(...),
                    genres: List[int] = Form(...),
                    picture_file: UploadFile = File(...),
                    **kwargs) -> Optional[schemas.Create]:
        obj = await self.model.create(**schema.user.dict(exclude_unset=True), hashed_password=self._get_password_hash_hex(schema.password), **kwargs)
        await obj.save()
        
        picture_file_path = await self.upload_file('user', picture_file)
        if picture_file_path['file_path'] != 'NULL':
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']

        _lib = await models.Library.create(user_id=obj.id)
        _artists = await models.Artist.filter(id__in=artists)
        _genres = await models.Genre.filter(id__in=genres)
        
        await _lib.artists.add(*_artists)
        await _lib.genres.add(*_genres)

        json_response = {'user': await self.get_schema.from_tortoise_orm(obj),
                        'genres': _genres,
                        'artists': _artists,
                        'library': _lib}

        return {
            "JSON Payload ": json_response,
            "filenames": picture_file_path['file_path']
        }

    async def change_picture(self, user_id: schemas.User_change_picture, new_picture_file: UploadFile = File(...)) -> Optional[schemas.User_change_picture_response]:
        obj = await self.model.get(id=user_id.id)
        picture_file_path = await self.upload_file('user', new_picture_file)
        if picture_file_path['file_path'] != 'NULL':
            if obj.picture_file_path != 'data/default_image.png':
                os.remove(obj.picture_file_path)
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']
        else:
            raise Exception

        return {'picture_file_path': obj.picture_file_path}

    async def delete_picture(self, user_id: schemas.User_change_picture):
        obj = await self.model.get(id=user_id.id)
        if obj.picture_file_path != 'data/default_image.png':
            os.remove(obj.picture_file_path)
        await self.model.filter(id=obj.id).update(picture_file_path='data/default_image.png')
        obj.picture_file_path = 'data/default_image.png'

    async def change_password(self, old_password: str, new_password: str, **kwargs) -> Optional[schemas.User_change_password]:
        _old_password_model_get = await self.model.filter(**kwargs).values('hashed_password')
        if self._check_password_valid(old_password, _old_password_model_get):
            await self.model.filter(**kwargs).update(hashed_password=self._get_password_hash_hex(new_password))
            return await self.get_schema.from_queryset_single(self.model.get(**kwargs))
        else: return HTTPException(status_code=400, detail=f'Old password is not valid')

    async def return_image(self, user_id: int):
        obj = await self.model.get(id=user_id)
        return {'file': FileResponse(obj.picture_file_path, 
                                    media_type=f'image/{obj.picture_file_path.split(".")[1]}', 
                                    filename=f'UserPicture_{obj.id}'),
                'metadata': {'filename': obj.picture_file_path.split("/")[-1]}}
        

    async def get_library(self, schema, **kwargs):
        obj = await self.model.get(**schema.dict(exclude_unset=True), **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)

    async def get(self, **kwargs):
        obj = await self.model.get(**kwargs)
        _lib = await models.Library.filter(user_id=obj.id).first()
        return {'user': await self.get_schema.from_tortoise_orm(obj),
                'library': _lib}

    async def delete(self, **kwargs):
        obj = await self.model.get(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404, detail='Object does not exist'
            )
        os.remove(obj.picture_file_path)
        await models.Library.filter(user_id=obj).delete()
        await obj.delete()


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

