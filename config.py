import re

#      DB connection config
#-----------------------------------
MYSQL_NAME = 'root'
MYSQL_PASS = 'qwerty'
MYSQL_HOST = 'host.docker.internal'
MYSQL_PORT = '3366'
MYSQL_DB_NAME = 'db'
#-----------------------------------

#               parser config
#----------------------------------------------
URL = "https://music.yandex.ru/album/22556299"
PATTERN = re.compile('var Mu=(.*?);')
HTML_PARSER_DATATYPE = 'album'
SCRIPTNUM = 0
HTML_PARSER_FILEPATH = 'json/1.json'
JSONPARSER_DATATYPE = 'album'
#  sub parser config(for 2 or more data types)
#----------------------------------------------
URL_EXT = {'artist': "https://music.yandex.ru/artist/8176408",
            'album': ["https://music.yandex.ru/album/22556299"] }
PATTERN_EXT = re.compile('var Mu=(.*?);')
HTML_PARSER_DATATYPE_EXT = ('artist', 'album') 
SCRIPTNUM_EXT = {'artist': 0,
                'album': 0}
JSONPARSER_DATATYPE_EXT = ('artist', 'album')
