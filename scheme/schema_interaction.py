from tortoise import Tortoise, run_async
from tortoise.query_utils import Prefetch
from hashlib import pbkdf2_hmac
import json
from os import urandom
from config import MYSQL_NAME, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB_NAME
from ..parser.YMparser import HtmlParser, JsonParser
import config as config
import models_fixed as models
import datetime
import librosa
from math import floor

async def init():
    await Tortoise.init(db_url=f"mysql://{MYSQL_NAME}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB_NAME}", 
                        modules={"models": ["models"]})
    await Tortoise.generate_schemas()

class Interface_db:
    def __init__(self, extended:bool = False):
        run_async(init())
        self.extended = extended
        self.jsonData = self.makeData()

    def makeData(self):
        if self.extended:
            #---------------------------------------- artist page ----------------------------------------
            artistPage = HtmlParser(url=config.URL_EXT['artist'], 
                                    patternStr=config.PATTERN_EXT, 
                                    dataType='artist')
            artistPage.makeJsonFile()
            subArtistPage = HtmlParser(url=f'{self.page.url}/tracks', 
                                    patternStr=config.PATTERN_EXT,
                                    dataType='artist')
            subArtistPage.makeJsonFile()
            jsonArtistData = JsonParser(mainFilePath=artistPage.dataPath, subFilePath={'albums': subArtistPage.dataPath}).getData()
            #----------------------------------------------------------------------------------------------
            
            #----------------------------------------- album page -----------------------------------------
            jsonArtistAlbumsData = []
            for album_url in config.URL_EXT['album']:
                albumPage = HtmlParser(url=album_url,
                                        patternStr=config.PATTERN_EXT,
                                        dataType=f'album{album_url[-8:]}')
                albumPage.makeJsonFile()
                albumData = JsonParser(mainFilePath=albumPage.dataPath, dataType='album')
                jsonArtistAlbumsData.append(albumData.getData())
            return {'artist': jsonArtistData, 'albums': jsonArtistAlbumsData, 'genres': albumData.getAllGenres()}
            #----------------------------------------------------------------------------------------------    
        else:
            page = HtmlParser(url=config.URL,
                            patternStr=config.PATTERN,
                            dataType=config.DATATYPE)
            page.makeJsonFile()
            jsonAlbumData = JsonParser(mainFilePath=self.page.dataPath, dataType=f'album{config.URL[-8]}').getData()
            return {'album': jsonAlbumData, 'genres': jsonAlbumData.getAllGenres()}

    def hash(inputData: str):
            key = pbkdf2_hmac('sha256',
                            inputData.encode('utf-8'),
                            config.SALT,
                            100000,
                            dklen=128)
            return {'salt': config.SALT, 'key': key}

#--------------------------------------------- artist interface ---------------------------------------------
    async def createArtistByJson(self): 
        '''
        imports artist data from <jsonData> variable into db
        returns <artist> field
        '''
        artist = await models.Artist.create(name=self.jsonData['artist']['name']).save()
        return artist

    async def createArtist(self, 
                        name: str, 
                        registrationDate: datetime.datetime = datetime.datetime.utcnow()[:10],
                        pictureFilePath: str = '', pictureFileType: str = 'jpg'):
        '''
        creating an artist field by given data
        :name: name of an artist
        :registrationDate: time of registration (default: time of the creation)
        :pictureFilePath: path to picture file on the server (default: no path)
        :pictureFileType: extention of the picture file (default: 'jpg')
        returns an artist field
        '''
        pictureFile = await models.File.create(file_name=pictureFilePath,
                                            file_type=pictureFileType,
                                            data_type='artist_image').save()
        artist = await models.Artist.create(name=name,
                                    registration_date=registrationDate,
                                    picture_id=pictureFile).save()

        return artist
#-------------------------------------------------------------------------------------------------------------


