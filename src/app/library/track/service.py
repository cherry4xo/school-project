import librosa
import os

from typing import Optional, List

from fastapi import HTTPException, Form, Depends, File, UploadFile
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

    async def create(self, 
                    schema: schemas.Track_create = Depends(), 
                    artists: List[int] = Form(...), 
                    album: int = Form(...), 
                    genre: int = Form(...),
                    picture_file: UploadFile = File(...),
                    track_file: UploadFile = File(...),
                    **kwargs) -> Optional[schemas.Track_create]:
        _album = await models.Album.get_or_none(id=album)
        _genre = await models.Genre.get_or_none(id=genre)
        if not _genre:
            raise HTTPException(status_code=404, detail=f'Genre {genre} does not exist')
        if _album:
            obj = await self.model.create(**schema.dict(exclude_unset=True), album=_album, genre=_genre, **kwargs)
        else:
            obj = await self.model.create(**schema.dict(exclude_unset=True), genre=_genre, **kwargs)
        await obj.save()
        
        picture_file_path = await self.upload_file('track/picture', picture_file)
        if picture_file_path['file_path'] != 'NULL':
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']
        
        track_file_path = await self.upload_file('track/track_file', track_file)
        if track_file_path['file_path'] != 'NULL':
            print(track_file_path['file_path'])
            track_duration_s = round(librosa.get_duration(filename=track_file_path['file_path']))
            await self.model.filter(id=obj.id).update(duration_s=track_duration_s, track_file_path=track_file_path['file_path'])
            obj.duration_s = track_duration_s
            obj.track_file_path = track_file_path['file_path']

        _artists = await models.Artist.filter(id__in=artists)
        if _artists:
            await obj.artists.add(*_artists)
        return {'track': await self.get_schema.from_tortoise_orm(obj),
                'artists': _artists,
                'genre': _genre,
                'album': _album.id if _album else None}

    async def change_picture(self, track_id: schemas.Track_change_picture, new_picture_file: UploadFile = File(...)) -> Optional[schemas.Track_change_picture_response]:
        obj = await self.model.get(id=track_id.id)
        picture_file_path = await self.upload_file('track/picture', new_picture_file)
        if picture_file_path['file_path'] != 'NULL':
            if obj.picture_file_path != 'data/default_image.png':
                os.remove(obj.picture_file_path)
            await self.model.filter(id=obj.id).update(picture_file_path=picture_file_path['file_path'])
            obj.picture_file_path = picture_file_path['file_path']
        else:
            raise Exception

        return {'picture_file_path': obj.picture_file_path}

    async def change_genre(self, schema, genre, **kwargs) -> Optional[schemas.Track_change_genre]:
        _genre = await models.get(id=genre)
        obj = await self.model.update(schema.dict(exclude_unset=True), genre=_genre, **kwargs)
        return await self.get_schema.from_tortoise_orm(obj)

    async def get(self, **kwargs) -> Optional[schemas.Track_get]:
        obj = await self.model.get(**kwargs)
        _artists = await models.Artist.filter(tracks=obj.id)
        _libraries = await models.Library.filter(tracks=obj.id)
        _playlists = await models.Playlist.filter(tracks=obj.id)
        return {'track': await self.get_schema.from_tortoise_orm(obj),
                'genre': {'id': obj.genre_id},
                'album': {'id': obj.album_id},
                'artists': _artists,
                'libraries': _libraries,
                'playlists': _playlists}

    async def delete(self, **kwargs):
        obj = await self.model.get(**kwargs)
        if not obj:
            raise HTTPException(
                status_code=404, detail='Object does not exist'
            )
        os.remove(obj.track_file_path)
        os.remove(obj.picture_file_path)
        await obj.delete()


track_s = Track_service()
    
