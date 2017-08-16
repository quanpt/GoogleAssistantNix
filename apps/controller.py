import re, sys
import urllib.request, json, random
import warnings, logging as l
from subprocess import check_output, CalledProcessError


sys.path.append('../')
from voice.command import VoiceCommand
from sound import amixer
from utils.maths import text2int

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
l.basicConfig(level=l.DEBUG, format=FORMAT)
warnings.filterwarnings("ignore", category=UserWarning, module='urllib')

# search param
_cmd = ''
_searchType = None
_searchParam1 = ''

# database & contants
_kodi_url = "http://localhost:8080/jsonrpc"
_allAlbums = []
_range = 10

# last search
_shownArtists = []
_shownSongs = []
_lastSearchType = None


def get_pid(name):
    try:
        return int(check_output(["pidof",name]).decode('utf-8'))
    except CalledProcessError:
        return -1


def request_kodi_rpc(param_dict):
    params = json.dumps(param_dict).encode('utf8')
    req = urllib.request.Request(_kodi_url, data=params,
                                 headers={'content-type': 'application/json'})

    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        return data['result']


def init_database():
    global _allAlbums

    if get_pid('kodi.bin') < 0:
        print('Error: please start Kodi first')
        sys.exit(-1)

    # https://stackoverflow.com/questions/44239822/urllib-request-urlopenurl-with-authentication
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, _kodi_url, 'kodi', 'doki')
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)

    def get_albums(order_by):
        param_get_albums = {"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums",
                            "params": {"limits": {"start": 0, "end": 0},
                                       "properties": ["artist"],
                                       "sort": {"order": "ascending", "method": order_by}},
                            "id": 1}
        return request_kodi_rpc(param_get_albums)['albums']

    # get all albums
    _allAlbums = get_albums('artist')
    l.info(len(_allAlbums))


def init_conversation():
    global _searchType, _searchParam1
    _searchType = None
    _searchParam1 = None


def is_valid_command(spoken_text):
    global _cmd, _searchType, _searchParam1
    _cmd = spoken_text
    init_conversation()

    (_searchType, _searchParam1) = VoiceCommand.extract_data(spoken_text)

    return _searchType is not None


def execute_command():

    global _shownArtists, _shownSongs, _lastSearchType
    _lastSearchType = _searchType

    l.info([_searchType, _searchParam1])

    if _searchType == VoiceCommand.ALBUM:
        for album in _allAlbums:
            if re.search(_searchParam1, album['label'], re.IGNORECASE):
                play_album(album)
                return

    if _searchType == VoiceCommand.ARTIST:
        artist_album = []
        for album in _allAlbums:
            for artist in album['artist']:
                if re.search(_searchParam1, artist, re.IGNORECASE):
                    artist_album.append(album)
                    break
        if len(artist_album) > 0:
            play_album(random.choice(artist_album))
            return

    if _searchType == VoiceCommand.SHOW_ARTIST:
        output = set()
        for x in [album['artist'] for album in _allAlbums]:
            for y in x:
                output.add(y)
        artist_list = list(output)
        _shownArtists = []
        for _ in range(_range):
            _shownArtists.append(random.choice(artist_list))
            print('\n'.join(['    {}. {}'.format(str(index + 1), _shownArtists[index]) for index in range(_range)]))
        return

    if _searchType == VoiceCommand.SHOW_ALBUM:
        _shownSongs = []
        for _ in range(_range):
            _shownSongs.append(random.choice([album['label'] for album in _allAlbums]))
        print('\n'.join(['    {}. {}'.format(str(index+1), _shownSongs[index]) for index in range(_range)]))
        return

    if _searchType == VoiceCommand.PLAY_NUMBER:
        if _lastSearchType == VoiceCommand.SHOW_ALBUM:
            label = _shownSongs[text2int(_searchParam1)]
        return

    if _searchType == VoiceCommand.PLAY_RANDOM:
        play_album(random.choice(_allAlbums))
        return

    if _searchType == VoiceCommand.VOLUME_UP:
        amixer.volume_up()
        return

    if _searchType == VoiceCommand.VOLUME_DOWN:
        amixer.volume_down()
        return

    if _searchType == VoiceCommand.HELP:
        VoiceCommand.print_voice_command()
        return

    print("Cannot execute: {}".format(_cmd))


def play_album(album):
    l.info(album)
    paramOpen = {"jsonrpc": "2.0", "id": 1, "method": "Player.Open", "params": {"item": {"albumid": album['albumid']}}}
    result = request_kodi_rpc(paramOpen)
    l.info('result: {}'.format(result))


def main():
    init_database()
    cmds = """play artist Elvis Presley please
play artist Celine Dion please
play album Relaxation Music Orchestra please
help""".split('\n')
    for cmd in cmds:
        print(cmd)
        if is_valid_command(cmd):
            execute_command()

if __name__ == '__main__':
    main()