# --------------------------------------------- album interface ----------------------------------------------    
    async def createAlbumsByJson(self):
        '''
        imports albums data from <jsonData> variable into db
        returns <list> of <album> fields 
        '''
        albums = [await models.Album.create(name=i['title'],
                                            releaseDate=i['releaseDate'][:10]).save() 
                for i in self.jsonData['album']['albums']]
        return albums

    async def createAlbum(self,
                        name: str,
                        releaseDate: datetime.datetime = datetime.datetime.utcnow()[:10],
                        tracksIds: list[int] = [],
                        artistsIds: list[int] = [],
                        pictureFilePath: str = '', pictureFileType: str = 'jpg'):
        '''
        creating an album field by given data
        :name: album title
        :releaseDate: time of playlist creation (default: time of the creation)
        :pictureFilePath: path to picture file on the server (default: no path)
        :pictureFileType: extention of the picture file (default: 'jpg')
        returns an album field
        '''
        pictureFile = await models.File.create(file_name=pictureFilePath,
                                            file_type=pictureFileType,
                                            data_type='album_image').save()

        album = await models.Album.create(name=name,
                                        release_date=releaseDate,
                                        picture=pictureFile).save()

        for i in tracksIds:
            track = await models.Track.all().filter(id=i)
            await models.Album.tracks_ids.participants.add(track).save()
        for i in artistsIds:
            artist = await models.Artist.all().filter(id=i)
            await models.Album.artists_ids.participants.add(artist).save()

        return album

    async def deleteAlbum(self,
                        albumId: int):  
        pictureId = await models.Album.all().filter(id=albumId).first().values('picture_id')
        picture = await models.File.all().filter(id=pictureId).delete()

        tracks = await models.Album.tracks_ids.all().filter(album_id=albumId).delete()
        artists = await models.Album.artists_ids.all().filter(Album_id=albumId).delete()

        album = await models.Album.all().filter(id=albumId).first().delete()

        return album

    async def addAlbumPicture(self,
                            albumId: int,
                            pictureFilePath: int,
                            pictureFileType: int):
        picture = await models.File.create(file_name=pictureFilePath,
                                        file_type=pictureFileType,
                                        data_type='album_image')

        album = (await models.Album.all().filter(id=albumId).first()
                    .update(picture_id=picture.id).save())

        return album

    async def deleteAlbumPicture(self, 
                                albumId: int):
        fileId = (await models.Album.all().filter(id=albumId).first()
                    .values('picture_id'))
        file = (await models.File.all().filter(id=fileId).first()
                    .delete())

        return file

    async def changeAlbumPicture(self,
                                albumId: int,
                                pictureFilePath: str,
                                pictureFileType: str):
        album = await models.Album.all().filter(id=albumId).first()

        picture = (await models.File.all().filter(id=album.picture_id)
                        .first().update(file_name=pictureFilePath,
                                        file_type=pictureFileType,
                                        data_type='album_picture').save())

        return picture

    async def changeAlbumName(self,
                            albumId: int,
                            newAlbumName: str):
        album = (await models.Album.all()
                    .filter(id=albumId).first()
                .update(name=newAlbumName).save())
        
        return album

    async def addAlbumTracks(self,
                            albumId: int,
                            tracksIds: list[int]):
        album = [(await models.Album.tracks_ids
                    .add(Track_id=i, album_id=albumId).save()) 
                for i in tracksIds]

        return album

    async def deleteAlbumTracks(self,
                                albumId: int,
                                tracksIds: list[int]):
        album = [(await models.Album.tracks_ids.all()
                    .filter(Track_id=i, album_id=albumId).delete())
                for i in tracksIds]

        return album

    async def addAlbumArtists(self,
                            albumId: int,
                            artistsIds: list[int]):
        album = [(await models.Album.tracks_ids.all()
                    .filter(Track_id=i, album_id=albumId).delete())
                for i in artistsIds]

        return album

    async def deleteAlbumArtists(self,
                                albumId: int,
                                artistsIds: list[int]):
        album = [(await models.Album.artists_ids.all()
                    .filter(Album_id=albumId, artist_id=artistId).first().delete())
                for artistId in artistsIds]

        return album

    async def changeReleaseDate(self,
                                albumId: int,
                                releaseDate: datetime.datetime = datetime.datetime.utcnow()[:10]):
        album = (await models.Album.all()
                    .filter(id=albumId).first().update(release_date=releaseDate).save())

        return album
