import re
from enum import Enum
import urllib.request, json, random
import warnings, logging as l

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
l.basicConfig(level=l.ERROR, format=FORMAT)
warnings.filterwarnings("ignore", category=UserWarning, module='urllib')

# search param
_cmd = ''
_searchType = None
_album = None
_artist = None

# database
kodiUrl = "http://localhost:8080/jsonrpc"
_allAlbums = None



class VoiceCommand(Enum):
    ALBUM = r'play song (.*)'
    ARTIST = r'play singer (.*)'
    SHOW_ARTIST = r'show me some singers'
    SHOW_ALBUM = r'show me some songs'
    HELP = r'help'

def printVoiceCommand():
    print("Available voice command:")
    for cmd in VoiceCommand:
        print('    {}'.format(cmd.value))

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
    global _cmd, _searchType, _album, _artist
    _cmd = spokenText
    initConversation()

    artist = re.search(VoiceCommand.ARTIST.value, _cmd, flags=re.IGNORECASE)
    if artist is not None:
        _artist = artist.group(1).lower()
        _searchType = VoiceCommand.ARTIST
        return True

    album = re.search(VoiceCommand.ALBUM.value, _cmd, flags=re.IGNORECASE)
    if album is not None:
        _album = album.group(1).lower()
        _searchType = VoiceCommand.ALBUM
        return True

    if re.search(VoiceCommand.SHOW_ARTIST.value, _cmd, flags=re.IGNORECASE):
        _searchType = VoiceCommand.SHOW_ARTIST
        return True

    if re.search(VoiceCommand.SHOW_ALBUM.value, _cmd, flags=re.IGNORECASE):
        _searchType = VoiceCommand.SHOW_ALBUM
        return True

    if re.search(VoiceCommand.HELP.value, _cmd, flags=re.IGNORECASE):
        _searchType = VoiceCommand.HELP
        return True

    return False

def executeCommand():

    l.info([_searchType, _album, _artist])

    if _searchType == VoiceCommand.ALBUM:
        for album in _allAlbums:
            if re.search(_album, album['label'], re.IGNORECASE):
                playAlbum(album)
                return

    if _searchType == VoiceCommand.ARTIST:
        artistAlbum = []
        for album in _allAlbums:
            for artist in album['artist']:
                if re.search(_artist, artist, re.IGNORECASE):
                    artistAlbum.append(album)
                    break
        if len(artistAlbum) > 0:
            playAlbum(random.choice(artistAlbum))
            return

    if _searchType == VoiceCommand.SHOW_ARTIST:
        artists = []
        output = set()
        for x in [album['artist'] for album in _allAlbums]:
            for y in x:
                output.add(y)
        artistList = list(output)
        for id in range(10):
            print(random.choice(artistList))
        return

    if _searchType == VoiceCommand.SHOW_ALBUM:
        artists = []
        for id in range(10):
            print(random.choice([album['label'] for album in _allAlbums]))
        return

    if _searchType == VoiceCommand.HELP:
        printVoiceCommand()
        return

    print("Cannot execute: {}".format(_cmd))

def playAlbum(album):
    l.info(album)
    paramOpen = {"jsonrpc":"2.0","id":1,"method":"Player.Open","params":{"item":{"albumid":album['albumid']}}}
    result = requestKodiRpc(paramOpen)
    l.info('result: {}'.format(result))

def main():
    initDatabase()
    cmds = """play artist Elvis Presley please
play artist Celine Dion please
play album Relaxation Music Orchestra please""".split('\n')
    for cmd in cmds:
        print(cmd)
        if isValidCommand(cmd):
            executeCommand()

if __name__ == '__main__':
    main()
