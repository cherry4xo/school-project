from tortoise import Tortoise, run_async
import json
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
            artistAlbumsData = []
            for album_url in config.URL_EXT['album']:
                albumPage = HtmlParser(url=album_url,
                                        patternStr=config.PATTERN_EXT,
                                        dataType=f'album{album_url[-8:]}')
                albumPage.makeJsonFile()
                albumData = JsonParser(mainFilePath=albumPage.dataPath, dataType='album')
                artistAlbumsData.append(albumData.getData())
                #self.artistAlbumsPages.append({albumPage: JsonParser(mainFilePath=albumPage.dataPath, dataType='album')}) another data I never use
            return {'artist': jsonArtistData, 'albums': artistAlbumsData}
            #----------------------------------------------------------------------------------------------    
        else:
            page = HtmlParser(url=config.URL,
                            patternStr=config.PATTERN,
                            dataType=config.DATATYPE)
            page.makeJsonFile()
            jsonAlbumData = JsonParser(mainFilePath=self.page.dataPath, dataType=f'album{config.URL[-8]}').getData()
            return {'album': jsonAlbumData}


        
    async def importArtistData(self):
        #album = await models.Album.create(name=self.jsonData['title'], 
        #                                release_date=self.jsonData['releaseDate'][:10]).save()