#----------------------------------------------------------------------------------------------------------


#--------------------------------------------- track interdace --------------------------------------------    
    async def createTracksByJson(self):
        '''
        imports tracks data from <jsonData> variable into db
        returns <list> of <track> fields
        ''' 
        tracks = [await models.Track.create(name=i['title']).save()
                for i in self.jsonData['album']['tracks']]
        return tracks

    async def createTrack(self, 
                        name: str,
                        trackFilePath: str, trackFileType: str,
                        genreId: int,
                        artistsIds: list[int] = [],
                        albumIds: list[int] = [],
                        pictureFilePath: str = '', pictureFileType: str = 'jpg'):
        '''
        creating a track field by given data
        :name: track title
        :duration: duration of the track
        :genre: genre of the track
        :pictureFilePath: path to picture file on the server (default: no path)
        :pictureFileType: extention of the picture file (default: 'jpg')
        '''
        pictureFile = await models.File.create(file_name=pictureFilePath,
                                            file_type=pictureFileType,
                                            data_type='track_image').save()
        genre = await models.Genre.all().filter(id=genreId)

        durationSeconds = floor(librosa.get_duraiton(filename=f'{trackFilePath}.{trackFileType}'))

        track = await models.Track.create(name=name,
                                        duration=durationSeconds,
                                        file_path=trackFilePath,
                                        file_type=trackFileType,
                                        picture_id=pictureFile,
                                        genre=genre).save()

        for i in artistsIds:
            artist = await models.Artist.all().filter(id=i).first()
            await models.Track.artists_ids.participants.add(artist).save()
        for i in albumIds:
            album = await models.Album.all().filter(id=i).first()
            await models.Track.album_ids.participants.add(album).save()

        return track

    async def deleteTrack(self,
                        trackId: int):
        artists = await models.Track.artists_ids.all().filter(id=trackId).delete() # TODO search bout it
        albums = await models.Track.album_ids.all().filter(id=trackId).delete() # TODO search bout it
        pictureId = await models.Track.all().filter(id=trackId).first().values('picture_id')
        picture = await models.File.all().filter(id=pictureId).first().delete()

        track = await models.Track.all().filter(id=trackId).delete()

        return track

    async def changeTrackGenre(self,
                            trackId: int,
                            newGenreId: int):
        newGenre = await models.Genre.all().filter(id=newGenreId)

        track = (await models.Track.all()
                    .filter(id=trackId).first()
                .update(genre=newGenre))

        return track

    async def addTrackPicture(self,
                            trackId: int,
                            pictureFilePath: str,
                            pictureFileType: str):
        track = await models.Track.all().filter(id=trackId).first()

        picture = (await models.File.create(file_name=pictureFilePath,
                                            file_type=pictureFileType,
                                            data_type='track_picture').save())
        track = (await track.update(picture_id=picture.id).save())

        return track

    async def changeTrackPicture(self,
                                trackId: int,
                                pictureFilePath: str,
                                pictureFileType: str):
        track = await models.Track.all().filter(id=trackId).first()

        picture = (await models.File.all().filter(id=track.picture_id)
                        .first().update(file_name=pictureFilePath,
                                        file_type=pictureFileType,
                                        data_type='track_picture').save())

        return picture

    async def addTrackArtists(self,
                            trackId: int,
                            artistsIds: list[int]):
        return [(await models.Track.artists_ids
                    .add(Track_id=trackId, artist_id=i).save())
                 for i in artistsIds]

    async def deleteTrackArtists(self,
                                trackId: int,
                                artistsIds: list[int]):
        return [(await models.Track.artists_ids
                    .filter(Track_id=trackId, artist_id=i).delete()) 
                for i in artistsIds]

    async def addTrackComment(self,
                            trackId: int,
                            commentText: str,
                            publishingDate: datetime.datetime = datetime.datetime.utcnow()[:10]):
        comment = (await models.Comment
                    .create(text=commentText, publishing_date=publishingDate).save())

        return (await models.Track.comments_ids
                    .add(Track_id=trackId, comment_id=comment.id).save())

    async def deleteTrackComment(self,
                                trackId: int,
                                commentId: int):
        return (await models.Track.comments_ids
                    .filter(Track_id=trackId, comment_id=commentId).delete())

    async def changeTrackName(self,
                            trackId: int,
                            newName: str):
        track = (await models.Track.all().filter(id=trackId)
                        .first().update(name=newName).save())

        return track

    async def changeTrackFile(self, 
                            trackId: int,
                            filePath: str,
                            fileType: str):

        durationSeconds = floor(librosa.get_duraiton(filename=f'{filePath}.{fileType}'))

        track = (await models.Track.all().filter(id=trackId)
                        .first().update(file_path=filePath,
                                        file_type=fileType,
                                        duration=durationSeconds).save())

        return track

    async def deleteTrackPicture(self,
                                trackId: int):
        pictureId = await models.Track.all().filter(id=trackId).first().values('picture_id')
        picture = await models.File.all().filter(id=pictureId).first().delete()

        return picture
