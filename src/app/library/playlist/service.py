import os
from typing import Optional, List

from fastapi import HTTPException, Form, Depends, File, UploadFile
#from tortoise.query_utils import Query

from ...base.service_base import Service_base
from .. import models
from ..playlist import schemas


class Playlist_service(Service_base):
    model = models.Playlist
    create_schema = schemas.Playlist_create
    update_schema = schemas.Playlist_update
    get_schema = schemas.Playlist_get_schema
    create_m2m_schema = schemas.Playlist_adds

    async def create(self, 
                    picture_file: UploadFile = File(...),
                    schema: schemas.Playlist_create = Depends(), 
                    tracks: List[int] = Form(...), 
                    genres: List[int] = Form(...), 
                    creator: int = Form(...), 
                    **kwargs) -> Optional[schemas.Playlist_get_creation]:
        _creator = await models.User.get_or_none(id=creator)
        if not _creator:
            raise HTTPException(status=404, detail=f'Creator {creator} does not exist')
        obj = await self.model.create(**schema.dict(exclude_unset=True), creator=_creator, **kwargs)
        await obj.save()

        picture_file_path = await self.upload_file('playlist', picture_file)
        if picture_file_path['file_path'] != 'NULL':
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']
        
        _tracks = await models.Track.filter(id__in=tracks)
        if _tracks:
            await obj.tracks.add(*_tracks)
        _genres = await models.Genre.filter(id__in=genres)
        if _genres:
            await obj.genres.add(*_genres)

        json_response = {'playlist': await self.get_schema.from_tortoise_orm(obj),
                        'creator': {'id': obj.creator_id},
                        'tracks': _tracks,
                        'genres': _genres}

        return json_response

    async def change_picture(self, 
                            playlist_id: schemas.Playlist_change_picture = Depends(schemas.Playlist_change_picture.as_form), 
                            new_picture_file: UploadFile = File(...)) -> Optional[schemas.Playlist_change_picture_response]:
        obj = await self.model.get(id=playlist_id.id)
        picture_file_path = await self.upload_file('playlist', new_picture_file)
        if picture_file_path['file_path'] != 'NULL':
            if obj.picture_file_path != 'data/default_image.png':
                os.remove(obj.picture_file_path)
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']
        else:
            raise Exception

        return {'picture_file_path': obj.picture_file_path}

    async def delete_picture(self, playlist_id: schemas.Playlist_change_picture = Depends(schemas.Playlist_change_picture.as_form)):
        obj = await self.model.get(id=playlist_id.id)
        if obj.picture_file_path != 'data/default_image.png':
            os.remove(obj.picture_file_path)
        await self.model.filter(id=obj.id).update(picture_file_path='data/default_image.png')
        obj.picture_file_path = 'data/default_image.png'

    async def add_tracks(self, playlist_id: int, tracks_id: List[int]):
        obj = await self.model.get_or_none(id=playlist_id)
        if not obj:
            raise HTTPException(status_code=404, detail=f'Playlist {playlist_id} does not exist')
        _tracks = await models.Track.filter(id__in=tracks_id)
        await obj.tracks.add(*_tracks)

    async def remove_tracks(self, playlist_id: int, tracks_id: List[int]):
        obj = await self.model.get_or_none(id=playlist_id)
        if not obj:
            raise HTTPException(status_code=404, detail=f'Playlist {playlist_id} does not exist')
        _tracks = await models.Track.filter(id__in=tracks_id)
        await obj.tracks.remove(*_tracks)

    async def add_genres(self, playlist_id: int, genres_id: List[int]):
        obj = await self.model.get_or_none(id=playlist_id)
        if not obj:
            raise HTTPException(status_code=404, detail=f'Playlist {playlist_id} does not exist')
        _genres = await models.Gerne.filter(id__in=genres_id)
        await obj.genres.add(*_genres)

    async def remove_genres(self, playlist_id: int, genres_id: List[int]):
        obj = await self.model.get_or_none(id=playlist_id)
        if not obj:
            raise HTTPException(status_code=404, detail=f'Playlist {playlist_id} does not exist')
        _genres = await models.Gerne.filter(id__in=genres_id)
        await obj.genres.remove(*_genres)

    async def get(self, **kwargs) -> Optional[schemas.Playlist_get]:
        obj = await self.model.get(**kwargs)
        _tracks = await models.Track.filter(playlists=obj.id)
        _genres = await models.Genre.filter(playlists=obj.id)
        _libraries = await models.Library.filter(playlists=obj.id)
        print(await self.get_schema.from_tortoise_orm(obj))
        return {'playlist': await self.get_schema.from_tortoise_orm(obj),
                'creator': {'id': obj.creator_id},
                'tracks': _tracks,
                'genres': _genres,
                'libraries': _libraries}

    async def delete(self, **kwargs):
        obj = await self.model.get(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404, detail='Object does not exist'
            )
        os.remove(obj.picture_file_path)
        await obj.delete()


playlist_s = Playlist_service()