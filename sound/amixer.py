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


import subprocess, re, os

_currentSoundLevel = 0
_maxSoundLevel = 0

def get_sound_level():
    global _maxSoundLevel
    result = subprocess.run(["amixer", "-D", "pulse", "get", "Master"], stdout=subprocess.PIPE)
    _maxSoundLevel = int(re.search(r'^.*Limits: Playback\s*0 - ([\d]+).*$',
                                   [x for x in result.stdout.decode('utf-8').split('\n') if x.find('Limits: Playback') > 0][0]).group(1))
    return int(re.search(r'^.*Playback ([\d]+) .*$',
                                   [x for x in result.stdout.decode('utf-8').split('\n') if x.find('[on]') > 0][0]).group(1))


def save_sound_level():
    global _currentSoundLevel
    _currentSoundLevel = get_sound_level()


def set_low_sound_level():
    save_sound_level()
    with open(os.devnull, 'w') as FNULL:
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "75%-"], stdout=FNULL, stderr=subprocess.STDOUT)


def restore_sound_level():
    with open(os.devnull, 'w') as FNULL:
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", str(_currentSoundLevel)], stdout=FNULL, stderr=subprocess.STDOUT)


def volume_up():
    global _currentSoundLevel
    _currentSoundLevel += _maxSoundLevel * 0.2
    print("Sound level: {}".format(_currentSoundLevel))

def volume_max():
    global _currentSoundLevel
    _currentSoundLevel = _maxSoundLevel
    print("Sound level: {}".format(_currentSoundLevel))


def volume_down():
    global _currentSoundLevel
    _currentSoundLevel -= _maxSoundLevel * 0.2
    _currentSoundLevel = 0 if _currentSoundLevel < 0 else _currentSoundLevel
    print("Sound level: {}".format(_currentSoundLevel))


if __name__ == '__main__':
    save_sound_level()
    print(get_sound_level())
    set_low_sound_level()
    print(get_sound_level())
    restore_sound_level()
    print(get_sound_level())