#----------------------------------------------------------------------------------------------------------


# -------------------------------------------- genres interface -------------------------------------------
    async def createGenresByJson(self):
        '''
        imports genres data from <jsonData> variable into db
        returns <list> of <genre> fields
        '''
        genres = [await models.Genre.create(name=i,
                                            alt_name=self.jsonData['genres'][i]).save()
                for i in self.jsonDate['genres'].keys()]
        return genres

    async def changeGenreName(self,
                            genreId: int,
                            newGenreName: str):
        genre = (await models.Genre.all()
                    .filter(id=genreId).update(name=newGenreName.save()))

        return genre
#-----------------------------------------------------------------------------------------------------------


#------------------------------------------- playlist interface --------------------------------------------
    async def createPlaylist(self,
                            name: str,
                            description: str,
                            creatorId: int,
                            tracksIds: list[int] = [],
                            releaseDate: datetime.datetime = datetime.datetime.utcnow()[:10]):
        playlist = await models.Playlist.create(name=name,
                                                description=description,
                                                release_date=releaseDate[:10]).save()
        await models.Playlist.all().filter(id=playlist.id).update(creator_id=await models.User.all().filter(id=creatorId).first())

        for i in tracksIds:
            track = models.Track.all().filter(id=i)
            await models.Playlist.tracks_ids.add(track)

        return playlist
    
    async def deletePlaylist(self, 
                            playlistId: int):
        pictureId = (await models.Playlist.all().filter(id=playlistId).first().values('picture_id'))
        picture = (await models.File.all().filter(id=pictureId).first().delete())
        tracks = (await models.Playlist.tracks_ids.all().filter(Playlist_id=playlistId).delete())
        users = (await models.Playlist.users_ids.all().filter(playlist_id=playlistId).delete())
        genres = (await models.Playlist.genres_ids.all().filter(Playlist_id=playlistId).delete())

        playlist = (await models.Playlist.all()
                        .filter(id=playlistId).delete())

        return playlist

    async def changePlaylistPicture(self,
                                    playlistId: int,
                                    pictureFilePath: str,
                                    pictureFileType: str = 'jpg'):
        playlist = await models.Playlist.all().filter(id=playlistId).first()

        picture = (await models.File.all().filter(id=playlist.picture_id)
                        .first().update(file_name=pictureFilePath,
                                        file_type=pictureFileType,
                                        data_type='playlist_picture').save())
        
        return picture

    async def addPlaylistPicture(self,
                                playlistId: int,
                                pictureFilePath: str,
                                pictureFileType: str = 'jpg'):
        picture = (await models.File.add(file_name=pictureFilePath,
                                        file_type=pictureFileType,
                                        data_type='playlist_picture').save())
        
        playlist = (await models.Playlist.all().filter(id=playlistId)
                        .update(picture_id=picture.id).save())

        return playlist

    async def changePlaylistName(self,
                                playlistId: int,
                                newPlaylistName: str):
        playlist = (await models.Playlist.all().filter(id=playlistId).first()
                        .update(name=newPlaylistName).save())

        return playlist

    async def changePlaylistReleaseDate(self,
                                        playlistId: int,
                                        newReleaseDate: datetime.datetime = datetime.datetime.utcnow()[:10]):
        playlist = (await models.Playlist.all().filter(id=playlistId).first()
                        .update(release_date=newReleaseDate[:10]).save())

        return playlist

    async def addPlaylistGenres(self, 
                                playlistId: int,
                                genresIds: list[int]):
        playlist = [(await models.Playlist.genres_ids.add(Playlist_id=playlistId, genre_id=genre))
                    for genre in genresIds]

        return playlist

    async def deletePlaylistGenres(self, 
                                playlistId: int,
                                genresIds: list[int]):
        genres = [(await models.Playlist.genres_ids.all().filter(Playlist_id=playlistId, genre_id=genre)
                        .delete())
                    for genre in genres]

        return genres

    async def addPlaylistTracks(self,
                                playlistId: int,
                                tracksIds: list[int]):
        playlist = [(await models.Playlist.tracks_ids
                        .add(Playlist_id=playlistId, track_id=track).save())
                    for track in tracksIds]
        
        return playlist

    async def deletePlaylistTracks(self,
                                playlistId: int,
                                tracksIds: list[int]):
        playlist = [(await models.Playlist.tracks_ids.all().filter(Playlist_id=playlistId, track_id=track)
                        .first().delete())
                    for track in tracksIds]

        return playlist

    async def addPlaylistDescription(self,
                                    playlistId: int,
                                    desc: str):
        playlist = (await models.Playlist.all().filter(id=playlistId).first()
                        .update(description=desc).save())

        return playlist

    async def changePlaylistDescription(self,
                                        playlistId: int,
                                        newDesc: str):
        playlist = (await models.Playlist.all().filter(id=playlistId).first()
                        .update(description=newDesc).save())
        
        return playlist

    async def deletePlaylistPicture(self, 
                                    playlistId: int):
        pictureId = (await models.Playlist.all().filter(id=playlistId).first()
                        .values('picture_id'))
        picture = await models.File.all().filter(id=pictureId).first().delete()

        return picture
                    

