from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from ..config import URL, PATTERN, HTML_PARSER_DATATYPE, JSONPARSER_DATATYPE, SCRIPTNUM, HTML_PARSER_FILEPATH, JSONPARSER_DATATYPE


class HtmlParser:

    def __init__(self, url = URL, patternStr:str = PATTERN, dataType:str = HTML_PARSER_DATATYPE):
        """ HtmlParser class constructor

        :url: website url for parse
        :patternStr: any pattern for page file parsing
        :dataType: type of content in the page file
            making (.*?)_<dataType>.json file
        """
        self.pattern = patternStr
        self.page = urlopen(url)
        self.html = self.page.read().decode('utf-8')
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.dataType = dataType

    def writeHtmlIntoFile(self, filePath:str):
        """ writing all the page data into <filePath>.html file

        :filePath: writing file path; 'w+' writing
        """
        with open(filePath, "w+", encoding='utf-8') as f:
            f.write(self.html)

    def makeJsonFile(self, scriptNum:int = SCRIPTNUM, filePath:str = HTML_PARSER_FILEPATH):
        """ writing [scriptNum] script into <filePath+dataType>.json file based on pattern

        :scriptNum: any number of script in the page file (be careful for <IndexError>) TODO make an exeption for <IndexError>
        :filePath: writing file path; 'w+' writing  
        """
        scripts = self.soup.findAll("script")
        self.dataPath = f'{filePath.rpartition(".")[0]}_{self.dataType}.json' # filePath with data type indication
        for script in scripts:
            if(self.pattern.match(str(script.string))):
                data = self.pattern.match(script.string)
                stock = json.loads(data.groups()[scriptNum])
                sample = [{first:second} for first, second in stock.items()]
                with open(self.dataPath, "w+", encoding='utf-8') as jsonf:
                    json_string = json.dumps(sample, ensure_ascii=False, default=lambda o: o.__dict__, sort_keys=True, indent=8)
                    jsonf.write(json_string)


class JsonParser:

    def __init__(self, mainFilePath, dataType:str = JSONPARSER_DATATYPE, subFilePath = {}):
        """ JsonParser class constructor
        
        :mainFilePath: main (.*?).json file path for parsing
        :dataType: type of content in <mainFilePath> file 
            doesnt accept any other argument beside this two:
            dataType='album'
            dataType='artist'
        :subFilePath: accepting a dict of subfiles for parsing
            for dataType='artist': required subDataArtistAlbums
        
        - making <data> var from <mainFilePath> file
        then making <maindata> var from <data> for better expression
        for dataType='artist': 
        - making <subDataArtistAlbums> var from <subFilePath> dict
        """
        with open(mainFilePath, 'r', encoding='utf-8') as self.jsonFile:
            self.data = json.load(self.jsonFile)
            self.maindata = self.data[9]['pageData']

        if(dataType == 'album' or dataType == 'artist'):
            self.dataType = dataType
        else: raise ValueError("Error: incorrect data type given for JsonParser")

        if self.dataType == 'artist':
            with open(subFilePath["albums"], 'r', encoding='utf-8') as self.jsonFile:
                self.subDataArtistAlbums = json.load(self.jsonFile)
                self.subData = self.subDataArtistAlbums[9]['pageData']
    
    def getAllGenres(self):
        """ returns all the genres of tracks
        - can be used to writing into (.*?).json file
        """
        return json.dumps(self.data[8]["genres"]["titles"], indent=8, sort_keys=True, ensure_ascii=False)

    def getData(self):
        """ returns data based on <dataType>
        for dataType='album': 
        - returns <json> object with:
            {title,
            trackCount,
            tracks,
            artistNames,
            releaseDate,
            genre,
            year}
        for dataType='artist':
        - returns <json> object with:
            {name,
            albums,
            tracks,
            genres,
            lastRelease}
        """
        if self.dataType == 'album':

            title = self.maindata["title"]
            trackCount = self.maindata["trackCount"]
            artistNames = [self.maindata['artists'][i]['name'] for i in range(len(self.maindata['artists']))]

            tracks = [{'name':              self.maindata['volumes'][0][i]['title'],
                        'trackPosition':    self.maindata['volumes'][0][i]['albums'][0]['trackPosition']['index'],
                        'trackDuration':    self.maindata['volumes'][0][i]['durationMs'],
                        'artists':          [self.maindata['volumes'][0][i]['artists'][j]['name'] 
                                                for j in range(len(self.maindata["volumes"][0][i]["artists"]))]} 
                        for i in range(len(self.maindata['volumes'][0]))]

            releaseDate = self.maindata["releaseDate"]
            genre = self.maindata["genre"]
            year = self.maindata["year"]

            albumData = {
                "title": title, 
                "trackCount": trackCount, 
                "tracks": tracks,
                "artistNames": artistNames, 
                "releaseDate": releaseDate,  
                "genre": genre,
                "year": year,
            }

            return json.dumps(albumData, indent=4, sort_keys=True, ensure_ascii=False)

        elif self.dataType == "artist":

            genres = [self.subData['artist']['genres'][i] 
                        for i in range(len(self.subData['artist']['genres']))]

            lastRelease = {'name':          self.subData['lastRelease']['title'],
                            'artists':      [self.subData['lastRelease']['artists'][i]['name'] 
                                                for i in range(len(self.subData['lastRelease']['artists']))],
                            'genre':        self.subData['lastRelease']['genre'],
                            'year' :        self.subData['lastRelease']['year']
                            }
            
            albums = [{'title':         self.subData['albums'][i]["title"],
                        'artists':      [self.subData['albums'][i]['artists'][j]['name'] 
                                            for j in range(len(self.subData['albums'][i]['artists']))],
                        'releaseDate':  self.subData['albums'][i]['releaseDate'],
                        'trackCount':   self.subData['albums'][i]['trackCount'],
                        'genre':        self.subData['albums'][i]['genre'],
                        'year':         self.subData['albums'][i]['year']
                        } 
                    for i in range(len(self.subData['albums']))
                    ]

            tracks = [{'title':         self.subData['tracks'][i]['title'],
                        'artists':      [self.subData['tracks'][i]['artists'][j]['name']
                                            for j in range(len(self.subData['tracks'][i]['artists']))],
                        'albums':       [{'title': self.subData['tracks'][i]['albums'][j]['title'],
                                          'artists': [self.subData['tracks'][i]['albums'][j]['artists'][k]['name'] 
                                                for k in range(len(self.subData['tracks'][i]['albums'][j]['artists']))],
                                          'genre': self.subData['tracks'][i]['albums'][j]['genre'],
                                          'trackCount': self.subData['tracks'][i]['albums'][j]['trackCount'],
                                          'year': self.subData['tracks'][i]['albums'][j]['year']}
                                                for j in range(len(self.subData['tracks'][i]['albums']))],
                        }
                    for i in range(len(self.subData['tracks']))
                    ]

            artistData = {
                'name': self.subDataArtistAlbums[9]["pageData"]["artist"]["name"],
                'albums': albums,
                'tracks': tracks,
                'genres': genres,
                'lastRelease': lastRelease
            }

            return json.dumps(artistData, indent=4, sort_keys=True, ensure_ascii=False)

