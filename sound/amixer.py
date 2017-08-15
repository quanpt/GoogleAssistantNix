import subprocess, re, os

_currentSoundLevel = 0

def getSoundLevel():
    result = subprocess.run(["amixer", "-D", "pulse", "get", "Master"], stdout=subprocess.PIPE)
    return re.search(r'^.*Playback ([\d]+) .*$',
                                   [x for x in result.stdout.decode('utf-8').split('\n') if x.find('[on]') > 0][0]).group(1)

def saveSoundLevel():
    global _currentSoundLevel
    _currentSoundLevel = getSoundLevel()

def setLowSoundLevel():
    saveSoundLevel()
    with open(os.devnull, 'w') as FNULL:
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "75%-"], stdout=FNULL, stderr=subprocess.STDOUT)

def restoreSoundLevel():
    with open(os.devnull, 'w') as FNULL:
        subprocess.run(["amixer", "-D", "pulse", "sset", "Master", str(_currentSoundLevel)], stdout=FNULL, stderr=subprocess.STDOUT)

if __name__ == '__main__':
    saveSoundLevel()
    print(getSoundLevel())
    setLowSoundLevel()
    print(getSoundLevel())
    restoreSoundLevel()
    print(getSoundLevel())