#-------------------------------------------------------------------------------------------------------------

#--------------------------------------------- comment interface ---------------------------------------------

    async def createComment(self,
                            text: str,
                            trackId: int,
                            userId):
        comment = await models.Comment.create(text=text).save()
        
        track = await models.Track.all().filter(id=trackId)
        await models.Comment.track_id.participants.add(track)

        user = await models.User.all().filter(id=userId)
        await models.Comment.user_id.participants.add(user)

        return comment

    async def deleteComment(self,
                            commentId: int):
        user = (await models.Comment.user_id.all().filter(comment_id=commentId).first()
                    .delete())
        track = (await models.Comment.track_id.all().filter(comment_id=commentId).first()
                    .delete())

        comment = (await models.Comment.all().filter(id=commentId).first().delete())

        return comment
#--------------------------------------------------------------------------------------------------------------

# ---------------------------------------------- file interafce ----------------------------------------------- 
    async def createFile(self,
                        filePath: str,
                        fileType: str,
                        dataType: str):
        file = (await models.File.create(file_name=filePath,
                                        file_type=fileType,
                                        data_type=dataType).save())
        return file
    
    async def deleteFile(self,
                        fileId: int):
        file = (await models.File.all().filter(id=fileId).first()
                    .delete())
        
        return file

    async def changePath(self,
                        fileId: int,
                        newFilePath: str,
                        newFileType: str):
        file = (await models.File.all().filter(id=fileId)
                    .first().update(file_name=newFilePath,
                                    file_type=newFileType).save())

        return file

    async def changeFileDataType(self,
                                fileId: int,
                                newDataType: str):
        file = (await models.File.all().filter(id=fileId)
                    .first().update(data_type=newDataType).save())

        return file
