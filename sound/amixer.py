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