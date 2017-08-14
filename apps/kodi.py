import re

_album = None
_artist = None

def initConversation():
    global _album, _artist
    _album = None
    _artist = None

def isValidCommand(spokenText):
    global _album, _artist
    initConversation()

    artist = re.search(r'play artist (.*) please', spokenText)
    if artist is not None:
        _artist = artist.group(1)
        return True

    album = re.search(r'play album (.*) please', spokenText)
    if album is not None:
        _album = album.group(1)
        return True

    return False

def executeCommand(param):
    print([_album, _artist])


def main():
    cmds = """play artist Elvis Presley please
play artist Celine Dion please
play album Relaxation Music Orchestra please""".split('\n')
    for cmd in cmds:
        print(cmd)
        if isValidCommand(cmd):
            executeCommand(cmd)

if __name__ == '__main__':
    main()