# -------------------------------------------------------------------------------------------------------------

# ---------------------------------------------- genre interface ----------------------------------------------
    async def createGenre(self, 
                        name: str,
                        altName: str):
        genre = (await models.Genre
                    .create(name=name, alt_name=altName).save())

        return genre

    async def deleteGenre(self,
                        genreId: int):
        users = (await models.Genre.genre_users.all().filter(genre_id=genreId)
                    .delete())
        playlists = (await models.Genre.playlists_ids.all().filter(genre_id=genreId)
                        .delete())
        artists = (await models.Genre.artists_ids.all().filter(genre_id=genreId)
                        .delete())
        albums = (await models.Genre.album_ids.all().filter(genre_id=genreId)
                        .delete())
        genre = (await models.Genre.all().filter(genre_id=genreId).first()
                    .delete())
            
        return genre

    async def changeGenreName(self,
                            genreId: int,
                            newName: str):
        genre = (await models.Genre.all().filter(id=genreId).first()
                    .update(name=newName).save())

        return genre

    async def addAltName(self,
                        genreId: int,
                        altName: str):
        genre = (await models.Genre.all().filter(id=genreId).first()
                    .update(alt_name=altName).save())

        return genre

    async def deleteAltName(self,
                            genreId: int):
        genre = (await models.Genre.all().filter(id=genreId).first()
                    .update(altname=None).save())

        return genre

    async def changeAltName(self,
                            genreId: int,
                            newAltName: str):
        genre = (await models.Genre.all().filter(id=genreId).fisrt()
                    .update(alt_name=newAltName).save())

        return genre
# -------------------------------------------------------------------------------------------------------------

