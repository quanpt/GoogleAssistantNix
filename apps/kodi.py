# Copyright (C) 2017 Tran Quan Pham
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import urllib.request
import json
import random
import sys
import re

from utils.sys import get_pid
from utils.maths import text2int


import logging as l
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
l.basicConfig(level=l.DEBUG, format=FORMAT)


# database & constants
_kodi_url = "http://localhost:8080/jsonrpc"
_allAlbums = []
_range = 10


# last search
_shownArtists = []
_shownSongs = []


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


def play_album(album):
    l.info(album)
    param_open = {"jsonrpc": "2.0", "id": 1, "method": "Player.Open", "params": {"item": {"albumid": album['albumid']}}}
    result = request_kodi_rpc(param_open)
    l.info('result: {}'.format(result))


def search_play_album(label):
    for album in _allAlbums:
        if re.search(label, album['label'], re.IGNORECASE):
            play_album(album)
            return True
    return False


def search_play_artist(name):
    artist_album = []
    for album in _allAlbums:
        for artist in album['artist']:
            if re.search(name, artist, re.IGNORECASE):
                artist_album.append(album)
                break
    if len(artist_album) > 0:
        play_album(random.choice(artist_album))
        return True
    else:
        return False


def show_artist():
    global _shownArtists
    output = set()
    for x in [album['artist'] for album in _allAlbums]:
        for y in x:
            output.add(y)
    artist_list = list(output)
    _shownArtists = []
    for _ in range(_range):
        _shownArtists.append(random.choice(artist_list))
        print('\n'.join(['    {}. {}'.format(str(index + 1), _shownArtists[index]) for index in range(_range)]))


def show_albums():
    global _shownSongs
    _shownSongs = []
    for _ in range(_range):
        _shownSongs.append(random.choice([album['label'] for album in _allAlbums]))
    print('\n'.join(['    {}. {}'.format(str(index + 1), _shownSongs[index]) for index in range(_range)]))


def play_random():
    play_album(random.choice(_allAlbums))


def play_number_from_album_list(number):
    label = _shownSongs[text2int(number)]
    search_play_album(label)


def play_number_from_artist_list(number):
    name = _shownArtists[text2int(number)]
    search_play_artist(name)
