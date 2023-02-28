import json
from typing import Optional, List

from fastapi import HTTPException
from fastapi.responses import FileResponse

from .base.service_base import Service_base
from .library import models as library_models
from .user import models as user_models
from . import router_schemas


class Main_service(Service_base):
    async def get_main_page(self, **kwargs) -> Optional[router_schemas.Main_page_get]:
        _user = await user_models.User.get_or_none(**kwargs)
        if not _user:
            raise HTTPException(404, detail=f'User {kwargs} does not exist')
        return {'user': await router_schemas.User_pydantic.from_tortoise_orm(_user)}

    async def get_library_page(self, **kwargs):
        library = await library_models.Library.get_or_none(**kwargs)
        if not library:
            raise HTTPException(404, detail=f'Library {kwargs} does not exist')
        
        _tracks = await library_models.Track.filter(libraries=library.id).values('id')
        tracks_response = []
        for i in _tracks:
            _track = await library_models.Track.get(id=i['id'])
            _artists_track = await library_models.Artist.filter(tracks=i['id']).values('id')
            _artists_track_response = []
            for j in _artists_track:
                _artist_track = await library_models.Artist.get(id=j['id'])
                _artists_track_response.append({'id': _artist_track.id,
                                                'name': _artist_track.name})
            tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                    'artists': _artists_track_response})
        
        _albums = await library_models.Album.filter(libraries=library.id).values('id')
        albums_response = []
        for i in _albums:
            _album = await library_models.Album.get(id=i['id'])
            _tracks = await library_models.Track.filter(album_id=i['id']).values('id')
            _artists = await library_models.Artist.filter(albums=_album).values('id')
            album_tracks_response = []
            for j in _tracks:
                _track = await library_models.Track.get(id=j['id'])
                _artists_track = await library_models.Artist.filter(tracks=j['id']).values('id')
                _artists_track_response = []
                for k in _artists_track:
                    _artist_track = await library_models.Artist.get(id=k['id'])
                    _artists_track_response.append({'id': _artist_track.id,
                                                    'name': _artist_track.name})
                album_tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                              'artists': _artists_track_response})
            album_artists_response = []
            for j in _artists:
                _artist = await library_models.Artist.get(id=j['id'])
                album_artists_response.append(await router_schemas.Artist_pydantic.from_tortoise_orm(_artist))
            albums_response.append({'album_data': await router_schemas.Album_pydantic.from_tortoise_orm(_album),
                                    'artists': album_artists_response,
                                    'tracks': album_tracks_response})

        _playlists = await library_models.Playlist.filter(libraries=library.id).values('id')
        playlists_response = []
        for i in _playlists:
            _playlist = await library_models.Playlist.get(id=i['id'])
            _creator = await user_models.User.get(id=_playlist.creator_id)
            _playlist_tracks = await library_models.Track.filter(playlists=_playlist.id).values('id')
            playlist_tracks_response = []
            for j in _playlist_tracks:
                _track = await library_models.Track.get(id=j['id'])
                _artists_track = await library_models.Artist.filter(tracks=j['id']).values('id')
                _artists_track_response = []
                for k in _artists_track:
                    _artist_track = await library_models.Artist.get(id=k['id'])
                    _artists_track_response.append({'id': _artist_track.id,
                                                    'name': _artist_track.name})
                playlist_tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                               'artists': _artists_track_response})
            playlists_response.append({'playlist_data': await router_schemas.Playlist_pydantic.from_tortoise_orm(_playlist),
                                        'tracks': playlist_tracks_response,
                                        'creator': await router_schemas.User_pydantic.from_tortoise_orm(_creator)})

        return {'tracks': tracks_response,
                'albums': albums_response,
                'playlists': playlists_response}

    async def get_search_page(self):
        _tracks = await library_models.Track.all().values('id')
        tracks_response = []
        for i in _tracks:
            _track = await library_models.Track.get_or_none(id=i['id'])
            _artists_track = await library_models.Artist.filter(tracks=_track.id).values('id')
            _artists_track_response = []
            for j in _artists_track:
                _artist_track = await library_models.Artist.get(id=j['id'])
                _artists_track_response.append({'id': _artist_track.id, 
                                                'name': _artist_track.name})
            tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                    'artists': _artists_track_response})
        
        _albums = await library_models.Album.all().values('id')
        albums_response = []
        for i in _albums:
            _album = await library_models.Album.get_or_none(id=i['id'])
            _tracks = await library_models.Track.filter(album_id=_album.id).values('id')
            _artists = await library_models.Artist.filter(albums=_album).values('id')
            album_tracks_response = []
            for j in _tracks:
                _track = await library_models.Track.get_or_none(id=j['id'])
                _artists_track = await library_models.Artist.filter(tracks=_track.id).values('id')
                _artists_track_response = []
                for k in _artists_track:
                    _artist_track = await library_models.Artist.get(id=k['id'])
                    _artists_track_response.append({'id': _artist_track.id,
                                                    'name': _artist_track.name})
                album_tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                              'artists': _artists_track_response})
            album_artists_response = []
            for j in _artists:
                _artist = await library_models.Artist.get(id=j['id'])
                album_artists_response.append(await router_schemas.Artist_pydantic.from_tortoise_orm(_artist))
            albums_response.append({'album_data': await router_schemas.Album_pydantic.from_tortoise_orm(_album),
                                    'artists': album_artists_response,
                                    'tracks': album_tracks_response})
        
        _artists = await library_models.Artist.all().values('id')
        artists_response = []
        for i in _artists:
            _artist = await library_models.Artist.get(id=i['id'])
            _genres_artist = await library_models.Genre.filter(artists=_artist.id).values('id')
            _genres_artist_response = []
            for j in _genres_artist:
                _genre_artist = await library_models.Genre.get(id=j['id'])
                _genres_artist_response.append({'id': _genre_artist.id,
                                                'name': _genre_artist.name})
            artists_response.append({'artist_data': await router_schemas.Artist_pydantic.from_tortoise_orm(_artist),
                                    'genres': _genres_artist_response})

        return {'tracks': tracks_response,
                'albums': albums_response,
                'artists': artists_response}

    async def get_track_page(self, **kwargs):
        _track = await library_models.Track.get_or_none(**kwargs)
        _artists_track = await library_models.Artist.filter(tracks=_track.id).values('id')
        _artists_track_response = []
        for j in _artists_track:
            _artist_track = await library_models.Artist.get(id=j['id'])
            _artists_track_response.append({'id': _artist_track.id, 
                                            'name': _artist_track.name})
        return {'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                'artists': _artists_track_response}

    async def get_album_page(self, **kwargs):
        _album = await library_models.Album.get_or_none(**kwargs)
        _tracks = await library_models.Track.filter(album_id=_album.id).values('id')
        _artists = await library_models.Artist.filter(albums=_album).values('id')
        album_tracks_response = []
        for j in _tracks:
            _track = await library_models.Track.get(id=j['id'])
            _artists_track = await library_models.Artist.filter(tracks=j['id']).values('id')
            _artists_track_response = []
            for k in _artists_track:
                _artist_track = await library_models.Artist.get(id=k['id'])
                _artists_track_response.append({'id': _artist_track.id,
                                                'name': _artist_track.name})
            album_tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                          'artists': _artists_track_response})
        album_artists_response = []
        for j in _artists:
            _artist = await library_models.Artist.get(id=j['id'])
            album_artists_response.append(await router_schemas.Artist_pydantic.from_tortoise_orm(_artist))

        return {'album_data': await router_schemas.Album_pydantic.from_tortoise_orm(_album),
                'artists': album_artists_response,
                'tracks': album_tracks_response}

    async def get_playlist_page(self, **kwargs):
        _playlist = await library_models.Playlist.get_or_none(**kwargs)
        _creator = await user_models.User.get(id=_playlist.creator_id)
        _playlist_tracks = await library_models.Track.filter(playlists=_playlist.id).values('id')
        playlist_tracks_response = []
        for j in _playlist_tracks:
            _track = await library_models.Track.get(id=j['id'])
            _artists_track = await library_models.Artist.filter(tracks=j['id']).values('id')
            _artists_track_response = []
            for k in _artists_track:
                _artist_track = await library_models.Artist.get(id=k['id'])
                _artists_track_response.append({'id': _artist_track.id,
                                                'name': _artist_track.name})
            playlist_tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                           'artists': _artists_track_response})
        return {'playlist_data': await router_schemas.Playlist_pydantic.from_tortoise_orm(_playlist),
                'tracks': playlist_tracks_response,
                'creator': await router_schemas.User_pydantic.from_tortoise_orm(_creator)}

    async def get_artist_page(self, **kwargs):
        _artist = await library_models.Artist.get(**kwargs)
        _artist_picture = FileResponse(_artist.picture_file_path, 
                                    media_type=f'image/{_artist.picture_file_path.split(".")[1]}', 
                                    filename=f'artist_{_artist.id}.{_artist.picture_file_path.split(".")[1]}')
        _followers_count = await library_models.Library.filter(artists=_artist.id).count()
        _tracks = await library_models.Track.filter(artists=_artist.id).values('id')
        _albums = await library_models.Album.filter(artists=_artist.id).values('id')
        artist_tracks_response = []
        for i in _tracks:
            _track = await library_models.Track.get(id=i['id'])
            _track_picture = FileResponse(_track.picture_file_path, 
                                        media_type=f'image/{_track.picture_file_path.split(".")[1]}', 
                                        filename=f'track_{_track.id}.{_track.picture_file_path.split(".")[1]}')
            _artists_track = await library_models.Artist.filter(tracks=i['id']).values('id')
            _artists_track_response = []
            for j in _artists_track:
                _artist_track = await library_models.Artist.get(id=j['id'])
                _artists_track_response.append({'id': _artist_track.id,
                                                'name': _artist_track.name})
            artist_tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                          'artists': _artists_track_response,
                                          'track_picture': _track_picture})
        artist_albums_response = []
        for i in _albums:
            _album = await library_models.Album.get_or_none(id=i['id'])
            _album_picture = FileResponse(_album.picture_file_path, 
                                        media_type=f'image/{_album.picture_file_path.split(".")[1]}', 
                                        filename=f'album_{_album.id}.{_album.picture_file_path.split(".")[1]}')
            _tracks = await library_models.Track.filter(album_id=_album.id).values('id')
            _artists = await library_models.Artist.filter(albums=_album).values('id')
            album_tracks_response = []
            for j in _tracks:
                _track = await library_models.Track.get_or_none(id=j['id'])
                _track_picture = FileResponse(_track.picture_file_path, 
                                            media_type=f'image/{_track.picture_file_path.split(".")[1]}', 
                                            filename=f'track_{_track.id}.{_track.picture_file_path.split(".")[1]}')
                _artists_track = await library_models.Artist.filter(tracks=_track.id).values('id')
                _artists_track_response = []
                for k in _artists_track:
                    _artist_track = await library_models.Artist.get(id=k['id'])
                    _artists_track_response.append({'id': _artist_track.id,
                                                    'name': _artist_track.name})
                album_tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                              'artists': _artists_track_response,
                                              'track_picture': _track_picture})
            album_artists_response = []
            for j in _artists:
                _album_artist = await library_models.Artist.get(id=j['id'])
                album_artists_response.append(await router_schemas.Artist_pydantic.from_tortoise_orm(_album_artist))
            artist_albums_response.append({'album_data': await router_schemas.Album_pydantic.from_tortoise_orm(_album),
                                        'artists': album_artists_response,
                                        'tracks': album_tracks_response,
                                        'album_picture': _album_picture})

        return {'artist_data': await router_schemas.Artist_pydantic.from_tortoise_orm(_artist),
                'artist_picture': _artist_picture,
                'followers_count': {'count': _followers_count},
                'tracks': artist_tracks_response,
                'albums': artist_albums_response}
    
    

main_s = Main_service()