# ---------------------------------------------- user interface -----------------------------------------------
    async def createUser(self, 
                        login: str, 
                        password: str, 
                        email: str,
                        favoriteGenresIds: list[int] = [],
                        followingArtistsIds: list[int] = []):
        user = await models.User.create(login=login, 
                                password=hash(password)['key'],
                                email=email).save()
                                
        for i in favoriteGenresIds:
            genre = await models.Genre.all().filter(id=i)
            await models.User.liked_genres.participants.add(genre)
        for i in followingArtistsIds:
            artist = await models.Artist.all().filter(id=i)
            await models.User.following_artists.participants.add(artist)

        return user

    async def deleteUser(self,
                        userId: int):
        tracks = (await models.User.liked_tracks.all().filter(User_id=userId)
                    .delete())

        commentsIds = (await models.User.comments.all().filter(User_id=userId)
                        .values('comment_id'))

        (await models.User.comments.all().filter(user_id=userId)
            .delete())

        comments = [(await models.User.comments.all().filter(comment_id=comment)
                        .delete())

                    for comment in commentsIds]
        artists = (await models.User.following_artists.all().filter(User_id=userId)
                        .delete())

        playlists = (await models.User.liked_playlists.all().filter(User_id=userId)
                        .delete())

        albums = (await models.User.liked_albums.all().filter(User_id=userId)
                        .delete())

        genres = (await models.User.liked_genres.all().filter(User_id=userId)
                        .delete())
        
        pictureId = (await models.User.all().filter(id=userId).first()
                        .values('picture_id'))
        await self.deleteFile(pictureId)

        user = (await models.User.all().filter(id=userId).first()
                    .delete())

        return user

    async def changeUserPicture(self,
                                userId: int,
                                pictureFilePath: str,
                                pictureFileType: str):
        user = await models.User.all().filter(id=userId).first()

        picture = (await models.File.all().filter(id=user.picture_id)
                        .first().update(file_name=pictureFilePath,
                                        file_type=pictureFileType,
                                        data_type='user_picture').save())

        return picture

    async def addUserPicture(self,
                            userId: int,
                            pictureFilePath: str,
                            pictureFileType: str):
        picture = (await models.File.create(file_name=pictureFilePath,
                                            file_type=pictureFileType,
                                            data_type='user_picture')
                    .save())
        
        user = (await models.User.all().filter(id=userId).first()
                    .update(picture_id=picture.id))
        
        return user

    async def deleteUserPicture(self,
                                userId: int):
        pictureId = (await models.User.all().filter(id=userId).first()
                        .values('picture_id'))

        user = (await models.User.all().filter(id=userId).first()
                    .update(picture_id=None).save())
        
        picture = (await models.File.all().filter(id=pictureId).first()
                        .delete())

        return user

    async def addUserEmail(self,
                        userId: int,
                        newEmail: str):
        user = (await models.User.all().filter(id=userId).first()
                    .update(email=newEmail).save())

        return user

    async def changeUserEmail(self,
                            userId: int,
                            email: str):
        user = (await models.User.all().filter(id=userId)
                        .first().update(email=hash(email)['key']).save())
        
        return user

    async def deleteUserEmail(self,
                            userId: int):
        user = (await models.User.all().filter(id=userId).first()
                    .update(email=None).save())
        
        return user

    async def changeUserPassword(self,
                                userId: int,
                                password: str):
        user = (await models.User.all().filter(id=userId)
                        .first().update(email=hash(password)['key']).save())

        return user

    async def changeUserLogin(self,
                            userId: int,
                            login: str):
        user = (await models.User.all().filter(id=userId)
                        .first().update(login=login).save())
        
        return user

    async def addUserTrack(self,
                            userId: int,
                            trackId: int):
        return await models.User.liked_tracks.add(Track_id=trackId, user_id=userId)

    async def addUserArtist(self,
                            userId: int,
                            artistId: int):
        return await models.User.following_artists.add(Artist_id=artistId, user_id=userId)

    async def addUserAlbum(self,
                        userId: int,
                        albumId: int):
        return await models.User.liked_albums.add(album_id=albumId, User_id=userId)

    async def addUserPlaylist(self,
                        userId: int,
                        playlistId: int):
        return await models.User.liked_playlists.add(playlist_id=playlistId, User_id=userId)

    async def addUserGenre(self,
                        userId: int,
                        genreId: int):
        return await models.User.liked_genres.add(genre_id=genreId, User_id=userId)

    async def deleteUserTrack(self,
                            userId: int,
                            trackId: int):
        return await models.User.liked_tracks.all().filter(Track_id=trackId, user_id=userId).first().delete()

    async def deleteUserArtist(self,
                            userId: int,
                            artistId: int):
        return await models.User.following_artists.all().filter(Artist_id=artistId, user_id=userId).first().delete()

    async def deleteUserAlbum(self,
                            userId: int,
                            albumId: int):
        return await models.User.liked_albums.all().filter(album_id=albumId, user_id=userId).first().delete()

    async def deleteUserPlaylist(self,
                                userId: int,
                                playlistId: int):
        return await models.User.liked_playlists.all().filter(playlist_id=playlistId, user_id=userId).first().delete()

    async def deleteUserGenre(self,
                            userId: int,
                            genreId: int):
        return await models.User.liked_genres.all().filter(genre_id=genreId, User_id=userId).first().delete()


# --------------------------------------------------------------------------------------------------------------

