import re
from enum import Enum
import urllib.request, json
import warnings, logging as l

l.basicConfig(level=l.DEBUG)
warnings.filterwarnings("ignore", category=UserWarning, module='urllib')

# search param
_searchType = None
_album = None
_artist = None

# database
kodiUrl = "http://localhost:8080/jsonrpc"
_allAlbums = None


class SearchType(Enum):
    ALBUM = 1
    ARTIST = 2
    ALBUM_ARTIST = 3

def requestKodiRpc(paramDict):
    params = json.dumps(paramDict).encode('utf8')
    req = urllib.request.Request(kodiUrl, data=params,
                                 headers={'content-type': 'application/json'})

    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        return data['result']

def initDatabase():
    global _allAlbums
    # https://stackoverflow.com/questions/44239822/urllib-request-urlopenurl-with-authentication
    passwordMgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passwordMgr.add_password(None, kodiUrl, 'kodi', 'doki')
    handler = urllib.request.HTTPBasicAuthHandler(passwordMgr)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)

    def getAlbums(orderBy):
        paramGetAlbums = {"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": { "limits": { "start" : 0, "end": 0 }, "properties": [ "artist" ], "sort": { "order": "ascending", "method": orderBy } }, "id": 1}
        return requestKodiRpc(paramGetAlbums)['albums']

    # get all albums
    _allAlbums = getAlbums('artist')

def initConversation():
    global _album, _artist, _searchType
    _searchType = None
    _album = None
    _artist = None

def isValidCommand(spokenText):
    global _searchType, _album, _artist
    initConversation()

    artist = re.search(r'play artist (.*) please', spokenText)
    if artist is not None:
        _artist = artist.group(1)
        _searchType = SearchType.ARTIST
        return True

    album = re.search(r'play album (.*) please', spokenText)
    if album is not None:
        _album = album.group(1)
        _searchType = SearchType.ALBUM
        return True

    return False

def executeCommand(param):
    print([_searchType, _album, _artist])
    if _searchType == SearchType.ALBUM:
        for album in _allAlbums:
            if album['label'].find(_album) >= 0:
                playAlbum(album)

def playAlbum(album):
    l.info('  playAlbum: {}'.format(album))


def main():
    initDatabase()
    cmds = """play artist Elvis Presley please
play artist Celine Dion please
play album Relaxation Music Orchestra please""".split('\n')
    for cmd in cmds:
        print(cmd)
        if isValidCommand(cmd):
            executeCommand(cmd)

if __name__ == '__main__':
    main()
