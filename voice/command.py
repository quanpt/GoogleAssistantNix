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


from enum import Enum
import re


class VoiceCommand(Enum):
    ALBUM = r'play song (.*)'
    ARTIST = r'play singer (.*)'
    SHOW_ARTIST = r'show me some singers'
    SHOW_ALBUM = r'show me some songs'
    PLAY_RANDOM = r'play some random songs'
    PLAY_NUMBER = r'play number (.*)'
    PLAY_NEXT = r'play next(.*)'
    STOP_PLAY = r'stop(.*)'
    VOLUME_UP = r'volume up'
    VOLUME_MAX = r'volume max'
    VOLUME_DOWN = r'volume down'
    YT_PLAY_SONG = r'youtube song (.*)'
    YT_PLAY_LIST = r'youtube list (.*)'

    HELP = r'help'

    @staticmethod
    def print_voice_command():
        print("Available voice command:")
        for cmd in VoiceCommand:
            print('    {}'.format(cmd.value))
        print()

    @staticmethod
    def extract_data(spoken_text):
        search_param_1 = None
        for cmd in VoiceCommand:
            match = re.search(cmd.value, spoken_text, flags=re.IGNORECASE)
            if match:
                if cmd.value.find('.*') > 0:
                    search_param_1 = match.group(1).lower()
                print('  Command "{}": "{}"'.format(cmd.value, search_param_1))
                return cmd, search_param_1
        return None, None
