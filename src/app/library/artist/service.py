import os

from typing import Optional, List, Union

from fastapi import HTTPException, Form, Depends, File, UploadFile
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

    async def create(self, 
                    schema: schemas.Artist_create, 
                    genres: List[int] = Form(...),
                    albums: List[int] = Form(...), 
                    tracks: List[int] = Form(...), 
                    picture_file: UploadFile = File(...),
                    **kwargs) -> Optional[schemas.Artist_get_creation]:
        obj = await self.model.create(**schema.dict(exclude_unset=True), **kwargs)
        await obj.save()
        
        picture_file_path = await self.upload_file('artist', picture_file)
        if picture_file_path['file_path'] != 'NULL':
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']
        if genres != ['']:
            _genres = await models.Genre.filter(id__in=genres)
            if _genres:
                await obj.genres.add(*_genres)
        else: _genres = []
        if albums != ['']:
            _albums = await models.Album.filter(id__in=albums)
            if _albums:
                await obj.albums.add(*_albums)
        else: _albums = []        
        if tracks != ['']:
            _tracks = await models.Track.filter(id__in=tracks)
            if _tracks:
                await obj.tracks.add(*_tracks)
        else: _tracks = []

        json_response = {'artist': await self.get_schema.from_tortoise_orm(obj),
                        'genres': _genres,
                        'albums': _albums,
                        'tracks': _tracks}

        return {'JSON_Payload': json_response,
                'picture_file_path': picture_file_path['file_path']}

    async def change_picture(self, 
                            artist_id: schemas.Artist_change_picture = Depends(schemas.Artist_change_picture.as_form), 
                            new_picture_file: UploadFile = File(...)) -> Optional[schemas.Artist_change_picture_response]:
        obj = await self.model.get(id=artist_id.id)
        picture_file_path = await self.upload_file('artist', new_picture_file)
        if picture_file_path['file_path'] != 'NULL':
            if obj.picture_file_path != 'data/default_image.png':
                os.remove(obj.picture_file_path)
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']
        else:
            raise Exception

        return {'picture_file_path': obj.picture_file_path}

    async def delete_picture(self, 
                            artist_id: schemas.Artist_change_picture = Depends(schemas.Artist_change_picture.as_form)):
        obj = await self.model.get(id=artist_id.id)
        if obj.picture_file_path != 'data/default_image.png':
            os.remove(obj.picture_file_path)
        await self.model.filter(id=obj.id).update(picture_file_path='data/default_image.png')
        obj.picture_file_path = 'data/default_image.png'

    async def add_albums(self, artist_id: int, albums_id: List[int]):
        obj = await self.model.get_or_none(id=artist_id)
        if not obj:
            raise HTTPException(status=404, detail=f'Artist {artist_id} does not exist')
        _albums = await models.Album.filter(id__in=albums_id)
        await obj.albums.add(*_albums)

    async def remove_albums(self, artist_id: int, albums_id: List[int]):
        obj = await self.model.get_or_none(id=artist_id)
        if not obj:
            raise HTTPException(status=404, detail=f'Artist {artist_id} does not exist')
        _albums = await models.Album.filter(id__in=albums_id)
        await obj.albums.remove(*_albums)

    async def add_tracks(self, artist_id: int, tracks_id: List[int]):
        obj = await self.model.get_or_none(id=artist_id)
        if not obj:
            raise HTTPException(status=404, detail=f'Artist {artist_id} does not exist')
        _tracks = await models.Track.filter(id__in=tracks_id)
        await obj.tracks.add(*_tracks)

    async def remove_tracks(self, artist_id: int, tracks_id: List[int]):
        obj = await self.model.get_or_none(id=artist_id)
        if not obj:
            raise HTTPException(status=404, detail=f'Artist {artist_id} does not exist')
        _tracks = await models.Track.filter(id__in=tracks_id)
        await obj.tracks.remove(*_tracks)

    async def add_genres(self, artist_id: int, genres_id: List[int]):
        obj = await self.model.get_or_none(id=artist_id)
        if not obj:
            raise HTTPException(status=404, detail=f'Artist {artist_id} does not exist')
        _genres = await models.Genre.filter(id__in=genres_id)
        await obj.genres.add(*_genres)

    async def remove_genres(self, artist_id: int, genres_id: List[int]):
        obj = await self.model.get_or_none(id=artist_id)
        if not obj:
            raise HTTPException(status=404, detail=f'Artist {artist_id} does not exist')
        _genres = await models.Genre.filter(id__in=genres_id)
        await obj.genres.remove(*_genres)

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

    async def delete(self, **kwargs):
        obj = await self.model.get(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404, detail='Object does not exist'
            )
        os.remove(obj.picture_file_path)
        await obj.delete()


artist_s = Artist_service()