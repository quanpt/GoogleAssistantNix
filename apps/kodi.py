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
l.basicConfig(level=l.INFO, format=FORMAT)

# database & constants
_kodi_url = "http://localhost:8080/jsonrpc"
_allAlbums = []
_range = 10

# last search
_shownArtists = []
_shownSongs = []

_kodiOff = False


def request_kodi_rpc(param_dict):
    if _kodiOff:
        return
    params = json.dumps(param_dict).encode('utf8')
    req = urllib.request.Request(_kodi_url, data=params,
                                 headers={'content-type': 'application/json'})

    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        return data['result']


def init_authorisation():
    global _kodiOff
    if get_pid('kodi.bin') < 0:
        print('Error: please start Kodi first')
        _kodiOff = True
        # sys.exit(-1)
    else:
        _kodiOff = False

    # https://stackoverflow.com/questions/44239822/urllib-request-urlopenurl-with-authentication
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, _kodi_url, 'kodi', 'doki')
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)


def init_database():
    init_authorisation()
    if _kodiOff:
        return
    global _allAlbums

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


def play_youtube_song(video_id):
    param_open = {"jsonrpc": "2.0", "id": "1", "method": "Player.Open",
                  "params": {"item": {"file": "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + video_id}}}
    result = request_kodi_rpc(param_open)
    l.info(result)


def play_youtube_album(video_id):
    param_open = {"jsonrpc": "2.0", "method": "Playlist.Clear", "params": {"playlistid": 1}, "id": 1}
    result = request_kodi_rpc(param_open)

    param_open = {"jsonrpc": "2.0", "method": "Player.Open",
                  "params": {"item": {"file": "plugin://plugin.video.youtube/play/?playlist_id=" + video_id + "&order=default&play=1"}}, "id": 2}
    result = request_kodi_rpc(param_open)

    #param_open = {"jsonrpc": "2.0", "method": "Player.Open", "params": {"item": {"playlistid": 1, "position": 0}}, "id": 3}
    #result = request_kodi_rpc(param_open)

    l.info(param_open)
    l.info(result)
    # [{"jsonrpc": "2.0", "method": "Playlist.Clear", "params": {"playlistid": 1}, "id": 1},
    #  {"jsonrpc": "2.0", "method": "Player.Open",
    #   "params": {"item": {"file": "plugin://plugin.video.youtube/play/?playlist_id=SOME_YT_PLAYLIST_ID"}}, "id": 2},
    #  {"jsonrpc": "2.0", "method": "Player.Open", "params": {"item": {"playlistid": 1, "position": 0}}, "id": 3}]


def play_next():
    param_get_player = {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}
    for player in request_kodi_rpc(param_get_player):
        param_next = {"jsonrpc": "2.0", "method": "Player.GoTo",
                      "params": {"playerid": player['playerid'], "to": "next"}, "id": 1}
        request_kodi_rpc(param_next)
    return True


def stop_audio():
    param_get_player = {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}
    for player in request_kodi_rpc(param_get_player):
        param_stop = {"jsonrpc": "2.0", "method": "Player.Stop", "params": {"playerid": player['playerid']}, "id": 1}
        request_kodi_rpc(param_stop)
    return True


def search_play_album(label):
    l.info(label)
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
    try:
        index = int(number)
    except ValueError:
        index = text2int(number)
    label = _shownSongs[index - 1]
    search_play_album(label)


def play_number_from_artist_list(number):
    try:
        index = int(number)
    except ValueError:
        index = text2int(number)
    name = _shownArtists[index - 1]
    search_play_artist(name)


def main():
    init_authorisation()
    play_youtube_album('PLougCVpA6za1ekshDLUoy0Ragmmi5GOaF')

if __name__ == '__main__':
    init_database()
    main()
