import os

from typing import Optional, List
from fastapi import HTTPException, Form, Depends, File, UploadFile
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

    async def create(self, 
                    schema: schemas.Album_create = Depends(), 
                    artists: List[int] = Form(...), 
                    tracks:List[int] = Form(...), 
                    genres: List[int] = Form(None), 
                    picture_file: UploadFile = File(...), 
                    **kwargs) -> Optional[schemas.Create]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        await obj.save()

        picture_file_path = await self.upload_file('album', picture_file)
        if picture_file_path['file_path'] != 'NULL':
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']

        _genres = await models.Genre.filter(id__in=genres)
        _artists = await models.Artist.filter(id__in=artists)
        await models.Track.filter(id__in=tracks).update(album=obj)
        _tracks = await models.Track.filter(id__in=tracks)
        if _artists:
            await obj.artists.add(*_artists)
        if _genres:
            await obj.genres.add(*_genres)

        json_response = {'album': await self.get_schema.from_tortoise_orm(obj),
                        'tracks': _tracks,
                        'artists': _artists,
                        'genres': _genres}

        return {'JSON_Payload': json_response,
                'picture_file_path': picture_file_path['file_path']}

    async def change_picture(self, 
                            album_id: schemas.Album_change_picture = Depends(schemas.Album_change_picture.as_form), 
                            new_picture_file: UploadFile = File(...)) -> Optional[schemas.Album_change_picture_response]:
        obj = await self.model.get(id=album_id.id)
        picture_file_path = await self.upload_file('album', new_picture_file)
        if picture_file_path['file_path'] != 'NULL':
            if obj.picture_file_path != 'data/default_image.png':
                os.remove(obj.picture_file_path)
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']
        else:
            raise Exception

        return {'picture_file_path': obj.picture_file_path}

    async def delete_picture(self, album_id: schemas.Album_change_picture = Depends(schemas.Album_change_picture.as_form)):
        obj = await self.model.get(id=album_id.id)
        if obj.picture_file_path != 'data/default_image.png':
            os.remove(obj.picture_file_path)
        await self.model.filter(id=obj.id).update(picture_file_path='data/default_image.png')
        obj.picture_file_path = 'data/default_image.png'

    async def get(self, **kwargs):
        obj = await self.model.get(**kwargs)
        _genres = await models.Genre.filter(albums=obj.id)
        _artists = await models.Artist.filter(albums=obj.id)
        _tracks = await models.Track.filter(album=obj)
        return {'album': await self.get_schema.from_tortoise_orm(obj),
                'tracks': _tracks,
                'artists': _artists,
                'genres': _genres}

    async def delete(self, **kwargs):
        obj = await self.model.get(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404, detail='Object does not exist'
            )
        os.remove(obj.picture_file_path)
        await obj.delete()


album_s = Album_service()