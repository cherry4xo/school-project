from typing import Optional, List

from fastapi import HTTPException

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
        
        _tracks = await library_models.Track.filter(libraries=library.id)
        tracks_response = []
        for i in _tracks:
            _track = await library_models.Track.get(id=i)
            _artists_track = await library_models.Artist.filter(tracks=i)
            _artists_track_response = []
            for j in _artists_track:
                _artist_track = await library_models.Artist.get(id=j)
                _artists_track_response.append({'id': _artist_track.id,
                                                'name': _artist_track.name})
            tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                    'artists': _artists_track_response})
        
        _albums = await library_models.Album.filter(libraries=library.id)
        albums_response = []
        for i in _albums:
            _album = await library_models.Album.get(id=i)
            _tracks = await library_models.Track.filter(album_id=i)
            _artists = await library_models.Artist.filter(albums=_album)
            album_tracks_response = []
            for i in _tracks:
                _track = await library_models.Track.get(id=i)
                _artists_track = await library_models.Artist.filter(tracks=i)
                _artists_track_response = []
                for j in _artists_track:
                    _artist_track = await library_models.Artist.get(id=j)
                    _artists_track_response.append({'id': _artist_track.id,
                                                    'name': _artist_track.name})
                album_tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                              'artists': _artists_track_response})
            album_artists_response = []
            for i in _artists:
                _artist = await library_models.Artist.get(id=i)
                album_artists_response.append(await router_schemas.Artist_pydantic.from_tortoise_orm(_artist))
            albums_response.append({'album_data': await router_schemas.Album_pydantic.from_tortoise_orm(_album),
                                    'artists': album_artists_response,
                                    'tracks': album_tracks_response})

        _playlists = await library_models.Playlist.filter(libraries=library.id)
        playlists_response = []
        for i in _playlists:
            _playlist = await library_models.Playlist.get(id=i)
            _creator = await user_models.User.get(id=_playlist.creator_id)
            playlist_tracks_response = []
            for j in _tracks:
                _track = await library_models.Track.get(id=j)
                _artists_track = await library_models.Artist.filter(tracks=j)
                _artists_track_response = []
                for k in _artists_track:
                    _artist_track = await library_models.Artist.get(id=k)
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
        _tracks = await library_models.Track.all()
        tracks_response = []
        for i in _tracks:
            _track = await library_models.Track.get(id=i)
            _artists_track = await library_models.Artist.filter(tracks=i)
            _artists_track_response = []
            for j in _artists_track:
                _artist_track = await library_models.Artist.get(tracks=j)
                _artists_track_response.append({'id': _artist_track.id, 
                                                'name': _artist_track.name})
            tracks_response.append({'track_data': await router_schemas.Track_pydantic.form_tortoise_orm(_track),
                                    'artists': _artists_track_response})

        _albums = await library_models.Album.all()
        albums_response = []
        for i in _albums:
            _album = await library_models.Album.get(id=i)
            _tracks = await library_models.Track.filter(album_id=i)
            _artists = await library_models.Artist.filter(albums=_album)
            album_tracks_response = []
            for j in _tracks:
                _track = await library_models.Track.get(id=j)
                _artists_track = await library_models.Artist.filter(tracks=j)
                _artists_track_response = []
                for k in _artists_track:
                    _artist_track = await library_models.Artist.get(id=k)
                    _artists_track_response.append({'id': _artist_track.id,
                                                    'name': _artist_track.name})
                album_tracks_response.append({'track_data': await router_schemas.Track_pydantic.from_tortoise_orm(_track),
                                              'artists': _artists_track_response})
            album_artists_response = []
            for j in _artists:
                _artist = await library_models.Artist.get(id=j)
                album_artists_response.append(await router_schemas.Artist_pydantic.from_tortoise_orm(_artist))
            albums_response.append({'album_data': await router_schemas.Album_pydantic.from_tortoise_orm(_album),
                                    'artists': album_artists_response,
                                    'tracks': album_tracks_response})

        _artists = await library_models.Artist.all()
        artists_response = []
        for i in _artists:
            _artist = await library_models.Artist.get(id=i)
            _genres_artist = await library_models.Genre.filter(artists=_artist.id)
            _genres_artist_response = []
            for j in _genres_artist:
                _genre_artist = await library_models.Genre.get(id=j)
                _genres_artist_response.append({'id': _genre_artist.id,
                                                'name': _genre_artist.name})
            artists_response.append({'artist_data': await router_schemas.Artist_pydantic.from_tortoise_orm(_artist),
                                    'genres': _genres_artist_response})

        return {'tracks': tracks_response,
                'albums': albums_response,
                'artists': artists_response}



main_s = Main_service()