# ---------------------------------------------- artist interface ----------------------------------------------
    async def createArtist(self,
                        name: str,
                        pictureFilePath: str = None, 
                        pictureFileType: str = None,
                        genresIds: list[int] = None,
                        albumsIds: list[int] = None,
                        tracksIds: list[int] = None,
                        registrationDate: datetime.datetime = datetime.datetime.utcnow()[:10]):
        if (not pictureFilePath and not pictureFileType):
            picture = (await models.File.create(file_name=pictureFilePath,
                                                file_type=pictureFileType,
                                                data_type='artist_picture').save())
        else: picture = None
        
        artist = (await models.Artist.create(name=name, 
                                            registrationDate=registrationDate,
                                            picture_id=picture.id)
                    .save())
        
        genres = [(await models.Artist.genres_ids
                        .add(Artist_id=artist.id, genre_id=genre))
                    for genre in genresIds]
        albums = [(await models.Artist.albums_ids
                        .add(artist_id=artist.id, Album_id=album))
                    for album in albumsIds]
        tracks = [(await models.Artist.track_ids
                        .add(artist_id=artist.id, Track_id=track))
                    for track in tracksIds]

        return artist

    async def deleteArtist(self,
                        artistId: int):
        tracks = (await models.Artist.track_ids.all().filter(artist_id=artistId)
                    .delete())
        albums = (await models.Artist.albums_ids.all().filter(artist_id=artistId)
                    .delete())
        genres = (await models.Artist.genres_ids.all().filter(Artist_id=artistId)
                    .delete())
        picture = (await models.File.all().filter(id=await models.Artist.all().filter(id=artistId).values('picture_id').first())
                    .delete())
        artist = (await models.Artist.all().filter(id=artistId).first()
                    .delete())

        return artist

    async def addArtistAlbums(self,
                            artistId: int,
                            albumsIds: list[int]):
        album = [(await models.Artist.albums_ids
                    .add(Album_id=album, artist_id=artistId).save())
                for album in albumsIds]

        return album

    async def deleteArtistAlbums(self,
                                artistId: int,
                                albumsIds: list[int]):
        album = [(await models.Artist.albums_ids.all().filter(artist_id=artistId, Album_id=album)
                    .first().delete())
                for album in albumsIds]

        return album

    async def addArtistTracks(self,
                            artistId: int,
                            tracksIds: list[int]):
        tracks = [(await models.Artist.track_ids
                        .add(Track_id=track, artist_id=artistId).save())
                for track in tracksIds]

        return tracks

    async def deleteArtistTracks(self,
                                artistId: int,
                                tracksIds: list[int]):
        tracks = [(await models.Artist.track_ids.all().filter(artist_id=artistId, Track_id=track)
                        .first().delete())
                for track in tracksIds]

        return tracks

    async def changeArtistTrack(self,
                                artistId: int,
                                newName: str):
        artist = (await models.Artist.all().filter(id=artistId).first()
                    .update(name=newName).save())

        return artist

    async def addArtistPicture(self,
                            artistId: int,
                            pictureFilePath: str,
                            pictureFileType: str):
        picture = (await models.File.create(file_name=pictureFilePath,
                                            file_type=pictureFileType,
                                            data_type='artist_picture').save())
        artist = (await models.Artist.all().filter(id=artistId).first()
                    .update(picture_id=picture.id).save())

        return artist

    async def deleteArtistPicture(self,
                                artistId: int):
        picture = (await models.File.all().filter(id=await models.Artist.all()
                                                    .filter(id=artistId).first().values('picture_id'))
                        .first().delete())
        artist = (await models.Artist.all().filter(id=artistId).first().update(picture_id=None))

        return artist

    async def changeArtistPicture(self,
                                artistId: int,
                                newPictureFilePath: str,
                                newPictureFileType: str):
        picture = (await models.all().filter(id=await models.Artist.all().filter(id=artistId).first().values('picture_id'))
                        .first().update(file_name=newPictureFilePath,
                                        file_type=newPictureFileType).save())

        return picture

    async def addArtistGenres(self,
                            artistId: int,
                            genresIds: list[int]):
        artist = [(await models.Artist.genres_ids
                        .add(Artist_id=artistId, genre_id=genre).save())
                    for genre in genresIds]

        return artist

    async def deleteArtistGenres(self,
                                artistId: int,
                                genresIds: list[int]):
        artist = [(await models.Artist.genres_ids.all().filter(Artist_id=artistId, genre_id=genre).first().delete())
                for genre in genresIds]

        return artist