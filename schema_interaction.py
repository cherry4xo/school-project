from tortoise import Tortoise, run_async
from hashlib import pbkdf2_hmac
import json
from os import urandom
from config import MYSQL_NAME, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB_NAME
from YMparser import HtmlParser, JsonParser
import config
import models

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
                #self.artistAlbumsPages.append({albumPage: JsonParser(mainFilePath=albumPage.dataPath, dataType='album')}) another data I never use
            return {'artist': jsonArtistData, 'albums': jsonArtistAlbumsData, 'genres': albumData.getAllGenres()}
            #----------------------------------------------------------------------------------------------    
        else:
            page = HtmlParser(url=config.URL,
                            patternStr=config.PATTERN,
                            dataType=config.DATATYPE)
            page.makeJsonFile()
            jsonAlbumData = JsonParser(mainFilePath=self.page.dataPath, dataType=f'album{config.URL[-8]}').getData()
            return {'album': jsonAlbumData, 'genres': jsonAlbumData.getAllGenres()}

        
    async def importArtistData(self):
        artist = await models.Executor.create(name=self.jsonData['artist']['name'])
        albums = [await models.Album.create(name=i['albums']['title'],
                                            releaseDate=i['releaseDate'][:10]).save()
                for i in self.jsonData['albums']]
        tracks = [await models.Track.create(name=i['title']) 
                for i in self.jsonData['albums']['tracks']]
        #album = await models.Album.create(name=self.jsonData['title'], 
        #                                release_date=self.jsonData['releaseDate'][:10]).save()
    async def importAlbumData(self):
        album = await models.Album.create(name=self.jsonData['album']['title'],
                                        releaseDate=self.jsonData['album']['releaseDate'][:10]).save()
        tracks = [await models.Track.create(name=i['name'],
                                            duration=i['durationMs'],
                                            releaseDate=i['releaseDate'])
                    for i in self.jsonData['album']['tracks']]

    async def importGenresData(self):
        return [await models.Genre.create(name=i, 
                                        alt_name=self.jsonData['genres'][i]) 
                for i in self.jsonData['genres'].keys()]

    async def createUser(self, name:str, email:str, password:str, saltLen:int=32):
        def hash(password:str):
            salt = urandom(saltLen)
            key = pbkdf2_hmac('sha256', 
                            password.encode('utf-8'), 
                            salt, 
                            100000, 
                            dklen=128)
            return {'salt': salt, 'key': key}
        await models.User.create(name=name,
                                email=email,
                                password=hash(password))
    
    

        
        
        
