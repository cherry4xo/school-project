import re
from YMparser import HtmlParser, JsonParser


def main():
    #url = "https://music.yandex.ru/artist/8176408"
    url = "https://music.yandex.ru/album/22556299"
    pattern = re.compile('var Mu=(.*?);')

    parser = HtmlParser(url=url, patternStr=pattern, dataType='album')
    #parser.writeHtmlIntoFile('album_index.html')
    parser.makeJsonFile(scriptNum=0, filePath='json/album.json')

    #subPageAlbums = HtmlParser(url=f'{url}/tracks', patternStr=pattern, dataType='sub_albums')
    #subPageAlbums.makeJsonFile(scriptNum=0, filePath='json/artist.json')

    #jsonData = JsonParser(mainFilePath=parser.dataPath, dataType='artist', subFilePath={"albums": subPageAlbums.dataPath})
    jsonData = JsonParser(mainFilePath=parser.dataPath, dataType='album')
    with open('json/genres.json', 'w+', encoding='utf-8') as f:
        f.write(jsonData.getAllGenres())

    with open('json/albumData.json', 'w+', encoding='utf-8') as f:
        f.write(jsonData.getData())

if __name__ == '__main__':
    main()