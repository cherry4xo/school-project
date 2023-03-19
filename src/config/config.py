import re
import pydub
import os
from pathlib import Path

#pydub.AudioSegment.converter = f"{os.getcwd()}".replace(os.path.sep, '/')
#pydub.AudioSegment.ffmpeg = f"{os.getcwd()}".replace(os.path.sep, '/')

#      DB connection config
#-----------------------------------
MYSQL_NAME = 'root'
MYSQL_PASS = 'qwerty'
MYSQL_HOST = 'host.docker.internal'
MYSQL_PORT = '3366'
MYSQL_DB_NAME = 'testing'
#-----------------------------------

#               Models config
#----------------------------------------------

MODELS = ['src.app.user.models',
        'src.app.library.models',
        'src.app.rec_service.models',
        'src.app.recognition_service.models']

#----------------------------------------------
#               hash config
#----------------------------------------------
SALT = [b'\x03=\x06\xddn\x8d\x07\x8b\x926H\x91\xfb\xc9\x8e\xf8I\x07$n\xbf=u\xd9R\x8b\xa3\xb6\xdb7\xb6\x0c'
        b'\xce\xa5\x88GE\x1db\x9b\x82}\rn\x06\xc8\xe4[2\xf4waB\x08\xb1z\x8c\x17\xd0\n\xd9$\x95\xb3', 
        b"\x08p\xf7\xd7z%w2\xee\x17\xaeH\xa2\x95\x1dR\xd8\x1d\x1d>\x118\xe4\x18\x92\xd73R\x1c\xb8\xc1'", 
        b'i\x8b\x97\x85\xa4\xf0\xae\x82K\xee\x1c\xb1\x13p \x99\xee\xc4u-{H0\x08\xbcE\x91\x89ue^y', 
        b'\x9e\xf2\xdc\x9b\x83\xaaA\x89G\xd7o\xb4j\xeaa*\xeb?\x84\x14s\xbbq\x93\x93\x95\x95\xef\xda\xad\xack', 
        b'\xdc\xb7\xa4,y-$}T\xde\xd1\x0b\xb4\x98\x0e\xdc:*R\xbe/\xe5\xecT\x93\xcbL\xd1\xad\xe6\xe6\xac', 
        b'6p\x8c\xe0q\x02\x99l\x96\xa9\xd0\xa0R\x96\x12\xbd\xf8\xad\xcdNX\xee\x80\xb9*\xd5\xca~\xa4%t\xbe', 
        b'\x1d\xd8\x04\xd7\xce\x00_\rQ\x18bG\x1f\x8a\xa96)\x95~\xb4;\xa9c\xd1/o\x7f|\x97\xa4h\x9f', 
        b'g\x17QC\xcf\x8e+\n4:\x86CxofQ3\xdf\xad\\\xfa\x12\xdc\xfa\xe0\xb8]\x88E\xcc\\4', 
        b'1!\x1ei\xf7\x16al+\xde4\x0b\x06lo~Tm,\xd3\x96\xf0\xa6\x03\xbb\xce\xea\xc9t\xba@\xdf', 
        b'h\xa7\xd6\xe2\xbfR~8]\xba\\0\xe3\x9a\x15\xc9F\x82\xc6\xb6\xe0\xe2\xcd\x11\xbf\x01>.9p\xca\x06', 
        b'}\x04]\xcd\xd3\xde\xdb\xe4\xea\x18\x81\xdd\xb8\xfe\x1a\x17\xebM\x1bI\xa2\x8c\x1a\x13v\x04\xf24m\x0cH\xc1', 
        b'\x84\x95F\xbe/f\x16\xd49.\x9a5+\xb2g$\xdaV\r\xbfkF\xdd\xebA\t\rr7\x8463', 
        b'\x01\x81\xd8-\x13tilo@\xf9\xba\x89/\xb4BO\xf8\xbe\xdf@\xe0\x8c\x99\x9aGXNA\xcd\xb0Q', 
        b'\x90\xfch\xc6u\x1e=\x98\xca\xe8\x92Y_nr\x84\xee\xbf\x8c\x11B\xf2\xac\xfe\xd2H2\xa90\xf2\x0e\x9a', 
        b"\xaaz\xd8}\xd3\xb9'\xa9\xd2\xf9\x1b3Z\x1c\xffM\x94\xe7\x89H*\xcb\x1e\xccx\x12\xbapp\xac\xc99", 
        b"R\xc0\xf7\xb7\xef\xdf\xeb\xa9\xeb\xaf\x86\xd7\x9c\x9b\n\xff\xe0\xeeZ\xea'`AE\xa3}`\xf7\xf4\x06\xf1b",
        b'"\xb3/\xbd\x9e,k\xab/\xb4\x8a\x0e1\x94\x14\xba\xe8XO1\x1e\xf5\xf7J\xfd\x84\x85\xa3\x9alL\x1b', 
        b'\x1eR\xf7m\xdc\x8aS\xe8R\x115\x05v\n_\xa3\xea-\xb8\xa1\xb7^k\xc7\x9f\x0f\xa8 \xfaX\x14\xf8', 
        b'\xb4\xd4\xd9\x86\xffbz\x0eF/%N\xafC\x85\xd0\xf7\x1e\xf4\x82\xe2\x04\xfe\xaf\xf2!\xb7\x90r4\xc0\x89']


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