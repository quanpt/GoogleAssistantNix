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


import logging as l
import warnings

from voice.command import VoiceCommand
from sound import amixer

from apps import kodi

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
l.basicConfig(level=l.DEBUG, format=FORMAT)
warnings.filterwarnings("ignore", category=UserWarning, module='urllib')

# search param
_cmd = ''
_searchType = None
_searchParam1 = ''

# last search
_shownArtists = []
_shownSongs = []
_lastSearchType = None


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

    l.info([_searchType, _searchParam1])

    if _searchType == VoiceCommand.ALBUM:
        if kodi.search_play_album(_searchParam1):
            return

    if _searchType == VoiceCommand.ARTIST:
        if kodi.search_play_artist(_searchParam1):
            return

    if _searchType == VoiceCommand.SHOW_ARTIST:
        _lastSearchType = _searchType
        return kodi.show_artist()

    if _searchType == VoiceCommand.SHOW_ALBUM:
        _lastSearchType = _searchType
        return kodi.show_albums()

    if _searchType == VoiceCommand.PLAY_NUMBER:
        if _lastSearchType == VoiceCommand.SHOW_ALBUM:
            return kodi.play_number_from_album_list(_searchParam1)
        elif _lastSearchType == VoiceCommand.SHOW_ARTIST:
            return kodi.play_number_from_artist_list(_searchParam1)

    if _searchType == VoiceCommand.PLAY_RANDOM:
        return kodi.play_random()

    if _searchType == VoiceCommand.PLAY_NEXT:
        return kodi.play_next()

    if _searchType == VoiceCommand.STOP_PLAY:
        return kodi.stop_audio()

    if _searchType == VoiceCommand.VOLUME_UP:
        amixer.volume_up()
        return

    if _searchType == VoiceCommand.VOLUME_MAX:
        amixer.volume_max()
        return

    if _searchType == VoiceCommand.VOLUME_DOWN:
        amixer.volume_down()
        return

    if _searchType == VoiceCommand.HELP:
        VoiceCommand.print_voice_command()
        return

    print("Cannot execute: {}".format(_cmd))


def init_database():
    kodi.init_database()


def main():
    kodi.init_database()
    cmds = """help
show me some songs
play number 2""".split('\n')
    for cmd in cmds:
        print(cmd)
        if is_valid_command(cmd):
            execute_command()

if __name__ == '__main__':
    main()
